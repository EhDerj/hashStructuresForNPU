from mat_hash import MatHash as HashClass
from typing import Any
from collections import defaultdict


class LinProb:
  def __init__(self, keySz: int, hshSz: int) -> None:
    self._recNum = 0
    self._arrSz = 1 << hshSz
    self._hash = HashClass(keySz, hshSz)
    self._arr = [None] * self._arrSz  # type: list[(Any, Any) or None]
    self._fatal = False

  def insert(self, key: Any, value: Any = "value") -> defaultdict:
    info = defaultdict(int)
    
    info["hCall"] += 1
    idx = self._hash(key)
    
    for _ in range(self._arrSz):
      info["rdNum"] += 1
      if self._arr[idx] is None or self._arr[idx][0] == key:
        if self._arr[idx] is None:
          self._recNum += 1
        info["wrNum"] += 1
        self._arr[idx] = (key, value)
        return info
      idx = (idx + 1) % self._arrSz
    self._fatal = True
    return info
  
  def search(self, key: Any) -> defaultdict:
    info = defaultdict(int)
    
    info["hCall"] += 1
    idx = self._hash(key)
    
    for _ in range(self._arrSz):
      info["rdNum"] += 1
      if self._arr[idx] is None or self._arr[idx][0] == key:
        break
      idx = (idx + 1) % self._arrSz
    return info
  
  def delete(self, key: Any) -> defaultdict:
    info = defaultdict(int)
    
    info["hCall"] += 1
    idx = self._hash(key)
    
    for _ in range(self._arrSz):
      info["rdNum"] += 1
      if self._arr[idx] is None:
        return info
      if self._arr[idx][0] == key:
        break
      idx = (idx + 1) % self._arrSz

    i, j = idx, (idx+1) % self._arrSz
    while 1:
      if j == i:  # if we run the entire array, usualy not used
        info["wrNum"] += 1
        self._arr[i] = None
        return info
      info["rdNum"] += 1
      if self._arr[j] is None:
        info["wrNum"] += 1
        self._arr[i] = None
        return info
      info["hCall"] += 1
      h = self._hash(self._arr[j][0])
      if not ((i - idx) % self._arrSz < (h - idx) % self._arrSz <= (j - idx) % self._arrSz):
        info["wrNum"] += 1
        self._arr[i] = self._arr[j]
        i = j
      j = (j+1) % self._arrSz
    self._fatal = True
