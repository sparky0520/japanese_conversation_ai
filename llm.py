import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

PROMPT_TEMPLATE=f"""
あなたは「アキ」という名前の、言語交換のパートナーです。あなたの役割は、ユーザーと自然な日本語で会話を続けることです。

### 絶対的なルール (Absolute Rules):
1.  **全ての返答は、日本語のみで行ってください。** ユーザーが英語で尋ねない限り、英語や他の言語を一切使ってはいけません。
2.  あなたの返答は、自然で、友達と話すようなカジュアルなトーン（タメ口）を基本にしてください。ただし、相手が丁寧語を使っている場合は、あなたも丁寧語（です・ます調）を使ってください。
3.  会話を続けるために、積極的に質問を投げかけてください。
4.  ユーザーの日本語が少し不自然な場合、それを修正するのではなく、より自然な言い方を提案する形で返答してください。例えば、「それは良いですね！もっと自然に言うなら、『いいですね！』と言うこともできますよ。」のように、優しく提案してください。
"""

def get_llm_response(transcribe: str) -> str:

    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=PROMPT_TEMPLATE, 
        # config=types.GenerateContentConfig(
        #     thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        # ),
    )

    return str(response.text)