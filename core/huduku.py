import os
import pickle

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from core.sanitizer import Sanitizer
from core.util import fetch_author


class Huduku:
    """
     Keywords Search using TFID
    """

    def __init__(self,):
        df = pd.read_json("data/data.json",)
        self.data = df["summaries"].apply(pd.Series)
        self.vocabulary()

    def load_tfidf_model(self):
        """Check if trained tfidf model exists else train."""
        if os.path.exists("data/tfidf.pkl"):
            return pickle.load(open("data/tfidf.pkl", "rb"))
        else:
            return self.train()

    def load_vocabulary(self):
        vocabulary = set()
        sanitized_summary = Sanitizer(self.data, "summary").sanitize()
        for words in sanitized_summary["clean_summary"]:
            vocabulary.update(words.split(","))
        with open("data/vocabulary.txt", "w") as f:
            f.write(str(list(vocabulary)))
        return list(vocabulary)

    def train(self):
        # Intializating the tfIdf model
        sanitized_summary = Sanitizer(self.data, "summary").sanitize()
        tfidf_vectorizer = TfidfVectorizer(vocabulary=self.vocabulary())
        train_vector = tfidf_vectorizer.fit_transform(sanitized_summary.clean_summary)
        pickle.dump(train_vector, open("data/tfidf.pkl", "wb"))
        return train_vector

    def vocabulary(self):
        if os.path.exists("data/vocabulary.txt"):
            with open("data/vocabulary.txt", "r") as file:
                return eval(file.readline())
        else:
            self.load_vocabulary()

    def gen_vector_T(self, tokens, tfidf):
        Q = np.zeros((len(self.vocabulary())))
        x = tfidf.transform(tokens)
        for token in tokens[0].split(","):
            try:
                ind = self.vocabulary().index(token)
                Q[ind] = x[0, tfidf.vocabulary_[token]]
            except Exception as e:
                print(e)
        return Q

    def cosine_sim(self, a, b):
        cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        return cos_sim

    def compute_similarity(self, trained_data, q_df, k, author=False, query=None):
        d_cosines = []
        tfidf = TfidfVectorizer(vocabulary=self.vocabulary(), dtype=np.float32)
        tfidf.fit(q_df)
        query_vector = self.gen_vector_T(q_df, tfidf)
        for d in trained_data:
            d_cosines.append(self.cosine_sim(query_vector, d))

        out = np.array(d_cosines).argsort()[-k:][::-1]
        d_cosines.sort()
        a = pd.DataFrame()
        for i, index in enumerate(out):
            a.loc[i, "id"] = str(index)
            a.loc[i, "summary"] = self.data["summary"][index]
            if query:
                a.loc[i, "query"] = query
            if author:
                a.loc[i, "author"] = fetch_author(index)
        for j, simScore in enumerate(d_cosines[-k:][::-1]):
            a.loc[j, "Score"] = simScore
        a.set_index("id")
        a = a[a.Score != 0]
        return a.drop(["Score",], axis=1).to_dict("records")

    def search(self, k, query):
        tfidf_model = self.load_tfidf_model()
        trained_data = tfidf_model.A
        q_df = pd.DataFrame([{"query": query}])
        q_df = Sanitizer(q_df, "query").sanitize()
        return self.compute_similarity(trained_data, q_df["clean_query"], k)

    def bulk_search(self, k, query_list):
        tfidf_model = self.load_tfidf_model()
        trained_data = tfidf_model.A
        results = []
        for query in query_list:
            q_df = pd.DataFrame([{"query": query}])
            q_df = Sanitizer(q_df, "query").sanitize()
            results.append(
                self.compute_similarity(
                    trained_data, q_df["clean_query"], k, True, query
                )
            )
        return results
