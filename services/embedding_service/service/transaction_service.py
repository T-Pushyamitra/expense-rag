from sqlalchemy.orm import Session

from ..database.models.transaction import Transaction, TransactionCreate
from ..settings import SETTINGS
from ..ollama import EmbeddingService
from ..database.models.transaction_embedding import TransactionEmbedding

import json

class TransactionService:

    def __init__(self, session):
        embedding_service = EmbeddingService(base_url=SETTINGS.ollama_api_embedding_service_url)
        session : Session = session
    
    def create_transaction(self, _transaction: TransactionCreate) -> Transaction:
        transaction_create = TransactionCreate(
            date=_transaction['date'],
            amount=_transaction['amount'],
            balance=_transaction['balance'],
            description=_transaction['description'],
            transaction_type=_transaction['type'],
            statement_file=_transaction['file_name'],
            page_no=_transaction['page_no'],
            transaction_no=_transaction['transaction_no']
        )
        new_transaction = Transaction(**transaction_create.model_dump())
        return new_transaction

    def save(self, transaction: dict): 
        transaction = json.loads(transaction)
        new_transaction = self.create_transaction(transaction)
        self.session.add(new_transaction)
        self.session.flush()
        txn_embedding = self.embedding_service.embed_transaction(self._format_transaction_text(new_transaction))
        transaction_embedding = TransactionEmbedding(
                    transaction_id=new_transaction.id,
                    embedding=txn_embedding)
        self.session.add(transaction_embedding)
        return new_transaction 
        
    def save_transactions(self, transactions: list):
        saved_transactions = []
        
        try:
            with self.session.beign():

                for transaction in transactions:
                    saved_transactions.append(self.save(transaction))  
            return saved_transactions
        except Exception as e:
            self.session.rollback()
            raise

    def _format_transaction_text(self, transaction: Transaction) -> str:

        direction = (
            "debited from"
            if transaction.transaction_type == "DEBIT"
            else "credited to"
        )

        return (
            f"Transaction {transaction.id} occurred on "
            f"{transaction.date}. "
            f"An amount of ₹{transaction.amount:.2f} was "
            f"{direction} the account. "
            f"Transaction details: "
            f"{transaction.description}. "
            f"The account balance after the transaction "
            f"was ₹{transaction.balance:.2f}."
        )

        