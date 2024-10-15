import streamlit as st # streamlit 라이브러리 임포트

# 타이틀 텍스트 출력
st.title('첫 번째 웹 어플 만들기 👋')

# 텍스트 출력
st.write('# 1. Markdown 텍스트 작성하기')

# Markdown 문법으로 작성된 문장 출력
st.markdown(
    '''
        # 마크다운 헤더 1
        - 마크다운 목록1. **굵게** 표시
        - 마크다운 목록2. *기울임* 표시
            - 마크다운 목록 2-1
            - 마크다운 목록 2-2

        ## 마크다운 헤더 2
        - [네이버](https://naver.com)
         [구글](https://google.com)

        ### 마크다운 헤더 3
        일반 텍스트
        '''
        )

# DataFrame 출력
import pandas as pd # pandas 라이브러리 임포트

st.write('# 2. DataFrame 표시하기') # 텍스트 출력
df = pd.DataFrame({ # DataFrame 생성
    '이름': ['홍길동','이순신','강감찬'],
    '나이': [20, 45, 35]
    })

st.dataframe(df) # DataFrame 출력

# 그래프 출력
import numpy as np # numpy 라이브러리 임포트

st.write('# 3. 그래프 표시하기') # 텍스트 출력
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a","b","c"]) 
# DataFrame 생성

st.bar_chart(chart_data) # 바 차트 출력`

# 이미지 출력
from PIL import Image # 이미지 처리를 위한 PIL 라이브러리 임포트

st.write('# 4. 이미지 표시하기') # 텍스트 출력
img = Image.open('python.png') # 이미지 파일 열기
st.image(img, width=300) # 이미지 출력
st.divider() # 👈 구분선





import streamlit as st

# 텍스트
st.header('🚗 텍스트 출력')
st.write('') # 빈 줄 삽입

st.write('# 마크다운 H1 : st.write()')
st.write('### 마크다운 H3 : st.write()')
st.write('')

st.title('제목 : st.title()')
st.header('헤더 : st.header()')
st.subheader('서브헤더 : st.subheader()')
st.text('본문 텍스트 : st.text()')
st.write('')

st.markdown(' # 마크다운 : st.markdown()')
st.markdown('''
            1. ordered item
                - unordered item
                - unordered item
            2. ordered item
            3. ordered item
            ''')
st.divider() # 👈 구분선

# 마크다운
'''
# 👑 Magic에 마크다운을 조합
1. ordered item
    - 강조: ** unordered item **
    - 기울임: *unordered item*
2. ordered item
3. ordered item
'''

# 데이터프레임
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3],'B': [4, 5, 6],'C': [7, 8, 9]})
st.write(df) # 👈 데이터프레임 출력

# 차트
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
fig # 👈 차트 출력

# 사이드바
st.header('⬅️⬅️⬅️⬅️ 사이드바')
st.sidebar.write(' # 사이드바 텍스트')
st.sidebar.checkbox('체크박스 1')
st.sidebar.checkbox('체크박스 2')
st.sidebar.radio('라디오 버튼', ['radio 1','radio 2','radio 3'])
st.sidebar.selectbox('셀렉트박스', ['select 1','select 2','select 3'])
