import psycopg2
import json
from datetime import datetime

class TransactionDB:

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="transactions",
            user="postgres",
            password="password"
        )

        self.cursor = self.conn.cursor()


    def insert_transaction(
        self,
        transaction_id,
        content,
        data,
        embedding
    ):

        self.cursor.execute(
            """
            INSERT INTO transactions
            (
                transaction_id,
                content,
                transaction_data,
                embedding,
                created_at
            )
            VALUES
            (%s, %s, %s, %s, %s)
            """,
            (
                transaction_id,
                content,
                json.dumps(data),
                embedding,
                datetime.now()
            )
        )

        self.conn.commit()


    def search_similar(self, embedding, limit=5):

        self.cursor.execute(
            """
            SELECT
                transaction_id,
                content,
                transaction_data
            FROM transactions

            ORDER BY embedding <=> %s::vector

            LIMIT %s
            """,
            (
                embedding,
                limit
            )
        )

        return self.cursor.fetchall()


    def close(self):

        self.cursor.close()
        self.conn.close()