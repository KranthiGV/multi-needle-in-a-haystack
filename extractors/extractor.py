import os
from dotenv import load_dotenv
import instructor
import google.generativeai as genai
from typing import List, Type, TypeVar, Iterable
from pydantic import BaseModel
import asyncio
from .utils import split_into_chunks
from tqdm.asyncio import tqdm

load_dotenv()
T = TypeVar("T", bound=BaseModel)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
client = instructor.from_gemini(
    client=genai.GenerativeModel(
        model_name="models/gemini-1.5-flash-latest",
    ),
    mode=instructor.Mode.GEMINI_JSON,
)


async def handle_extraction_from_chunk(
    schema: Type[T],
    chunk: str,
    example_needles: List[str],
    semaphore: asyncio.Semaphore,
) -> List[T]:
    """
    Handles the extraction of needles from a chunk of text.
    """
    async with semaphore:
        schemas = Iterable[schema]

        resp = client.messages.create(
            messages=[
                {
                    "role": "user",
                    "content": """You are an information extraction expert. 
                    Here are some examples of the information you would be extracting:
                    <examples>
                    {% for example in examples %}
                        <example>
                            {{ example }}
                        </example>
                    {% endfor %}
                    </examples>
                    
                    Now, please extract the following information from the text:
                    <context>
                        {{ data }}
                    </context>""",
                }
            ],
            response_model=schemas,
            context={"data": chunk, "examples": example_needles},
        )
        return resp


async def extract_multi_needle_async(
    schema: Type[T], haystack: str, example_needles: List[str], max_concurrency: int
) -> List[T]:
    """
    Helper function to extract needles asynchronously.
    """
    semaphore = asyncio.Semaphore(max_concurrency)

    # Configure max lines based on actual haystack data distribution
    # We want needle finding to be efficient. So, we chunk the haystack into smaller pieces
    chunks = split_into_chunks(haystack, max_lines=10_000)

    tasks = [
        handle_extraction_from_chunk(schema, chunk, example_needles, semaphore)
        for chunk in chunks
    ]
    results = await tqdm.gather(*tasks)
    extracted_needles = [item for sublist in results for item in sublist]

    return extracted_needles


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
    try:
        return asyncio.run(
            extract_multi_needle_async(
                schema, haystack, example_needles, max_concurrency=5
            )
        )
    except Exception as e:
        print(f"An error occurred during extraction: {e}")
