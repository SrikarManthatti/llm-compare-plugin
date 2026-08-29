import time
from llm_compare.compare import run_compare

class Response:
    def __init__(self, text): self._text=text
    def text(self): return self._text
class Conversation:
    def __init__(self, model): self.model=model
    def prompt(self, prompt, **kwargs): return self.model.make(prompt, **kwargs)
class Model:
    def __init__(self, name, delay=0, error=None): self.name=name; self.delay=delay; self.error=error
    def conversation(self): return Conversation(self)
    def make(self, prompt, **kwargs):
        if self.delay: time.sleep(self.delay)
        if self.error: raise RuntimeError(self.error)
        return Response(f"Response from {self.name}")

def test_order_is_preserved(monkeypatch):
    models={"slow":Model("slow",.05),"fast":Model("fast")}
    monkeypatch.setattr("llm_compare.compare.llm.get_model", lambda x: models[x])
    results=run_compare(prompt="hi", model_ids=["slow","fast"])
    assert [r.model_id for r in results]==["slow","fast"]
    assert [r.response.text() for r in results]==["Response from slow","Response from fast"]

def test_failure_does_not_stop_others(monkeypatch):
    models={"a":Model("A"),"bad":Model("bad",error="Intentional test failure"),"b":Model("B")}
    monkeypatch.setattr("llm_compare.compare.llm.get_model", lambda x: models[x])
    results=run_compare(prompt="hi", model_ids=["a","bad","b"])
    assert results[0].response.text()=="Response from A"
    assert results[1].error=="Intentional test failure"
    assert results[2].response.text()=="Response from B"
