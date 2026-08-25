from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any
import llm


@dataclass
class CompareResult:
    model_id: str
    response: Any | None = None
    error: str | None = None


def _validated_options(model, options):
    if not options:
        return {}
    options_class = getattr(model, "Options", None)
    if options_class is None:
        return dict(options)

    try:
        validated = options_class(**options)
        if hasattr(validated, "model_dump"):
            return {k: v for k, v in validated.model_dump().items() if v is not None}
        if hasattr(validated, "dict"):
            return {k: v for k, v in validated.dict().items() if v is not None}
        return dict(options)
    except Exception as ex:
        raise ValueError(f"Invalid model options: {ex}") from ex


def run_compare(
    *,
    prompt,
    model_ids,
    system=None,
    options=None,
    attachments=None,
    fragments=None,
    database=None,
    max_workers=8,
    log_responses=True,
):
    options = options or {}
    attachments = attachments or []
    fragments = fragments or []

    def run_model(model_id):
        try:
            model = llm.get_model(model_id)
            validated = _validated_options(model, options)
            conversation = model.conversation()
            kwargs = dict(system=system, attachments=attachments, fragments=fragments)
            kwargs.update(validated)
            response = conversation.prompt(prompt, **kwargs)
            response.text()

            if (
                database is not None
                and log_responses
                and hasattr(response, "log_to_db")
            ):
                response.log_to_db(database)
            return CompareResult(model_id=model_id, response=response)
        except Exception as ex:
            return CompareResult(model_id=model_id, error=str(ex))

    workers = min(max(1, len(model_ids)), max_workers)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(run_model, model_id) for model_id in model_ids]
        return [future.result() for future in futures]
