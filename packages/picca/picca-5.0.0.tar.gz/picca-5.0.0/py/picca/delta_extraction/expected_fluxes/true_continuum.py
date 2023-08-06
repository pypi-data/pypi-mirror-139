"""This module defines the class TrueContinuum"""
import logging
import multiprocessing

import fitsio
from astropy.io import fits
import numpy as np
from scipy.interpolate import interp1d
import healpy
from pkg_resources import resource_filename

from picca.delta_extraction.astronomical_objects.forest import Forest
from picca.delta_extraction.astronomical_objects.pk1d_forest import Pk1dForest
from picca.delta_extraction.errors import ExpectedFluxError
from picca.delta_extraction.expected_flux import ExpectedFlux

accepted_options = ["input directory", "iter out prefix",
                    "num processors",
                    "var lss binning"]

defaults = {
    "iter out prefix": "delta_attributes",
}


class TrueContinuum(ExpectedFlux):
    """Class to compute the expected flux using the true unabsorbed contiuum
    for mocks.
    It uses var_lss pre-computed from mocks and the mean flux modeled from a 2nd order polinomial in effective optical depth.

    Methods
    -------
    extract_deltas (from ExpectedFlux)
    __init__
    _parse_config
    compute_expected_flux
    compute_mean_cont_lin
    compute_mean_cont_log
    read_true_continuum
    read_var_lss
    populate_los_ids
    save_delta_attributes

    Attributes
    ----------
    los_ids: dict (from ExpectedFlux)
    A dictionary to store the mean expected flux, the weights, and
    the inverse variance for each line of sight. Keys are the identifier for the
    line of sight and values are dictionaries with the keys "mean expected flux",
    and "weights" pointing to the respective arrays. If the given Forests are
    also Pk1dForests, then the key "ivar" must be available. Arrays have the same
    size as the flux array for the corresponding line of sight forest instance.

    out_dir: str (from ExpectedFlux)
    Directory where logs will be saved.

    get_var_lss: scipy.interpolate.interp1d
    Interpolation function to compute mapping functions var_lss. See equation 4 of
    du Mas des Bourboux et al. 2020 for details. Data for interpolation is read from a file.

    input_directory: str
    Directory where true continum data is store

    iter_out_prefix: str
    Prefix of the iteration files. These file contain the statistical properties
    of deltas at a given iteration step. Intermediate files will add
    '_iteration{num}.fits.gz' to the prefix for intermediate steps and '.fits.gz'
    for the final results.

    num_processors: int or None
    Number of processors to be used to compute the mean continua. None for no
    specified number (subprocess will take its default value).
    """

    def __init__(self, config):
        """Initialize class instance.

        Arguments
        ---------
        config: configparser.SectionProxy
        Parsed options to initialize class

        Raise
        -----
        ExpectedFluxError if Forest.wave_solution is not 'lin' or 'log'
        """
        self.logger = logging.getLogger(__name__)
        super().__init__(config)

        # load variables from config
        self.input_directory = None
        self.iter_out_prefix = None
        self.num_processors = None
        self._parse_config(config)

        # read large scale structure variance
        self.get_var_lss = None
        self.read_var_lss()


    def _parse_config(self, config):
        """Parse the configuration options

        Arguments
        ---------
        config: configparser.SectionProxy
        Parsed options to initialize class

        Raises
        ------
        ExpectedFluxError if iter out prefix is not valid
        """
        self.input_directory = config.get("input directory")
        if self.input_directory is None:
            raise ExpectedFluxError(
                "Missing argument 'input directory' required "
                "by TrueContinuum")

        self.iter_out_prefix = config.get("iter out prefix")
        if self.iter_out_prefix is None:
            raise ExpectedFluxError(
                "Missing argument 'iter out prefix' required "
                "by TrueContinuum")
        if "/" in self.iter_out_prefix:
            raise ExpectedFluxError(
                "Error constructing TrueContinuum. "
                "'iter out prefix' should not incude folders. "
                f"Found: {self.iter_out_prefix}")

        self.num_processors = config.getint("num processors")

        self.var_lss_binning = config.get("var lss binning", 'log')


    def compute_expected_flux(self, forests):
        """

        Arguments
        ---------
        forests: List of Forest
        A list of Forest from which to compute the deltas.

        Raise
        -----
        ExpectedFluxError if Forest.wave_solution is not 'lin' or 'log'
        """

        if Forest.wave_solution == "log":
            num_bins = (int(
            (Forest.log_lambda_max_rest_frame -
             Forest.log_lambda_min_rest_frame) / Forest.delta_log_lambda) + 1)

            self.log_lambda_rest_frame = (
            Forest.log_lambda_min_rest_frame + (np.arange(num_bins) + 0.5) *
            (Forest.log_lambda_max_rest_frame -
             Forest.log_lambda_min_rest_frame) / num_bins)

        elif Forest.wave_solution == "lin":
            num_bins = (int(
            (Forest.lambda_max_rest_frame -
             Forest.lambda_min_rest_frame) / Forest.delta_lambda) + 1)

            self.lambda_rest_frame = (
            Forest.lambda_min_rest_frame + (np.arange(num_bins) + 0.5) *
            (Forest.lambda_max_rest_frame -
             Forest.lambda_min_rest_frame) / num_bins)
        else:
            raise ExpectedFluxError("Forest.wave_solution must be "
                                            "either 'log' or 'linear'")


        context = multiprocessing.get_context('fork')
        for iteration in range(1):
            pool = context.Pool(processes=self.num_processors)
            self.logger.progress(
                f"Reading continum with {self.num_processors} processors"
            )

            forests = pool.map(self.read_true_continuum, forests)
            pool.close()

        if Forest.wave_solution == "log":
            self.compute_mean_cont_log(forests)
        elif Forest.wave_solution == "lin":
            self.compute_mean_cont_lin(forests)
        else:
            raise ExpectedFluxError("Forest.wave_solution must be "
                                            "either 'log' or 'linear'")
        # now loop over forests to populate los_ids
        self.populate_los_ids(forests)
        # Save delta atributes
        self.save_delta_attributes()

    def compute_mean_cont_lin(self, forests):
        """Compute the mean quasar continuum over the whole sample assuming a
        linear wavelength solution. Then updates the value of self.get_mean_cont
        to contain it

        Arguments
        ---------
        forests: List of Forest
        A list of Forest from which to compute the deltas.
        """
        num_bins = self.lambda_rest_frame.size
        mean_cont = np.zeros(num_bins)
        mean_cont_weight = np.zeros(num_bins)

        for forest in forests:
            if forest.bad_continuum_reason is not None:
                continue
            bins = (
                (forest.lambda_ /
                 (1 + forest.z) - Forest.lambda_min_rest_frame) /
                (Forest.lambda_max_rest_frame - Forest.lambda_min_rest_frame) *
                num_bins).astype(int)

            var_lss = self.get_var_lss(forest.lambda_)
            var_pipe = 1. / forest.ivar / forest.continuum**2
            variance = var_lss + var_pipe
            weights = 1 / variance
            cont = np.bincount(bins,
                               weights=forest.continuum * weights)
            mean_cont[:len(cont)] += cont

            cont = np.bincount(bins, weights=weights)
            mean_cont_weight[:len(cont)] += cont

        w = mean_cont_weight > 0
        mean_cont[w] /= mean_cont_weight[w]
        mean_cont /= mean_cont.mean()
        lambda_cont = self.lambda_rest_frame[w]

        self.get_mean_cont = interp1d(lambda_cont,
                                      mean_cont,
                                      fill_value="extrapolate")
        self.get_mean_cont_weight = interp1d(lambda_cont,
                                             mean_cont_weight,
                                             fill_value=0.0,
                                             bounds_error=False)

    def compute_mean_cont_log(self, forests):
        """Compute the mean quasar continuum over the whole sample assuming a
        log-linear wavelength solution. Then updates the value of
        self.get_mean_cont to contain it

        Arguments
        ---------
        forests: List of Forest
        A list of Forest from which to compute the deltas.
        """
        num_bins = self.log_lambda_rest_frame.size
        mean_cont = np.zeros(num_bins)
        mean_cont_weight = np.zeros(num_bins)

        for forest in forests:
            if forest.bad_continuum_reason is not None:
                continue
            bins = ((forest.log_lambda - Forest.log_lambda_min_rest_frame -
                     np.log10(1 + forest.z)) /
                    (Forest.log_lambda_max_rest_frame -
                     Forest.log_lambda_min_rest_frame) * num_bins).astype(int)

            var_lss = self.get_var_lss(forest.log_lambda)
            var_pipe = 1. / forest.ivar/ forest.continuum**2
            variance = var_lss + var_pipe
            weights = 1 / variance
            cont = np.bincount(bins, weights= forest.continuum * weights)
            mean_cont[:len(cont)] += cont

            cont = np.bincount(bins, weights=weights)
            mean_cont_weight[:len(cont)] += cont

        w = mean_cont_weight > 0
        mean_cont[w] /= mean_cont_weight[w]
        mean_cont /= mean_cont.mean()
        log_lambda_cont = self.log_lambda_rest_frame[w]

        self.get_mean_cont = interp1d(log_lambda_cont,
                                      mean_cont,
                                      fill_value="extrapolate")
        self.get_mean_cont_weight = interp1d(log_lambda_cont,
                                             mean_cont_weight,
                                             fill_value=0.0,
                                             bounds_error=False)

    def read_true_continuum(self, forest):
        """Read the forest continuum and insert it into

        Arguments
        ---------
        forest: Forest
        A forest instance where the continuum will be computed

        Return
        ------
        forest: Forest
        The modified forest instance

        Raise
        -----
        ExpectedFluxError if Forest.wave_solution is not 'lin' or 'log'
        """
        in_nside = 16
        healpix = healpy.ang2pix(in_nside, np.pi / 2 - forest.dec, forest.ra,
                                 nest=True)
        filename_truth = (
            f"{self.input_directory}/{healpix//100}/{healpix}/truth-{in_nside}-"
            f"{healpix}.fits")
        hdul = fits.open(filename_truth)
        wmin = hdul["TRUE_CONT"].header["WMIN"]
        wmax = hdul["TRUE_CONT"].header["WMAX"]
        dwave = hdul["TRUE_CONT"].header["DWAVE"]
        twave = np.arange(wmin, wmax + dwave, dwave)
        true_cont = hdul["TRUE_CONT"].data
        hdul.close()
        indx = np.where(true_cont["TARGETID"]==forest.targetid)
        true_continuum = interp1d(twave, true_cont["TRUE_CONT"][indx])

        if Forest.wave_solution == "log":
            forest.continuum = true_continuum(10**forest.log_lambda)[0]
            mean_optical_depth = np.ones(forest.log_lambda.size)
            tau, gamma, lambda_rest_frame = 0.0023, 3.64, 1215.67
            w = 10.**forest.log_lambda / (1. + forest.z) <= lambda_rest_frame
            z = 10.**forest.log_lambda / lambda_rest_frame - 1.

        elif Forest.wave_solution == "lin":
            forest.continuum = true_continuum(forest.lambda_)[0]
            mean_optical_depth = np.ones(forest.lambda_.size)
            tau, gamma, lambda_rest_frame = 0.0023, 3.64, 1215.67
            w = forest.lambda_ / (1. + forest.z) <= lambda_rest_frame
            z = forest.lambda_ / lambda_rest_frame - 1.
        else:
            raise ExpectedFluxError("Forest.wave_solution must be either 'log' "
                                    "or 'lin'")

        mean_optical_depth[w] *= np.exp(-tau * (1. + z[w])**gamma)
        forest.continuum *= mean_optical_depth
        forest.hpcont = healpix
        return forest

    def read_var_lss(self):
        """Read the LSS delta variance from files (written by the raw analysis)
        """
        #var_lss files are only for lya so far, this will need to be updated so that regions other than Lya are available

        if self.var_lss_binning == 'log':
            filename = 'colore_v9_lya_log.fits.gz'
        elif self.var_lss_binning == 'lin_2.4':
            filename = 'colore_v9_lya_lin_2.4.fits.gz'
        elif self.var_lss_binning == 'lin_3.2':
            filename = 'colore_v9_lya_lin_3.2.fits.gz'
        else:
            self.logger.info(f'Trying to use costume var_lss file from {self.var_lss_binning}')
            filename = self.var_lss_binning

        if filename == self.var_lss_binning:
            var_lss_file = self.var_lss_binning
        else:
            var_lss_file = resource_filename('picca', 'delta_extraction')
            var_lss_file += '/expected_fluxes/var_lss/' + filename

        self.logger.info(f"Using var_lss from: {var_lss_file}")
        try:
            hdul = fits.open(var_lss_file)
        except:
            raise ExpectedFluxError(f"var_lss from {var_lss_file} couldn't be loaded")

        _lambda = hdul[1].data['LAMBDA']
        flux_variance = hdul[1].data['VAR']
        mean_flux = hdul[1].data['MEANFLUX']
        hdul.close()

        var_lss=flux_variance/mean_flux**2

        self.get_var_lss = interp1d(_lambda,
                                    var_lss,
                                    fill_value='extrapolate',
                                    kind='nearest')

    def populate_los_ids(self, forests):
        """Populate the dictionary los_ids with the mean expected flux, weights,
        and inverse variance arrays for each line-of-sight.

        Arguments
        ---------
        forests: List of Forest
        A list of Forest from which to compute the deltas.
        """
        for forest in forests:
            if forest.bad_continuum_reason is not None:
                continue
            # get the variance functions
            if Forest.wave_solution == "log":
                var_lss = self.get_var_lss(forest.log_lambda)
            elif Forest.wave_solution == "lin":
                var_lss = self.get_var_lss(forest.lambda_)
            else:
                raise ExpectedFluxError("Forest.wave_solution must be either "
                                        "'log' or 'lin'")

            mean_expected_flux = forest.continuum
            var_pipe = 1. / forest.ivar/ forest.continuum**2
            variance =  var_lss + var_pipe
            weights = 1. / variance

            if isinstance(forest, Pk1dForest):
                ivar = forest.ivar / mean_expected_flux**2

                self.los_ids[forest.los_id] = {
                    "mean expected flux": mean_expected_flux,
                    "weights": weights,
                    "ivar": ivar,
                    "continuum": forest.continuum,
                }
            else:
                self.los_ids[forest.los_id] = {
                    "mean expected flux": mean_expected_flux,
                    "weights": weights,
                    "continuum": forest.continuum,
                }

    def save_delta_attributes(self):
        """Save mean continuum in the delta attributes file.

        Raise
        -----
        ExpectedFluxError if Forest.wave_solution is not 'lin' or 'log'
        """
        iter_out_file = self.iter_out_prefix + ".fits.gz"

        with fitsio.FITS(self.out_dir + iter_out_file, 'rw',
                         clobber=True) as results:
            header = {}
            header["FITORDER"] = -1
            if Forest.wave_solution == "log":
                num_bins = int((Forest.log_lambda_max - Forest.log_lambda_min) /
                               Forest.delta_log_lambda) + 1

                results.write([
                    self.log_lambda_rest_frame,
                    self.get_mean_cont(self.log_lambda_rest_frame),
                    self.get_mean_cont_weight(self.log_lambda_rest_frame),
                ],
                              names=['loglam_rest', 'mean_cont', 'weight'],
                              extname='CONT')

            elif Forest.wave_solution == "lin":
                num_bins = int((Forest.lambda_max - Forest.lambda_min) /
                               Forest.delta_lambda) + 1

                results.write([
                    self.lambda_rest_frame,
                    self.get_mean_cont(self.lambda_rest_frame),
                    self.get_mean_cont_weight(self.lambda_rest_frame),
                ],
                              names=['lam_rest', 'mean_cont', 'weight'],
                              extname='CONT')

            else:
                raise ExpectedFluxError("Forest.wave_solution must be either "
                                        "'log' or 'lin'")
