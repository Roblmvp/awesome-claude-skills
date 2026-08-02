WEIGHTS={"proven":1.0,"transferable":0.65,"developable":0.25,"unproven":0.0,"prohibitive":0.0,"unknown":0.0}
def score_fit(fit,profile=None):
    out=dict(fit); matches=fit["requirement_matches"]; denom=len(matches) or 1; components={k:sum(m["classification"]==k for m in matches)*v for k,v in WEIGHTS.items()}
    out["qualification_fit_score"]=round(100*sum(components.values())/denom,2)
    out["strategic_value_score"]=None if profile is None else round(sum(profile.get("criteria",{}).values())/max(len(profile.get("criteria",{})),1),2)
    unknown_ratio=fit.get("unknown_count",0)/denom; out["confidence_score"]=round(max(0,fit["evidence_coverage_score"]*(1-unknown_ratio)),2)
    prohibitive=fit.get("prohibitive_count",0); q=out["qualification_fit_score"]
    if unknown_ratio>.5: cls="manual_review"
    elif prohibitive: cls="future_state"
    elif q>=80: cls="direct_fit"
    elif q>=55: cls="bridge_fit"
    elif q>0: cls="strategic_stretch"
    else: cls="future_state"
    out["opportunity_class"]=cls; out["scoring_profile_version"]=profile.get("version") if profile else None; out["score_components"]={"weights":WEIGHTS,"weighted_counts":components,"denominator":denom,"unknown_ratio":unknown_ratio,"strategic_profile_supplied":profile is not None}; return out
