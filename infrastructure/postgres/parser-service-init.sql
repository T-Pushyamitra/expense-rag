CREATE EXTENSION IF NOT EXISTS vector;


CREATE TABLE IF NOT EXISTS transactions (

    id BIGSERIAL PRIMARY KEY,

    transaction_id VARCHAR(100),

    content TEXT,

    transaction_data JSONB,

    embedding vector(768),

    created_at TIMESTAMP DEFAULT NOW()

);