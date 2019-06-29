pypreload
===

LD_PRELOAD, but for Python.

# What?

pypreload is a Python package that enables quick dynamic hooking and replacing of foreign code. This is done by writing some script with hooks, and then invoking Python with the environment variable `PY_PRELOAD` pointed at the script.

# Example

The following example will make standard random operations in Python deterministic.

```python
import random
import os

from pypreload import hook, original

random_seeder = random.Random(42)

@hook(random.Random, 'seed')
def hooked_seed(self, a=None, version=2):
    original_seed = original()
    a = random_seeder.getrandbits(32)
    return original_seed(self, a, version)

random._inst.seed()

@hook(os, 'urandom')
def hooked_urandom(size):
    bits = random.getrandbits(8 * size)
    return bits.to_bytes(size, 'little')
```

In order to inject these hooks, Python must be run with the `PY_PRELOAD` environment variable:
```sh
PY_PRELOAD=examples/unrandom.py python
```

Now, standard random operations in Python will be deterministic:

```python
>>> import random
>>> random.random()
0.9148943365318702
>>> import os
>>> os.urandom(4)
b'\x04F\x8a^'
```

```python
>>> import random
>>> random.random()
0.9148943365318702
>>> import os
>>> os.urandom(4)
b'\x04F\x8a^'
```
