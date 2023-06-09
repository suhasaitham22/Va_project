import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sentiment Analysis of Tweets about US Airlines",
                   page_icon=":airplane:", layout="wide")

st.title("Sentiment Analysis of Tweets about US Airlines")

data = pd.read_csv('Tweets.csv')
data['tweet_created'] = pd.to_datetime(data['tweet_created'])

if st.checkbox('Display Top 5 rows of the data'):
    st.write(data.head())

st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.sidebar.markdown("This application is a Streamlit app used to analyze the sentiment of tweets 🐦 about US airlines ✈️")

st.sidebar.subheader("Show random tweet")

random_tweet = st.sidebar.radio('Sentiment type', ('positive', 'negative', 'neutral'))

st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of tweets by sentiment type")

select = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie Chart'], key='1')

sentiment_count = data['airline_sentiment'].value_counts()

sentiment_count = pd.DataFrame({'Sentiment' :sentiment_count.index, 'Tweets' :sentiment_count.values})

if not st.sidebar.checkbox('Hide', True):
    st.markdown("### Number of tweets by Sentiment")

    if select == "Histogram":
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader("When and where are the users tweeting from?")

hour = st.sidebar.slider("Hour of day", 0, 23)

modified_data = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Close", True, key='1'):
    st.markdown("### Tweets location based on the time of the day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Breakdown airline tweets by sentiment")

choice = st.sidebar.multiselect("Pick airlines", ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key='0')

if len(choice) > 0:
    airline_names = ", ".join(choice)
    choice_data = data[data.airline.isin(choice)]
    fig_0 = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment', facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width=800)
    fig_0.update_layout(title=f"Number of tweets by sentiment for {airline_names}")
    st.plotly_chart(fig_0)

st.sidebar.header("Word Cloud")

word_sentiment = st.sidebar.radio('Display word cloud for which sentiment?', ('positive', 'negative', 'neutral'))

if not st.sidebar.checkbox("Close", True, key='3'):
    st.header('Word cloud for %s sentiment' % (word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    stopwords = set(STOPWORDS)
    stopwords.update(["flight", "flights", "usairways", "americanair", "united", "southwest", "delta", "jetblue", "virginamerica"])

    wc = WordCloud(stopwords=stopwords, background_color="white", max_words=2000, width=800, height=600)
    wc.generate(words)

    fig, ax = plt.subplots()
    ax.imshow(wc)
    ax.set_axis_off()

    st.pyplot(fig)

st.sidebar.markdown("### About")

st.sidebar.info(
    """
    This app performs sentiment analysis on tweets about US airlines and visualizes the results.
    """
)

st.sidebar.markdown("### Credits")

st.sidebar.info(
    """
    - Built by Suhas Aitham
    - Data source: [Crowdflower](https://www.figure-eight.com/data-for-everyone/)
    - Word cloud visualization powered by [WordCloud](https://github.com/amueller/word_cloud)
    """
)
