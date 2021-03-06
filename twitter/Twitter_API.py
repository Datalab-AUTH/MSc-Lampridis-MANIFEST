import logging
import time
from json import JSONDecodeError

import requests

import config as cfg


class TwitterAPI:
    """
    Class that connects to a Twitter developer account and fetches data via the API
    """
    api = None
    auth = None

    def __init__(self):
        self.token = cfg.bearer_token
        self.prefix = 'Bearer'

    def get_tweet_text(self, tweet_id):
        headers = {"Authorization": '%s %s' % (self.prefix, self.token)}

        # By default, the endpoint only returns id and text
        params = 'expansions=author_id'

        retries = 1
        success = False
        while not success:
            try:
                response = requests.get("https://api.twitter.com/2/tweets/" + str(tweet_id),
                                        params=params, headers=headers)
                print(response)

                if response.status_code == 429:
                    wait = 60
                    print('Too many requests! Waiting %s secs and re-trying...' % wait)
                    time.sleep(wait)
                    continue

                success = True
                try:
                    print(response.json())
                    author_id = response.json()['data']['author_id']
                    text = response.json()['data']['text']
                    return author_id, text
                except KeyError:
                    logging.info("Tweet doesn't exist anymore")
                    return None
                except JSONDecodeError:
                    logging.info("json decode error")
                    return None
                except:
                    return None

            except Exception as e:
                wait = retries * 30
                print('Error! Waiting %s secs and re-trying...' % wait)
                time.sleep(wait)
                retries += 1


if __name__ == "__main__":
    twitter_api = TwitterAPI()
