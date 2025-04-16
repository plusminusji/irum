import streamlit as st
from streamlit_option_menu import option_menu
from app.components.profile_management import show_profile_management
from app.components.job_management import show_job_management
from streamlit_google_auth import GoogleAuth
import os

# 이미지 URL 설정
LOGO_URL = "https://i.imgur.com/thQZtYk.png"

# Google OAuth 설정
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# 페이지 기본 설정
st.set_page_config(
    page_title="이룸 - 미래로의 문을 여는 곳",
    page_icon="🚀",
    layout="wide"
)

def main():
    # CSS 스타일 적용
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
        }
        /* 로그인 전 화면 스타일 */
        .block-container {
            padding: 2rem !important;
            max-width: 100% !important;
        }
        .main-container {
            max-width: 600px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        .text-container {
            text-align: left;
            color: white;
        }
        [data-testid="stImage"] {
            width: 600px !important;
            margin: 0 auto !important;
            padding: 10rem 2rem 0 2rem !important;
        }
        [data-testid="stImage"] > img {
            margin: 0 !important;
        }
        /* 사이드바 스타일 */
        section[data-testid="stSidebar"] {
            background-color: #4285f4;
        }
        section[data-testid="stSidebar"] > div {
            background-color: #4285f4;
        }
        /* 로그인 후 메인 영역 스타일 */
        .stApp.authenticated {
            background-color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Google 인증 초기화
    auth = GoogleAuth(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        redirect_uri="http://localhost:8501/oauth2callback",
        scopes=["email", "profile"]
    )

    # 인증 상태 확인
    if not st.session_state.get("authenticated", False):
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #4285f4;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # 로고
        st.image(LOGO_URL, width=300)
        
        # 텍스트
        st.markdown(
            """
            <div class="main-container">
                <div class="text-container">
                    <h1 style="font-size: 2rem; margin-bottom: 1.5rem; font-weight: 500; line-height: 1.35; color: white;">미래로의 문을 여는 곳, 이룸</h1>
                    <div style="font-size: 1.1rem; margin-bottom: 3rem; line-height: 1.6; color: white;">
                        이룸은 이력 관리와 지원 공고 분석을 통해 취업과 이직을 위한 맞춤형 서류 제작은 물론 경력 관리까지 지원하는 서비스입니다.
                        <br><br>
                        여러분의 경험을 이해하고, 커리어 시장에서 원하는 미래로 나아가는 길을 함께 엽니다.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 구글 로그인 버튼
        if st.button("구글 계정으로 로그인"):
            auth_url = auth.get_authorization_url()
            st.markdown(f'<a href="{auth_url}" target="_self">구글 로그인</a>', unsafe_allow_html=True)
        
        # 인증 코드 처리
        code = st.experimental_get_query_params().get("code")
        if code:
            token = auth.get_token(code[0])
            user_info = auth.get_user_info(token)
            
            if user_info:
                st.session_state.authenticated = True
                st.session_state.email = user_info.get("email")
                st.session_state.name = user_info.get("name")
                st.experimental_rerun()
        
        return

    # 로그인 후 메인 화면
    with st.sidebar:
        st.image(LOGO_URL, width=150)
        selected = option_menu(
            menu_title=None,
            options=["대시보드", "이력 관리", "공고 관리", "서류 관리"],
            icons=["house", "person-vcard", "briefcase", "file-earmark-text"],
            menu_icon="house",
            default_index=0,
            styles={
                "container": {"background-color": "#4285f4"},
                "icon": {"color": "white"},
                "nav-link": {"color": "white"},
                "nav-link-selected": {"background-color": "#3367d6"},
            }
        )

    # 메인 컨텐츠
    if selected == "대시보드":
        st.title("대시보드")
        st.write(f"환영합니다, {st.session_state.name}님!")
        st.write("대시보드 기능은 준비 중입니다.")
    elif selected == "이력 관리":
        show_profile_management()
    elif selected == "공고 관리":
        show_job_management()
    elif selected == "서류 관리":
        st.title("서류 관리")
        st.write("서류 관리 기능은 준비 중입니다.")

if __name__ == "__main__":
    main()
