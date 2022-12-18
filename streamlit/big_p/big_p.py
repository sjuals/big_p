# streamlit run streamlit\big_p\big_p.py

import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')


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

    
    
    
    
    
# main
st.title('다회용컵 대여·반납기 입지선정 분석 결과 보고서')

# st.header('지역별(동) 최적 설치 지수')
end = pd.read_csv('streamlit/big_p/end.csv', encoding='cp949')
end.rename(columns={'y':'지수'}, inplace=True)
end = end.sort_values(by='지수', ascending=False)
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

st.header('서구 쌍촌동 카페 및 설치 위치')
components.html(p.read(), width=950, height=650)
st.markdown('### 기기 정보')
cc


st.markdown('### 지역별 인구정보')
end.index = end['지역']
end = end.sort_values(by='등록인구 (명)', ascending=False)
st.bar_chart(end['등록인구 (명)'], use_container_width=True, height=550)




import seaborn as sns
import matplotlib.pyplot as plt
# 이미지 해상도 높이기 
# %config InlineBackend.figure_format = 'retina'
#한글
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


# val_count  = end['column_name'].value_counts()
fig = plt.figure(figsize=(18,5))
plt.xticks(rotation=90)
sns.barplot(end['지역'], end['등록인구 (명)'])
plt.ylabel('등록인구(명)', fontsize=12)
plt.xlabel('지역(동)', fontsize=12)
st.pyplot(fig)



fig = plt.figure(figsize=(18,5))
plt.xticks(rotation=90)
plt.bar(end['지역'], end['등록인구 (명)'])
plt.ylabel('등록인구(명)', fontsize=12)
plt.xlabel('지역(동)', fontsize=12)
plt.xlim(-0.5,66.5)
st.pyplot(fig)