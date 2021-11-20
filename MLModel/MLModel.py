import re
import pickle
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from sklearn import feature_extraction


class PredictionModel:
    def __init__(self):
        self.prediction_model = pickle.load(open('CachedData\\prediction_model.sav', 'rb'))
        self.tfidf_train_data = pickle.load(open('CachedData\\xtrain.sav', 'rb'))

        self.tfidf = feature_extraction.text.TfidfVectorizer(
            encoding='utf-8',
            ngram_range=(1, 1),
            max_features=5000,
            norm='l2',
            sublinear_tf=True
        )

    def clean_request_text(self, df, text_field, new_text_field_name):
        df[new_text_field_name] = df[text_field].str.lower()

        # Removing numbers
        df[new_text_field_name] = df[new_text_field_name].apply(
            lambda elem: re.sub(r"\d+", "", elem)
        )

        # Removing URLs
        df[new_text_field_name] = df[new_text_field_name].apply(
            lambda elem: re.sub(r"https?://\S+|www\.\S+", "", elem)
        )

        # Removing HTML tags
        df[new_text_field_name] = df[new_text_field_name].apply(
            lambda elem: re.sub(r"<.*?>", "", elem)
        )

        # Removing emojis
        df[new_text_field_name] = df[new_text_field_name].apply(
            lambda elem: re.sub(r"["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                "]+", "", elem)
        )
        return df

    def replace_request_stopwords(self, df):
        stop = stopwords.words('russian')

        df["CLEAN_TEXT"] = df["CLEAN_TEXT"].apply(
            lambda x: ' '.join([word for word in x.split() if word not in (stop)])
        )
        return df

    def tokenize_request_text(self, df):
        df["TEXT_TOKENS"] = df["CLEAN_TEXT"].apply(
            lambda x: word_tokenize(x)
        )
        return df

    def stem_request_text(self, df):
        def word_stemmer(text):
            stem_text = [SnowballStemmer('russian').stem(i) for i in text]
            return stem_text

        df["TEXT_CLEAN_TOKENS"] = df["TEXT_TOKENS"].apply(
            lambda x: word_stemmer(x)
        )
        return df

    def make_prediction(self, post_text):
        prediction_request = list([post_text])
        prediction_request = pd.DataFrame(columns=['POST_TEXT'], data=prediction_request)

        clean_prediction_request = self.clean_request_text(prediction_request, 'POST_TEXT', 'CLEAN_TEXT')
        clean_prediction_request = self.replace_request_stopwords(clean_prediction_request)
        clean_prediction_request = self.tokenize_request_text(clean_prediction_request)
        clean_prediction_request = self.stem_request_text(clean_prediction_request)

        self.tfidf.fit_transform(self.tfidf_train_data).toarray()
        prediction_features = self.tfidf.transform(clean_prediction_request["CLEAN_TEXT"]).toarray()

        return self.prediction_model.predict_proba(prediction_features)
