import os
from dotenv import load_dotenv

from utils.deb import p


load_dotenv(override=True)

TOKEN = os.getenv('TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
EMAIL_PASS = os.getenv('EMAIL_PASS')
EMAIL_ADDRES = os.getenv('EMAIL_ADDRES')

p(DATABASE_URL)
