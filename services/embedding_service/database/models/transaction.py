from sqlmodel import SQLModel, Field
from pgvector.sqlalchemy import Vector

class Transaction(SQLModel, table=True):
    id: int = Field(primary_key=True)
    date: str = Field(default=None)
    amount: float = Field(default=None)
    balance: float = Field(default=None)
    description: str = Field(default=None)
    transaction_type: str = Field(default=None)
    statement_file: str = Field(default=None)
    page_no: int = Field(default=None)
    transaction_no: int = Field(default=None)
    
class TransactionCreate(SQLModel):
    date: str 
    amount: float 
    balance: float 
    description: str 
    transaction_type: str 
    statement_file: str 
    page_no: int 
    transaction_no: int 
    
class TransactionRead(SQLModel):
    id: int
    date: str 
    amount: float 
    balance: float 
    description: str 
    transaction_type: str 
    statement_file: str 
    page_no: int 
    transaction_no: int 