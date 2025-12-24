import gradio as gr
from chatbot import KoreanChatbot


# 챗봇 인스턴스 생성
print("챗봇 로딩 중...")
bot = KoreanChatbot()
print("챗봇 로딩 완료!\n")


def chat_interface(message, history):
    """
    Gradio ChatInterface용 채팅 함수

    Args:
        message: 사용자 메시지 (문자열 또는 멀티모달 리스트)
        history: Gradio 대화 이력

    Returns:
        str: AI 응답
    """
    # 메시지를 문자열로 변환 (멀티모달 형식 처리)
    if isinstance(message, list):
        # [{'text': '내용', 'type': 'text'}] 형식에서 텍스트 추출
        text_parts = []
        for part in message:
            if isinstance(part, dict) and part.get('type') == 'text':
                text_parts.append(part.get('text', ''))
        message = ' '.join(text_parts)

    # Gradio history를 Ollama 메시지 포맷으로 변환
    ollama_history = []
    for chat in history:
        # history가 딕셔너리 형태인 경우
        if isinstance(chat, dict):
            if "role" in chat and "content" in chat:
                content = chat["content"]
                # content가 멀티모달 형식일 수 있음
                if isinstance(content, list):
                    text_parts = []
                    for part in content:
                        if isinstance(part, dict) and part.get('type') == 'text':
                            text_parts.append(part.get('text', ''))
                    content = ' '.join(text_parts)
                ollama_history.append({"role": chat["role"], "content": content})
        # history가 리스트/튜플 형태인 경우 [user_msg, bot_msg]
        elif isinstance(chat, (list, tuple)) and len(chat) == 2:
            user_msg, bot_msg = chat

            # user_msg도 멀티모달 형식일 수 있음
            if isinstance(user_msg, list):
                text_parts = []
                for part in user_msg:
                    if isinstance(part, dict) and part.get('type') == 'text':
                        text_parts.append(part.get('text', ''))
                user_msg = ' '.join(text_parts)

            # bot_msg도 멀티모달 형식일 수 있음
            if isinstance(bot_msg, list):
                text_parts = []
                for part in bot_msg:
                    if isinstance(part, dict) and part.get('type') == 'text':
                        text_parts.append(part.get('text', ''))
                bot_msg = ' '.join(text_parts)

            if user_msg:  # user_msg가 비어있지 않은 경우만 추가
                ollama_history.append({"role": "user", "content": str(user_msg)})
            if bot_msg:  # bot_msg가 None이 아닌 경우만 추가
                ollama_history.append({"role": "assistant", "content": str(bot_msg)})

    # 챗봇 응답 생성
    response = bot.chat(message, ollama_history)
    return response


# Gradio 인터페이스 생성
demo = gr.ChatInterface(
    fn=chat_interface,
    title="Qwen 2.5 한국어 챗봇",
    description="Ollama + Qwen 2.5 7B로 구동되는 로컬 AI 챗봇입니다.",
    examples=[
        "안녕하세요! 자기소개 해주세요.",
        "Python으로 피보나치 수열 코드 작성해줘",
        "한국의 수도는 어디인가요?",
        "간단한 레시피 하나 추천해줘",
        "AI와 머신러닝의 차이점은 뭐야?",
    ],
)


if __name__ == "__main__":
    print("="*50)
    print("Gradio 웹 서버 시작 중...")
    print("="*50)
    print("브라우저에서 http://localhost:7860 접속")
    print("="*50 + "\n")

    demo.launch(
        server_name="0.0.0.0",  # 외부 접속 허용
        server_port=7860,
        share=False,  # True로 설정 시 공개 링크 생성
        show_error=True
    )
