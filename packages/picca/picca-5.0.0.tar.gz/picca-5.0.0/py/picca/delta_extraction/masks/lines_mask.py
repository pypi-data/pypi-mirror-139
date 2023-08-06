"""This module defines the class LinesMask in the masking of (sky) lines"""
from astropy.table import Table
import numpy as np

from picca.delta_extraction.astronomical_objects.forest import Forest
from picca.delta_extraction.errors import MaskError
from picca.delta_extraction.mask import Mask

defaults = {
    "absorber mask width": 2.5,
}

accepted_options = ["filename"]

class LinesMask(Mask):
    """Class to mask (sky) lines

    Methods
    -------
    __init__
    apply_mask

    Attributes
    ----------
    los_ids: dict (from Mask)
    Empty dictionary

    mask_rest_frame: astropy.Table
    Table with the rest-frame wavelength of the lines to mask

    mask_obs_frame: astropy.Table
    Table with the observed-frame wavelength of the lines to mask. This usually
    contains the sky lines.
    """
    def __init__(self, config):
        """Initialize class instance.

        Arguments
        ---------
        config: configparser.SectionProxy
        Parsed options to initialize class
        """
        super().__init__()

        mask_file = config.get("filename")
        if mask_file is None:
            raise MaskError("Missing argument 'filename' required by LinesMask")
        try:
            mask = Table.read(mask_file,
                              names=('type', 'wave_min', 'wave_max', 'frame'),
                              format='ascii')
            mask['log_wave_min'] = np.log10(mask['wave_min'])
            mask['log_wave_max'] = np.log10(mask['wave_max'])

            select_rest_frame_mask = mask['frame'] == 'RF'
            select_obs_mask = mask['frame'] == 'OBS'

            self.mask_rest_frame = mask[select_rest_frame_mask]
            self.mask_obs_frame = mask[select_obs_mask]
        except (OSError, ValueError):
            raise MaskError("Error loading SkyMask. Unable to read mask file. "
                            f"File {mask_file}")

    def apply_mask(self, forest):
        """Apply the mask. The mask is done by removing the affected
        pixels from the arrays in Forest.mask_fields

        Arguments
        ---------
        forest: Forest
        A Forest instance to which the correction is applied

        Raise
        -----
        CorrectionError if Forest.wave_solution is not 'lin' or 'log'
        """
        # find masking array
        if Forest.wave_solution == "log":
            w = np.ones(forest.log_lambda.size, dtype=bool)
            for mask_range in self.mask_obs_frame:
                w &= ((forest.log_lambda < mask_range['log_wave_min']) |
                      (forest.log_lambda > mask_range['log_wave_max']))
            log_lambda_rest_frame = forest.log_lambda - np.log10(1.0 + forest.z)
            for mask_range in self.mask_rest_frame:
                w &= ((log_lambda_rest_frame < mask_range['log_wave_min']) |
                      (log_lambda_rest_frame > mask_range['log_wave_max']))
        elif Forest.wave_solution == "lin":
            w = np.ones(forest.lambda_.size, dtype=bool)
            for mask_range in self.mask_obs_frame:
                w &= ((forest.lambda_ < mask_range['wave_min']) |
                      (forest.lambda_ > mask_range['wave_max']))
            lambda_rest_frame = forest.lambda_/(1.0 + forest.z)
            for mask_range in self.mask_rest_frame:
                w &= ((lambda_rest_frame < mask_range['wave_min']) |
                      (lambda_rest_frame > mask_range['wave_max']))
        else:
            raise MaskError("Unable to apply SkyMask. Forest.wave_solution is "
                            "required to be either 'log' or 'lin'. Found "
                            f"{Forest.wave_solution}")

        # do the actual masking
        for param in Forest.mask_fields:
            setattr(forest, param, getattr(forest, param)[w])
