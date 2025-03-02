from dotenv import load_dotenv
load_dotenv()
llm_config = {
    "model": "gpt-3.5-turbo", 
    "api_key": os.getenv("OPENAI_API_KEY")
}