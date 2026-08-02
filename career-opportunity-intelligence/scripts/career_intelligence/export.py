import csv, io, json

def sanitize(value):
    if isinstance(value,list): return [sanitize(item) for item in value]
    if not isinstance(value,dict): return value
    out={k:sanitize(v) for k,v in value.items()}
    if out.get("confidentiality_class") in {"private","restricted"} and "supported_text" in out:
        out["supported_text"]="[REDACTED]"
    return out

def to_json(records): return json.dumps(sanitize(records),indent=2,sort_keys=True,ensure_ascii=False)+"\n"
def flatten(v): return json.dumps(v,sort_keys=True,ensure_ascii=False) if isinstance(v,(dict,list)) else v
def to_csv(records):
    rows=sanitize(records if isinstance(records,list) else [records]); fields=sorted({k for r in rows for k in r}); buf=io.StringIO(newline=""); w=csv.DictWriter(buf,fieldnames=fields,lineterminator="\n"); w.writeheader(); w.writerows([{k:flatten(r.get(k)) for k in fields} for r in sorted(rows,key=lambda x:str(x.get("job_id",x.get("operation_id",""))))]); return buf.getvalue()
def to_markdown(records):
    rows=sanitize(records if isinstance(records,list) else [records]); lines=["# Career Opportunity Intelligence Export",""]
    for row in sorted(rows,key=lambda x:str(x.get("job_id",x.get("operation_id","")))):
        lines += [f"## {row.get('job_id',row.get('operation_id','Record'))}"]+[f"- **{k}:** {flatten(v)}" for k,v in sorted(row.items())]+[""]
    return "\n".join(lines)
def render(records,fmt): return {"json":to_json,"csv":to_csv,"markdown":to_markdown}[fmt](records)
