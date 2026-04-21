import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_DRIVER = os.getenv("DB_DRIVER")

connection_string = (
    f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_DATABASE}"
    f"?driver={DB_DRIVER.replace(' ', '+')}"
    "&Encrypt=yes"
    "&TrustServerCertificate=yes"
)

engine = create_engine(connection_string)
SessionLocal = sessionmaker(bind=engine)