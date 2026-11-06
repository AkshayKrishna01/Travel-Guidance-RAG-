from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()
@dataclass
class Config:
    db_port: str
    db_host: str
    db_name: str
    db_username: str
    db_password: str
    port: int
    host: str
    log_level: str

def get_config():
    return Config(
        db_port=os.getenv('DB_Port', '5432'),
        db_host=os.getenv('DB_Host', 'localhost'),
        db_name=os.getenv('Data_Base', 'student_db'),
        db_username=os.getenv('DB_User', 'postgres'),
        db_password=os.getenv('DB_PASSWORD', 'Admin'),
        port=int(os.getenv('PORT', '8080')),
        host=os.getenv('HOST', '0.0.0.0'),
        log_level=os.getenv('LOG_LEVEL', 'INFO')
    )

config = get_config()
