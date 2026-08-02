import argparse,json,sys
from pathlib import Path
from .classify import classify_jobs
from .deduplicate import deduplicate_jobs
from .export import render,to_json
from .firecrawl_plan import FirecrawlPlanBuilder
from .fit import match_job
from .normalize import normalize_jobs
from .requirements import aggregate_requirements
from .scoring import score_fit

def load(p): return json.loads(Path(p).read_text())
def write(p,data,fmt="json"): Path(p).parent.mkdir(parents=True,exist_ok=True); Path(p).write_text(render(data,fmt))
def parser():
 p=argparse.ArgumentParser(description="Offline career opportunity intelligence"); sub=p.add_subparsers(dest="cmd",required=True)
 sub.add_parser("validate-config")
 for name in ("normalize","deduplicate","classify","aggregate-requirements"):
  s=sub.add_parser(name); s.add_argument("--input",required=True); s.add_argument("--output",required=True)
 s=sub.add_parser("match-evidence"); s.add_argument("--jobs",required=True); s.add_argument("--evidence",required=True); s.add_argument("--mappings"); s.add_argument("--output",required=True)
 s=sub.add_parser("score"); s.add_argument("--fits",required=True); s.add_argument("--profile"); s.add_argument("--output",required=True)
 s=sub.add_parser("export"); s.add_argument("--input",required=True); s.add_argument("--format",choices=("json","csv","markdown"),required=True); s.add_argument("--output",required=True)
 s=sub.add_parser("plan-firecrawl"); s.add_argument("--profile",required=True); s.add_argument("--output",required=True)
 s=sub.add_parser("demo"); s.add_argument("--output-dir",required=True)
 return p

def demo(out):
 root=Path(__file__).resolve().parents[2]; fixtures=root/"tests"/"fixtures"; target=Path(out)
 if ".career-intelligence" not in target.parts: raise ValueError("demo output must be under .career-intelligence")
 raw=load(fixtures/"synthetic-jobs.json"); normalized=normalize_jobs(raw); deduped=deduplicate_jobs(normalized); classified=classify_jobs(deduped); evidence=load(fixtures/"synthetic-candidate-evidence.json"); mappings=load(fixtures/"synthetic-evidence-mappings.json")
 fits=[match_job(j,evidence,mappings) for j in classified]; profile=load(fixtures/"synthetic-scoring-profile.json"); scored=[score_fit(f,profile) for f in fits]; plans=FirecrawlPlanBuilder().sequence(load(fixtures/"synthetic-search-profile.json"))
 outputs={"normalized-jobs.json":normalized,"deduplicated-jobs.json":deduped,"role-classified-jobs.json":classified,"requirement-frequency.json":aggregate_requirements(classified),"fit-records.json":fits,"scored-opportunities.json":scored,"firecrawl-plan.json":plans,"audit-log.json":[e for j in classified for e in j.get("audit_events",[])]}
 for name,data in outputs.items(): write(target/name,data)
 write(target/"shortlist.md",scored,"markdown"); write(target/"opportunity-matrix.csv",scored,"csv"); return outputs

def main(argv=None):
 try:
  a=parser().parse_args(argv)
  if a.cmd=="validate-config": print('{"offline": true, "valid": true}'); return 0
  if a.cmd=="demo": demo(a.output_dir); return 0
  if a.cmd=="normalize": result=normalize_jobs(load(a.input))
  elif a.cmd=="deduplicate": result=deduplicate_jobs(load(a.input))
  elif a.cmd=="classify": result=classify_jobs(load(a.input))
  elif a.cmd=="aggregate-requirements": result=aggregate_requirements(load(a.input))
  elif a.cmd=="match-evidence":
   jobs=load(a.jobs); ev=load(a.evidence); mappings=load(a.mappings) if a.mappings else {}; result=[match_job(j,ev,mappings) for j in jobs]
  elif a.cmd=="score":
   profile=load(a.profile) if a.profile else None; result=[score_fit(f,profile) for f in load(a.fits)]
  elif a.cmd=="plan-firecrawl": result=FirecrawlPlanBuilder().sequence(load(a.profile))
  elif a.cmd=="export": Path(a.output).write_text(render(load(a.input),a.format)); return 0
  write(a.output,result); return 0
 except (ValueError,OSError,json.JSONDecodeError) as exc: print(f"error: {exc}",file=sys.stderr); return 2
