import os, json, uuid
from typing import Dict, Any, Generator, List
from adapters_shim import get_providers
from scoring import weighted_total, standardize

ENABLE_REAL = (os.getenv("ENABLE_REAL_CALLS","false").lower()=="true")
SELF_PENALTY = float(os.getenv("SELF_SCORE_PENALTY","0.5"))
STANDARDIZE = (os.getenv("STANDARDIZE_SCORES","true").lower()=="true")

def run_streaming(question:str):
    sid = str(uuid.uuid4())
    yield {"type":"session.start","id":sid,"question":question}

    teams = {}
    providers = get_providers()

    for p in providers:
        model = p.key
        yield {"type":"team.start","model":model}
        out = p.team_discussion(question)
        for role in ["leader","blue","research","red"]:
            yield {"type":"role.done","model":model,"role":role,"message":{"role":role,"content":out[role]}}
        yield {"type":"team.summary","model":model,"summary":out["summary"]}
        yield {"type":"team.done","model":model}
        teams[model] = out
    yield {"type":"stage.done","stage":1}

    evaluations = []
    for ev in providers:
        ev_key = ev.key
        target_summaries = { m: t["summary"] for m,t in teams.items() }
        data = ev.evaluate_targets(question, target_summaries)
        for target in target_summaries.keys():
            scores = data.get("scores", [])
            total = weighted_total(scores)
            if target == ev_key:
                total *= SELF_PENALTY
            evaluations.append({"evaluator":ev_key,"target":target,"scores":scores,"total":round(total,1),"notes":data.get("notes","")})
            yield {"type":"evaluation.done","evaluator":ev_key,"target":target,"evaluation":evaluations[-1]}
    yield {"type":"stage.done","stage":2}

    targets = sorted(teams.keys())
    per_target = {t: [] for t in targets}
    for e in evaluations:
        per_target[e["target"]].append(e["total"])

    final = []
    for t, arr in per_target.items():
        avg = round(sum(arr)/len(arr),1) if arr else 0.0
        # Use first eval's scores as proxy breakdown (demo)
        first_scores = next((e["scores"] for e in evaluations if e["target"]==t), [])
        final.append({"model":t,"total":avg,"breakdown":first_scores})
    final.sort(key=lambda x: x["total"], reverse=True)

    session = {"id":sid,"question":question,"teams":[{"model":m, **teams[m]} for m in targets], "evaluations":evaluations, "finalRanking":final}
    yield {"type":"final","session":session}
