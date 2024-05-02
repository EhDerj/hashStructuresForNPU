import random as rd
import numpy as np


class MatHash:
  def __init__(self, keySz: int, hshSz: int, *, slt=None, mat = None):
    self._keySz = keySz
    self._hshSz = hshSz
    self._keyPows = 1 << np.arange(keySz)[::-1]
    self._hshPows = 1 << np.arange(hshSz)[::-1]
    
    if slt is None:
      slt = rd.randrange(2**hshSz)
    self._slt = slt
        
    if mat is None:
      mat = np.random.choice((0, 1), (keySz, hshSz))
    self._mat = np.array(mat)


  def __call__(self, key: int):
    v = ((key & self._keyPows) > 0).astype(int)
    res = np.dot(v, self._mat) % 2
    res = res * self._hshPows
    return res.sum() ^ self._slt
