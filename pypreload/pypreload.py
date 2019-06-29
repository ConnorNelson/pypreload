#!/usr/bin/env python

import os
import functools
import inspect
import runpy

_originals = dict()

def install_hooks():
    path = os.getenv('PY_PRELOAD')
    if path is None:
        return

    runpy.run_path(path, run_name='py_preloaded')

def hook(obj, attr):
    original = getattr(obj, attr)
    def wrapper(new_attr):
        wrapped_attr = new_attr
        setattr(obj, attr, wrapped_attr)
        if hasattr(wrapped_attr, '__code__'):
            _originals[wrapped_attr.__code__] = original
        return wrapped_attr
    return wrapper

def original():
    for frame_info in inspect.stack():
        frame = frame_info.frame
        if frame.f_code in _originals:
            return _originals[frame.f_code]
    else:
        raise Exception("`original` must be called from a hooked function")
