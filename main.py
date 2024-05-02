import numpy as np
import pandas as pd
import random as rd
import sys

from collections import Counter, defaultdict
from itertools import product

from struct_linear import LinProb
from struct_peacock import PeacHash
from struct_universal import UniHash

KEYSIZE = 60
REPEATS_NUM = 10
HASH_SIZES = np.array([8, 10, 12, 14, 16])
DENSITY_VALUES = np.array([29, 24, 20, 16]) / 32

def initInfo():
  return Counter({
    'repeats': 0,
    'failure': 0,
    'success': 0,
    
    'isKey_insert_hCall': 0,
    'isKey_insert_rdNum': 0,
    'isKey_insert_wrNum': 0,
    
    'isKey_search_hCall': 0,
    'isKey_search_rdNum': 0,
    'isKey_search_wrNum': 0,
    
    'isKey_delete_hCall': 0,
    'isKey_delete_rdNum': 0,
    'isKey_delete_wrNum': 0,
    
    'noKey_insert_hCall': 0,
    'noKey_insert_rdNum': 0,
    'noKey_insert_wrNum': 0,
    
    'noKey_search_hCall': 0,
    'noKey_search_rdNum': 0,
    'noKey_search_wrNum': 0,
    
    'noKey_delete_hCall': 0,
    'noKey_delete_rdNum': 0,
    'noKey_delete_wrNum': 0,
  })

def fill(structType, hashSz, num, **args):
    struct = structType(KEYSIZE, hashSz, **args)
    keySet = set()
    while len(keySet) < num:
      keySet.add(rd.randrange(1<<KEYSIZE))
    for key in keySet:
        struct.insert(key, 0)
        if struct._fatal:
          return None, None
    return struct, keySet

def notInSet(st):
  res = rd.randrange(1<<KEYSIZE)
  while res in st:
    res = rd.randrange(1<<KEYSIZE)
  return res

def UniHash5(keySz, hshSz):
  return UniHash(keySz, hshSz, 5)

def UniHash15(keySz, hshSz):
  return UniHash(keySz, hshSz, 15)

def PeacHash5(keySz, hshSz):
  return PeacHash(keySz, hshSz, 5)

def PeacHashMax(keySz, hshSz):
  return PeacHash(keySz, hshSz, hshSz+1)

def main():
  if len(sys.argv) > 1:
    nRepeats = int(sys.argv[1])
  else:
    nRepeats = REPEATS_NUM

  infoLinProb     = defaultdict(initInfo)
  infoUniHash5    = defaultdict(initInfo)
  infoUniHash15   = defaultdict(initInfo)
  infoPeacHash5   = defaultdict(initInfo)
  infoPeacHashMax = defaultdict(initInfo)

  for _ in range(nRepeats):
    for hSize, density in product(HASH_SIZES, DENSITY_VALUES):
      for infoDict, typeStruct in zip(
        [infoLinProb, infoUniHash5, infoUniHash15, infoPeacHash5, infoPeacHashMax],
        [LinProb, UniHash5, UniHash15, PeacHash5, PeacHashMax]
      ):
        infoDict[hSize + density]['repeats'] += 1
        struct, currKeys = fill(typeStruct, hSize, (1<<hSize)*density)
        if struct is None:
          infoDict[hSize + density]['failure'] += 1
        else:
          srcNo = struct.search(notInSet(currKeys))
          delNo = struct.delete(notInSet(currKeys))
          insNo = struct.insert(notInSet(currKeys), 0)
          
          srcIs = struct.search(rd.choice(list(currKeys)))
          insIs = struct.insert(rd.choice(list(currKeys)), 0)
          delIs = struct.delete(rd.choice(list(currKeys)))
          
          if struct._fatal:
            infoDict[hSize + density]['failure'] += 1
          else:
            infoDict[hSize + density]['success'] += 1
            infoDict[hSize + density].update({f"isKey_insert_{i}": j for i, j in insIs.items()})
            infoDict[hSize + density].update({f"isKey_search_{i}": j for i, j in srcIs.items()})
            infoDict[hSize + density].update({f"isKey_delete_{i}": j for i, j in delIs.items()})
            
            infoDict[hSize + density].update({f"noKey_insert_{i}": j for i, j in insNo.items()})
            infoDict[hSize + density].update({f"noKey_search_{i}": j for i, j in srcNo.items()})
            infoDict[hSize + density].update({f"noKey_delete_{i}": j for i, j in delNo.items()})

  for infoDict, fileName in zip(
    [infoLinProb, infoUniHash5, infoUniHash15, infoPeacHash5, infoPeacHashMax],
    ["infoLinProb.csv", "infoUniHash5.csv", "infoUniHash15.csv", "infoPeacHash5.csv", "infoPeacHashMax.csv"]
  ):
    tmp1 = pd.read_csv(fileName, index_col=0)
    tmp2 = pd.DataFrame.from_dict(infoDict, orient='index')
    (tmp1 + tmp2).to_csv(fileName)


if __name__ == "__main__":
  for _ in range(22):
    main()