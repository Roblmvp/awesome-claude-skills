from abc import ABC, abstractmethod
import json
class LiveExecutionDisabled(RuntimeError): pass
class FirecrawlAdapter(ABC):
    @abstractmethod
    def execute(self,operation,params): raise NotImplementedError
class FixtureFirecrawlAdapter(FirecrawlAdapter):
    def __init__(self,path): self.data=json.loads(open(path,encoding="utf-8").read())
    def execute(self,operation,params): return self.data.get(operation,[])
class DisabledLiveFirecrawlAdapter(FirecrawlAdapter):
    def execute(self,operation,params): raise LiveExecutionDisabled(f"live Firecrawl {operation} execution is disabled in Phase 2B-1")
    def __getattr__(self,name): return lambda **kwargs: self.execute(name,kwargs)
