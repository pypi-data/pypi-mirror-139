from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import contextlib
import numpy as np
import pathlib

if TYPE_CHECKING:
    import collections.abc

__all__ = [
    "expand",
    "temporary_seed",
]


def expand(path: str, dir: Optional[str] = None) -> str:
    """Expand relative path or path with user shortcut.

    Parameters
    ----------
    path : str
        The path.
    dir : Optional[str], optional
        The directory containing the path, by default None.

    Returns
    -------
    str
        The explicit absolute path.
    """
    p = pathlib.Path(path).expanduser()
    if dir is not None:
        p = pathlib.Path(dir).joinpath(p)
    return str(p.expanduser().resolve())


@contextlib.contextmanager
def temporary_seed(seed: int) -> collections.abc.Generator[None, None, None]:
    """Temporarily set numpy random seed.

    Parameters
    ----------
    seed : int
        Random seed.
    """
    # adapted from https://stackoverflow.com/a/49557127
    state = np.random.get_state()
    if seed is not None:
        np.random.seed(seed)
    try:
        yield
    finally:
        np.random.set_state(state)
