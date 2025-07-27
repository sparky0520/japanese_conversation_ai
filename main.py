from asr import VoiceActivatedASR
from llm import JapaneseChatBot
from metrics import runtime_metrics
from tts import tts_stream

def main():

    """Main chat loop"""
    print("🌸 日本語チャットボット「アキ」と話そう！ 🌸")
    print("('quit', 'exit', 'bye' で終了 | 'reset' で会話履歴をリセット)")
    print("-" * 50)
    asr = VoiceActivatedASR()
    chat_bot = JapaneseChatBot()
    
    while True:
        try:
            # Get transcription (blocks until speech is complete)
            transcription = asr.listen_for_speech()

            if transcription.strip():
                print(f"You said: {transcription}")

                # Check for exit commands
                if transcription.lower() in ['quit', 'exit', 'bye', 'さようなら', 'バイバイ']:
                    print("アキ: さようなら！また話しましょうね！")
                    break
                
                # Check for reset command
                if transcription.lower() in ['reset', 'リセット']:
                    chat_bot.reset_conversation()
                    print("アキ: 新しい会話を始めましょう！何について話したいですか？")
                    continue
                
                # Get and display AI response
                print("Fetching llm response...")
                response = chat_bot.get_response(transcription)
                print(f"アキ: {response}")
                # Before calling TTS
                if response and response.strip():
                    tts_stream(response)
                else:
                    print("Skipping TTS - empty response")
            else:
                print("No speech detected")
        except KeyboardInterrupt:
            tts_stream("さようなら！また話しましょうね！")
            print("\n\nアキ: さようなら！また話しましょうね！")
            break
        except Exception as e:
            tts_stream("わー、エラーが発生しました")
            print(f"エラーが発生しました (main.py): {str(e)}")
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    runtime_metrics(main)
            
        