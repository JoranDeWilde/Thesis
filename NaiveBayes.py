import re

import pandas
from bs4 import BeautifulSoup
from nltk import RegexpTokenizer, SnowballStemmer
from sklearn import preprocessing, naive_bayes, metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score, RepeatedKFold
import numpy as np

df = pandas.read_excel('5500comments.xlsx')
df_id = df["id"]
df_text = df["text"]
df_sentiment = df["sentiment"]

# ---------------- NOISE REMOVAL ------------------
allezinnen=[]
for sentence in df_text:
    if not isinstance(sentence, str):
        print("")
    else:
        soup = BeautifulSoup(sentence,features="html.parser")
        for m in soup.find_all('a'):
            m.replaceWithChildren()
        w = re.sub(r'^https?:\/\/.*[\r\n]*', '', str(soup), flags=re.MULTILINE)
        w = re.sub(r'http\S+', '', w)

        # Automatisch uitfilteren van html zaken zoals <p>, <br>,...
        cleanr = re.compile('<.*?>')
        w = re.sub(cleanr, '', sentence.lower())

        tokenizer = RegexpTokenizer(r'\w+')
        w = w.replace("ste ", " ")
        w = w.replace("tje", " ")

        words = tokenizer.tokenize(w)

        stemmer = SnowballStemmer("dutch")
        gestemde_woorden = []
        for w in words:

            a = stemmer.stem(w)

            if a[len(a) - 1] == a[len(a) - 2]:
                a = a[:-1]

            gestemde_woorden.append(a)
        zin = " ".join(gestemde_woorden)
        allezinnen.append(zin)
df_text = allezinnen

# split the dataset into training and validation datasets


encoder = preprocessing.LabelEncoder()
sentiment = encoder.fit_transform(df_sentiment)
commentaren = df_text

# --------------- COUNT VECTORS AS FEATURES---------------

# create a count vectorizer object
count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
count_vect.fit(commentaren)
commentarenCount = count_vect.transform(commentaren)
# Naive Bayes on Count Vectors
classifier = naive_bayes.MultinomialNB()

scores = cross_val_score(classifier, commentarenCount, sentiment, cv=10)

print("Accuracy: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std()))




