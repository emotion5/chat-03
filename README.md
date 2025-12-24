# Qwen 2.5 한국어 챗봇

Ollama + Qwen 2.5 7B 모델을 사용한 로컬 실행 한국어 AI 챗봇

## 주요 특징

- **강력한 한국어 성능**: Qwen 2.5 7B 모델 사용
- **로컬 실행**: 인터넷 없이 완전히 로컬에서 동작
- **코딩 특화**: Python, JavaScript 등 코드 생성 능력 우수
- **웹 UI**: Gradio 기반 깔끔한 채팅 인터페이스
- **CLI 지원**: 터미널에서도 사용 가능

## 기술 스택

- **모델**: Qwen 2.5 7B (Alibaba Cloud)
- **프레임워크**: Ollama
- **UI**: Gradio
- **언어**: Python 3.9+

## 시스템 요구사항

- **OS**: macOS, Linux, Windows
- **메모리**: 8GB RAM 이상 권장
- **저장공간**: 약 5GB (모델 포함)
- **Python**: 3.9 이상

## 설치 방법

### 1. Ollama 설치

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# https://ollama.com/download 에서 다운로드
```

### 2. Ollama 서비스 시작

```bash
# macOS (Homebrew)
brew services start ollama

# Linux/Windows
ollama serve
```

### 3. Qwen 2.5 모델 다운로드

```bash
ollama pull qwen2.5:7b
```

모델 다운로드는 약 5분 소요됩니다 (인터넷 속도에 따라 다름).

### 4. Python 의존성 설치

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 의존성 설치
pip install -r requirements.txt
```

## 사용 방법

### 웹 UI 실행 (추천)

```bash
python app_gradio.py
```

브라우저에서 http://localhost:7860 접속

### CLI 실행

```bash
python chatbot.py
```

터미널에서 직접 대화 가능

## 프로젝트 구조

```
chat-03/
├── venv/                   # 가상환경
├── chatbot.py             # 챗봇 코어 모듈
├── app_gradio.py          # Gradio 웹 UI
├── requirements.txt       # Python 의존성
├── README.md             # 문서
└── .gitignore            # Git 제외 파일
```

## 성능 비교

### GPT4All (Llama 3.2 1B) vs Ollama (Qwen 2.5 7B)

| 항목 | GPT4All | Qwen 2.5 |
|------|---------|----------|
| 모델 크기 | 1B (0.7GB) | 7B (4.7GB) |
| 한국어 성능 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 코딩 능력 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 추론 능력 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 응답 속도 | 빠름 | 중간 |
| 메모리 사용량 | 4GB | 8GB |

## 예제 프롬프트

- "안녕하세요! 자기소개 해주세요."
- "Python으로 피보나치 수열 코드 작성해줘"
- "한국의 수도는 어디인가요?"
- "간단한 레시피 하나 추천해줘"
- "AI와 머신러닝의 차이점은 뭐야?"

## 모델 변경

다른 모델을 사용하고 싶다면:

```bash
# 사용 가능한 모델 확인
ollama list

# 다른 모델 다운로드
ollama pull llama3.1:8b

# 코드에서 모델명 변경
bot = KoreanChatbot(model_name="llama3.1:8b")
```

## 문제 해결

### Ollama 연결 오류

```bash
# Ollama 서비스 상태 확인
brew services list | grep ollama  # macOS

# 서비스 재시작
brew services restart ollama
```

### 모델이 응답하지 않음

```bash
# 모델 다운로드 확인
ollama list

# 모델 재다운로드
ollama pull qwen2.5:7b
```

## 라이선스

MIT License

## 기여

이슈 및 PR 환영합니다!

## 참고

- [Ollama 공식 문서](https://ollama.com)
- [Qwen 2.5 모델](https://huggingface.co/Qwen)
- [Gradio 문서](https://gradio.app)
