import os
from time import monotonic
from typing import Any, Awaitable, Callable, Dict, List
import prometheus_client
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    REGISTRY,
    CollectorRegistry,
    generate_latest,
)
from prometheus_client.multiprocess import MultiProcessCollector
from starlette.requests import Request
from starlette.responses import Response


DEFAULT_BUCKETS = (
    0.005,
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.125,
    0.15,
    0.175,
    0.2,
    0.25,
    0.3,
    0.5,
    0.75,
    1.0,
    2.5,
    5.0,
    7.5,
    float('+inf'),
)


REQUEST_COUNT = prometheus_client.Counter(
    "http_requests_total",
    "Total count of HTTP requests",
    ["method", "endpoint", "http_status"],
)

RESPONSES_2XX_COUNT = prometheus_client.Counter(
    "successful_responses",
    "Total count of successful responses",
    ["method", "endpoint", "http_status"],
)

RESPONSES_4XX_COUNT = prometheus_client.Counter(
    "http_4xx_responses_total",
    "Total count of responses with 4XX status codes",
    ["method", "endpoint", "http_status"],
)

RESPONSES_5XX_COUNT = prometheus_client.Counter(
    "http_5xx_responses_total",
    "Total count of responses with 5XX status codes",
    ["method", "endpoint", "http_status"],
)


async def prometheus_metrics(request: Request, call_next: Callable[..., Awaitable[Any]]) -> Awaitable[Any]:
    method = request.method
    path = request.url.path

    response = await call_next(request)
    if path in ['/favicon.ico', '/metrics']:
        return response
    REQUEST_COUNT.labels(method=method, endpoint=path, http_status=str(response.status_code)).inc()

    if 200 <= response.status_code < 300:
        RESPONSES_2XX_COUNT.labels(method=method, endpoint=path, http_status=str(response.status_code)).inc()
    if 400 <= response.status_code < 500:
        RESPONSES_4XX_COUNT.labels(method=method, endpoint=path, http_status=str(response.status_code)).inc()
    if 500 <= response.status_code < 600:
        RESPONSES_5XX_COUNT.labels(method=method, endpoint=path, http_status=str(response.status_code)).inc()

    return response


def metrics(request: Request) -> Response:
    if 'prometheus_multiproc_dir' in os.environ:
        registry = CollectorRegistry()
        MultiProcessCollector(registry)
    else:
        registry = REGISTRY

    return Response(generate_latest(registry), headers={'Content-Type': CONTENT_TYPE_LATEST})