### C221070_채지오
### 배포링크 : 

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import geopandas as gpd
from folium import IFrame
import altair as alt
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# Streamlit Multi-Page Application
# ==========================================
st.set_page_config(
    page_title="Korean Higher Education Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# Data Preparation
# ==========================================
@st.cache_data
# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme="viridis"):
    heatmap = alt.Chart(input_df).mark_rect().encode(
        y=alt.Y(f'{input_y}:O', axis=alt.Axis(
            title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X(f'{input_x}:O', axis=alt.Axis(
            title="Region", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        color=alt.Color(f'{input_color}:Q',
                        legend=alt.Legend(title=input_color, titleFontSize=14, labelFontSize=12),
                        scale=alt.Scale(scheme=input_color_theme)),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25)
    ).properties(
        width=900,
        height=300
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )
    return heatmap

@st.cache_data
def load_and_clean_data():
    # 데이터 불러오기
    data = pd.read_csv("고등 주요 01-시도별 신입생 충원율(2010-2024)_240902.csv", encoding='utf-8', skiprows=8)

    # 열 이름 변경
    data.columns = [
        '조사년도', '시도', '전체_모집인원', '전체_입학생수', '전체_충원율',
        '일반대학_모집인원', '일반대학_입학생수', '일반대학_충원율',
        '전문대학_모집인원', '전문대학_입학생수', '전문대학_충원율',
        '대학원_입학정원', '대학원_입학생수', '대학원_충원율'
    ] + list(data.columns[14:])  # 나머지 열 유지

    # NaN 값과 관련 없는 행 제거
    data = data.iloc[1:, :14].dropna(how='all', axis=1)

    # 열 형 변환
    data['조사년도'] = pd.to_numeric(data['조사년도'], errors='coerce').astype('Int64')
    for col in ['전체_모집인원', '전체_입학생수']:
        data[col] = data[col].str.replace(',', '').astype(float).astype('Int64')
    data['전체_충원율'] = data['전체_충원율'].astype(float)

    # 다른 관련 열에 변환 적용
    for col in ['일반대학_모집인원', '일반대학_입학생수', '전문대학_모집인원', '전문대학_입학생수', '대학원_입학정원', '대학원_입학생수']:
        data[col] = data[col].str.replace(',', '').astype(float).astype('Int64')
    for col in ['일반대학_충원율', '전문대학_충원율', '대학원_충원율']:
        data[col] = data[col].astype(float)

    return data

@st.cache_data
def load_geojson():
    # GeoJSON 파일 로드
    gdf_kor = gpd.read_file("gdf_korea_sido_2022.json")
    return gdf_kor
gdf_kor = gpd.read_file("gdf_korea_sido_2022.json")
gdf_kor['CTP_KOR_NM'] = ['서울','부산','대구','인천','광주','대전','울산','세종',
                         '경기','강원','충북','충남','전북','전남','경북','경남','제주']
geo_json_data = gdf_kor.to_json()
korea_center = [36.5, 127.5]


# ==========================================
# Split Data by Category
# ==========================================
@st.cache_data
def split_data(data):
    columns_common = ['조사년도', '시도']

    data_total = data[columns_common + ['전체_모집인원', '전체_입학생수', '전체_충원율']].copy()
    data_uni = data[columns_common + ['일반대학_모집인원', '일반대학_입학생수', '일반대학_충원율']].copy()
    data_col = data[columns_common + ['전문대학_모집인원', '전문대학_입학생수', '전문대학_충원율']].copy()
    data_gra = data[columns_common + ['대학원_입학정원', '대학원_입학생수', '대학원_충원율']].copy()

    return data_total, data_uni, data_col, data_gra

# 데이터 준비
data = load_and_clean_data()
geo_data = load_geojson()
data_total, data_uni, data_col, data_gra = split_data(data)

# 사이드바 메뉴
with st.sidebar:
    st.title("교육기관 구분")
    page = st.sidebar.radio("페이지 선택:", ["전체", "일반대학", "전문대학", "대학원"])

if page == "전체":
    st.title("📊 전체 (Total Institutions)")
    col = st.columns((1, 1), gap='medium')
    with col[0] : 
        # 데이터프레임 출력
        st.subheader("데이터 테이블")
        st.dataframe(data_total)
        
    with col[1] :
        # 트렌드 시각화
        st.subheader("트렌드 시각화")
        df = data_total    
        # 막대 그래프 그리기
        fig = px.bar(
            df,     # 데이터프레임
            x="시도",
            y="전체_충원율",    # x축, y축 데이터
            animation_frame="조사년도",     # year를 기준으로 slider 생성
            width=700,
            height=450,     # 그래프 크기
            )
        st.plotly_chart(fig, use_container_width=True)
        
    col = st.columns((3, 1), gap = 'medium')
    with col[0] : 
        # 지도 시각화
        st.subheader("지도 시각화")
        # 슬라이더로 연도 선택
        year = st.slider("조사년도 선택", min_value=int(data_uni["조사년도"].min()), max_value=int(data_uni["조사년도"].max()), value=int(data_uni["조사년도"].min()))
        df = data_total[~data_total['시도'].isin(['전국'])]
        df = df[df['조사년도'] == year]
    
    
        map = folium.Map(
            location=korea_center,
            zoom_start=7,
            tiles='cartodbpositron')
        # Choropleth map 그리기
        folium.Choropleth(
            geo_data=geo_json_data, # GeoJSON 파일
            data=df, # 데이터프레임
            columns= ['시도', '전체_충원율'], # 열
            key_on='feature.properties.CTP_KOR_NM', # key
            fill_color='BuPu', # 색상 Blue-Purple
            fill_opacity=0.7, # 투명도
            line_opacity=0.5, # 선 투명도
            legend_name='전체_충원율' # 범례 이름
            ).add_to(map)
        # Popup 추가
        for idx, row in df.iterrows():
            region_name = row['시도']
            total_rate = row['전체_충원율']
            total_new = row['전체_입학생수']
            total = row['전체_모집인원']
            geo_match = gdf_kor[gdf_kor['CTP_KOR_NM'] == region_name]
            if not geo_match.empty:
                coords = geo_match.geometry.representative_point().y.values[0], geo_match.geometry.representative_point().x.values[0]

                # HTML 팝업 생성
                popup_html = f"""
                <b>시도:</b> {region_name}<br>
                <b>전체 충원율:</b> {total_rate:.2f}%<br>
                <b>전체 입학생수:</b> {total_new:,}명<br>
                <b>전체 모집인원:</b> {total:,}명
                """
                iframe = IFrame(popup_html, width=250, height=150)
                popup = folium.Popup(iframe, max_width=300)

                # Marker 추가
                folium.Marker(location=coords,popup=popup,
                              icon=folium.Icon(icon="info-sign")).add_to(map)

        # 지도 렌더링
        st_folium(map, width=700, height=500)

    with col[1] : 
        # Streamlit 레이아웃
        st.subheader("전체 충원율")

        # 데이터프레임 정렬
        df_selected_year_sorted = df.sort_values(by="전체_충원율", ascending=False)

        # 데이터프레임 출력
        st.dataframe(
            df_selected_year_sorted,
            column_order=["시도", "전체_충원율"],  # 표시할 컬럼 지정
            hide_index=True,
            use_container_width=True,
            column_config={
                "시도": st.column_config.TextColumn(
                    label="Region",  # 컬럼 헤더
                ),
                "전체_충원율": st.column_config.ProgressColumn(
                    label="Fulfillment Rate (%)",  # 컬럼 헤더
                    format="%.1f%%",  # 퍼센트 형식
                    min_value=0,  # 최소값
                    max_value=max(df_selected_year_sorted['전체_충원율']),  # 최대값
                )})
    
    # 히트맵
    st.subheader("히트맵 시각화")
    heatmap_chart = make_heatmap(
    input_df=data_total,
    input_y="조사년도",
    input_x="시도",
    input_color="전체_충원율",
    input_color_theme="viridis"
    )
    # Streamlit에 Altair 차트 렌더링
    st.altair_chart(heatmap_chart, use_container_width=True)

elif page == "일반대학":
    st.title("📊 일반대학 (Universities)")
    col = st.columns((1, 1), gap='medium')
    with col[0] : 
        # 데이터프레임 출력
        st.subheader("데이터 테이블")
        st.dataframe(data_uni)
        
    with col[1] :
        # 트렌드 시각화
        st.subheader("트렌드 시각화")
        df = data_uni    
        # 막대 그래프 그리기
        fig = px.bar(
            df,     # 데이터프레임
            x="시도",
            y="일반대학_충원율",    # x축, y축 데이터
            animation_frame="조사년도",     # year를 기준으로 slider 생성
            width=700,
            height=450,     # 그래프 크기
            )
        st.plotly_chart(fig, use_container_width=True)
        
    col = st.columns((3, 1), gap = 'medium')
    with col[0] : 
        # 지도 시각화
        st.subheader("지도 시각화")
        # 슬라이더로 연도 선택
        year = st.slider("조사년도 선택", min_value=int(data_uni["조사년도"].min()), max_value=int(data_uni["조사년도"].max()), value=int(data_uni["조사년도"].min()))
        df = data_uni[~data_uni['시도'].isin(['전국'])]
        df = df[df['조사년도'] == year]

        map = folium.Map(
            location=korea_center,
            zoom_start=7,
            tiles='cartodbpositron')
        # Choropleth map 그리기
        folium.Choropleth(
            geo_data=geo_json_data, # GeoJSON 파일
            data=df, # 데이터프레임
            columns= ['시도', '일반대학_충원율'], # 열
            key_on='feature.properties.CTP_KOR_NM', # key
            fill_color='BuPu', # 색상 Blue-Purple
            fill_opacity=0.7, # 투명도
            line_opacity=0.5, # 선 투명도
            legend_name='일반대학_충원율' # 범례 이름
            ).add_to(map)
        # Popup 추가
        for idx, row in df.iterrows():
            region_name = row['시도']
            total_rate = row['일반대학_충원율']
            total_new = row['일반대학_입학생수']
            total = row['일반대학_모집인원']
            geo_match = gdf_kor[gdf_kor['CTP_KOR_NM'] == region_name]
            if not geo_match.empty:
                coords = geo_match.geometry.representative_point().y.values[0], geo_match.geometry.representative_point().x.values[0]

                # HTML 팝업 생성
                popup_html = f"""
                <b>시도:</b> {region_name}<br>
                <b>일반대학 충원율:</b> {total_rate:.2f}%<br>
                <b>일반대학 입학생수:</b> {total_new:,}명<br>
                <b>일반대학 모집인원:</b> {total:,}명
                """
                iframe = IFrame(popup_html, width=250, height=150)
                popup = folium.Popup(iframe, max_width=300)

                # Marker 추가
                folium.Marker(location=coords,popup=popup,
                              icon=folium.Icon(icon="info-sign")).add_to(map)

        # 지도 렌더링
        st_folium(map, width=700, height=500)
    
    with col[1] : 
        # Streamlit 레이아웃
        st.subheader("일반대학 충원율")

        # 데이터프레임 정렬
        df_selected_year_sorted = df.sort_values(by="일반대학_충원율", ascending=False)

        # 데이터프레임 출력
        st.dataframe(
            df_selected_year_sorted,
            column_order=["시도", "일반대학_충원율"],  # 표시할 컬럼 지정
            hide_index=True,
            use_container_width=True,
            column_config={
                "시도": st.column_config.TextColumn(
                    label="Region",  # 컬럼 헤더
                ),
                "일반대학_충원율": st.column_config.ProgressColumn(
                    label="Fulfillment Rate (%)",  # 컬럼 헤더
                    format="%.1f%%",  # 퍼센트 형식
                    min_value=0,  # 최소값
                    max_value=max(df_selected_year_sorted['일반대학_충원율']),  # 최대값
                )})
    
    # 히트맵
    st.subheader("히트맵 시각화")
    heatmap_chart = make_heatmap(
    input_df=data_uni,
    input_y="조사년도",
    input_x="시도",
    input_color="일반대학_충원율",
    input_color_theme="viridis"
    )
    # Streamlit에 Altair 차트 렌더링
    st.altair_chart(heatmap_chart, use_container_width=True)

elif page == "전문대학":
    st.title("📊 전문대학 (Colleges)")
    col = st.columns((1, 1), gap='medium')
    with col[0] : 
        # 데이터프레임 출력
        st.subheader("데이터 테이블")
        st.dataframe(data_col)
        
    with col[1] :
        # 트렌드 시각화
        st.subheader("트렌드 시각화")
        df = data_col   
        # 막대 그래프 그리기
        fig = px.bar(
            df,     # 데이터프레임
            x="시도",
            y="전문대학_충원율",    # x축, y축 데이터
            animation_frame="조사년도",     # year를 기준으로 slider 생성
            width=700,
            height=450,     # 그래프 크기
            )
        st.plotly_chart(fig, use_container_width=True)

    col = st.columns((3, 1), gap = 'medium')
    with col[0] : 
        # 지도 시각화
        st.subheader("지도 시각화")
        # 슬라이더로 연도 선택
        year = st.slider("조사년도 선택", min_value=int(data_uni["조사년도"].min()), max_value=int(data_uni["조사년도"].max()), value=int(data_uni["조사년도"].min()))
        df = data_col[~data_col['시도'].isin(['전국'])]
        df = df[df['조사년도'] == year]
    
        map = folium.Map(
            location=korea_center,
            zoom_start=7,
            tiles='cartodbpositron')
        # Choropleth map 그리기
        folium.Choropleth(
            geo_data=geo_json_data, # GeoJSON 파일
            data=df, # 데이터프레임
            columns= ['시도', '전문대학_충원율'], # 열
            key_on='feature.properties.CTP_KOR_NM', # key
            fill_color='BuPu', # 색상 Blue-Purple
            fill_opacity=0.7, # 투명도
            line_opacity=0.5, # 선 투명도
            legend_name='전문대학_충원율' # 범례 이름
            ).add_to(map)
        # Popup 추가
        for idx, row in df.iterrows():
            region_name = row['시도']
            total_rate = row['전문대학_충원율']
            total_new = row['전문대학_입학생수']
            total = row['전문대학_모집인원']
            geo_match = gdf_kor[gdf_kor['CTP_KOR_NM'] == region_name]
            if not geo_match.empty:
                coords = geo_match.geometry.representative_point().y.values[0], geo_match.geometry.representative_point().x.values[0]

                # HTML 팝업 생성
                popup_html = f"""
                <b>시도:</b> {region_name}<br>
                <b>전문대학 충원율:</b> {total_rate:.2f}%<br>
                <b>전문대학 입학생수:</b> {total_new:,}명<br>
                <b>전문대학 모집인원:</b> {total:,}명
                """
                iframe = IFrame(popup_html, width=250, height=150)
                popup = folium.Popup(iframe, max_width=300)

                # Marker 추가
                folium.Marker(location=coords,popup=popup,
                              icon=folium.Icon(icon="info-sign")).add_to(map)

        # 지도 렌더링
        st_folium(map, width=700, height=500)
    
    with col[1] : 
        # Streamlit 레이아웃
        st.subheader("전문대학 충원율")

        # 데이터프레임 정렬
        df_selected_year_sorted = df.sort_values(by="전문대학_충원율", ascending=False)

        # 데이터프레임 출력
        st.dataframe(
            df_selected_year_sorted,
            column_order=["시도", "전문대학_충원율"],  # 표시할 컬럼 지정
            hide_index=True,
            use_container_width=True,
            column_config={
                "시도": st.column_config.TextColumn(
                    label="Region",  # 컬럼 헤더
                ),
                "전문대학_충원율": st.column_config.ProgressColumn(
                    label="Fulfillment Rate (%)",  # 컬럼 헤더
                    format="%.1f%%",  # 퍼센트 형식
                    min_value=0,  # 최소값
                    max_value=max(df_selected_year_sorted['전문대학_충원율']),  # 최대값
                )})
    
    # 히트맵
    st.subheader("히트맵 시각화")
    heatmap_chart = make_heatmap(
    input_df=data_col,
    input_y="조사년도",
    input_x="시도",
    input_color="전문대학_충원율",
    input_color_theme="viridis"
    )
    # Streamlit에 Altair 차트 렌더링
    st.altair_chart(heatmap_chart, use_container_width=True)

elif page == "대학원":
    st.title("📊 대학원 (Graduate Schools)")
    col = st.columns((1, 1), gap='medium')
    with col[0] : 
        # 데이터프레임 출력
        st.subheader("데이터 테이블")
        st.dataframe(data_gra)
        
    with col[1] :
        # 트렌드 시각화
        st.subheader("트렌드 시각화")
        df = data_gra   
        # 막대 그래프 그리기
        fig = px.bar(
            df,     # 데이터프레임
            x="시도",
            y="대학원_충원율",    # x축, y축 데이터
            animation_frame="조사년도",     # year를 기준으로 slider 생성
            width=700,
            height=450,     # 그래프 크기
            )
        st.plotly_chart(fig, use_container_width=True)

    col = st.columns((3, 1), gap='medium')
    with col[0] :
        # 지도 시각화
        st.subheader("지도 시각화")
        # 슬라이더로 연도 선택
        year = st.slider("조사년도 선택", min_value=int(data_uni["조사년도"].min()), max_value=int(data_uni["조사년도"].max()), value=int(data_uni["조사년도"].min()))
        df = data_gra[~data_gra['시도'].isin(['전국'])]
        df = df[df['조사년도'] == year]
    
        map = folium.Map(
            location=korea_center,
            zoom_start=7,
            tiles='cartodbpositron')
        # Choropleth map 그리기
        folium.Choropleth(
            geo_data=geo_json_data, # GeoJSON 파일
            data=df, # 데이터프레임
            columns= ['시도', '대학원_충원율'], # 열
            key_on='feature.properties.CTP_KOR_NM', # key
            fill_color='BuPu', # 색상 Blue-Purple
            fill_opacity=0.7, # 투명도
            line_opacity=0.5, # 선 투명도
            legend_name='대학원_충원율' # 범례 이름
            ).add_to(map)
        # Popup 추가
        for idx, row in df.iterrows():
            region_name = row['시도']
            total_rate = row['대학원_충원율']
            total_new = row['대학원_입학생수']
            total = row['대학원_입학정원']
            geo_match = gdf_kor[gdf_kor['CTP_KOR_NM'] == region_name]
            if not geo_match.empty:
                coords = geo_match.geometry.representative_point().y.values[0], geo_match.geometry.representative_point().x.values[0]

                # HTML 팝업 생성
                popup_html = f"""
                <b>시도:</b> {region_name}<br>
                <b>대학원 충원율:</b> {total_rate:.2f}%<br>
                <b>대학원 입학생수:</b> {total_new:,}명<br>
                <b>대학원 입학정원:</b> {total:,}명
                """
                iframe = IFrame(popup_html, width=250, height=150)
                popup = folium.Popup(iframe, max_width=300)

                # Marker 추가
                folium.Marker(location=coords,popup=popup,
                              icon=folium.Icon(icon="info-sign")).add_to(map)

        # 지도 렌더링
        st_folium(map, width=700, height=500)
    
    with col[1] : 
        # Streamlit 레이아웃
        st.subheader("대학원 충원율")

        # 데이터프레임 정렬
        df_selected_year_sorted = df.sort_values(by="대학원_충원율", ascending=False)

        # 데이터프레임 출력
        st.dataframe(
            df_selected_year_sorted,
            column_order=["시도", "대학원_충원율"],  # 표시할 컬럼 지정
            hide_index=True,
            use_container_width=True,
            column_config={
                "시도": st.column_config.TextColumn(
                    label="Region",  # 컬럼 헤더
                ),
                "대학원_충원율": st.column_config.ProgressColumn(
                    label="Fulfillment Rate (%)",  # 컬럼 헤더
                    format="%.1f%%",  # 퍼센트 형식
                    min_value=0,  # 최소값
                    max_value=max(df_selected_year_sorted['대학원_충원율']),  # 최대값
                )})
    # 히트맵
    st.subheader("히트맵 시각화")
    heatmap_chart = make_heatmap(
    input_df=data_gra,
    input_y="조사년도",
    input_x="시도",
    input_color="대학원_충원율",
    input_color_theme="viridis"
    )
    # Streamlit에 Altair 차트 렌더링
    st.altair_chart(heatmap_chart, use_container_width=True)

# Footer
st.markdown("Developed with Streamlit, Altair, Plotly, and GeoPandas. 📊")
