import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os  
from PIL import Image

# 페이지 설정
st.set_page_config(page_title="공장 전력 예측 솔루션", layout="wide")

# 머신러닝 pkl 모델 불러오기 
@st.cache_resource
def load_model():
    model_path = 'best_lgbm_model.pkl' # 현재 폴더의 파일명과 맞는지 확인 필수!!!!!!!!!!!!!!!!!!    
    # 파일이 실제로 존재하는지 확인
    if not os.path.exists(model_path):
        # 파일이 없으면 에러 메시지를 화면에 띄움
        st.error(f" 모델 파일을 찾을 수 없습니다! 현재 위치: {os.getcwd()}")
        st.info("파일이 'best_lgbm_model.pkl'이라는 이름으로 app.py와 같은 폴더에 있는지 확인해주세요.")
        return None
    
    return joblib.load(model_path)

# 모델 로드 실행
model = load_model()

#  화면 디자인
st.title("🏭 스마트 팩토리 에너지 관리 AI")
st.markdown(
    """
    <div style="text-align: right; color: gray; font-size: 0.9rem;">
        ✨ PHS | Predictive Hybrid Solution<br>
        누구에게나 예측가능한 솔루션을 제공합니다 ;)
    </div>
    """, 
    unsafe_allow_html=True
)
st.markdown("---") # 얇은 구분선으로 깔끔하게 분리
st.markdown("""
이 대시보드는 운영 변수(시간, 요일, 부하)로 공장의 예상 전력 소비량을 예측합니다.
""")

#  사이드바: 사용자 입력 받기
st.sidebar.header("📋 운영 조건 설정")

# (A) 입력 받기
# NSM: 자정부터 흐른 초 (0 ~ 86400)
nsm_input = st.sidebar.slider("현재 시간 (NSM)", 0, 86400, 36000, help="자정(0)부터 현재까지 흐른 초(Seconds)")

# WeekStatus: 평일(Weekday) vs 주말(Weekend)
week_status_input = st.sidebar.radio("주중/주말", ["Weekday", "Weekend"])

# Day_of_week: 요일
day_input = st.sidebar.selectbox("요일", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

# Load_Type: 부하 종류
load_input = st.sidebar.selectbox("부하 상태", ["Light_Load", "Medium_Load", "Maximum_Load"])

# Season: 계절 (데이터셋에 따라 이름 확인 필요, 보통 LabelEncoder는 알파벳순 정렬)
season_input = st.sidebar.selectbox("계절", ["Fall", "Spring", "Summer", "Winter"]) # 알파벳순 가정

# Month: 월
month_input = st.sidebar.slider("월 (Month)", 1, 12, 1)


#  입력값을 모델이 아는 숫자(0, 1, 2...)로 변환
week_map = {"Weekday": 0, "Weekend": 1}
input_dict = {
    'NSM': nsm_input,
    'WeekStatus': 0 if week_status_input == "Weekday" else 1,
    'Day_of_week': ["Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "Wednesday"].index(day_input), # 알파벳순
    'Load_Type': ["Light_Load", "Maximum_Load", "Medium_Load"].index(load_input), # 알파벳
    'Season': ["Fall", "Spring", "Summer", "Winter"].index(season_input),
    'month': month_input
}

# 예측 실행
if st.button("⚡ 전력 사용량 예측하기"):
    
    #  NSM(초)을 시간(0~23)으로 변환
    hour_val = nsm_input // 3600
    
    # 요일을 숫자로 변환 
    day_map = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6}
    day_num = day_map[day_input]

    # 사용자가 입력한 값을 모델이 요구하는 8개 순서대로 무조건~~~~!!!!!!! 주의 순서바뀌면 이상해짐
    final_features = [[
        nsm_input,                                  #  NSM
        1 if week_status_input == "Weekend" else 0, #  WeekStatus
        day_num,                                    #  Day_of_week
        ["Light_Load", "Medium_Load", "Maximum_Load"].index(load_input), #  Load_Type
        hour_val,                                   # hour (NSM으로 계산됨)
        month_input,                                # month
        day_num,                                    # dayofweek (동일하게 적용)
        ["Fall", "Spring", "Summer", "Winter"].index(season_input) # Season
    ]]
    
    # 예측 수행
    try:
        prediction = model.predict(final_features)[0]
        
        # 결과 보여주기
        st.divider()
        st.balloons() 

        #  두 개의 컬럼 
        col1, col2 = st.columns([2, 1]) # 비율을 2:1로 설정 

        with col1:
            # 왼쪽 컬럼: 예상 전력 사용량 표시
            st.header(f"예상 전력 사용량: :blue[{prediction:.2f}] kWh")
            # 분석 리포트도 텍스트 옆에 
            st.info(f"📍 현재 설정: {month_input}월, {day_input}, {hour_val}시, {load_input} 상태")

        with col2:
            # 오른쪽 컬럼: 스폰지밥 이미지를 
            img = Image.open('sponzebob_img.png')
            
            # 컬럼 안에서 이미지 
            st.image(img, width=230, caption="스폰지밥이 에너지를 감시 중!")
    except Exception as e:
        st.error(f"예측 중 오류가 발생했습니다: {e}")

