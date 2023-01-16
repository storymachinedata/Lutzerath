import numpy as np
import altair as alt
import pandas as pd
import streamlit as st

import plotly.express as px
from datetime import datetime,timedelta
import pytz
import re

#from germansentiment import SentimentModel

st.set_page_config(layout="wide")


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

import time

col1,col2= st.columns(2)

with col1:
   #st.header("A cat")
   st.image("https://storymachine.mocoapp.com/objects/accounts/a201d12e-6005-447a-b7d4-a647e88e2a4a/logo/b562c681943219ea.png", width=200)
   


st.title('Lutzerath Posts Monitoring')

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/640px-LinkedIn_logo_initials.png",
    width=100,
)

my_bar = st.progress(0)

for percent_complete in range(100):
     time.sleep(0.05)
     my_bar.progress(percent_complete + 1)





df =pd.read_csv('https://phantombuster.s3.amazonaws.com/UhrenaxfEnY/5EdaCLr0ieNAju7fa00niA/lutzerath_mentions.csv')

df.insert(len(df.columns), 'Keyword', 'Lutzerath')


df = df.dropna(how='any', subset=['textContent'])


df.drop(['connectionDegree', 'timestamp'], axis=1, inplace=True)


def getActualDate(url):

    a= re.findall(r"\d{19}", url)

    a = int(''.join(a))

    a = format(a, 'b')

    first41chars = a[:41]

    ts = int(first41chars,2)

    #tz = pytz.timezone('Europe/Paris')

    actualtime = datetime.fromtimestamp(ts/1000).strftime("%Y-%m-%d %H:%M:%S %Z")

    return actualtime

df['postDate'] = df.postUrl.apply(getActualDate)


df = df.dropna(how='any', subset=['postDate'])


import datetime as dt

#def datenow(date):
     #a = re.(datetime.now() - df.postDate.days >1:)

#df5= df
#df5['date'] =  pd.to_datetime(df5['postDate'])
df['date'] =  pd.to_datetime(df['postDate'])

df.drop_duplicates(subset=['postUrl'], inplace=True)
df = df.reset_index(drop=True)

df['Total Interactions'] = df['likeCount'] + df['commentCount']



df['likeCount'] = df['likeCount'].fillna(0)
df['commentCount'] = df['commentCount'].fillna(0)
df['Total Interactions'] = df['Total Interactions'].fillna(0)

df['likeCount'] = df['likeCount'].astype(int)
df['commentCount'] = df['commentCount'].astype(int)
df['Total Interactions'] = df['Total Interactions'].astype(int)


####################

col1, col2 = st.columns(2)

with col1:
   st.header("Select Time Range")
   
   number = st.number_input('Select the days you want to see the posts', min_value=1, max_value=30, value=1, step=1)
   if number:
            df = df[df['date']>=(dt.datetime.now()-dt.timedelta(days=number))] #hours = 6,12, 24
            st.success(f'Monitor Posts from last {int(number)} Days', icon="✅")

with col2:
   
        st.write('')



st.header('')
st.header('')
################

tab1, tab2 = st.tabs(["Lutzerath", "Search for a Keyword Inside Posts"])

#df = df.sort_values(by='postDate', ascending=False)
df_orig = df
df_orig['Hour'] = pd.to_datetime(df_orig.postDate).dt.strftime("%H")


