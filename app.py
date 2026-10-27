import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# 1. 앱 제목 설정
st.title("부산 지하철 역별 이용객 수 지도 분석")

# 호선별 색상 매핑 사전 (1호선: 주황, 2호선: 초록, 3호선: 갈색, 4호선: 파랑)
COLOR_MAP = {
    '1호선': 'orange',
    '2호선': 'green',
    '3호선': 'brown',
    '4호선': 'blue'
}

# 2. CSV 파일 업로드
uploaded_file = st.file_uploader("busan_subway.csv 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # CSV 데이터 불러오기
    df = pd.read_csv(uploaded_file)

    # ① 전체 데이터 표 출력
    st.subheader("Subway Data Table")
    st.dataframe(df)

    # ② 호선 필터 (multiselect)
    lines = df['호선'].unique().tolist()
    selected_lines = st.multiselect("조회할 호선을 선택하세요:", options=lines, default=lines)

    # 선택된 호선의 데이터만 필터링
    filtered_df = df[df['호선'].isin(selected_lines)]

    # ③ 이용객 상위 5개 역 표로 표시
    st.subheader("이용객 상위 5개 역")
    top5_df = filtered_df.sort_values(by='이용객수', ascending=False).head(5)
    st.dataframe(top5_df[['호선', '역명', '이용객수']])

    # ④ 지도 생성 및 필터링된 데이터 표시
    st.subheader("Subway Map")
    busan_map = folium.Map(location=[35.1795543, 129.0756416], zoom_start=11)

    for _, row in filtered_df.iterrows():
        # 이용객수에 비례하여 반지름 계산 (제곱근 사용)
        radius_val = np.sqrt(row['이용객수']) * 0.1

        # 호선별 색상 지정 (사전에 없는 호선은 기본값 'gray')
        marker_color = COLOR_MAP.get(str(row['호선']), 'gray')

        # 지도에 CircleMarker 추가
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=radius_val,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.6,
            tooltip=f"[{row['호선']}] {row['역명']}",
            popup=f"{row['역명']} ({row['호선']})<br>이용객수: {row['이용객수']:,}명"
        ).add_to(busan_map)

    # Streamlit 화면에 지도 출력
    st_folium(busan_map, width=700, height=500)

else:
    st.info("분석할 CSV 파일을 업로드해주세요.")