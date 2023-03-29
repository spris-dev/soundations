from typing import Literal
from opentelemetry import trace
from opentelemetry.util.types import AttributeValue


PayloadKey = Literal["track_search_prompt"]


class Tracer:
    def add(self, key: PayloadKey, value: AttributeValue) -> None:
        span = trace.get_current_span()
        span.set_attribute(key, value)
