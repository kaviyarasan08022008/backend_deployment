import os
from dotenv import load_dotenv
from sqlalchemy  import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:AcademyRootPassword@localhost:5432/village_voice_api")

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False 
)


Base = declarative_base()
