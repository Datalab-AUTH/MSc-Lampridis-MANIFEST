import json
import re
import sys

import numpy as np
import tweepy

import config as cfg
from Twitter_API import TwitterAPI


def upgrade_to_work_with_single_class(SklearnPredictor):
    class UpgradedPredictor(SklearnPredictor):
        def __init__(self, *args, **kwargs):
            self._single_class_label = None
            super().__init__(*args, **kwargs)

        @staticmethod
        def _has_only_one_class(y):
            return len(np.unique(y)) == 1

        def _fitted_on_single_class(self):
            return self._single_class_label is not None

        def fit(self, X, y=None):
            if self._has_only_one_class(y):
                self._single_class_label = y[0]
            else:
                super().fit(X, y)
            return self

        def predict(self, X):
            if self._fitted_on_single_class():
                return np.full(X.shape[0], self._single_class_label)
            else:
                return super().predict(X)

    return UpgradedPredictor


# authorization tokens
consumer_key = cfg.consumer_key
consumer_secret = cfg.consumer_secret
access_key = cfg.access_key
access_secret = cfg.access_secret



def list2string(list):
    return ','.join(map(str, list))


def cleanPunc(sentence):
    cleaned = re.sub(r'[?|!|\'|"|#]', r'', sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]', r' ', cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n", " ")
    return cleaned


# function to clean relics of dataset
def clean_relics(text):
    text = re.sub(r"RT", "", text)
    text = re.sub(r"#USER#", "", text)
    text = re.sub(r"#HASHTAG#", "", text)
    text = re.sub(r"#URL#", "", text)
    return text


if __name__ == "__main__":
    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # set access to user's access key and access secret
    auth.set_access_token(access_key, access_secret)
    # calling the api
    api = tweepy.API(auth)

    twitter_api = TwitterAPI()

    with open('covid_filtered_replies_tweet_ids.json', 'r') as fp:
        data_tweet_ids = json.load(fp)

    # Remove tweets that have less than 10 replies
    for index, value in list(data_tweet_ids.items()):
        if len(value) < 10 or len(value) > 200:
            del data_tweet_ids[index]

    no_of_replies_list = list()
    for index, value in data_tweet_ids.items():
        no_of_replies_list.append(len(value))

    print(no_of_replies_list)
    print(sum(no_of_replies_list) / len(no_of_replies_list))
    print(len(data_tweet_ids))
    sys.exit()
    predicted_labels = list()
    true_labels = list()

    dictionary = {
        'results': []
    }

    for index, value in data_tweet_ids.items():

        tweet_id = index
        df = pd.DataFrame(columns=['user_id', 'text', 'tweet_text'])

        try:
            user_id, tweet_text = twitter_api.get_tweet_text(tweet_id)
        except TypeError:
            continue

        print(tweet_id)
        print(user_id)
        print(tweet_text)

        # catch exception when user id doesn't exist
        try:
            # fetching the statuses
            statuses = api.user_timeline(user_id=user_id, count=100)
        except TweepError:
            continue

        s = """"""
        # printing the statuses
        for status in statuses:
            s += status.text

        temp_df = pd.DataFrame({'user_id': user_id,
                                'text': s,
                                'tweet_text': tweet_text}, index=[0])

        df = df.append(temp_df, ignore_index=True)

        for tweet_id in value:

            try:
                user_id, tweet_text = twitter_api.get_tweet_text(tweet_id)
            except TypeError:
                continue

            # print(tweet_id)
            # print(user_id)
            # print(tweet_text)

            # catch exception when user id doesn't exist
            try:
                # fetching the statuses
                statuses = api.user_timeline(user_id=user_id, count=100)
            except TweepError:
                continue

            s = """"""
            for status in statuses:
                s += status.text

            temp_df = pd.DataFrame({'user_id': user_id,
                                    'text': s,
                                    'tweet_text': tweet_text}, index=[0])

            df = df.append(temp_df, ignore_index=True)
            df = df.drop_duplicates()

        data_readability = feature_extraction.get_readability_features(df)

        df['text'] = df.text.apply(clean_text)
        df['text'] = [list2string(list) for list in df['text']]

        data_tfidf = feature_extraction.get_tfidf_vectors_from_pickle(df[['user_id', 'text']])

        i = 0
        features = list()

        features.append([data_tfidf, data_readability])

        for feature_combination in features:
            features = pd.concat([i.set_index('user_id') for i in feature_combination], axis=1, join='outer')

            X = features

            # load gender classifier
            filename = 'XGBoost_final.sav'
            clf = pickle.load(open(filename, 'rb'))

            y = clf.predict(X)
            df['label'] = y

            final_df = (df[['tweet_text', 'label']])

            print(final_df)

            final_df['tweet_text'] = final_df.tweet_text.apply(clean_text)
            final_df['tweet_text'] = [list2string(list) for list in final_df['tweet_text']]

            instance_df = final_df.loc[[0]]
            final_df = final_df.iloc[1:]

            print(instance_df)
            print(final_df)

            vectorizer = TfidfVectorizer(stop_words='english', min_df=0.01, max_df=0.90,
                                         ngram_range=(1, 3))

            vectors = vectorizer.fit_transform(final_df['tweet_text'])

            # save sparse tfidf vectors to dataframe to use with other features
            vectors_pd = pd.DataFrame(vectors.toarray())

            X = vectors_pd
            y = final_df['label']

            print(X)
            print(y)

            # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

            if len(y.unique()) != 2:
                print("All labels in same class, assigning that to prediction...")
                true_label = instance_df['label'].loc[[0]].values[0]
                y_instance = final_df['label'].to_list()[0]
                print(y_instance)
                print(true_label)
                predicted_labels.append(y_instance)
                true_labels.append(true_label)
                continue

            clf = LogisticRegression()
            clf.fit(X, y)
            # y_pred = clf.predict(X_test)

            # print("Accuracy:", accuracy_score(y_test, y_pred))

            instance = instance_df['tweet_text'].loc[[0]].values[0]
            true_label = instance_df['label'].loc[[0]].values[0]

            instance = [instance]

            instance_vector = vectorizer.transform(instance)
            y_instance = clf.predict(instance_vector)[0]
            print(y_instance)
            print(true_label)

            predicted_labels.append(y_instance)
            true_labels.append(true_label)

            # final_df.to_csv('tweets_replies_labels.csv', mode='a', header=True)

    print(len(predicted_labels))
    print(predicted_labels)
    print(true_labels)

    print(accuracy_score(predicted_labels, true_labels))
