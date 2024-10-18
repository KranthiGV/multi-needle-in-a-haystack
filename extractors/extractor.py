import os
from dotenv import load_dotenv
import instructor
import google.generativeai as genai
from models import User
from typing import List, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

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


def extract_multi_needle(
    schema: Type[T], haystack: str, example_needles: List[str]
) -> List[T]:
    """
    Extracts and structures information from a large text corpus based on a given schema and examples.

    Args:
    schema (Type[T]): A Pydantic model defining the structure of the needle to be extracted.
    haystack (str): The large text corpus to search through (haystack).
    example_needles (List[str]): A list of example sentences (needles).

    Returns:
    List[T]: A list of extracted needles conforming to the provided schema.
    """
    # Implementation goes here
    extracted_needles = []
    return extracted_needles
