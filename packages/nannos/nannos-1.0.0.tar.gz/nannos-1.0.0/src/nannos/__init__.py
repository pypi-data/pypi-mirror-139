#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of nannos
# License: GPLv3
# See the documentation at nannos.gitlab.io

import os

from .__about__ import __author__, __description__, __version__
from .__about__ import data as _data
from .log import *

available_backends = ["numpy", "scipy", "autograd", "jax", "torch"]


def print_info():
    print(f"nannos v{__version__}")
    print("=============")
    print(__description__)
    print(f"Author: {__author__}")
    print(f"Licence: {_data['License']}")


def has_torch():
    try:
        import torch

        return True
    except ModuleNotFoundError:
        return False


def _has_cuda():
    try:
        import torch

        return torch.cuda.is_available()
    except ModuleNotFoundError:
        return False


HAS_TORCH = has_torch()
HAS_CUDA = _has_cuda()

_nannos_device = "cpu"


def use_gpu():
    global _nannos_device

    if BACKEND not in ["torch"]:
        log.info(f"Cannot use GPU with {BACKEND} backend.")

    if not HAS_TORCH:
        _nannos_device = "cpu"
        log.info("pytorch not found. Cannot use GPU.")
    elif not HAS_CUDA:
        _nannos_device = "cpu"
        log.info("cuda not found. Cannot use GPU.")
    else:
        _nannos_device = "cuda"
        log.info("Using GPU.")


def jit(fun, **kwargs):
    if BACKEND == "jax":
        from jax import jit

        return jit(fun, **kwargs)
    else:
        return fun


def _delvar(VAR):
    if VAR in globals():
        del globals()[VAR]


def set_backend(backend):
    """Set the numerical backend.

    Parameters
    ----------
    backend : str
        Either ``numpy``, ``scipy``, ``autograd``, ``torch`` or ``jax``.


    """

    import importlib
    import sys

    global _NUMPY
    global _SCIPY
    global _AUTOGRAD
    global _JAX
    global _TORCH
    global _FORCE_BACKEND

    _FORCE_BACKEND = 1

    if backend == get_backend():
        return
    #
    # _backend_env_var = os.environ.get("NANNOS_BACKEND")
    # if _backend_env_var is not None:
    #     if _backend_env_var in available_backends:
    #         if backend != _backend_env_var:
    #             # _delvar("_FORCE_BACKEND")
    #             pass
    #         else:
    #             backend = _backend_env_var

    if backend == "autograd":
        log.info("Setting autograd backend")
        _AUTOGRAD = True
        _delvar("_JAX")
        _delvar("_TORCH")
        _delvar("_SCIPY")
    elif backend == "scipy":
        log.info("Setting scipy backend")
        _SCIPY = True
        _delvar("_JAX")
        _delvar("_TORCH")
        _delvar("_AUTOGRAD")
    elif backend == "jax":
        log.info("Setting jax backend")
        _JAX = True
        _delvar("_SCIPY")
        _delvar("_TORCH")
        _delvar("_AUTOGRAD")
    elif backend == "torch":
        _TORCH = True
        log.info("Setting torch backend")
        _delvar("_SCIPY")
        _delvar("_JAX")
        _delvar("_AUTOGRAD")
    elif backend == "numpy":
        _NUMPY = True
        log.info("Setting numpy backend")
        _delvar("_SCIPY")
        _delvar("_JAX")
        _delvar("_AUTOGRAD")
        _delvar("_TORCH")
    else:
        raise ValueError(
            f"Unknown backend '{backend}'. Please choose between 'numpy', 'scipy', 'jax', 'torch' and 'autograd'."
        )

    import nannos

    importlib.reload(nannos)

    its = [s for s in sys.modules.items() if s[0].startswith("nannos")]
    for k, v in its:
        importlib.reload(v)


def get_backend():

    if "_SCIPY" in globals():
        return "scipy"
    elif "_AUTOGRAD" in globals():
        return "autograd"
    elif "_JAX" in globals():
        return "jax"
    elif "_TORCH" in globals():
        return "torch"
    else:
        return "numpy"


def grad(f):
    raise NotImplementedError(f"grad is not implemented for {BACKEND} backend.")


if "_SCIPY" in globals():

    import numpy

    backend = numpy
elif "_AUTOGRAD" in globals():
    from autograd import grad, numpy

    backend = numpy
elif "_JAX" in globals():

    from jax.config import config

    config.update("jax_platform_name", "cpu")
    config.update("jax_enable_x64", True)

    # TODO: jax eig not implemented on GPU
    # see https://github.com/google/jax/issues/1259
    # if _nannos_device == "cpu":
    #     config.update("jax_platform_name", "cpu")
    # else:
    #     config.update("jax_platform_name", "gpu")
    from jax import grad, numpy

    backend = numpy
elif "_TORCH" in globals():
    if HAS_TORCH:
        import numpy
        import torch

        # torch.set_default_tensor_type(torch.cuda.FloatTensor)

        backend = torch

        def _array(a, **kwargs):
            if isinstance(a, backend.Tensor):
                return a.to(torch.device(_nannos_device))
            else:
                return backend.tensor(a, **kwargs).to(torch.device(_nannos_device))

        backend.array = _array

        def grad(f):
            def df(x, *args, **kwargs):
                x = backend.array(x, dtype=bk.float64)
                _x = x.clone().detach().requires_grad_(True)
                return backend.autograd.grad(
                    f(_x, *args, **kwargs), _x, allow_unused=True
                )[0]

            return df

    else:
        log.info("pytorch not found. Falling back to default numpy backend.")
        set_backend("numpy")
else:
    import numpy

    backend = numpy


# TODO: support jax properly (is it faster than autograd? use jit?)
# jax does not support eig
# for autodif wrt eigenvectors yet.
# see: https://github.com/google/jax/issues/2748

BACKEND = get_backend()

_backend_env_var = os.environ.get("NANNOS_BACKEND")

if _backend_env_var in available_backends and _backend_env_var is not None:
    if BACKEND != _backend_env_var and not "_FORCE_BACKEND" in globals():
        log.info(f"Found environment variable NANNOS_BACKEND={_backend_env_var}")
        set_backend(_backend_env_var)

from .constants import *
from .excitation import *
from .lattice import *
from .layers import *
from .parallel import *
from .sample import *
from .simulation import *
from .utils import *
