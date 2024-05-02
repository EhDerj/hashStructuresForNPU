from mat_hash import MatHash as HashClass
import random as rd
from typing import Any, Hashable
from collections import defaultdict


class PeacHash:
  def __init__(self, keySz: int, hshSz: int, arrNum: int = 5) -> None:
    self._recNum = 0
    arrNum -= 1
    self._arrSzs = [hshSz -1 - i for i in range(arrNum)]
    self._arrSzs[-1] += 1
    self._arrNum = arrNum
    self._hashes = [HashClass(keySz, hs) for hs in self._arrSzs]
    self._arrays: list[list[(Any, Any)]] = [[None] * (1<<sz) for sz in self._arrSzs]
    self._fatal = False
    
  def insert(self, key: Hashable, value: Any = "value") -> Any:
    info = defaultdict(int)
    for curHsh, curArr in zip(self._hashes, self._arrays):
      info["hCall"] += 1
      idx = curHsh(key)
      info["rdNum"] += 1
      if curArr[idx] is None or curArr[idx][0] == key:
        if curArr[idx] is None:
          self._recNum += 1
        info["wrNum"] += 1
        curArr[idx] = (key, value)
        break
    self._fatal = True
    return info

  def search(self, key: Any) -> Any:
    info = defaultdict(int)
    for curHsh, curArr in zip(self._hashes, self._arrays):
      info["hCall"] += 1
      idx = curHsh(key)
      info["rdNum"] += 1
      if curArr[idx] is not None and curArr[idx][0] == key:
        break
    return info

  def delete(self, key: Any) -> Any:
    info = defaultdict(int)
    for curHsh, curArr in zip(self._hashes, self._arrays):
      info["hCall"] += 1
      idx = curHsh(key)
      info["rdNum"] += 1
      if curArr[idx] is not None and curArr[idx][0] == key:
        info["wrNum"] += 1
        curArr[idx] = None
        self._recNum -= 1
        break
    return info
