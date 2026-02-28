import streamlit as st
import time

# 📝 적당한 난이도의 문제 세팅 (한글 위주 + 숫자/영문 약간)
quiz_data = {
    "1단계 (몸풀기)": "안 촉촉한 초코칩 나라의 안 촉촉한 초코칩 1234개",
    "2단계 (숫자 섞기)": "동탄역에서 출발하는 SRT 열차는 2026년에 시속 300km로 달린다!",
    "3단계 (전공 한스푼)": "포스텍 전자과 필수 과목: 회로이론 1, 전자기학 2 (A+ 가즈아~)",
    "4단계 (영문 콤보)": "Python 코딩으로 완성하는 완벽한 MT Game 100점 만점",
    "5단계 (최종 보스)": "맥스웰(Maxwell) 방정식 4가지를 10초 안에 정확히 타이핑하시오."
}

st.set_page_config(page_title="MT 취중 타자왕", page_icon="🍺")

# 🔄 게임 상태를 완전히 초기화하는 함수
def init_game():
    st.session_state.start_time = None
    st.session_state.game_started = False
    st.session_state.current_stage = None

# 처음 접속 시 상태 초기화
if 'game_started' not in st.session_state:
    init_game()

# ==========================================
# 🏠 메인 화면 (시작 창)
# ==========================================
if not st.session_state.game_started:
    st.title("🍺 MT 취중 타자 대항전")
    st.subheader("도전할 스테이지를 선택하세요!")
    
    st.write("---")
    # 버튼을 2열로 예쁘게 배치
    cols = st.columns(2)
    for i, stage_name in enumerate(quiz_data.keys()):
        if cols[i % 2].button(f"🔥 {stage_name}", use_container_width=True):
            # 문제 선택 시 해당 게임 화면으로 이동
            st.session_state.current_stage = stage_name
            st.session_state.game_started = True
            st.rerun()

# ==========================================
# 🎮 게임 화면 (타이핑 창)
# ==========================================
else:
    target_text = quiz_data[st.session_state.current_stage]
    st.title(f"🎯 {st.session_state.current_stage}")
    
    # 제시문 강조
    st.info(f"**제시문:** {target_text}")
    st.caption("⚠️ 주의: 복사/붙여넣기 적발 시 무효 처리됩니다! (직접 치세요)")

    # 입력창
    user_input = st.text_input("위 문장을 띄어쓰기, 영문 대소문자까지 똑같이 입력하고 '엔터'를 누르세요!")

    # 첫 글자 입력 시 시간 측정 시작
    if user_input and st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    # 결과 판정
    if user_input:
        if user_input == target_text:
            # 🕒 [복붙 방지 로직] 소요 시간 계산
            end_time = time.time()
            total_time = end_time - st.session_state.start_time
            
            # 너무 빨리 끝나는 버그(0초) 방지
            if total_time < 0.1:
                total_time = 0.1
                
            # 분당 타수(CPM) 계산
            typing_speed = len(user_input) / (total_time / 60) 

            # 복붙 감지 (분당 1200타 이상이면 사람의 속도가 아니라고 간주)
            if typing_speed > 1200:
                st.error(f"🚨 삐빅- 복사 붙여넣기가 감지되었습니다! (속도: {int(typing_speed)}타/분) 양심껏 직접 치세요!")
                if st.button("양심 챙기고 다시 하기"):
                    st.session_state.start_time = None
                    st.rerun()
            else:
                # 정상적인 타이핑으로 성공했을 때
                st.success(f"🎊 성공! 기록: {total_time:.2f}초 (약 {int(typing_speed)}타/분)")
                st.balloons()
                
                if st.button("🏠 메인 화면으로 돌아가기"):
                    init_game()
                    st.rerun()
        else:
            # 입력 중일 때는 놔두고, 글자 수가 정답만큼 길어졌을 때만 오타 알림
            if len(user_input) >= len(target_text):
                st.error("❌ 오타가 있습니다! 대소문자나 띄어쓰기를 다시 확인해 보세요.")

    st.write("---")
    # 게임 중 언제든지 뒤로 갈 수 있는 버튼
    if st.button("🔙 포기하고 다른 문제 고르기"):
        init_game()
        st.rerun()
