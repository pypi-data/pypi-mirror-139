from __future__ import annotations
from typing import Iterable, Optional

import contextlib
import math
import numpy as np
import scipy.linalg
import scipy.spatial

from .utils import temporary_seed

__all__ = [
    "divisors",
    "lcm",
    "linearly_independent",
    "nearest_points",
    "nontrivial_vector",
    "normalize",
    "orthogonal_decomp",
    "periodicity",
    "perpendicular_vector",
    "reflection_matrix",
    "rotation_matrix",
    "sample_spherical_lune",
    "sample_spherical_triangle",
    "spherical_excess",
    "tetrahedron_volume",
]


def divisors(n: int) -> list[int]:
    """Find all positive integer divisors of a given positive integer.

    Parameters
    ----------
    n : int
        Number whose divisors are to be found.

    Returns
    -------
    list[int]
        List of divisors of :math:`n`.
    """
    if n == 1:
        return [1]

    d = [1, n]

    sqrt = math.ceil(math.sqrt(n))

    for k in range(2, sqrt):
        if n % k == 0:
            d.extend([k, n // k])

    if n == sqrt ** 2 and sqrt not in d:
        d.append(sqrt)

    return sorted(d)


def lcm(numbers: Iterable[int]) -> int:
    """Find least common multiple of a list of integers.

    Parameters
    ----------
    numbers : Iterable[int]
        Integers whose least common multiple is to be found

    Returns
    -------
    int
        Least common multiple
    """
    a, *b = numbers
    if len(b) > 1:
        return lcm(numbers=(a, lcm(numbers=b)))
    else:
        [b] = b
        return a * b // math.gcd(a, b)


def linearly_independent(
    vectors: np.ndarray, indep: Optional[np.ndarray] = None
) -> np.ndarray:
    """Select a linearly independent subset of vectors from the given set.

    Parameters
    ----------
    vectors : np.ndarray
        Array of :math:`N` :math:`k`-dimensional candidate vectors.
        Shape: :math:`(k,N)`
    indep : Optional[np.ndarray], optional
        Array of :math:`M` known linearly independent :math:`k`-dimensional vectors.
        By default None.
        Shape: :math:`(k,M)`

    Returns
    -------
    np.ndarray
        Linearly independent subset of vectors
    """
    # vectors is kxNv array where Nv is number of vectors
    # indep is kxNi array where Ni is number of linearly independent vectors

    if indep is None:
        indep = np.array([[]])

    k, _ = vectors.shape  # dimension of vectors
    _, n = indep.shape  # number of independent vectors

    arrays = (np.vstack([*indep.T, v]) for v in vectors.T)
    try:
        indep = next(
            a for a in arrays if scipy.linalg.null_space(a).shape[-1] == k - n - 1
        ).T
        return linearly_independent(vectors=vectors, indep=indep)
    except StopIteration:
        return indep


def nearest_points(points: np.ndarray, m: int) -> np.ndarray:
    """
    Find the nearest points from a given list of points.

    Parameters
    ----------
    points : numpy.ndarray
        Array of :math:`n` points in :math:`d`-dimensional space.
        Shape: :math:`(d,n)`

    m : int
        number of nearest points to find

    Returns
    -------
    numpy.ndarray:
        Array of the :math:`m` nearest points from the given list of points.
        Shape: :math:`(d,m)`
    """

    tree = scipy.spatial.KDTree(points.T)

    # this ensures that the first loop finds the two nearest points of all the points
    centroid = points

    for i in range(m - 1):
        dists, inds = tree.query(centroid.T, k=2 + i)

        if i == 0:
            nn_dists = dists[:, -1]
            inds = inds[np.argmin(nn_dists), :]

        cluster = points.T[inds].T

        centroid = cluster.mean(axis=1)

    return cluster


def nontrivial_vector(R: np.ndarray, seed: Optional[int] = None) -> np.ndarray:
    """
    Generates a random vector acted upon nontrivially
    (i.e. is sent to a linearly independent vector)
    by the given rotation matrix.

    Parameters
    ----------
    R: numpy.ndarray
        Array representing a rotation matrix.
        Shape: :math:`(3,3)`

    Returns
    -------
    numpy.ndarray:
        Array representing a vector which is acted upon nontrivially by R.
        Shape: :math:`(3,1)`
    """
    identity = np.eye(3)
    if (
        np.allclose(R, identity)
        or np.allclose(R, -identity)
        or np.allclose(R, np.zeros_like(identity))
    ):
        return None

    # get the eigenvectors with real (i.e. 1 or -1) eigenvalues,
    # since these are mapped to colinear vectors by R
    # each column of evecs is an eigenvector of R
    evals, evecs = scipy.linalg.eig(R)

    real_eigenbasis = np.real(evecs.T[np.isclose(np.imag(evals), 0)].T)

    # form the linear combination of the "trivial" eigenvectors
    # get random coefficients between 1 and 2 so that 0 is never chosen
    # the result is guaranteed to be mapped to a linearly independent vector
    # by R because the "trivial" eigenvectors do not all have the same eigenvalues
    # this is true because R is not proportional to the identity matrix
    with temporary_seed(seed=seed) if seed is not None else contextlib.nullcontext():
        coeffs = np.random.uniform(low=1, high=2, size=(real_eigenbasis.shape[1], 1))

    return normalize(v=real_eigenbasis @ coeffs)


def normalize(v: np.ndarray) -> np.ndarray:
    """Normalize a vector.

    Parameters
    ----------
    v : numpy.ndarray
        Vector to be normalized.
        Shape: :math:`(3,1)`

    Returns
    -------
    numpy.ndarray
        Normalized vector.
        Shape: :math:`(3,1)`
    """
    norm = np.linalg.norm(v)

    return v / norm if norm > 0 else v


def orthogonal_decomp(v: np.ndarray, u: np.ndarray) -> np.ndarray:
    """Decompose a vector into a projection and the orthogonal complement.

    Parameters
    ----------
    v : numpy.ndarray
        Array to be decomposed.
        Shape: :math:`(3,1)`
    u : numpy.ndarray
        Array defining the subspace decomposition.
        Shape: :math:`(3,1)`

    Returns
    -------
    numpy.ndarray
        Projection of :math:`v` along :math:`u`.
        Shape: :math:`(3,1)`
    numpy.ndarray
        Orthogonal complement of :math:`v` relative to :math:`u`.
        Shape: :math:`(3,1)`
    """
    a = normalize(u)
    projection = np.dot(v.T, a) * a
    complement = v - projection

    return projection, complement


def periodicity(matrix: np.ndarray) -> int:
    # if A is periodic, then its eigenvalues are roots of unity,
    # and its periodicity is the lcm of the periodicities of these roots of unity
    # kth roots of unity form the vertices of
    # a regular k-gon with internal angles 2*pi/k
    # the angle between two such vertices z1=a+jb and
    # z2=c+jd is given by cos(theta) = a*c + b*d = Re(z1*conj(z2))
    # choose z2 = z1**2 (clearly z2 is still a root of unity);
    # then z1*conj(z2) = exp(2*pi*j/k)*exp(-4*pi*j/k) = exp(-2*pi*j/k)
    # then Re(z1*conj(z2)) = Re(exp(-2*pi*j/k)) = cos(2*pi*j/k) = Re(z1)
    # so 2*pi*j/k = arccos(Re(z1)) -> j/k = arccos(Re(z1))/(2*pi),
    # and k = lcm(k/j1, k/j2,...)
    evals = scipy.linalg.eigvals(matrix)
    angles = (max(min(z.real, 1), -1) for z in evals if not np.isclose(z, 1))
    # if z is close to 1, then it contributes a period of 1,
    # which doesn't impact the lcm and therefore the final period
    periods = [int((2 * np.pi / np.arccos(angle)).round()) for angle in angles]

    if len(periods) == 0:
        # all evals must have been close to 1
        return 1
    else:
        return lcm(numbers=periods)


def perpendicular_vector(a: np.ndarray, b: Optional[np.ndarray] = None) -> np.ndarray:
    """
    Generates a unit vector which is perpendicular to
    one or two given nonzero vector(s).

    Parameters
    ----------
    a: numpy.ndarray
        Array representing a nonzero vector.
        Shape: :math:`(3,1)`
    b: numpy.ndarray
        Array representing a nonzero vector.
        Shape: :math:`(3,1)`

    Returns
    -------
    numpy.ndarray:
        Array representing a unit vector which
        is perpendicular to a (and b, if applicable).
        Shape: :math:`(3,1)`
    """
    if b is None:
        m = np.zeros(a.shape)

        # storing in variable for reuse
        ravel_a = np.ravel(a)

        # index of the first nonzero element of a
        i = (ravel_a != 0).argmax()
        # first index of a which is not i
        j = next(ind for ind in range(len(ravel_a)) if ind != i)
        # unravel indices for 3x1 arrays m and a
        i, j = (
            np.unravel_index(i, a.shape),
            np.unravel_index(j, a.shape),
        )

        # make m = np.array([[-ay,ax,0]]).T so np.dot(m.T,a) = -ax*ay + ax*ay = 0
        m[j] = a[i]
        m[i] = -a[j]
    else:
        m = np.cross(a.T, b.T).T

    return normalize(v=m)


def reflection_matrix(normal: np.ndarray) -> np.ndarray:
    """Generates a reflection matrix given a normal vector.

    Parameters
    ----------
    normal : numpy.ndarray
        Array normal to the reflection plane.
        Shape: :math:`(3,1)`

    Returns
    -------
    numpy.ndarray
        Reflection matrix.
        Shape: :math:`(3,3)`
    """
    n = normalize(normal)
    return np.eye(3) - 2 * np.outer(n, n)


def rotation_matrix(
    axis: Optional[np.ndarray] = None,
    theta: Optional[float] = None,
    m: Optional[np.ndarray] = None,
    n: Optional[np.ndarray] = None,
    improper: Optional[bool] = False,
) -> np.ndarray:
    """Generates a rotation matrix given an axis and angle.

    Parameters
    ----------
    axis: numpy.ndarray
        Axis of rotation.
        Shape: :math:`(3,1)`
    theta: float
        Angle of rotation (in radians) about the axis of rotation.
    m: numpy.ndarray
        The vector to be rotated.
        Shape: :math:`(3,1)`
    n: numpy.ndarray
        The vector after rotation, i.e. the target vector.
        Shape: :math:`(3,1)`
    improper: bool
        If true, return an improper rotation.
        By default False.

    Returns
    -------
    numpy.ndarray:
        Rotation matrix.
        Shape: :math:`(3,3)`
    """
    if m is not None and n is not None:
        a = normalize(np.cross(m.T, n.T).T)
        c = np.dot(normalize(m).T, normalize(n))
    elif axis is not None and theta is not None:
        a = normalize(axis)
        c = np.cos(theta)
    else:
        raise ValueError("Provide either an axis and an angle or a pair of vectors.")

    u1, u2, u3 = np.ravel(a)

    K = np.array([[0, -u3, u2], [u3, 0, -u1], [-u2, u1, 0]])

    s = np.sqrt(1 - c ** 2)

    R = (np.eye(3) + s * K + (1 - c) * (K @ K)).astype("float64")

    if improper:
        R = R @ reflection_matrix(a)

    R, _ = scipy.linalg.polar(R)

    return R


def sample_spherical_lune(n1: np.ndarray, n2: np.ndarray) -> np.ndarray:
    """Sample point on unit sphere from within lune defined by two plane normals.

    Parameters
    ----------
    n1 : np.ndarray
        First plane normal.
        Shape: :math:`(3,1)`
    n2 : np.ndarray
        Second plane normal.
        Shape: :math:`(3,1)`

    Returns
    -------
    np.ndarray
        Sampled point.
        Shape: :math:`(3,1)`
    """
    # angular extent of lune
    dphi = np.arccos(np.dot(n1.T, n2)).item()

    # sample point from standard polar lune of correct angular extent
    eps = np.finfo(float).eps

    phi = np.random.uniform(low=eps, high=dphi)
    cos_theta = np.random.uniform(low=-1, high=1)
    sin_theta = np.sqrt(1 - cos_theta ** 2)

    q = np.array([[sin_theta * np.cos(phi), sin_theta * np.sin(phi), cos_theta]]).T

    # rotate sampled point to lie within correct lune
    y = np.array([[0, 1, 0]]).T
    v = np.array([[-np.sin(dphi), np.cos(dphi), 0]]).T
    Ru = rotation_matrix(m=y, n=n1)

    _, vprime = orthogonal_decomp(Ru @ v, n1)
    _, n2prime = orthogonal_decomp(n2, n1)
    axis = np.cross(n2.T, vprime.T)
    theta = np.arccos(np.dot(normalize(vprime).T, normalize(n2prime)))
    Rv = rotation_matrix(axis=axis, theta=theta)

    return (Rv @ Ru) @ q


def sample_spherical_triangle(
    A: np.ndarray,
    B: np.ndarray,
    C: np.ndarray,
    sin_alpha: float,
    sin_beta: float,
    sin_gamma: float,
    seed: Optional[int] = None,
) -> np.ndarray:
    """Sample point from spherical triangle defined by vertices.

    Parameters
    ----------
    A : np.ndarray
        First vertex coordinates.
        Shape: :math:`(3,1)`
    B : np.ndarray
        Second vertex coordinates.
        Shape: :math:`(3,1)`
    C : np.ndarray
        Third vertex coordinates.
        Shape: :math:`(3,1)`
    sin_alpha : float
        Sine of angle at vertex :math:`A`.
    sin_beta : float
        Sine of angle at vertex :math:`B`.
    sin_gamma : float
        Sine of angle at vertex :math:`C`.
    seed : Optional[int], optional
        Random seed.
        By default None.

    Returns
    -------
    np.ndarray
        Sampled point.
        Shape: :math:`(3,1)`
    """
    # see https://www.graphics.cornell.edu/pubs/1995/Arv95c.pdf
    # a, b, and c are cross products of normal vectors, so their magnitudes
    # are the sine of the angles between these normal vectors; these angles
    # are also the angles between planes and therefore the great arcs which
    # define the legs of the triangle; therefore, these angles are also
    # the internal angles of the triangle
    eps = np.finfo(float).eps  # machine precision

    with temporary_seed(seed=seed):
        fraction, cos_theta = np.random.uniform(low=eps, high=1, size=2)

    cos_alpha, cos_beta, cos_gamma = np.sqrt(
        (1 - sin_alpha ** 2, 1 - sin_beta ** 2, 1 - sin_gamma ** 2)
    )

    area = fraction * spherical_excess(
        cos_alpha=cos_alpha, cos_beta=cos_beta, cos_gamma=cos_gamma
    )
    cos_area, sin_area = np.cos(area), np.sin(area)

    # s = sin(area - alpha)
    s = sin_area * cos_alpha - cos_area * sin_alpha
    # t = cos(area - alpha)
    t = cos_area * cos_alpha + sin_area * sin_alpha
    u = t - cos_alpha
    # spherical law of cosines
    v = s + (cos_gamma + cos_beta * cos_alpha) / sin_beta

    q = ((v * t - u * s) * cos_alpha - v) / ((v * s + u * t) * sin_alpha)
    _, x = orthogonal_decomp(C, A)
    C_prime = q * A + np.sqrt(1 - q ** 2) * normalize(x)

    z = 1 - cos_theta * (1 - np.dot(C_prime.T, B))
    _, x = orthogonal_decomp(C_prime, B)
    return z * B + np.sqrt(1 - z ** 2) * normalize(x)


def spherical_excess(cos_alpha: float, cos_beta: float, cos_gamma: float) -> float:
    # Girard's formula for spherical excess
    return np.arccos((cos_alpha, cos_beta, cos_gamma)).sum() - np.pi


def tetrahedron_volume(vertices: np.ndarray) -> float:
    """Calculate volume of a tetrahedron given its vertices.

    Parameters
    ----------
    vertices : numpy.ndarray
        Vertex coordinates.
        Shape: :math:`(3,4)`

    Returns
    -------
    float
        Volume of tetrahedron
    """
    a, b, c, d = np.vsplit(vertices.T, 4)
    return np.abs(np.einsum("ij,ij->i", a - d, np.cross(b - d, c - d))) / 6
