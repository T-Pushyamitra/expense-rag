from sqlmodel import SQLModel, Session, create_engine

from services.embedding_service.settings import SETTINGS
from services.embedding_service.database.models.transaction import Transaction
from services.embedding_service.database.models.transaction_embedding import TransactionEmbedding

# host=SETTINGS.metadata_host
# port=SETTINGS.metadata_port
# database=SETTINGS.metadata_database
# user=SETTINGS.metadata_user
# password=SETTINGS.metadata_password
    
metadata_engine = create_engine(
    url = (
    f"postgresql+psycopg2://{SETTINGS.metadata_user}:{SETTINGS.metadata_password}@{SETTINGS.metadata_host}:{SETTINGS.metadata_port}/{SETTINGS.metadata_database}"),
    echo=False,
)

def init_db():
    SQLModel.metadata.create_all(metadata_engine)
    
def get_metadata_session():
    with Session(metadata_engine) as session:
        yield session