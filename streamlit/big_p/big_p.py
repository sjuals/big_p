# streamlit run streamlit\big_p\big_p.py

import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')


st.title('다회용컵 대여·반납기 입지선정 분석 결과 보고서')

# st.header('지역별(동) 최적 설치 지수')
data_row = pd.read_csv('streamlit/big_p/data.csv', encoding='cp949')
data_row.rename(columns={'y':'지수'}, inplace=True)
data_row = data_row.sort_values(by='지수', ascending=False)
data_row.reset_index(drop=True, inplace=True)
# checkbox를 선택하면 원본 데이터프레임이 나타남
if st.checkbox('원본 데이터 보기'):
    st.subheader('지역별(동) 최적 설치 지수')
    st.dataframe(data_row)

# , use_column_width='Ture'
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




# 지도
import folium
from folium.plugins import MarkerCluster

m = folium.Map(location=[35.152421, 126.855071], tiles='openstreetmap', zoom_start=15)
 
for i in range(len(cc)):
    folium.Marker([cc.iloc[i][1], cc.iloc[i][0]], popup=cc.index[i], icon=folium.Icon(color='red')).add_to(m)

mc = MarkerCluster()
for x in range(len(df)):
    mc.add_child(folium.Circle(location = [df.iloc[x][1], df.iloc[x][0]],popup=df['상호명'].iloc[x], radius=3))
    
m.add_child(mc)

m.save('map.html')



# 지도 불러오기
import streamlit.components.v1 as components
p = open('map.html', encoding='utf-8')

st.header('서구 쌍촌동 설치 현황')
components.html(p.read(), width=950, height=650)
st.markdown('### 기기 정보')
cc


