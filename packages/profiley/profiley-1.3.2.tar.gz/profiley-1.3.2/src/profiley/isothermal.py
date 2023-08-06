from astropy.constants import G
import numpy as np

from .core import Profile
from .helpers.decorators import array, inMpc
from .helpers.lensing import BaseLensing
from .helpers.spherical import mass_from_radius, radius_from_mass


class SIS(Profile):
    """Singular Isothermal Sphere"""

    def __init__(self, mass
