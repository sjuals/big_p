# streamlit run streamlit\big_p\big_p.py

import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

import branca
def fancy_html(row):
    i = row
    Number_of_2 = cc.index[i] 
    Number_of_3 = cc['기기상태'].iloc[i]                             
    Number_of_4 = cc['컵 잔여량'].iloc[i]  
    Number_of_5 = cc['컵 반납용량'].iloc[i]
    Number_of_6 = cc['범위 내 카페 수'].iloc[i] 

    
    left_col_colour = "#2A799C"
    right_col_colour = "#C5DCE7"
    
    html = """<!DOCTYPE html>
    <html>

    </head>
        <table style="height: 126px; width: 330px;">
    <tbody>
    <tr>
    <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">기기번호</span></td>
    <td style="width: 160px;background-color: """+ right_col_colour +""";">{}</td>""".format(Number_of_2) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">기기상태</span></td>
    <td style="width: 160px;background-color: """+ right_col_colour +""";">{}</td>""".format(Number_of_3) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">컵 잔여량</span></td>
    <td style="width: 160px;background-color: """+ right_col_colour +""";">{}</td>""".format(Number_of_4) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">컵 반납용량</span></td>
    <td style="width: 160px;background-color: """+ right_col_colour +""";">{}</td>""".format(Number_of_5) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">범위 내 카페 수</span></td>
    <td style="width: 160px;background-color: """+ right_col_colour +""";">{}</td>""".format(Number_of_6) + """

    </tr>
    </tbody>
    </table>
    </html>
    """
    return html


# sidebar
with st.sidebar:
    st.sidebar.image('streamlit/big_p/trash_busters.jpg', use_column_width=True)
    st.header('TRASH BUSTERS')
    add_selectbox = st.sidebar.selectbox('어떻게 도와드릴까요?',('Office phone', 'Email', 'Mobile phone'))   
if add_selectbox =='Office phone':
    st.sidebar.title('02 6010 1164')
elif add_selectbox == 'Mobile phone':
    st.sidebar.title('010 1234 5678')
else:
    st.sidebar.title('hello@trashbusters.kr')

with st.sidebar:
    st.write('''
    ##### 주소: 서울시 마포구 성미산로7안길 12 
    ##### 오피스 주소: 서울시 마포구 성미산로7안길 12
    ''')    

    
st.title('다회용 컵 대여·반납기 솔루션')
    
    
    
    
tab1, tab2, tab3 = st.tabs(['입지선정', '변수 분석', '측정 결과'])

with tab1:    
    # main
    st.header('■ 다회용컵 대여·반납기 입지선정 분석')

    end = pd.read_csv('streamlit/big_p/end.csv', encoding='cp949')
    end.rename(columns={'y':'지수'}, inplace=True)
    end = end.sort_values(by='지수', ascending=False)
    end = end.drop(['인구밀도 (명/㎢)', '평균연령 (세)'], axis=1)
    end.reset_index(drop=True, inplace=True)
    # checkbox를 선택하면 원본 데이터프레임이 나타남
    if st.checkbox('원본 데이터 보기'):
        st.subheader('지역별(동) 최적 설치 지수')
        st.dataframe(end)




    # k-means
    df = pd.read_csv('streamlit/big_p/서구 쌍촌동.csv')
    df = df[['경도','위도']]

    from sklearn.cluster import KMeans

    points = df.values
    kmeans = KMeans(n_clusters=5).fit(points)

    cc= pd.DataFrame(columns=['경도','위도'], data=kmeans.cluster_centers_)


    df['cluster_id']= kmeans.labels_
    cdf = pd.concat([df,cc],axis=0)
    cdf['cluster_id'].fillna('설치위치',inplace=True)

    df = pd.read_csv('streamlit/big_p/서구 쌍촌동.csv')
    df = df[['경도', '위도', '상호명']]
    df['카페구분'] = kmeans.labels_


    cc['기기상태'] = ['정상', '점검중', '고장', '정상', '정상']
    cc['컵 잔여량'] = [1561, 220, 3000, 231, 0]
    cc['컵 반납용량'] = [1, 0.8, 0.2, 0.1, 0]
    cc['범위 내 카페 수'] = [35, 52, 47, 71, 32]

    
    # 지도

  
    
    import folium
    from folium.plugins import MarkerCluster

    m = folium.Map(location=[df['위도'].mean(), df['경도'].mean()], tiles='openstreetmap', zoom_start=15)

    for i in range(len(cc)):
        num_of_casualties1 = cc.index[i]
        if num_of_casualties1 == 1:
            color = 'blue'
        elif num_of_casualties1 == 2:
            color = 'green'
        elif num_of_casualties1 == 3:
            color = 'orange'
        elif num_of_casualties1 == 4:
            color = 'purple'
        else:
            color = 'red'

        html = fancy_html(i)
        iframe = branca.element.IFrame(html=html,width=350,height=150)
        popup = folium.Popup(iframe,parse_html=True)
        folium.Marker([cc.iloc[i][1], cc.iloc[i][0]],tooltip=(cc.index[i],cc['기기상태'].iloc[i]), popup=popup, icon=folium.Icon(color=color)).add_to(m)



    # mc = MarkerCluster()
    for x in range(len(df)):
        num_of_casualties = df['카페구분'].iloc[x]
        if num_of_casualties == 1:
            color = 'blue'
        elif num_of_casualties == 2:
            color = 'green'
        elif num_of_casualties == 3:
            color = 'orange'
        elif num_of_casualties == 4:
            color = 'purple'
        else:
            color = 'red'
        iframe = folium.IFrame(df['상호명'].iloc[x])
        popup = folium.Popup(iframe, min_width=100, max_width=100)
        folium.Circle(location = [df.iloc[x][1], df.iloc[x][0]], popup=popup, color=color, radius=3).add_to(m)
