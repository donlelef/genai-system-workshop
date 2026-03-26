import base64
import logging
import os

from openinference.instrumentation.agno import AgnoInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

logger = logging.getLogger(__name__)


def configure_langfuse_tracing() -> None:
    langfuse_public = os.environ["LANGFUSE_PUBLIC_KEY"]
    langfuse_secret = os.environ["LANGFUSE_SECRET_KEY"]
    langfuse_base = os.environ.get("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")

    auth_token = base64.b64encode(
        f"{langfuse_public}:{langfuse_secret}".encode()
    ).decode()

    otel_endpoint = f"{langfuse_base}/api/public/otel"
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = otel_endpoint
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth_token}"

    tracer_provider = TracerProvider()
    tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
    AgnoInstrumentor().instrument(tracer_provider=tracer_provider)

    logger.info("Langfuse tracing configured -> %s", otel_endpoint)
