from core.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

synchronus_session = sessionmaker(create_engine(config.WRITER_DB_URL, pool_recycle=3600), expire_on_commit=True)()
