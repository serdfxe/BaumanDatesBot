import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
EMAIL_PASS = os.getenv('EMAIL_PASS')
EMAIL_ADDRES = os.getenv('EMAIL_ADDRES')
