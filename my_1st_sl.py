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

# 사이드바
st.header('⬅️⬅️⬅️⬅️ 사이드바')
st.sidebar.write(' # 사이드바 텍스트')
st.sidebar.checkbox('체크박스 1')
st.sidebar.checkbox('체크박스 2')
st.sidebar.radio('라디오 버튼', ['radio 1','radio 2','radio 3'])
st.sidebar.selectbox('셀렉트박스', ['select 1','select 2','select 3'])
st.divider() # 👈 구분선

# 레이아웃: 컬럼
st.header(' 컬럼 레이아웃')
col_1, col_2, col_3 = st.columns([1, 2, 1]) # 컬럼 인스턴스 생성. 1:2:1 비율로 컬럼을 나눔

with col_1 :
    st.write('## 1번 컬럼')
    st.checkbox('이것은 1번 컬럼에 속한 체크박스 1')
    st.checkbox('이것은 1번 컬럼에 속한 체크박스 2')
    
with col_2 : 
    st.write('## 2번 컬럼')
    st.radio('2번 컬럼의 라디오 버튼', ['radio 1','radio 2','radio 3'])
    # 동일한 라디오 버튼을 생성할 수 없음
    # 사이드바에 이미 라디오 버튼이 생성되어 있기 때문에, 
    # 여기서는 라디오 버튼의 내용을 변경해야 오류가 발생하지 않음
    
col_3.write('## 3번 컬럽')
col_3.selectbox('3번 컬럼의 셀렉트박스', ['select 1','select 2','select 3'])  
 # 사이드바에 이미 셀렉트박스가 생성되어 있기 때문에, 
 # 여기서는 셀렉트 박스의 내용을 변경해야 오류가 발생하지 않음

# 레이아웃: 탭
st.header('탭 레이아웃')

# 탭 인스턴스 생성. 3개의 탭을 생성
tab_1, tab_2, tab_3 = st.tabs(['탭AAAAA','탭BBBBB','탭CCCCC'])
with tab_1:
    st.write(' # 탭AAAAA')
    st.write('이것은 탭A의 내용입니다.')
    
with tab_2:
    st.write(' # 탭BBBBB')
    st.write('이것은 탭B의 내용입니다.')
    '''
    ```python
    import pandas as pd
    a=3
    b=4
    ```
    '''
    
tab_3.write(' # 탭CCCCC')
tab_3.write('이것은 탭C의 내용입니다.')
st.divider() # 👈 구분선

# 사용자 입력 ============================
st.header('🤖 :blue[사용자 입력]')

# 텍스트 입력은 입력된 값을 반환
st.write(' # :orange[텍스트 입력]')
text = st.text_input('여기에 텍스트를 입력하세요')
st.write(f'입력된 텍스트: {text}')

# 숫자 입력은 입력된 값을 반환
st.write(' # :orange[숫자 입력]')
number = st.number_input('여기에 숫자를 입력하세요')
st.write(f'입력된 숫자: {number}')

# 날짜 입력은 입력된 값을 반환
st.write(' # :orange[날짜 입력]')
date = st.date_input('날짜를 선택하세요')
st.write(f'선택된 날짜: {date}')

# 시간 입력은 입력된 값을 반환
st.write(' # :orange[시간 입력]')
time = st.time_input('시간을 선택하세요')
st.write(f'선택된 시간: {time}')

# 파일 업로드는 업로드된 파일을 반환
st.write(' # :orange[파일 업로드]')
file = st.file_uploader('파일을 업로드하세요')
if file:
    st.write(f'업로드된 파일: {file}')
st.divider() # 👈 구분선

# 체크박스, 라디오 버튼, 셀렉트 박스, 멀티 셀렉트 박스 ============================
st.header('✔️ :blue[체크박스, 라디오 버튼, 셀렉트 박스, 멀티 셀렉트 박스]')

# 체크박스는 True/False 값을 반환
st.write(' # :orange[체크박스]')
check = st.checkbox('여기를 체크하세요')
if check:
    st.write('체크되었습니다.')

# 라디오 버튼은 선택된 값을 반환
st.write(' # :orange[라디오 버튼]')
radio = st.radio('여기에서 선택하세요', ['선택 1','선택 2','선택 3'])
st.write(radio+'가 선택되었습니다.')

# 셀렉트박스는 선택된 값을 반환
st.write(' # :orange[셀렉트 박스]')
select = st.selectbox('여기에서 선택하세요', ['선택 1','선택 2','선택 3'])
st.write(select+'가 선택되었습니다.')

