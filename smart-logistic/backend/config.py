import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./logistics.db")
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
