import secrets

# 32바이트(256비트) 길이의 안전한 랜덤 문자열 생성
cookie_secret = secrets.token_hex(32)
print(f"Generated cookie_secret: {cookie_secret}")

# secrets.toml 파일 내용 업데이트를 위한 안내
print("\n이 값을 .streamlit/secrets.toml 파일의 cookie_secret에 복사하세요.") 