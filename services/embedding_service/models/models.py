#### API REQUEST/RESPONSE
from pydantic import BaseModel
from common_lib.enum.route_enum import RouteEnum


class ErrorModel(BaseModel):
    message: str


class EmbeddingResponse(BaseModel):
    status: int
    error: ErrorModel | None = None


class BatchEmbedRequest(BaseModel):
    transactions: list


class Filters(BaseModel):
    amount_gt: int
    amount_lt: int
    categories: list[str]
    months: list[str]
    semantic_query: list[str]


class QueryRequest(BaseModel):
    free_text: str
    filters: Filters | None = None
    model_name: str | None = None
    route: RouteEnum


class QueryResponse(BaseModel):
    result: str | list
    error: ErrorModel | None = None