with tab1:
   filter_number = st.number_input('Insert a number to view post with Total Interaaction greater than this number', )
   df_all = df_orig[df_orig['Total Interactions']>=filter_number]
   df_all = df_all.reset_index(drop=True)
   if st.button('Show Data'):
      st.write(df_all)

   #df_all = df_all[df_all['date']>=(dt.datetime.now()-dt.timedelta(days=1))] #hours = 6,12, 24
   st.write(f'Total posts found in last Hours: ', df_all.shape[0])
   #st.subheader('Total Interaction getting in past hours in the day')
   #st.bar_chart(df_all, x='Hour', y='Total Interactions')
   fig = px.bar(

    df_all,x="Hour",y="Total Interactions",color='Hour')


   fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
   #st.plotly_chart(fig)


   st.header(f'Most Recent Posts')
   st.info('Most recent posts appear first', icon="ℹ️")
   df_all.sort_values(['postDate'], ascending=False, inplace=True)
   df_all = df_all.reset_index(drop=True)
   df_all_100 = df_all
   num_posts = df_all_100.shape[0]

   if  num_posts>0:

     #splits = np.array_split(df5,5)
     splits = df_all_100.groupby(df_all_100.index // 3)
     for _, frames in splits:
          frames = frames.reset_index(drop=True)
          #print(frames.head())
          thumbnails = st.columns(frames.shape[0])
          for i, c in frames.iterrows():
               with thumbnails[i]:

                    if not pd.isnull(c['profileImgUrl']):
                        st.image(c['profileImgUrl'], width=150)
                    if not pd.isnull(c['profileUrl']):
                        #st.image(c['profileImgUrl'], width=150)
                        st.subheader(frames.fullName[i])
                        st.write('Personal Account')
                        st.write(c['title']) #postType
                        st.write('-----------')
                        if not pd.isnull(c['postImgUrl']):
                            st.image(c['postImgUrl'])
                        st.info(c['textContent'])  #postContent
                        st.write('Total Interactions 📈:  ',c['Total Interactions']) #totInteractions
                        st.write('Likes 👍:  ',c['likeCount']) #totInteractions
                        st.write('Comments 💬:  ',c['commentCount']) #totInteractions
                        #st.write('Action 📌:  ',c['action']) #totInteractions
                        st.write('Publish Date & Time 📆:         ',c['postDate']) #publishDate
                        with st.expander('Link to this Post 📮'):
                             st.write(c['postUrl']) #linktoPost
                        with st.expander('Link to  Profile 🔗'):
                             st.write(c['profileUrl']) #linktoProfile
                    
                    if not pd.isnull(c['logoUrl']):
                        st.image(c['logoUrl'], width=150)
                    
                        st.subheader(c['companyName'])
                        st.write('Corporate Account')
                        st.write('👥:  ',c['followerCount'])
                        if not pd.isnull(c['postImgUrl']):
                            st.image(c['postImgUrl'])
                        st.info(c['textContent'])  #postContent
                        st.write('Total Interactions 📈:  ',c['Total Interactions']) #totInteractions
                        st.write('Likes 👍:  ',c['likeCount']) #totInteractions
                        st.write('Comments 💬:  ',c['commentCount']) #totInteractions
                        #st.write('Action 📌:  ',c['action']) #totInteractions
                        st.write('Publish Date & Time 📆:         ',c['postDate']) #publishDate
                        with st.expander('Link to this Post 📮'):
                             st.write(c['postUrl']) #linktoPost
                        with st.expander('Link to  Company Profile 🔗'):
                             st.write(c['companyUrl']) #linktoProfile
                        
                    
                    
                       

                    
                    #st.write('Type of Post 📨:  ',c['type']) #postType
                    
                    # if not pd.isnull(c['postImgUrl']):
                    #     st.image(c['postImgUrl'])
                    #     st.write('Image from the Post  🗾')
                    
   else:
            st.image('https://img.freepik.com/premium-vector/hazard-warning-attention-sign-with-exclamation-mark-symbol-white_231786-5218.jpg?w=2000', width =200)
            st.subheader('Oops... No new post found in last Hours.')



with tab2:

   #st.info('Search is c', icon="ℹ️")
   title = st.text_input('Search for a keyword inside posts', 'lutzerath')
   title = title.lower()
   #title= f’\b{title}\b’
   #st.write( title)

   df_all.textContent= df_all.textContent.str.lower()

   df_all['client'] = df_all.textContent.str.contains(title)
   #df30['client'] = df30['textContent'].apply(lambda row: row.astype(str).str.contains(title).any())

   #st.write(df30['client'].value_counts())

   df_search = df_all.loc[df_all.client == 1] 
   df_search = df_search.reset_index(drop=True)
   st.write(f'Posts found with keyword {title}:',df_search.shape[0])
   #st.write(df_search)


   st.header(f'Posts which mention the keyword {title}')
   num_posts = df_search.shape[0]

   if  num_posts>0:

     #splits = np.array_split(df5,5)
     splits = df_search.groupby(df_search.index // 3)
     for _, frames in splits:
          frames = frames.reset_index(drop=True)
          #print(frames.head())
          thumbnails = st.columns(frames.shape[0])
          for i, c in frames.iterrows():
               with thumbnails[i]:

                    if not pd.isnull(c['profileImgUrl']):
                        st.image(c['profileImgUrl'], width=150)
                    if not pd.isnull(c['profileUrl']):
                        #st.image(c['profileImgUrl'], width=150)
                        st.subheader(frames.fullName[i])
                        st.write('Personal Account')
                        st.write(c['title']) #postType
                        st.write('-----------')
                        if not pd.isnull(c['postImgUrl']):
                            st.image(c['postImgUrl'])
                        st.info(c['textContent'])  #postContent
                        st.write('Total Interactions 📈:  ',c['Total Interactions']) #totInteractions
                        st.write('Likes 👍:  ',c['likeCount']) #totInteractions
                        st.write('Comments 💬:  ',c['commentCount']) #totInteractions
                        #st.write('Action 📌:  ',c['action']) #totInteractions
                        st.write('Publish Date & Time 📆:         ',c['postDate']) #publishDate
                        with st.expander('Link to this Post 📮'):
                             st.write(c['postUrl']) #linktoPost
                        with st.expander('Link to  Profile 🔗'):
                             st.write(c['profileUrl']) #linktoProfile
                    
                    if not pd.isnull(c['logoUrl']):
                        st.image(c['logoUrl'], width=150)
                    
                        st.subheader(c['companyName'])
                        st.write('Corporate Account')
                        st.write('👥:  ',c['followerCount'])
                        if not pd.isnull(c['postImgUrl']):
                            st.image(c['postImgUrl'])
                        st.info(c['textContent'])  #postContent
                        st.write('Total Interactions 📈:  ',c['Total Interactions']) #totInteractions
                        st.write('Likes 👍:  ',c['likeCount']) #totInteractions
                        st.write('Comments 💬:  ',c['commentCount']) #totInteractions
                        #st.write('Action 📌:  ',c['action']) #totInteractions
                        st.write('Publish Date & Time 📆:         ',c['postDate']) #publishDate
                        with st.expander('Link to this Post 📮'):
                             st.write(c['postUrl']) #linktoPost
                        with st.expander('Link to  Company Profile 🔗'):
                             st.write(c['companyUrl']) #linktoProfile
                    
   else:
            st.image('https://img.freepik.com/premium-vector/hazard-warning-attention-sign-with-exclamation-mark-symbol-white_231786-5218.jpg?w=2000', width =200)
            st.subheader(f'Oops... No new post found with keyword {title}.')
