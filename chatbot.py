import ollama
import re
from typing import Optional


class KoreanChatbot:
    def __init__(self, model_name: str = "qwen2.5:7b") -> None:
        """
        한국어 챗봇 초기화

        Args:
            model_name: Ollama 모델명 (기본값: qwen2.5:7b)
        """
        self.model_name = model_name
        self.system_prompt = """你是韩语专家助手。

【严格规则 - 必须遵守】
1. 回答必须100%使用韩语（한글），一个中文字都不能出现
2. 严禁使用中文标点符号：、。，等
3. 只能使用韩语标点：, . ! ? 등
4. 检查每个字：如果不是한글、英文、数字、标点，就不要写

【示例】
错误 ✗: "的"、"了"、"等"、"可以"、"历史"、"尤其"
正确 ✓: "의"、했습니다"、"등"、"할 수 있습니다"、"역사"、"특히"

回答前请自查：有中文字吗？如果有，改成韩语再回答。

You MUST respond in 100% Korean language. Check every character before responding."""

        print(f"챗봇 초기화 완료!")
        print(f"모델: {self.model_name}")

    def has_chinese(self, text: str) -> bool:
        """텍스트에 중국어 문자가 포함되어 있는지 확인"""
        # 중국어 유니코드 범위 체크
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
        return bool(chinese_pattern.search(text))

    def chat(self, user_input: str, history: Optional[list[dict[str, str]]] = None) -> str:
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
            # 최대 3번 재시도
            max_retries = 3
            for attempt in range(max_retries):
                response = ollama.chat(
                    model=self.model_name,
                    messages=messages
                )
                answer = response['message']['content']

                # 중국어 체크
                if not self.has_chinese(answer):
                    return answer

                # 중국어가 발견되면 재요청
                if attempt < max_retries - 1:
                    messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                    messages.append({
                        "role": "user",
                        "content": "你的回答中包含了中文字符。请用纯韩语重新回答，不要使用任何中文字。/ Your answer contains Chinese characters. Please answer again in pure Korean only."
                    })

            # 3번 시도 후에도 중국어가 있으면 그대로 반환
            return answer

        except Exception as e:
            return f"오류가 발생했습니다: {str(e)}"

    def run(self) -> None:
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
