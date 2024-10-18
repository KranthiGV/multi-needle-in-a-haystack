import os
from dotenv import load_dotenv
import instructor
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from typing import List, Type, TypeVar, Iterable, Callable, Optional
from pydantic import BaseModel
import asyncio
from .utils import split_into_chunks
from tqdm.asyncio import tqdm
import traceback

load_dotenv()
T = TypeVar("T", bound=BaseModel)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
client = instructor.from_gemini(
    client=genai.GenerativeModel(
        model_name="models/gemini-1.5-pro",
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
        try:
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
                        
                        Do not extract anything for the examples provided. Use only the context given below.
                        Please extract the following information from the text:
                        <context>
                            {{ data }}
                        </context>""",
                    }
                ],
                response_model=schemas,
                context={"data": chunk, "examples": example_needles},
                max_retries=3,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                },
            )

            print(f"[DEBUG]: Extracted {len(resp)} needles from chunk.")
            print(f"[DEBUG]: Extracted needles: {resp}")

            return resp
        except Exception as e:
            print(f"An exception occurred during LLM call: {e}")
            print(traceback.format_exc())
            raise e
            return []


async def extract_multi_needle_async(
    schema: Type[T],
    haystack: str,
    example_needles: List[str],
    max_concurrency: int,
    is_valid_chunk: Optional[Callable[[str], bool]] = None,
) -> List[T]:
    """
    Helper function to extract needles asynchronously.
    """
    semaphore = asyncio.Semaphore(max_concurrency)

    # Configure max lines based on actual haystack data distribution
    # We want needle finding to be efficient. So, we chunk the haystack into smaller pieces
    chunks = split_into_chunks(haystack, max_lines=500)

    # Filter chunks based on the provided lambda
    if is_valid_chunk:
        chunks = filter(is_valid_chunk, chunks)

    tasks = [
        handle_extraction_from_chunk(schema, chunk, example_needles, semaphore)
        for chunk in chunks
    ]
    results = await tqdm.gather(*tasks)

    extracted_needles = [item for sublist in results for item in sublist]

    return extracted_needles


def extract_multi_needle(
    schema: Type[T],
    haystack: str,
    example_needles: List[str],
    is_valid_chunk: Optional[Callable[[str], bool]] = None,
) -> List[T]:
    """
    Extracts and structures information from a large text corpus based on a given schema and examples.

    Args:
    schema (Type[T]): A Pydantic model defining the structure of the needle to be extracted.
    haystack (str): The large text corpus to search through (haystack).
    example_needles (List[str]): A list of example sentences (needles).
    is_valid_chunk (Callable[[str], bool]): A function to determine if a chunk is a valid candidate.

    Returns:
    List[T]: A list of extracted needles conforming to the provided schema.
    """
    try:
        return asyncio.run(
            extract_multi_needle_async(
                schema,
                haystack,
                example_needles,
                max_concurrency=25,
                is_valid_chunk=is_valid_chunk,
            )
        )
    except Exception as e:
        print(f"An error occurred during extraction: {e}")
        print(traceback.format_exc())
