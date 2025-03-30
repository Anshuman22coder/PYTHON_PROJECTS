import os
from dotenv import load_dotenv
load_dotenv("./a.env")
email_password = os.environ.get("EMAIL_PASSWORD")
print(email_password)  # Debug print