#         folium.Circle(location = [df.iloc[x][1], df.iloc[x][0]], popup=df['상호명'].iloc[x], color=color, radius=3).add_to(m)



#     m.save('map.html')




    # selectbox를 사용하여 '호선' 선택: 데이터프레임은 바로 이전에 사용한 최종 데이터프레임 사용
    # .unique() 매소드를 사용하여 selectbox에 호선이 각각 하나만 나타나게 함
    option = st.selectbox('지역(동) 선택',end['지역'].unique())
    end_selected = end.loc[(end['지역'] == option)]
    st.write(option, '데이터', end_selected)





    # 지도 불러오기
    import streamlit.components.v1 as components
    p = open('map.html', encoding='utf-8')

    st.header('서구 쌍촌동 카페 및 설치 위치')
    components.html(p.read(), width=950, height=650)

    st.markdown('### 기기 정보')
    if st.checkbox('기기 정보 데이터 보기'):
        st.dataframe(cc)
    
    option = st.selectbox('',cc.index.unique())
    df_selected1 = cc.loc[(cc.index.unique() == option)]
    df_selected2 = df.loc[(df['카페구분'] == option)]
    st.write(option, '번 기기', df_selected1)
    st.write(option, '번 기기 범위 카페 목록', df_selected2)
    
    
    
    

with tab2:
    end[['등록인구 (명)', '탑승량', '플라스틱 배출량', '카페수', '편의점수', '유동인구', '의료기관 수', '대학교 수', '지수']].astype(int)

    # 차트
    st.header('■ 지역별 변수 분석')



    st.markdown('### 인구정보')

    if st.checkbox('인구정보 데이터 보기'):
        st.dataframe(end[['지역', '등록인구 (명)']])

    end.index = end['지역']
    end = end.sort_values(by='등록인구 (명)', ascending=False)
    st.bar_chart(end['등록인구 (명)'], use_container_width=True, height=550)



    st.markdown('### 대중교통 탑승량')

    end.reset_index(drop=True, inplace=True)
    if st.checkbox('대중교통 탑승량 데이터 보기'):
        st.dataframe(end[['지역', '탑승량']])

    end.index = end['지역']
    end = end.sort_values(by='탑승량', ascending=False)
    st.bar_chart(end['탑승량'], use_container_width=True, height=550)



    st.markdown('### 플라스틱 배출량')

    end.reset_index(drop=True, inplace=True)
    if st.checkbox('플라스틱 배출량 데이터 보기'):
        st.dataframe(end[['지역', '플라스틱 배출량']])

    end.index = end['지역']
    end = end.sort_values(by='플라스틱 배출량', ascending=False)
    st.bar_chart(end['플라스틱 배출량'], use_container_width=True, height=550)



    st.markdown('### 카페 수')

    end.reset_index(drop=True, inplace=True)
    if st.checkbox('카페 수 데이터 보기'):
        st.dataframe(end[['지역', '카페수']])

    end.index = end['지역']
    end = end.sort_values(by='카페수', ascending=False)
    st.bar_chart(end['카페수'], use_container_width=True, height=550)



    st.markdown('### 편의점 수')

    end.reset_index(drop=True, inplace=True)
    if st.checkbox('편의점 수 데이터 보기'):
        st.dataframe(end[['지역', '편의점수']])

    end.index = end['지역']
    end = end.sort_values(by='편의점수', ascending=False)
    st.bar_chart(end['편의점수'], use_container_width=True, height=550)



    st.markdown('### 유동인구')

    end.reset_index(drop=True, inplace=True)
    if st.checkbox('유동인구 데이터 보기'):
        st.dataframe(end[['지역', '유동인구']])

    end.index = end['지역']
    end = end.sort_values(by='유동인구', ascending=False)
    st.bar_chart(end['유동인구'], use_container_width=True, height=550)



    st.markdown('### 의료기관 수')

    end.reset_index(drop=True, inplace=True)
    if st.checkbox('의료기관 수 데이터 보기'):
        st.dataframe(end[['지역', '의료기관 수']])

    end.index = end['지역']
    end = end.sort_values(by='의료기관 수', ascending=False)
    st.bar_chart(end['의료기관 수'], use_container_width=True, height=550)



    st.markdown('### 대학교 수')

    end.reset_index(drop=True, inplace=True)
    if st.checkbox('대학교 수 데이터 보기'):
        st.dataframe(end[['지역', '대학교 수']])

    end.index = end['지역']
    end = end.sort_values(by='대학교 수', ascending=False)
    st.bar_chart(end['대학교 수'], use_container_width=True, height=550)



    st.markdown('### 입지선정 지수')

    end.reset_index(drop=True, inplace=True)
    if st.checkbox('입지선정 지수 데이터 보기'):
        st.dataframe(end[['지역', '지수']])

    end.index = end['지역']
    end = end.sort_values(by='지수', ascending=False)
    st.bar_chart(end['지수'], use_container_width=True, height=550)

    
    
    

with tab3:   
    st.header('■ 측정 결과')
    st.markdown('### 1. 탄소 저감량')
    st.markdown('### 2. 재활용률')
    st.markdown('### 3. 폐기량 변화량')