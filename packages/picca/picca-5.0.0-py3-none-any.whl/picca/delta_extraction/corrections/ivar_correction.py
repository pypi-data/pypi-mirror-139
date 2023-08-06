"""This module defines the abstract class IvarCorrection"""
import fitsio
from scipy.interpolate import interp1d

from picca.delta_extraction.correction import Correction
from picca.delta_extraction.errors import CorrectionError

accepted_options = ["filename"]

class IvarCorrection(Correction):
    """Class to correct inverse variance errors measured from other spectral
    regions.

    Methods
    -------
    __init__
    apply_correction

    Attributes
    ----------
    correct_ivar: scipy.interpolate.interp1d
    Interpolation function to adapt the correction to slightly different
    grids of wavelength
    """
    def __init__(self, config):
        """Initialize class instance.

        Arguments
        ---------
        config: configparser.SectionProxy
        Parsed options to initialize class

        Raise
        -----
        CorrectionError if input file does not have extension VAR_FUNC
        CorrectionError if input file does not have fields loglam and/or eta
        in extension VAR_FUNC
        """
        filename = config.get("filename")
        if filename is None:
            raise CorrectionError("Missing argument 'filename' required by SdssIvarCorrection")
        try:
            hdu = fitsio.read(filename, ext="VAR_FUNC")
            if "loglam" in hdu.dtype.names:
                log_lambda = hdu['loglam']
                self.wave_solution = "log"
            elif "lambda" in hdu.dtype.names:
                lambda_ = hdu['lambda']
                self.wave_solution = "lin"
            else:
                raise CorrectionError("Error loading IvarCorrection. In "
                                      "extension 'VAR_FUNC' in file "
                                      f"{filename} one of the fields 'loglam' "
                                      "or 'lambda' should be present. I did not"
                                      "find them.")

            eta = hdu['eta']
        except OSError:
            raise CorrectionError("Error loading IvarCorrection. "
                                  f"File {filename} does not have extension "
                                  "'VAR_FUNC'")
        except ValueError:
            raise CorrectionError("Error loading IvarCorrection. "
                                  f"File {filename} does not have fields "
                                  "'loglam' and/or 'eta' in HDU 'VAR_FUNC'")
        if self.wave_solution == "log":
            self.correct_ivar = interp1d(log_lambda,
                                         eta,
                                         fill_value="extrapolate",
                                         kind="nearest")
        elif self.wave_solution == "lin":
            self.correct_ivar = interp1d(lambda_,
                                         eta,
                                         fill_value="extrapolate",
                                         kind="nearest")
        else:
            raise CorrectionError("Forest.wave_solution must be either "
                                  "'log' or 'lin'")


    def apply_correction(self, forest):
        """Apply the correction. Correction is applied by dividing the
        data inverse variance by the loaded correction.

        Arguments
        ---------
        forest: Forest
        A Forest instance to which the correction is applied

        Raise
        -----
        CorrectionError if forest instance does not have the attribute
        'log_lambda'
        """
        if self.wave_solution == "log":
            if not hasattr(forest, "log_lambda"):
                raise CorrectionError("Forest instance is missing "
                                      "attribute 'log_lambda' required by "
                                      "IvarCorrection")
            correction = self.correct_ivar(forest.log_lambda)
        elif self.wave_solution == "lin":
            if not hasattr(forest, "lambda_"):
                raise CorrectionError("Forest instance is missing "
                                      "attribute 'lambda_' required by "
                                      "IvarCorrection")
            correction = self.correct_ivar(forest.log_lambda)
        else:
            raise CorrectionError("In IvarCorrection wave_solution must "
                                  "be either 'log' or 'lin'")

        forest.ivar /= correction
