import typing
import bitsets
import numpy as np


BinaryFeatureVector = typing.Union["bitsets.bases.MemberBits", "np.ndarray"]


def operational_taxonomic_units(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> typing.Tuple[float, float, float, float]:
    """Calculates Operational Taxonomic Units table for two vectors

    Args:
        x (BinaryFeatureVector): first binary feature vector
        y (BinaryFeatureVector): second binary feature vector
        mask (BinaryFeatureVector): mask of which features will be used for calculating similarity

    Returns:
        typing.Tuple[float, float, float, float]: values from the table
    """
    if isinstance(x, np.ndarray):
        if mask is None:
            not_x = np.invert(x)
            not_y = np.invert(y)
        else:
            x = x & mask
            y = y & mask

            not_x = np.invert(x) & mask
            not_y = np.invert(y) & mask

        a = np.count_nonzero(x & y)
        b = np.count_nonzero(not_x & y)
        c = np.count_nonzero(x & not_y)
        d = np.count_nonzero(not_x & not_y)
    elif isinstance(x, bitsets.bases.MemberBits):
        Vector = type(x)
        universum = Vector.supremum

        if mask is None:
            not_x = universum ^ x
            not_y = universum ^ y
        else:
            x = x & mask
            y = y & mask

            not_x = (universum ^ x) & mask
            not_y = (universum ^ y) & mask

        a = Vector.fromint(x & y).count()
        b = Vector.fromint(not_x & y).count()
        c = Vector.fromint(x & not_y).count()
        d = Vector.fromint(not_x & not_y).count()
    else:
        raise ValueError(
            "Function is defined only for 'bitsets.bases.MemberBits' or 'np.ndarray'."
        )

    return a, b, c, d
