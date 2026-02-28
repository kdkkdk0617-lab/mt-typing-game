import streamlit as st
import time

# 문구 목록
sentences = [
    "안 촉촉한 초코칩 나라에 살던 안 촉촉한 초코칩이 촉촉한 초코칩 나라의 촉촉한 초코칩을 보고...",
    "서울특별시 특허허가과 허가과장 허과장",
    "뙤약볕 아래서 똠양꿍 먹으며 뜀박질하는 띔박이",
    "전자기학적 맥스웰 방정식의 시공간적 연속성을 증명하시오."
]

st.set_page_config(page_title="MT 취중 타자왕", page_icon="🍺")
st.title("🍺 MT 취중 타자 대항전")

# 1. 초기화 함수 정의
def reset_game():
    st.session_state.start_time = None
    st.session_state.user_input = ""

# 2. 세션 상태 설정
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# 3. 문장 선택 (바꿀 때마다 초기화)
target = st.selectbox("도전할 문장을 고르세요", sentences, on_change=reset_game)
st.info(f"👉 입력할 문장: **{target}**")

# 4. 입력창 (key를 주어 제어 가능하게 함)
user_input = st.text_input("여기에 입력하고 '엔터'를 누르세요!", key="user_input")

# 5. 시간 기록 시작
if user_input == "" and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# 6. 결과 판정
if user_input:
    if user_input == target:
        end_time = time.time()
        duration = end_time - st.session_state.start_time
        st.success(f"🎉 성공! 기록: {duration:.2f}초")
        st.balloons()
        
        # 다시 하기 버튼 (누르면 페이지 리로드)
        if st.button("새 문장으로 다시 도전"):
            reset_game()
            st.rerun()
    else:
        st.error("❌ 오타가 있어요! 다시 확인해보세요.")
