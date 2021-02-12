import pickle
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

warnings.filterwarnings('ignore')


def main():
    df = pd.read_csv("final_complete_features_with_labels_and_ids", sep=",", encoding="utf8")

    data_tfidf = df[['user_id', 'tf_idf']]
    data_readability = df[
        ['user_id', 'avg_word_count', 'emoji_count', 'slang_count', 'capitalized_count', 'full_capitalized_count',
         'retweets_count', 'user_mentions_count', 'hashtags_count', 'url_count']]
    data_sentiment = df[
        ['user_id', 'anger', 'fear', 'joy', 'sadness', 'negation', 'vader_compound_score', 'textblob_polarity_score']]
    data_personality = df[['user_id', 'E', 'AVOIDANCE', 'C', 'O', 'N', 'A', 'ANXIETY']]
    data_gender = df[['user_id', 'gender']]
    data_liwc = df.drop(
        ['tf_idf', 'avg_word_count', 'emoji_count', 'slang_count', 'capitalized_count', 'full_capitalized_count',
         'retweets_count', 'user_mentions_count', 'hashtags_count', 'url_count', 'anger', 'fear', 'joy', 'sadness',
         'negation', 'vader_compound_score', 'textblob_polarity_score', 'E', 'AVOIDANCE', 'C', 'O', 'N', 'A', 'ANXIETY',
         'gender', 'ground_truth'], axis=1)
    data_ground_truth = df[['user_id', 'ground_truth']]

    print(data_sentiment['anger'].sort_values(ascending=False, kind='quicksort'))
    print(data_sentiment['fear'].sort_values(ascending=False, kind='quicksort'))
    print(data_sentiment['joy'].sort_values(ascending=False, kind='quicksort'))
    print(data_sentiment['sadness'].sort_values(ascending=False, kind='quicksort'))

    i = 0
    feature_names = [
        # "tfidf",
        # "tfidf_readability",
        # "tfidf_readability_sentiment",
        "tfidf_readability_sentiment_personality_gender",
        # "tfidf_readability_sentiment_liwc_personality_gender",
        # "tfidf_readability_sentiment",
        # "tfidf_readability_sentiment_personality",
        # "tfidf_readability_sentiment_gender",
        # "readability_sentiment_personality_gender",
        # "readability_sentiment_personality",
        # "readability_sentiment_gender"
    ]

    features = list()
    # features.append([data_tfidf])
    # features.append([data_tfidf, data_readability, data_ground_truth])
    # features.append([data_tfidf, data_readability, data_sentiment, data_ground_truth])
    features.append([data_tfidf, data_readability, data_sentiment, data_personality, data_gender, data_ground_truth])
    # features.append(
    #    [data_tfidf, data_readability, data_sentiment, data_liwc, data_personality, data_gender, data_ground_truth])
    # features.append([data_tfidf, data_readability, data_sentiment, data_ground_truth])
    # features.append([data_tfidf, data_readability, data_sentiment, data_personality, data_ground_truth])
    # features.append([data_tfidf, data_readability, data_sentiment, data_gender, data_ground_truth])
    # features.append([data_readability, data_sentiment, data_personality, data_gender, data_ground_truth])
    # features.append([data_readability, data_sentiment, data_personality, data_ground_truth])
    # features.append([data_readability, data_sentiment, data_gender, data_ground_truth])

    for feature_combination in features:
        print("feature_combination: " + str(feature_names[i]))

        features = pd.concat([i.set_index('user_id') for i in feature_combination], axis=1, join='outer')

        print(features)
        features.to_csv('features_with_labels_and_ids')

        X = features.drop(['ground_truth'], axis=1).reset_index(drop=True)
        y = features[['ground_truth']].values.ravel()
        print(X)
        print(y)
        print(X.shape)
        print(y.shape)
        # train-test split
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # try many classifiers to find the best performing
        names = [
            "Nearest Neighbors",
            "SVM",
            "Decision Tree",
            "Random Forest",
            "AdaBoost",
            # "Multinomial Naive Bayes",
            # "Logistic Regression",
            "Gradient Boosting",
            "XGBoost"
        ]

        classifiers = [
            KNeighborsClassifier(),
            SGDClassifier(),
            DecisionTreeClassifier(),
            RandomForestClassifier(),
            AdaBoostClassifier(),
            # MultinomialNB(),
            # LogisticRegression(),
            GradientBoostingClassifier(),
            XGBClassifier(objective="binary:logistic", random_state=42)
        ]

        best_clf = None
        best_classifier = ""
        best_accuracy = 0

        for clf, name in zip(classifiers, names):
            print("Classifier:", name)

            accuracy = cross_val_score(clf, X, y, scoring='accuracy', cv=10)
            print('Accuracy', np.mean(accuracy))
            recall = cross_val_score(clf, X, y, scoring='recall', cv=10)
            print('Recall', np.mean(recall))
            precision = cross_val_score(clf, X, y, cv=10, scoring='precision')
            print('Precision', np.mean(precision))
            f1 = cross_val_score(clf, X, y, cv=10, scoring='f1')
            print('F1', np.mean(f1))
            cv_accuracy = np.mean(accuracy)

            if best_accuracy <= cv_accuracy:
                clf.fit(X, y)
                best_clf = clf
                best_classifier = name
                best_accuracy = cv_accuracy

        print("Best classifier: ", best_classifier)
        print("Best accuracy: \n", best_accuracy)

        # save the model to disk
        filename = 'classifiers/fake_news/' + str(best_classifier) + '_' + str(feature_names[i]) + '_' + str(
            best_accuracy) + '.sav'
        pickle.dump(best_clf, open(filename, 'wb'))
        i += 1


if __name__ == "__main__":
    main()
