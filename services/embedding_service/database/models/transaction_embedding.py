from pgvector.sqlalchemy import Vector
from sqlmodel import Field, SQLModel


class TransactionEmbedding(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    transaction_id: int = Field(
        foreign_key="transaction.id",
        index=True,
    )

    embedding: list[float] = Field(sa_type=Vector(768))
