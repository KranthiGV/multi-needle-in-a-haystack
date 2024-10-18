import os
from dotenv import load_dotenv
import instructor
import google.generativeai as genai
from models import User

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

client = instructor.from_gemini(
    client=genai.GenerativeModel(
        model_name="models/gemini-1.5-flash-latest",
    ),
    mode=instructor.Mode.GEMINI_JSON,
)

resp = client.messages.create(
    messages=[
        {
            "role": "user",
            "content": "Extract Jason is 25 years old.",
        }
    ],
    response_model=User,
)

print (isinstance(resp, User))
print (resp.name)
print (resp.age)