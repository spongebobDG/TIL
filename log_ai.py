import sys
import datetime
import os
import requests

# TIL 폴더 안에 날짜별로 저장되도록 설정
BASE_DIR = "TIL"
OLLAMA_URL = "http://localhost:11434/api/generate"

def get_today_file_path():
    """오늘 날짜의 파일 경로를 반환하고, 폴더가 없으면 생성합니다."""
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return os.path.join(BASE_DIR, f"{today_date}.md")

def get_ai_analysis(raw_message):
    """Notion 포트폴리오용 문서 초안을 작성하도록 프롬프트를 고도화했습니다."""
    prompt = f"""
    당신은 테크 리드(Tech Lead)급 개발자입니다. 
    사용자가 작성한 짧은 트러블슈팅 로그를 바탕으로, Notion이나 기술 블로그에 즉시 복사-붙여넣기 할 수 있는 '구조화된 기술 문서 초안'을 작성하세요.

    [지시사항]
    1. 답변은 반드시 자연스러운 한국어로 작성하세요.
    2. 마크다운(Markdown) 포맷을 사용하여 시각적으로 깔끔하게 구성하세요.
    3. 기술적 원리를 분석할 때는 C++, 로봇 SW, 메모리 구조, 인공지능 모델 구조 등의 깊이 있는 관점을 포함하세요.

    [작성 형식]
    ### 🎯 Issue: (문제의 한 줄 요약)
    * **상황 및 증상:** (사용자 입력 내용을 바탕으로 상황을 구체화)
    * **근본 원인 (Root Cause):** (기술적인 원인 심층 분석)
    * **해결 방안 및 배운 점:** (이 문제를 통해 얻은 인사이트)
    * **Keywords:** #태그1 #태그2 #태그3

    [사용자 로그]
    "{raw_message}"
    """
    
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "gemma2:2b", # 현재 사용하는 모델명 확인
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        
        response.encoding = 'utf-8'
        result = response.json().get('response', '').strip()
        return result
    except Exception as e:
        return f"AI 분석 중 오류 발생: {e}"

def save_log(message):
    now_time = datetime.datetime.now().strftime("%H:%M:%S")
    file_path = get_today_file_path()
    
    print("🤖 노션에 붙여넣을 기술 문서를 작성 중입니다... (gemma2:2b)")
    
    ai_analysis = get_ai_analysis(message)
    
    # 파일이 처음 생성되는 경우 헤더 추가
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            date_title = datetime.datetime.now().strftime("%Y년 %m월 %d일")
            f.write(f"# 📅 {date_title} - TIL (Today I Learned)\n\n")

    # 내용 이어쓰기
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"## ⏱️ {now_time}\n")
        f.write(f"**[내 기록]**: {message}\n\n")
        f.write(f"{ai_analysis}\n\n")
        f.write("---\n\n")
        
    print(f"✅ 문서 생성 완료! ({file_path}를 확인하세요.)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("💡 사용법: python log_ai.py \"기록할 내용\"")
    else:
        user_message = " ".join(sys.argv[1:])
        save_log(user_message)