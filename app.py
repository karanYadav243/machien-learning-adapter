

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')
import seaborn as sns
import nltk
import re
import wordcloud
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
  

'''

project name : DS's Project
author : @kanishksh4rma

'''

df = pd.read_csv('damn.csv')


# cleaning the comments

def clntxt(text):
  text = re.sub(r'@[a-zA-Z0-9]+','',text) #Remove all @mentions
  text = re.sub(r'#','',text)             # Removing '#' symbols
  text = re.sub(r'https?\/\/\S+','',text) #Removing all the web links
  
  return text

df['comments'] = df['comments'].apply(clntxt)
df['comments'].head()

from textblob import TextBlob

#get the subjectivity
def subjectivity(txt):
  return TextBlob(txt).sentiment.subjectivity

#get the polarity
def polarity(txt):
  return TextBlob(txt).sentiment.polarity


df['subjectivity'] = df['comments'].apply(subjectivity)
df['polarity'] = df['comments'].apply(polarity)



#Visualize most used words

allwords = ' '.join(x for x in df['comments'])

wordclouD = wordcloud.WordCloud(width=500,height=300,random_state=21,max_font_size= 156).generate(allwords)

plt.imshow(wordclouD,interpolation='bilinear')
plt.axis('off')
plt.show()

#converting polarity to sentiment

def sentiment(polarity):
  if polarity<0:
    report = 'Negative'
  elif polarity == 0:
    report = 'Neutral'
  else:
    report = 'Positive'
  return report

df['Sentiment'] = df['polarity'].apply(sentiment)
df.head()

# print all the positive comments
j = 1
sorted_df = df.sort_values('polarity',ascending=False)
for i in range(0,sorted_df.shape[0]):
  if (sorted_df.iloc[i]['Sentiment'] == 'Positive'):
    #print(j,')',sorted_df.iloc[i]['comments'])  #UNCOMMENT IF WANNA PRINT THIS UP
    #print()
    j += 1

# print all the negative comments

j = 1
sorted_df = df.sort_values('polarity')
for i in range(0,sorted_df.shape[0]):
  if (sorted_df['Sentiment'][i] == 'Negative'):
    #print(j,')',sorted_df['comments'][i])  #SAME AS ABOVE
    #print()
    j += 1

# percentage f all the comments
pos_tweets = df[df['Sentiment']=='Positive']
pos_tweets = round(pos_tweets.shape[0] / df.shape[0] *100,1)

# percentage f all the comments
neg_tweets = df[df['Sentiment']=='Negative']
neg_tweets = round(neg_tweets.shape[0] / df.shape[0] *100,1)

print('Comment sentiments : ')
print('Positive comments : ',pos_tweets,'%')
print('Negative comments : ',neg_tweets,'%')

"""## Data Visualization"""

sns.scatterplot(x='polarity',y='subjectivity',data=df)
plt.savefig('pol-sub.png', dpi=300)
sns.countplot(df.Sentiment)
plt.savefig('sentiments.png', dpi=300)

print("Saving graphs...")


