from openai import OpenAI
from dotenv import load_dotenv
import os

# load .env file
load_dotenv()

# create client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Hello"
)

print(response.output_text)