# 멀티셀렉트박스는 선택된 값을 리스트로 반환
st.write(' # :orange[멀티 셀렉트 박스]')
multi = st.multiselect('여기에서 여러 값을 선택하세요', ['선택 1','선택 2','선택 3'])
st.write(f'{type(multi) = }, {multi}가 선택되었습니다.')
st.divider() # 👈 구분선

# 슬라이더, 프로그레스 바 ============================
st.header(':blue[슬라이더, 프로그레스 바]')

# 슬라이더는 선택된 값을 반환
st.write('### :orange[슬라이더]')
slider = st.slider('여기에서 값을 선택하세요', 0, 100, 50)
st.write(f'현재의 값은 {slider} 입니다.')

# 선택 슬라이더는 선택된 값을 반환
st.write('### :orange[선택 슬라이더]')
range_slider = st.select_slider('여기에서 값을 선택하세요', options=range(101), value=(25, 75))
st.write(f'현재의 값은 {range_slider} 입니다.')

# 컬러피커는 선택된 값을 반환
st.write('### :orange[컬러 피커]')
color = st.color_picker('색을 선택하세요','#00f900')
st.write(f'선택된 색은 {color} 입니다.')

# 프로그레스 바는 진행 상태를 반환
import time
st.write('### :orange[프로그레스 바]')
button1 = st.button('실시') # 버튼은 클릭 여부를 반환
if button1:
    progress = st.progress(0)
    for i in range(101):
        progress.progress(i)
        if i % 20 == 0:
            st.write(f'진행 상태: {i}%')
        time.sleep(0.05)

# spinner는 진행 상태를 반환
st.write('### :orange[스피너]')
button2 = st.button('로드') # 버튼은 클릭 여부를 반환
if button2:
    with st.spinner('로딩 중입니다...'):
        time.sleep(3)
        st.success('로딩 완료!')
st.divider() # 👈 구분선

# 버튼 ============================
st.header(':blue[버튼]')

button3 = st.button('여기를 클릭하세요') # 버튼은 클릭 여부를 반환
if button3:
    st.write('버튼이 클릭되었습니다.')
    st.success('버튼이 클릭되었습니다.') # 성공 메시지 출력

st.download_button('다운로드',
                    '이 내용이 다운로드 됨',
                    'download.txt') # 다운로드 버튼 생성
st.divider() # 👈 구분선

# 애니메이션 ============================
st.header(':blue[애니메이션]')
button4 = st.button('풍선을 띄워보세요') # 버튼은 클릭 여부를 반환
if button4:
    st.balloons() # 풍선 애니메이션 출력
st.divider() # 👈 구분선

button5 = st.button('눈을 내려 보세요') # 버튼은 클릭 여부를 반환
if button5:
    st.snow() # 풍선 애니메이션 출력

# 캐싱
st.header('💼 :blue[캐싱 적용]')

import time

@st.cache_data
def long_running_function(param1):
    time.sleep(5)
    return param1*param1

start = time.time()
num_1 = st.number_input('입력한 숫자의 제곱을 계산합니다.') # 숫자 입력은 입력된 값을 반환
st.write(f'{num_1}의 제곱은 {long_running_function(num_1)} 입니다. 계산시간은 {time.time()-start:.2f}초 소요')
st.write('🔖 :green[캐싱이 적용되면 동일한 계산은 저장된 결과를 사용하여 빠르게 처리함]')

# 세션 상태
st.header(':blue[세션 상태]')

import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(20, 2), columns=["x","y"])

st.write(' # :orange[session_state를 사용하지 않은 경우]')
color1 = st.color_picker("Color1","#FF0000")

st.divider() # 구분선
st.scatter_chart(df, x="x", y="y", color=color1)

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(np.random.randn(20, 2), columns=["x","y"])

st.write(' # :orange[session_state를 사용한 경우]')
color2 = st.color_picker("Color2","#FF0000")
st.divider() # 구분선
st.scatter_chart(st.session_state.df, x="x", y="y", color=color2)
st.write('🔖 :green[session_state를 사용하면, 저장된 state를 사용하므로 값이 고정됨]')
st.divider() # 구분선

# 앞의 코드 +
import streamlit as st

st.title('이것은 서브페이지 1')

import streamlit as st

st.title('이것은 서브페이지 2')
