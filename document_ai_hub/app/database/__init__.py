from app.database.session import engine
from app.database.model import UserChunk

UserChunk.metadata.create_all(bind=engine)