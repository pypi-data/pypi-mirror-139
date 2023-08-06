from surfinpy import p_vs_t as pt
from surfinpy import utils as ut
import numpy as np
from scipy.constants import value


def temperature_correction(T, thermochem, adsorbant):
    """Make the energy of the adsorbing species a temperature
    dependent term by scaling it with experimental data.

    Parameters
    ----------
    T : :py:attr:`int`
        Temperature to scale the energy to
    thermochem : :py:attr:`array_like`
        nist_janaf table
    adsorbant : :py:attr:`float`
        DFT energy of adsorbant

    Returns
    -------
    adsorbant : :py:attr:`float`
        Scaled energy of adsorbant
    """
    temperature_range = np.arange(2, np.amax(thermochem[:, 0]))
    shift = ut.cs_fit(thermochem[:, 0], thermochem[:, 2], temperature_range)
    shift = (T * (shift[(T - 1)] / 1000)) / 96.485
    adsorbant = adsorbant - shift
    return adsorbant


def calculate_surface_energy(stoich,
                             data,
                             SE,
                             adsorbant,
                             thermochem,
                             T,
                             P,
                             coverage=None):
    """Calculate the surface energy at a specific temperature
    and pressure.

    Parameters
    ----------
    stoich : :py:class:`surfinpy.data.ReferenceDataSet`
        information about the stoichiometric surface
    data : :py:attr:`list`
        list of dictionaries containing information on the "adsorbed" surfaces
    SE : :py:attr:`float`
        surface energy of the stoichiomteric surface
    adsorbant : :py:attr:`float`
        dft energy of adsorbing species
    coverage : :py:attr:`array_like`
        Numpy array containing the different coverages of adsorbant.
    thermochem : :py:attr:`array_like`
        Numpy array containing thermochemcial data downloaded from NIST_JANAF
        for the adsorbing species.
    T : :py:attr:`float`
        Temperature to calculate surface energy
    P : :py:attr:`float`
        Pressure to calculate the surface energy
    coverage : :py:attr:`array_like` 
        Coverage of adsorbed specied on the surface.

    Returns
    -------
    SEs : :py:attr:`array_like`
        surface energies for each surface at T/P
    """
    if coverage is None:
        coverage = ut.calculate_coverage(data)
    R = value('molar gas constant')
    N_A = value('Avogadro constant')
    lnP = np.log(10 ** P)
    adsorbant = temperature_correction(T, thermochem, adsorbant)
    AE = pt.adsorption_energy(data, stoich, adsorbant)
    SEs = np.array([SE])
    for i in range(0, len(data)):
        S = SE + (coverage[i] / N_A) * (AE[i] - (lnP * (T * R)))
        SEs = np.append(SEs, S)
    return SEs
