import streamlit as st
import folium
import pandas as pd
import numpy as np
import geopandas as gpd
from streamlit_folium import folium_static 


st.title("데이터시각화_과제3번_C221070_채지오 : 행정구역별 합계출산율 시각화")
st.write("이 앱은 Folium과 Streamlit을 사용하여 대한민국 행정구역별 합계출산율을 시각화합니다.")
st.markdown("#### 배포 링크 : https://datavisualization-hw3-c221070-chaejioh.streamlit.app/")
st.divider()
 
st.write('# 1. 데이터 불러오기')
# 데이터 로드
st.write('## (1) 합계출산율 데이터')
@st.cache_data
def load_data():
    gdf_kor = gpd.read_file("gdf_korea_sido_2022.json")
    df = pd.read_csv("HW3_data.csv")
    return gdf_kor, df
gdf_kor, df = load_data()
df

st.write('## (2) 행정구역 데이터')
gdf_kor 
st.divider()


st.write('# 2. 데이터 정제하기')
st.write('## (1) 합계출산율 데이터')
'''
#### 컬럼 추출
1. 합계출산율 열만 필요하므로, 인덱스가 되어줄 부분과 합계출산율 열만 가져온다. 
2. 전국 데이터는 사용하지 않으므로 제거(drop)한다. 
3. 행과 열의 이름이 너무 복잡하므로, 행렬의 이름을 더 직관적으로 수정한다.
4. 마지막으로 결과를 확인한다
'''
df_sel = df.iloc[:, [0,1]]
df_sel.columns = ['행정구역별', '합계출산율']
df_sel.drop([0], axis=0, inplace=True)
df_sel['행정구역별'] = df_sel['행정구역별'].str.split().str[1]
df_sel
st.divider()


st.write('# 2. 두 데이터셋 간의 매칭 확인')
'''
#### 데이터셋의 행정구역별 열에 대하여 매칭을 확인한다.
1. 먼저 각 데이터의 공백을 제거한다.
2. 그후 두 데이터셋의 행정구역명에 대하여 서로 매칭되지 않는 값들이 있는지 확인한다.
3. print 결과 아무 결과도 나오지 않으면 넘어가고, 그렇지 않은 경우 별도의 과정을 추가적으로 수행한다.
'''
st.write('## (1) 매칭 결과 확인')
'''
#### '행정구역별'과 'CTP_KOR_NM'에서 공백 제거
##### => 아무런 결과도 나오지 않는 것이 best!
'''
df_sel['행정구역별'] = df_sel['행정구역별'].str.strip()
gdf_kor['CTP_KOR_NM'] = gdf_kor['CTP_KOR_NM'].str.strip()
# 매칭되지 않은 데이터 확인
unmatched = df_sel[~df_sel['행정구역별'].isin(gdf_kor['CTP_KOR_NM'])]
print("매칭되지 않은 데이터:")
print(unmatched)

st.write('## (2) 매칭되지 않는 데이터 처리 및 확인')
'''
- 만약 위 과정에서 결과가 나왔다면 위 결과에 기반하여 서로 매칭되지 않는 데이터들의 값을 임의로 조정한다.
- 이 과정도 아무런 결과가 뜨지 않는 것이 best
'''
name_corrections = {
    '강원특별자치도': '강원도'
}
df_sel['행정구역별'] = df_sel['행정구역별'].replace(name_corrections)

unmatched = df_sel[~df_sel['행정구역별'].isin(gdf_kor['CTP_KOR_NM'])]
print("매칭되지 않은 데이터:")
print(unmatched)
st.divider()


st.write('# 3. 지도 시각화(folium)')
'''
##### folium 라이브러리와 앞에서 정제한 데이터셋을 활용하여 지도로 시각화한다.
'''
# Folium 지도 생성
st.subheader("Choropleth 지도")

geo_json_data = gdf_kor.to_json()
korea_center = [36.5, 127.5]
map = folium.Map(
    location=korea_center,
    zoom_start=7,
    tiles='cartodbpositron')

st.header('행정구역별 합계출산율')
# Choropleth map 그리기
folium.Choropleth(
    geo_data=geo_json_data, # GeoJSON 파일
    data=df_sel, # 데이터프레임
    columns= ['행정구역별', '합계출산율'], # 열
    key_on='feature.properties.CTP_KOR_NM', # key
    fill_color='BuPu', # 색상 Blue-Purple
    fill_opacity=0.7, # 투명도
    line_opacity=0.5, # 선 투명도
    legend_name='합계출산율' # 범례 이름
).add_to(map)
# Popup 추가: 각 지역의 지역명과 합계출산율
for idx, row in df_sel.iterrows():
    region_name = row['행정구역별']
    birth_rate = row['합계출산율']
    geo_match = gdf_kor[gdf_kor['CTP_KOR_NM'] == region_name]
    if not geo_match.empty:
        coords = geo_match.geometry.centroid.y.values[0], geo_match.geometry.centroid.x.values[0]
        popup_text = f"<b>지역명:</b> {region_name}<br><b>합계출산율:</b> {birth_rate}"
        folium.Marker(location=coords, popup=folium.Popup(popup_text, max_width=300)).add_to(map)
map # 지도 출력하기
folium_static(map)


# 사용자 상호작용
st.subheader("지역별 합계출산율 확인")  # 섹션 제목 추가

col1, col2 = st.columns(2)  # 2개의 컬럼으로 나누기

with col1:
    selected_region = st.selectbox(
        "지역을 선택하세요", 
        options=df_sel['행정구역별'].unique()
    )

with col2:
    if selected_region:
        selected_data = df_sel[df_sel['행정구역별'] == selected_region]
        st.metric(
            label=selected_region,
            value=f"합계출산율: {selected_data['합계출산율'].values[0]}"
        )
