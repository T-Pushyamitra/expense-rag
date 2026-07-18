from sqlmodel import Session, create_engine

from services.embedding_service.settings import SETTINGS

vector_engine = ""

# create_engine(
#     SETTINGS.vector_database_url,
#     echo=False,
# )


def get_vector_session():
    pass
    # with Session(vector_engine) as session:
    #     yield session
