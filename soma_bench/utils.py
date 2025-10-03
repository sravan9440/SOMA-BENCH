from dataclasses import dataclass
import numpy as np
import random

@dataclass
class RNGs:
    np: np.random.Generator
    py: random.Random

def make_rng(seed: int) -> RNGs:
    return RNGs(np=np.random.default_rng(seed), py=random.Random(seed))
