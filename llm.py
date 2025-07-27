from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

SYSTEM_PROMPT = """
あなたは「アキ」という名前の、言語交換のパートナーです。あなたの役割は、ユーザーと自然な日本語で会話を続けることです。

### 絶対的なルール (Absolute Rules):
1.  **全ての返答は、日本語のみで行ってください。** ユーザーが英語で尋ねない限り、英語や他の言語を一切使ってはいけません。
2.  あなたの返答は、自然で、友達と話すようなカジュアルなトーン（タメ口）を基本にしてください。ただし、相手が丁寧語を使っている場合は、あなたも丁寧語（です・ます調）を使ってください。
3.  会話を続けるために、積極的に質問を投げかけてください。
4.  ユーザーの日本語が少し不自然な場合、それを修正するのではなく、より自然な言い方を提案する形で返答してください。例えば、「それは良いですね！もっと自然に言うなら、『いいですね！』と言うこともできますよ。」のように、優しく提案してください。
"""

class JapaneseChatBot:
    def __init__(self):
        self.client = genai.Client()
        self.conversation_history = []
        self.model = "gemini-2.5-flash"
        
    def get_response(self, user_input: str) -> str:
        """Get a response from Aki for the given user input"""
        
        # Add user input to conversation history
        self.conversation_history.append(user_input)
        
        # Build the conversation context as a single string
        conversation_context = SYSTEM_PROMPT + "\n\n"
        
        # Add conversation history
        for i, message in enumerate(self.conversation_history):
            if i % 2 == 0:  # User messages (even indices)
                conversation_context += f"ユーザー: {message}\n"
            else:  # AI responses (odd indices)
                conversation_context += f"アキ: {message}\n"
        
        # Add prompt for current response
        if len(self.conversation_history) % 2 == 1:  # If last message was from user
            conversation_context += "アキ: "
        
        try:
            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=conversation_context,
                config=types.GenerateContentConfig(
                    temperature=0.7,  # Make responses a bit more natural/varied
                    max_output_tokens=500  # Limit response length
                )
            )
            
            ai_response = response.text.strip()
            
            # Add AI response to conversation history
            self.conversation_history.append(ai_response)
            
            return ai_response
            
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
        print("会話履歴がリセットされました。")
