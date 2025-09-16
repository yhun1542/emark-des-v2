from typing import List, Dict, Any
import math

RUBRIC = [
  {"key":"feasibility","label":"실현가능성","weight":0.2},
  {"key":"creativity","label":"창의성","weight":0.2},
  {"key":"logic","label":"논리성","weight":0.2},
  {"key":"risk","label":"리스크분석","weight":0.2},
  {"key":"economics","label":"경제성","weight":0.2},
]

def weighted_total(scores: List[Dict[str,Any]]) -> float:
    weights = {r["key"]: r["weight"] for r in RUBRIC}
    total = 0.0
    for s in scores:
        total += (s["score"]/100.0) * weights.get(s["criterion"], 0.0) * 100.0
    return round(total, 1)

def standardize(totals: List[float]) -> List[float]:
    if not totals: return []
    mean = sum(totals)/len(totals)
    var = sum([(t-mean)**2 for t in totals])/len(totals) if len(totals)>1 else 1.0
    std = math.sqrt(var) or 1.0
    return [ round(((t-mean)/std*15 + 75), 1) for t in totals ]
