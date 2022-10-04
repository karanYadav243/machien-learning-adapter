import pandas as pd
  
# create an Empty DataFrame object
df = pd.DataFrame(columns=["comments"])
import sys
import requests
import argparse
import logging

def main(argv):

    APIKEY = "AIzaSyDCLsWdeD106RhRHyIcA3hEf-1jhmHbnuQ"

    parser = argparse.ArgumentParser(add_help=False, description=('Youtube Comment Downloader made by Kazu'))
    parser.add_argument('--help', '-h', action='help', help='Show help message')
    parser.add_argument('--limit', '-l', type=int, default=100, help='Limit number of comments (default: 100)')
    parser.add_argument('--output', '-o', default="txt", help='Choose output file type (default: txt)')
    parser.add_argument('--order', '-r', default="relevance", help='Choose ordering type (available: relevance, time) (default: relevance)')
    args = parser.parse_args(argv)

    limit = args.limit
    fileType = args.output
    order = args.order

    logging.basicConfig(filename="ycd.log", filemode='w', format='%(asctime)s | %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
        
    print("Welcome!")
    print("You can limit number of comments by using flag -l LIMIT (default: 100)")
    print("You can choose an order type by using flag -r ORDER (available: relevance, time) (default: relevance")
    print("You can choose an output file type by using flag -o OUTPUT (default: txt)")
    print("If you want to exit the script type 'e' or 'exit'")
    youtubeLink = input("Insert a youtube video link: ")

    logging.info("Youtube link loaded: %s", youtubeLink)

    if(youtubeLink=="e" or youtubeLink=="exit"):
        quit()

    if youtubeLink.find("v="):
        youtubeLink = youtubeLink.split("v=")[1].split("&")[0]
        print(youtubeLink)
    else:
        youtubeLink = youtubeLink.split("/")[3]
        print(youtubeLink)

    try:
        logging.info("Sending a request to API with options: youtubeID: %s, order: %s, limit: %s.", youtubeLink, order, str(limit))
        r = requests.get(url = "https://www.googleapis.com/youtube/v3/commentThreads?key=" + APIKEY + "&textFormat=plainText&part=snippet&videoId="+youtubeLink+"&order="+order+"&maxResults="+str(limit)).json()
        with open('output.' + fileType, 'w', encoding="utf-8") as outFile:
            print("Dumping...")
            for f in r["items"]:
                # author = f["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                comment = f["snippet"]["topLevelComment"]["snippet"]["textOriginal"]

                df.loc[len(df)] = comment+"\n"
                outFile.write(comment + "\n")
        logging.info("Successfully dumped to output.%s!", fileType)
        print("Successfully dumped to output." + fileType + "!")
        df.to_csv("damn.csv")
    except Exception as e:
        logging.error("Error has occurred: %s, Request body: %s", e, r)
        print("Error has occurred: " + str(e) + ". Check ycd.log for additional info.")

if __name__ == "__main__":
    main(sys.argv[1:])
