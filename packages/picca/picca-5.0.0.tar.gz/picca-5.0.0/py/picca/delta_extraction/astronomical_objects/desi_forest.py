"""This module defines the class DesiForest to represent DESI forests"""
from picca.delta_extraction.astronomical_objects.forest import Forest
from picca.delta_extraction.errors import AstronomicalObjectError

class DesiForest(Forest):
    """Forest Object

    Methods
    -------
    __gt__ (from AstronomicalObject)
    __eq__ (from AstronomicalObject)
    class_variable_check (from Forest)
    consistency_check (from Forest)
    get_data (from Forest)
    rebin (from Forest)
    __init__
    coadd
    get_header

    Class Attributes
    ----------------
    delta_lambda: float or None (from Forest)
    Variation of the wavelength (in Angs) between two pixels. This should not
    be None if wave_solution is "lin". Ignored if wave_solution is "log".

    delta_log_lambda: float or None (from Forest)
    Variation of the logarithm of the wavelength (in Angs) between two pixels.
    This should not be None if wave_solution is "log". Ignored if wave_solution
    is "lin".

    lambda_max: float or None (from Forest)
    Maximum wavelength (in Angs) to be considered in a forest. This should not
    be None if wave_solution is "lin". Ignored if wave_solution is "log".

    lambda_max_rest_frame: float or None (from Forest)
    As wavelength_max but for rest-frame wavelength. This should not
    be None if wave_solution is "lin". Ignored if wave_solution is "log".

    lambda_min: float or None (from Forest)
    Minimum wavelength (in Angs) to be considered in a forest. This should not
    be None if wave_solution is "lin". Ignored if wave_solution is "log".

    lambda_min_rest_frame: float or None (from Forest)
    As wavelength_min but for rest-frame wavelength. This should not
    be None if wave_solution is "lin". Ignored if wave_solution is "log".

    log_lambda_max: float or None (from Forest)
    Logarithm of the maximum wavelength (in Angs) to be considered in a forest.
    This should not be None if wave_solution is "log". Ignored if wave_solution
    is "lin".

    log_lambda_max_rest_frame: float or None (from Forest)
    As log_lambda_max but for rest-frame wavelength. This should not be None if
    wave_solution is "log". Ignored if wave_solution is "lin".

    log_lambda_min: float or None (from Forest)
    Logarithm of the minimum wavelength (in Angs) to be considered in a forest.
    This should not be None if wave_solution is "log". Ignored if wave_solution
    is "lin".

    log_lambda_min_rest_frame: float or None (from Forest)
    As log_lambda_min but for rest-frame wavelength. This should not be None if
    wave_solution is "log". Ignored if wave_solution is "lin".

    mask_fields: list of str (from Forest)
    Names of the fields that are affected by masking. In general it will
    be "flux" and "ivar" but some child classes might add more.

    wave_solution: "lin" or "log" (from Forest)
    Determines whether the wavelength solution has linear spacing ("lin") or
    logarithmic spacing ("log").

    Attributes
    ----------
    dec: float (from AstronomicalObject)
    Declination (in rad)

    healpix: int (from AstronomicalObject)
    Healpix number associated with (ra, dec)

    los_id: longint (from AstronomicalObject)
    Line-of-sight id. Same as targetid

    ra: float (from AstronomicalObject)
    Right ascention (in rad)

    z: float (from AstronomicalObject)
    Redshift

    bad_continuum_reason: str or None
    Reason as to why the continuum fit is not acceptable. None for acceptable
    contiuum.

    continuum: array of float or None (from Forest)
    Quasar continuum. None for no information

    deltas: array of float or None (from Forest)
    Flux-transmission field (delta field). None for no information

    flux: array of float (from Forest)
    Flux

    ivar: array of float (from Forest)
    Inverse variance

    lambda_: array of float or None (from Forest)
    Wavelength (in Angstroms)

    log_lambda: array of float or None (from Forest)
    Logarithm of the wavelength (in Angstroms)

    mean_snr: float (from Forest)
    Mean signal-to-noise of the forest

    transmission_correction: array of float (from Forest)
    Transmission correction.

    weights: array of float or None (from Forest)
    Weights associated to the delta field. None for no information

    night: list of int
    Identifier of the night where the observation was made. None for no info

    petal: list of int
    Identifier of the spectrograph used in the observation. None for no info

    targetid: int
    Targetid of the object

    tile: list of int
    Identifier of the tile used in the observation. None for no info
    """
    def __init__(self, **kwargs):
        """Initialize instance

        Arguments
        ---------
        **kwargs: dict
        Dictionary contiaing the information

        Raise
        -----
        AstronomicalObjectError if there are missing variables
        """
        self.night = []
        if kwargs.get("night") is not None:
            self.night.append(kwargs.get("night"))
            del kwargs["night"]

        self.petal = []
        if kwargs.get("petal") is not None:
            self.petal.append(kwargs.get("petal"))
            del kwargs["petal"]

        self.targetid = kwargs.get("targetid")
        if self.targetid is None:
            raise AstronomicalObjectError("Error constructing DesiForest. "
                                          "Missing variable 'targetid'")
        del kwargs["targetid"]

        self.tile = []
        if kwargs.get("tile") is not None:
            self.tile.append(kwargs.get("tile"))
            del kwargs["tile"]

        # call parent constructor
        kwargs["los_id"] = self.targetid
        super().__init__(**kwargs)

        # rebin arrays
        super().rebin()

    def coadd(self, other):
        """Coadd the information of another forest.

        Forests are coadded by calling the coadd function from Forest.
        DESI night, petal and night from other are added to the current list

        Arguments
        ---------
        other: DesiForest
        The forest instance to be coadded.

        Raise
        -----
        AstronomicalObjectError if other is not a DesiForest instance
        """
        if not isinstance(other, DesiForest):
            raise AstronomicalObjectError("Error coadding DesiForest. Expected "
                                          "DesiForest instance in other. Found: "
                                          f"{type(other)}")
        self.night += other.night
        self.petal += other.petal
        self.tile += other.tile
        super().coadd(other)

    def get_header(self):
        """Return line-of-sight data to be saved as a fits file header

        Adds specific DESI keys to general header (defined in class Forest)

        Return
        ------
        header : list of dict
        A list of dictionaries containing 'name', 'value' and 'comment' fields
        """
        header = super().get_header()
        header += [
            {
                'name': 'TARGETID',
                'value': self.targetid,
                'comment': 'Object identification'
            },
            {
                'name': 'NIGHT',
                'value': "-".join(str(night) for night in self.night),
                'comment': "Observation night(s)"
            },
            {
                'name': 'PETAL',
                'value': "-".join(str(petal) for petal in self.petal),
                'comment': 'Observation petal(s)'
            },
            {
                'name': 'TILE',
                'value': "-".join(str(tile) for tile in self.tile),
                'comment': 'Observation tile(s)'
            },
        ]

        return header
