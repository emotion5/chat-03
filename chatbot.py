import ollama


class KoreanChatbot:
    def __init__(self, model_name="qwen2.5:7b"):
        """
        한국어 챗봇 초기화

        Args:
            model_name: Ollama 모델명 (기본값: qwen2.5:7b)
        """
        self.model_name = model_name
        self.system_prompt = """당신은 친절하고 유능한 한국어 AI 어시스턴트입니다.
사용자의 질문에 정확하고 도움이 되는 답변을 제공합니다.
코딩, 일반 상식, 추론, 번역 등 다양한 분야에서 도움을 줄 수 있습니다.

**중요**: 답변은 반드시 순수한 한글로만 작성해주세요. 한자를 절대 사용하지 마세요.
예시: "開發" (X) → "개발" (O), "實行" (X) → "실행" (O)
답변은 간결하면서도 명확하게 작성해주세요."""

        print(f"챗봇 초기화 완료!")
        print(f"모델: {self.model_name}")

    def chat(self, user_input, history=None):
        """
        사용자 입력에 대한 응답 생성

        Args:
            user_input: 사용자 메시지
            history: 대화 이력 (list of dicts)

        Returns:
            str: AI 응답
        """
        if history is None:
            history = []

        messages = [
            {"role": "system", "content": self.system_prompt},
            *history,
            {"role": "user", "content": user_input}
        ]

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            return f"오류가 발생했습니다: {str(e)}"

    def run(self):
        """터미널에서 대화형 챗봇 실행"""
        print("\n" + "="*50)
        print("한국어 챗봇 시작!")
        print(f"모델: {self.model_name}")
        print("종료하려면 'quit', 'exit', '종료'를 입력하세요")
        print("="*50 + "\n")

        conversation_history = []

        while True:
            try:
                user_input = input("사용자: ")

                if user_input.lower() in ['quit', 'exit', '종료']:
                    print("\n챗봇을 종료합니다. 안녕히 가세요!")
                    break

                if not user_input.strip():
                    continue

                print("AI: ", end="", flush=True)
                response = self.chat(user_input, conversation_history)
                print(response)
                print()

                # 대화 이력 저장
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": response})

            except KeyboardInterrupt:
                print("\n\n챗봇을 종료합니다. 안녕히 가세요!")
                break
            except Exception as e:
                print(f"\n오류 발생: {e}\n")


if __name__ == "__main__":
    bot = KoreanChatbot()
    bot.run()
