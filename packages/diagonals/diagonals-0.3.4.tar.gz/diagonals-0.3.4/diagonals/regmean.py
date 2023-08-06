import logging
import numpy as np
import dask.array as da

from numba import vectorize

import diagonals

logger = logging.getLogger(__name__)

__all__ = ['compute_regmean_2d', 'compute_regmean_3d',
           'compute_regmean_levels']


def compute_regmean_2d(var, basins, area):
    """Function that checks device and calls computing functions.

    Checks if the computations are going performed in the CPU or the GPU:

    Parameters
    ----------
    var : float32
        Masked array containing variable data. Can not contain NaNs
    basins : float32
        List containing basin names and masks.
    area : float32
        Masked array containing cell area.

    Returns
    -------
    regmean: float32
        List containing regional mean for variable var
    """
    if diagonals.CONFIG.use_gpu:
        logger.warning('GPU routines not implemented for regmean diagnostic.'
                       'Using CPU instead')
    regmean = _compute_regmean_2d_cpu(var, basins, area)
    return regmean


def compute_regmean_3d(var, basins, volume):
    """Function that checks device and calls computing functions.

    Checks if the computations are going performed in the CPU or the GPU:

    Parameters
    ----------
    var : float32
        Masked array containing variable data. Can not contain NaNs
    basins : float32
        List containing basin names and masks.
    volume : float32
        Masked array containing cell volume.

    Returns
    -------
    regmean: float32
        List containing regional mean for variable var
    """
    if diagonals.CONFIG.use_gpu:
        logger.warning('GPU routines not implemented for regmean diagnostic.'
                       'Using CPU instead')
    regmean = _compute_regmean_3d_cpu(var, basins, volume)
    return regmean


def compute_regmean_levels(var, basins, volume):
    """Function that checks device and calls computing functions.

    Checks if the computations are going performed in the CPU or the GPU:

    Parameters
    ----------
    var : float32
        Masked array containing variable data. Can not contain NaNs
    basins : float32
        List containing basin names and masks.
    volume : float32
        Masked array containing cell volume.

    Returns
    -------
    regmean: float32
        List containing regional mean for variable var at each level.
    """
    if diagonals.CONFIG.use_gpu:
        logger.warning('GPU routines not implemented for regmean diagnostic.'
                       'Using CPU instead')
    else:
        regmean = _compute_regmean_levels_cpu(
            var, basins, volume
        )
    return regmean


def _compute_regmean_2d_cpu(var, basins, area):
    """Function that computes the regional mean for 2D vars in the cpu.

       Computes the weights for each region and performs a weighted average.

    Parameters
    ----------
    var : float32
        Masked array containing variable data.
    basins : float32
        List containing basin names and masks.
    area : float32
        Masked array containing cell area.

    Returns
    -------
    regmean_total: float32
        List containing regional mean for variable var.
    """
    regmean_total = {}
    for basin, mask in basins.items():
        weights = _compute_weights_2d(mask, area)
        regmean = da.ma.average(
            var,
            axis=(1, 2),
            weights=da.broadcast_to(weights, var.shape)
            )
        regmean_total[basin] = regmean
    return regmean_total


def _compute_regmean_3d_cpu(var, basins, volume):
    """Function that computes the regional mean for 3D vars in the cpu.

    Computes the weights for each region and performs a weighted average.

    Parameters
    ----------
    var : float32
        Masked array containing variable data.
    basins : float32
        List containing basin names and masks.
    volume : float32
        Masked array containing cell volume.

    Returns
    -------
    regmean_total: float32
        List containing the regional mean for variable var.
    """
    regmean_total = {}
    for basin, mask in basins.items():
        weights = _compute_weights_3d(mask, volume)
        regmean = da.ma.average(
                var,
                axis=(1, 2, 3),
                weights=da.broadcast_to(weights, var.shape)
                )
        regmean_total[basin] = regmean
    return regmean_total


def _compute_regmean_levels_cpu(var, basins, volume):
    """Function that computes the regional mean at every depth level
    for 3D vars in the cpu.

    Computes the weights for each region and performs a weighted average.

    Parameters
    ----------
    var : float32
        Masked array containing variable data.
    basins : float32
        List containing basin names and masks.
    volume : float32
        Masked array containing cell volume.

    Returns
    -------
    regmean_total: float32
        List containing regional mean at every depth level for variable var.
    """
    regmean_total = {}
    for basin, mask in basins.items():
        weights = _compute_weights_3d(mask, volume)
        regmean = da.ma.average(
            var,
            axis=(2, 3),
            weights=da.broadcast_to(weights, var.shape)
        )
        regmean_total[basin] = regmean
    return regmean_total


@vectorize(['float32(float32, float32)'], target='cpu')
def _compute_weights_2d(mask, area):
    """Function that computes the regional weights for 2D vars in the cpu.

    Parameters
    ----------
    mask : float32
        Mask array containing a region mask.
    area : float32
        Masked array containing cell area.

    Returns
    -------
    weights: float32
        Masked array containing the weights for a given region.
    """
    weights = mask * area
    if np.isnan(weights):
        weights = 0
    return weights


@vectorize(['float32(float32, float32)'], target='cpu')
def _compute_weights_3d(mask, volume):
    """Function that computes the regional weights for 3D vars in the cpu.

    Parameters
    ----------
    mask : float32
        Mask array containing a region mask.
    volume: float32
        Masked array containing cell volume.

    Returns
    -------
    weights: float32
        Masked array containing the weights for a given region.
    """
    weights = mask * volume
    if np.isnan(weights):
        weights = 0
    return weights
