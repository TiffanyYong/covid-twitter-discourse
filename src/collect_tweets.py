import os
import tweepy as tw
import pandas as pd
import random
import datetime
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bearer')
    args = parser.parse_args()
    
    bearer_token = args.bearer

    random.seed(100)

    client = tw.Client(bearer_token=bearer_token)

    query = '(COVID OR vaccination OR vaccinated OR vaccines OR vaccine OR vax OR Moderna OR Pfizer OR AstraZeneca OR Janssen OR "Johnson & Johnson" OR "J&J" "Johnson and Johnson" OR sars-cov-2 OR coronavirus OR #covid OR #covid-19 OR #vaccination) -is:retweet lang:en'

    initial = '2021-11-30T00:00:00Z'
    initial_datetime = datetime.datetime.strptime(initial, '%Y-%m-%dT%H:%M:%SZ')

    df = pd.DataFrame(columns=('id', 'date', 'content', 'topic', 'sentiment'))

    start_times = random.sample(range(259200), 130)

    for second in start_times:
        terminate_datetime = initial_datetime + datetime.timedelta(seconds=second)
        terminate_datestring = terminate_datetime.isoformat('T') + 'Z'
        
        new_datetime = terminate_datetime - datetime.timedelta(seconds=10)
        new_datestring = new_datetime.isoformat('T') + 'Z'

        for tweet in tw.Paginator(client.search_recent_tweets, query=query, start_time=new_datestring, 
                                    end_time=terminate_datestring, tweet_fields='text,created_at', max_results=10, limit=1).flatten():
    
            df.loc[len(df)] = {'id': tweet.id, 'date': tweet.created_at, 'content': tweet.text}
            pass

    df.to_csv('raw_data.csv', sep=',', index=False)

if __name__ == '__main__':
    main()