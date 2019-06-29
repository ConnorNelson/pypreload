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
