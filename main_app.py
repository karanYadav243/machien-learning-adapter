from flask import *
import flask
# from chat import chat
from flask_cors import CORS, cross_origin
app = Flask(__name__,static_folder="myCSS") #,template_folder="/content/COVID-Brain-Tumour-Project/project folder")

#app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


print("* Initializing the process ...")

import matplotlib.pyplot as plt
plt.style.use('seaborn')
import seaborn as sns
import nltk
import re
import wordcloud
import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
import numpy as np
import sys
import requests
import argparse
import logging
print("* Initializing the process ...")
# create an Empty DataFrame object
df = pd.DataFrame(columns=["comments"])

def main_app(df):

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

	# plt.imshow(wordclouD,interpolation='bilinear')
	# plt.axis('off')
	# plt.show()

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
	plt.savefig('templates/pol-sub.png', dpi=300)
	sns.countplot(df.Sentiment)
	plt.savefig('templates/sentiments.png', dpi=300)

	print("Saving graphs...")
	return (pos_tweets,neg_tweets)



@app.route("/fetch.html", methods=['GET', 'POST'])
def fetch_comments():
	if request.method=="POST":
		youtubeLink = request.form["search"]
		youtubeLink = str(youtubeLink)
		APIKEY = "AIzaSyDCLsWdeD106RhRHyIcA3hEf-1jhmHbnuQ"
	    #logging.basicConfig(filename="ycd.log", filemode='w', format='%(asctime)s | %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

		print("Welcome!")
		print("You can limit number of comments by using flag -l LIMIT (default: 100)")
		print("You can choose an order type by using flag -r ORDER (available: relevance, time) (default: relevance")
		print("You can choose an output file type by using flag -o OUTPUT (default: txt)")
		print("If you want to exit the script type 'e' or 'exit'")


		print("Youtube link loaded: %s", youtubeLink)

		if(youtubeLink=="e" or youtubeLink=="exit"):
			quit()

		if youtubeLink.find("v="):
			youtubeLink = youtubeLink.split("v=")[1].split("&")[0]
			print(youtubeLink)
		else:
			youtubeLink = youtubeLink.split("/")[3]
			print(youtubeLink)

		try:
			logging.info("Sending a request to API with options: youtubeID: %s .", youtubeLink)
			r = requests.get(url = "https://www.googleapis.com/youtube/v3/commentThreads?key=" + APIKEY + "&textFormat=plainText&part=snippet&videoId="+youtubeLink+"&order=relevance"+"&maxResults="+str(100)).json()

			print("Dumping...")

			for f in r["items"]:
				# print("here.")
	            # author = f["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
				comment = f["snippet"]["topLevelComment"]["snippet"]["textOriginal"]

				df.loc[len(df)] = comment
				#df.loc[len(df)] = comment+"\n"

			# logging.info("Successfully dumped to output.%s!", fileType)
	        #print("Successfully dumped to output." + fileType + "!")
	        #df.to_csv("damn.csv")
			#print(df.head(5))
			pos,neg=main_app(df)

			return render_template('/fetch.html',pos=pos,neg=neg)

		except Exception as e:
			logging.error("Error has occurred: %s, Request body: %s", e, e)
			print("Error has occurred: " + str(e) + ". Check ycd.log for additional info.")
	else:
		return render_template('/fetch.html',pos=0,neg=0)


print("* Done ...")
@app.route("/", methods=['GET'])
def indexxx():
	return render_template('/index.html')

@app.route("/show_rank.html", methods=['GET', 'POST'])
def rest_aapi():
	if request.method=="POST":
		userText = request.form["search"]
		userText = str(userText)
		userText = userText.lower()
		result = df.loc[userText]
		integer_list,avg=fetch_details(result)
		_,avg_4=fetch_details(df4.loc[userText])
		print(userText[6:9])
		course,colg="",""
		if userText[6:9]=="020":
			course="BCA"
		if userText[3:6]=="177":
			colg="VIPS"

		return render_template('/show_rank.html',Namee=result.Name,Markss=integer_list,avgg=avg,batch=userText[-4:],colg=colg,course=course,avgg_4=avg_4)
	else:
		return render_template('/show_rank.html',Namee=0,Markss=0,avgg=0)


@app.route("/api/<string:userText>")
def rest_api(userText):
	response = ''
	userText = str(userText)
	userText = userText.lower()
	result = df.loc[userText]

	integer_list,avg=fetch_details(result)

	result = {
	"Name":result.Name,
	"Marks":integer_list,
	"Average":avg,
	"API":"running"
	}
	return jsonify(result)




if __name__ == "__main__":

     app.run()
