import pandas as pd
from collections import defaultdict

from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class Sanitizer:
    """
        Data Preparation before training model to find similar documents
        Step1 - Clean the Data(Remove punctuations, new lines, and white spaces)
        Step2 - Preprocess Data(Remove new lines and extra white spaces)
    """

    def __init__(self, data, label):
        self.data = pd.DataFrame(data)
        self.label = label
        self.clean_label = "clean_" + label

    def sanitize(self):
        self.clean()
        self.preprocess()
        return self.data

    def clean(self):
        self.data[self.clean_label] = self.data[self.label].replace(
            to_replace="The Book in Three Sentences:", value=" ", regex=True
        )  # remove common sentence
        self.data[self.clean_label] = self.data[self.clean_label].replace(
            to_replace="[!\"#$%&'()*+,/:;<=>?@[\\]^_`{|}~]", value=" ", regex=True
        )  # remove punctuation except
        self.data[self.clean_label] = self.data[self.clean_label].replace(
            to_replace="-", value=" ", regex=True
        )
        self.data[self.clean_label] = self.data[self.clean_label].replace(
            to_replace="\s+", value=" ", regex=True
        )  # remove new line
        self.data[self.clean_label] = self.data[self.clean_label].replace(
            to_replace="  ", value="", regex=True
        )  # remove white space
        self.data[self.clean_label] = self.data[self.clean_label].apply(
            lambda x: x.strip()
        )  # Ltrim and Rtrim of whitespace

    def preprocess(self):
        self.data[self.clean_label] = [
            data.lower() for data in self.data[self.clean_label]
        ]
        self.data[self.clean_label] = [
            word_tokenize(data) for data in self.data[self.clean_label]
        ]
        self.data[self.clean_label] = self.__lemmatize(self.data[self.clean_label])

    def __lemmatize(self, data):
        tag_map = defaultdict(lambda: wn.NOUN)
        tag_map["J"] = wn.ADJ
        tag_map["V"] = wn.VERB
        tag_map["R"] = wn.ADV
        file_clean_k = pd.DataFrame()
        for index, entry in enumerate(data):
            final_words = []
            word_lemmatized = WordNetLemmatizer()
            for word, tag in pos_tag(entry):
                # Below condition is to check for Stop words and consider only alphabets
                if (
                    len(word) > 1
                    and word not in stopwords.words("english")
                    and word.isalpha()
                ):
                    word_final = word_lemmatized.lemmatize(word, tag_map[tag[0]])
                    final_words.append(word_final)
                    # The final processed set of words for each iteration will be stored in 'text_final'
                    file_clean_k.loc[index, "keyword_final"] = str(final_words)
                    file_clean_k.loc[index, "keyword_final"] = str(final_words)
                    file_clean_k = file_clean_k.replace(
                        to_replace="\[.", value="", regex=True
                    )
                    file_clean_k = file_clean_k.replace(
                        to_replace="'", value="", regex=True
                    )
                    file_clean_k = file_clean_k.replace(
                        to_replace=" ", value="", regex=True
                    )
                    file_clean_k = file_clean_k.replace(
                        to_replace="\]", value="", regex=True
                    )
        return file_clean_k
