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

            if transcription:
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
                tts_stream(response)  # Blocks until complete
                print(f"Result: {response}")
            else:
                print("No speech detected")
        except KeyboardInterrupt:
            print("\n\nアキ: さようなら！また話しましょうね！")
            break
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    runtime_metrics(main)
            
        