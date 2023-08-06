import math

from binsdpy.utils import operational_taxonomic_units, BinaryFeatureVector


def peirce1(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Peirce similarity (v1)

    Peirce, C. S. (1884).
    The numerical measure of the success of predictions.
    Science, (93), 453-454.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / ((a + b) * (c + d))


def peirce2(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Peirce similarity (v2)

    Peirce, C. S. (1884).
    The numerical measure of the success of predictions.
    Science, (93), 453-454.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / ((a + c) * (b + d))


def yuleq(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Yule's Q similarity

    Yule, G. U. (1912).
    On the methods of measuring association between two attributes.
    Journal of the Royal Statistical Society, 75(6), 579-652.

    Yule, G. U. (1900).
    On the association of attributes in statistics.
    Philosophical Transactions of the Royal Society. Series A, 194, 257-319.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / (a * d + b * c)


def yulew(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Yule's W similarity

    Yule, G. U. (1912).
    On the methods of measuring association between two attributes.
    Journal of the Royal Statistical Society, 75(6), 579-652.

    Yule, G. U. (1900).
    On the association of attributes in statistics.
    Philosophical Transactions of the Royal Society. Series A, 194, 257-319.


    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (math.sqrt(a * d) - math.sqrt(b * c)) / (math.sqrt(a * d) + math.sqrt(b * c))


def pearson1(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Pearson Chi-Squared similarity

    Pearson, K., & Heron, D. (1913).
    On theories of association.
    Biometrika, 9(1/2), 159-315.

    Pearson, K. X. (1900).
    On the criterion that a given system of deviations from the probable in the case 538 of a correlated system of variables is such that it can be reasonably supposed to have arisen 539 from random sampling.
    London, Edinburgh, Dublin Philos. Mag. J. Sci, 540, 50.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return (n * ((a * d - b * c) ** 2)) / ((a + b) * (a + c) * (b + d) * (c + d))


def pearson2(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Pearson similarity (v2)

    Pearson, K., & Heron, D. (1913).
    On theories of association.
    Biometrika, 9(1/2), 159-315.

    Pearson, K. X. (1900).
    On the criterion that a given system of deviations from the probable in the case 538 of a correlated system of variables is such that it can be reasonably supposed to have arisen 539 from random sampling.
    London, Edinburgh, Dublin Philos. Mag. J. Sci, 540, 50.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    x_2 = pearson1(x, y, mask)

    return math.sqrt(x_2 / (a + b + c + d + x_2))


def phi(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Phi similarity

    Yule, G. U. (1912).
    On the methods of measuring association between two attributes.
    Journal of the Royal Statistical Society, 75(6), 579-652.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / math.sqrt((a + b) * (a + c) * (b + d) * (c + d))


def michael(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Michael similarity

    Michael, E. L. (1920).
    Marine ecology and the coefficient of association: a plea in behalf of quantitative biology.
    Journal of Ecology, 8(1), 54-59.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return 4 * (a * d - b * c) / ((a + d) ** 2 + (b + c) ** 2)


def cole1(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Cole similarity (v1)

    Cole, L. C. (1957).
    The measurement of partial interspecific association.
    Ecology, 38(2), 226-233.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / ((a + c) * (c + d))


def cole2(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Cole similarity (v2)

    Cole, L. C. (1957).
    The measurement of partial interspecific association.
    Ecology, 38(2), 226-233.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / ((a + b) * (b + d))


def cole(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Cole similarity
    
    Cole, L. C. (1957).
    The measurement of partial interspecific association.
    Ecology, 38(2), 226-233.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    if (a * d) >= (b * c):
        return (a * d - b * c) / ((a + b) * (b + d))
    elif (a * d) < (b * c) and a <= d:
        return (a * d - b * c) / ((a + b) * (a + c))
    else:
        return (a * d - b * c) / ((b + d) * (c + d))


def cohen(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Cohen similarity

    Cohen, J. (1960).
    A coefficient of agreement for nominal scales.
    Educational and psychological measurement, 20(1), 37-46.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (2 * (a * d - b * c)) / math.sqrt((a + b) * (b + d) + (a + c) * (c + d))


def maxwell_pilliner(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Maxwell-Pilliner similarity

    Maxwell, A. E., & Pilliner, A. E. G. (1968).
    Deriving coefficients of reliability and agreement for ratings.
    British Journal of Mathematical and Statistical Psychology, 21(1), 105-116.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (2 * (a * d - b * c)) / ((a + b) * (c + d) + (a + c) * (b + d))


def dennis(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Dennis similarity

    Dennis, S. F. (1965).
    The Construction of a Thesaurus Automatically From.
    In Statistical Association Methods for Mechanized Documentation: Symposium Proceedings (Vol. 269, p. 61).
    US Government Printing Office.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / math.sqrt((a + b + c + d) * (a + b) * (a + c))


def disperson(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Disperson similarity

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return (a * d - b * c) / (n * n)


def consonni_todeschini5(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Consonni and Todeschini (v5)

    Consonni, V., & Todeschini, R. (2012).
    New similarity coefficients for binary data.
    Match-Communications in Mathematical and Computer Chemistry, 68(2), 581.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return (math.log(1 + a * d) - math.log(1 + b * c)) / math.log(
        1 + n * n / 4
    )


def stiles(
    x: BinaryFeatureVector, y: BinaryFeatureVector, mask: BinaryFeatureVector = None
) -> float:
    """Stiles similarity

    Stiles, H. E. (1961).
    The association factor in information retrieval.
    Journal of the ACM (JACM), 8(2), 271-279.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    t = abs(a * d - b * c) - .5 * n

    return math.log10(
        (n * t * t)
        / ((a + b) * (a + c) * (b + d) * (c + d))
    )
