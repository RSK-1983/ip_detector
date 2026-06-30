import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('YD_TOKEN')
print(token)