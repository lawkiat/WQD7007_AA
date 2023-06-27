# Import libraries
import pandas as pd
from transformers import pipeline
import plotly.graph_objects as go

df = pd.read_csv("tweetscrap.csv")
sentiment_classifier = pipeline('sentiment-analysis')

# Passing tweets into sentiment pipeline and extracting the seniment score and label
df = (
    df
    .assign(sentiment = lambda x: x['Tweet'].apply(lambda s: sentiment_classifier(s)))
    .assign(
         label = lambda x: x['sentiment'].apply(lambda s: (s[0]['label'])),
         score = lambda x: x['sentiment'].apply(lambda s: (s[0]['score']))
    )
)


# Visualizing the sentiments
fig = go.Figure()

fig.add_trace(go.Bar(x = df["score"],
                    y = df["label"],
                orientation = "h")) #set orientation to horizontal because we want to flip the x and y-axis

fig.update_layout(plot_bgcolor = "white")              
                                #apply our custom category order

fig.show()