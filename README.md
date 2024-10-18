# Multi-Needle in a Haystack

## Instruction to run

1. Clone the repository
2. Create a new environment and activate it.
For example:
```
conda create -n needle python=3.11
```

3. Install the requirements
```
pip install -r requirements.txt
```
4. Configure the environment
- Create `.env` file in the root directory
- Add the following environment variables:
```
GOOGLE_API_KEY=<your_google_api_key>
```
- You can get a free/paid API key here: https://aistudio.google.com/

5. Run the script
`python main.py`
6. Observe the output in the `output` directory.

## Ideas to improve

- Improve prompt and add robust retry mechanisms.
- This helps us use a less sophisticated LLM model. It can drastically reduce the cost and time to process.
- Use a more sophisticated classification mechanisms to filter chunks.
- Try different chunking mechanisms.