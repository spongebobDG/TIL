import sys
import datetime
import os

LOG_FILE = "dev_history.md"

def save_log(message):
    # 현재 날짜와 시간 포맷팅
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 파일이 존재하지 않으면 제목(Header) 추가
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("# 🧠 My Dev-Brain History\n\n")
            f.write("> 매일의 트러블슈팅과 배움을 기록하는 공간입니다.\n\n")

    # 로그 내용 이어쓰기 (Append Mode)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"### 🗓️ {now}\n")
        f.write(f"- **Issue/Learned:** {message}\n\n")
        
    print(f"✅ 기록 완료! ({LOG_FILE}에 저장되었습니다.)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("💡 사용법: python log.py '기록할 내용을 따옴표 안에 적어주세요'")
    else:
        # 띄어쓰기가 포함된 여러 인자를 하나의 문자열로 합침
        user_message = " ".join(sys.argv[1:])
        save_log(user_message)