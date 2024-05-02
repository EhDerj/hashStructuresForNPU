from mat_hash import MatHash as HashClass
import random as rd
from typing import Any, Hashable
from collections import defaultdict
from collections import deque
from itertools import cycle

class UniHash:
  def __init__(self, keySz: int, hshSz: int, hshNum: int = 1) -> None:
    self._recNum = 0
    self._arrSz = 1 << hshSz
    self._hshNum = hshNum
    self._toPush = deque(range(hshNum))
    rd.shuffle(self._toPush)
    self._hashes = [HashClass(keySz, hshSz) for _ in range(hshNum)]
    self._arr: list[(Any, Any)] = [None] * self._arrSz
    self._fatal = False

  def insert(self, key: Hashable, value: Any = "value") -> Any:
    info = defaultdict(int)
    for _ in range(3):
      for _ in range(50):
        cur = self._toPush[0]
        self._toPush.rotate(-1)
        for n, hFun in enumerate(self._hashes):
          info["hCall"] += 1
          info["rdNum"] += 1
          idx = hFun(key)
          if self._arr[idx] is None or self._arr[idx][0] == key:
            if self._arr[idx] is None:
              self._recNum += 1
            info["wrNum"] += 1
            self._arr[idx] = (key, value)
            return info
          if n == cur:
            currenPush = idx
        info["wrNum"] += 1
        (key, value), self._arr[currenPush] = self._arr[currenPush], (key, value)
      rd.shuffle(self._toPush)
    self._fatal = True
    return info


  def search(self, key: Any) -> Any:
    info = defaultdict(int)
    for hFun in self._hashes:
      info["hCall"] += 1
      info["rdNum"] += 1
      idx = hFun(key)
      if self._arr[idx] is not None and self._arr[idx][0] == key:
        break
    return info


  def delete(self, key: Any) -> Any:
    info = defaultdict(int)
    for hFun in self._hashes:
      info["hCall"] += 1
      info["rdNum"] += 1
      idx = hFun(key)
      if self._arr[idx] is not None and self._arr[idx][0] == key:
        info["wrNum"] += 1
        self._arr[idx] = None
        self._recNum -= 1
        break
    return info