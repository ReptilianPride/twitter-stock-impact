#importing required python packages
import asyncio
from twikit import Client, TooManyRequests
from datetime import datetime
import pandas as pd
import time
import random
import os
import argparse

#twitter scrapper options (input)
parser=argparse.ArgumentParser(description="Argument Parser")

parser.add_argument("-c", "--count", type=int, required=True, help="Tweet Count")
parser.add_argument("-q", "--query", type=str, required=True, help="Search Query")
parser.add_argument("-f", "--filename", type=str, required=True, help="Export File Name")

args=parser.parse_args()

#twitter scrapper options (can be turned into input statements)
TWEET_LIMITER=args.count
QUERY=args.query
FILENAME=args.filename


#twitter dummy user account
USERNAME='BabuJohJoh'
PASSWORD='Alistor0147896325'
EMAIL='anonymousisactive@gmail.com'
AUTH_TOKEN="74205533eb80dc20cdac36bb618ea0a59a3c8dfa"
CT_ZERO="86b1eefb0fb3e4a9f81b5dd2236ae4464ca981b60c4f6ea277555fbb72154fbdd08106b16867b1732dab400d4abf08770112621227055dbf1da95995b771199c07ec0115247606575f8e2e08a60e3520"


#additional required functions
#delay function
def randomWait():
    time.sleep(random.randint(1,7))

#handle rate limit related errors
def handleRateLimitReached(e):
    rate_limit_reset=datetime.fromtimestamp(e.rate_limit_reset)
    print(f"Rate limit reached! Waiting until {rate_limit_reset}")
    wait_time=rate_limit_reset-datetime.now()
    time.sleep(wait_time.total_seconds())

#grab the tweets
tweets=None
async def twitter_handler():
    global client,QUERY,tweets
    if(tweets is None):
        print('[!]Starting thread to scrape tweets.')
        tweets=await client.search_tweet(QUERY,'Top')
    else:
        randomWait()
        os.system('cls')
        print('[!]Grabbing more tweets!')
        await tweets.next()
    return tweets

#Activate Twitter Scrapper Client
client=Client('en-US')
client.set_cookies(
    {
        'auth_token':AUTH_TOKEN,
        'ct0':CT_ZERO
    }
)
async def main():
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD
    )

    #main
    tweet_count=0
    tweet_data=[]
    

    while(tweet_count<=TWEET_LIMITER):
        try:
            tweets=await twitter_handler()
        except TooManyRequests as e:
            handleRateLimitReached(e)
            continue

        if not tweets:
            print('[!]No more tweets to be found!')
            break

        for tweet in tweets:
            tweet_data.append([tweet.user.name,tweet.created_at,tweet.favorite_count,tweet.lang,tweet.view_count,tweet.reply_count,tweet.text])
            tweet_count+=1
            time.sleep(1)

        print(f'[!]Found {tweet_count} tweets!!!')

    print('[!]Converting to DataFrame')
    df_pre_defined_columns=['username','created_at','likes','language','views','reply_count','text']
    df=pd.DataFrame(tweet_data,columns=df_pre_defined_columns)


    print(f'[!]Writing to csv with filename {FILENAME}')
    df.to_csv(FILENAME,index=False)
    print('[!]Write Complete! EOP')
    
    

#start process for client
# loop_handle=asyncio.get_running_loop()
# if(loop_handle.is_running()):
#     asyncio.create_task(main())
# else:
asyncio.run(main())