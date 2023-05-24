import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import datetime

tweets_df = pd.DataFrame()
st.write("# Twitter data scraping")
option = st.selectbox('How would you like the data to be searched?',('Keyword', 'Hashtag'))
word = st.text_input('Please enter a '+option, 'LIC Policy')
start = st.date_input("Select the start date", datetime.date(2009, 6, 4),key='d1')
end = st.date_input("Select the end date", datetime.date(2009, 16, 6),key='d2')
tweet_c = st.slider('How many tweets to scrape', 0, 100000, 5)
tweets_list = []

# Scrape using TwitterSearchScraper
if word:
    try:
        if option=='Keyword':
            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} lang:en since:{start} until:{end}').get_items()):
                if i>tweet_c-1:
                    break
                tweets_list.append([ tweet.id, tweet.date, tweet.flag, tweet.user.username, tweet.content])
            tweets_df = pd.DataFrame(tweets_list, columns=['id', 'date', 'flag', 'username', 'content'])
        else:
            for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} lang:en since:{start} until:{end}').get_items()):
                if i>tweet_c-1:
                    break
                tweets_list.append([ tweet.id, tweet.date, tweet.flag, tweet.user.username, tweet.content ])
            tweets_df = pd.DataFrame(tweets_list, columns=['id', 'date', 'flag', 'username', 'content'])
    except Exception as e:
        st.error(f"Too many requests, Limit exceeded, please try again after few hours")
        st.stop()

else:
    st.warning(option,' cant be empty', icon="⚠️")

#sidebar
with st.sidebar:
    st.info('DETAILS', icon="ℹ️")
    if option=='Keyword':
        st.info('Keyword is '+word)
    else:
        st.info('Hashtag is '+word)
    st.info('Starting Date is '+str(start))
    st.info('End Date is '+str(end))
    st.info("Number of Tweets "+str(tweet_c))
    st.info("Total Tweets Scraped "+str(len(tweets_df)))
    x=st.button('Show Tweets',key=1)

# Downloading to csv
@st.cache # IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(df):
    return df.to_csv().encode('utf-8')

if not tweets_df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        csv = convert_df(tweets_df) # csv
        c=st.download_button(label="Download data as CSV",data=csv,file_name='Twitter_data.csv',mime='text/csv',)
    with col2:    #json
        json_string = tweets_df.to_json(orient ='records')
        j=st.download_button(label="Download data as JSON",file_name="Twitter_data.json",mime="application/json",data=json_string,)

    with col3: #show
        y=st.button('Show Tweets',key=2)

if c:
    st.success("The Scraped Data is Downloaded as .CSV file:",icon="✅")
if j:
    st.success("The Scraped Data is Downloaded as .JSON file",icon="✅")
if x: # display
    st.success("The Scraped Data is:",icon="✅")
    st.write(tweets_df)
if y: # display
    st.balloons()
    st.success("Tweets Scraped Successfully:",icon="✅")
    st.write(tweets_df)





