# MAIN klasse
# Hierin wordt een gelabeled excel document ingelezen waarna
# berekend wordt hoe goed het Rule Based model hierop scoort.
import pandas
from NoiseRemoval import noiseRemoval
from WordRater import RateTokenizedSentence as rate
import numpy as np
import time
import xlsxwriter
from langdetect import detect
import math


class Comment(object):

    def __init__(self, id, text, sentiment, training, lang):
        self.id = id
        self.text = text
        self.sentiment = sentiment
        self.training = training
        self.lang = lang


start = time.time()

# Excel stuff
df = pandas.read_excel('5500comments.xlsx')
df_id = df["id"]
df_text = df["text"]
df_sentiment = df["sentiment"]
df_training = df["training"]
df_lang = df["taal"]

# Lijsten om tekst bij te houden en de comment zelf
commentlijst = []
comments = []

# Analyse stuff
aantalComments = 0
aantalPos = 0
aantalNeg = 0
aantalNeu = 0

aantalPosVoorspeld = 0
aantalNegVoorspeld = 0
aantalNeuVoorspeld = 0

aantalFPPos = 0
aantalFPNeg = 0
aantalFPNeu = 0

aantalFNPos = 0
aantalFNNeg = 0
aantalFNNeu = 0

aantalPosJuist = 0
aantalNegJuist = 0
aantalNeuJuist = 0

aantalPosNegVoorspeld = 0
aantalNegPosVoorspeld = 0

for x in range(df_id.size):
    c = Comment(df_id.get(x), df_text.get(x), df_sentiment.get(x), df_training.get(x), df_lang.get(x))
    commentlijst.append(c.text)
    comments.append(c)

vertalingsLijst = noiseRemoval(commentlijst)

for y in range(len(vertalingsLijst)):

    # print(vertalingsLijst[y])

    # score = RateTokenizedSentence(vertalingsLijst[y])
    score = rate(vertalingsLijst[y])

    '''
    if comments[y].training == "T" and np.sign(comments[y].sentiment) != np.sign(score):
        print('Analyse van zin: ', end=" ")
        print(vertalingsLijst[y])
        print(comments[y].text)
        print('Mijn score: ' + str(comments[y].sentiment) + '\nScore van programma: ' + str(score), end="\n\n\n")
    
    # print('Score van programma: ', end=" ")

    # print(score)
    # print('Score van mij: ', end=" ")
    # print(comments[y].sentiment)
    '''
    # Analyse

    if comments[y].training == "TE":

        aantalComments += 1

        if score > 0:
            aantalPosVoorspeld += 1
            if comments[y].sentiment > 0:
                aantalPos += 1
                aantalPosJuist += 1
            if comments[y].sentiment == 0:
                aantalNeu += 1
                aantalFPPos += 1
                aantalFNNeu += 1
            if comments[y].sentiment < 0:
                aantalNeg += 1
                aantalFPPos += 1
                aantalFNNeg += 1
                aantalNegPosVoorspeld += 1

        if score == 0:
            aantalNeuVoorspeld += 1
            if comments[y].sentiment > 0:
                aantalPos += 1
                aantalFNPos += 1
                aantalFPNeu += 1
            if comments[y].sentiment == 0:
                aantalNeu += 1
                aantalNeuJuist += 1
            if comments[y].sentiment < 0:
                aantalNeg += 1
                aantalFPNeu += 1
                aantalFNNeg += 1

        if score < 0:
            aantalNegVoorspeld += 1
            if comments[y].sentiment > 0:
                aantalPos += 1
                aantalFNPos += 1
                aantalFPNeg += 1
                aantalPosNegVoorspeld += 1
            if comments[y].sentiment == 0:
                aantalNeu += 1
                aantalFNNeu += 1
                aantalFPNeg += 1
            if comments[y].sentiment < 0:
                aantalNeg += 1
                aantalNegJuist += 1

print('EINDRESULTAAT:')
print('Totaal aantal comments: ' + str(aantalComments))

if aantalNegPosVoorspeld is not 0:
    print('Pos. reviews:  #Pos reviews = ' + str(aantalPos) + "    aantal positieve voorspeld: " + str(
        aantalPosVoorspeld) + "    aantal daarvan juist: " + str(aantalPosJuist) + "   #FP = " + str(
        aantalFPPos) + "   #FN = " + str(aantalFNPos) + " percentage juist: " + str(
        100 * aantalPosJuist / aantalPosVoorspeld) + "%")
else:
    print('Pos. reviews:  #Pos reviews = ' + str(aantalPos) + "    aantal positieve voorspeld: " + str(
        aantalPosVoorspeld) + "    aantal daarvan juist: " + str(aantalPosJuist) + "   #FP = " + str(
        aantalFPPos) + "   #FN = " + str(aantalFNPos) + " percentage juist: " + str(0) + "%")
if aantalNeuVoorspeld is not 0:
    print('Neu. reviews:  #Neu reviews = ' + str(aantalNeu) + "    aantal neutrale voorspeld: " + str(
        aantalNeuVoorspeld) + "    aantal daarvan juist: " + str(aantalNeuJuist) + "   #FP = " + str(
        aantalFPNeu) + "   #FN = " + str(aantalFNNeu) + " percentage juist: " + str(
        100 * aantalNeuJuist / aantalNeuVoorspeld) + "%")
else:
    print('Neu. reviews:  #Neu reviews = ' + str(aantalNeu) + "    aantal neutrale voorspeld: " + str(
        aantalNeuVoorspeld) + "    aantal daarvan juist: " + str(aantalNeuJuist) + "   #FP = " + str(
        aantalFPNeu) + "   #FN = " + str(aantalFNNeu) + " percentage juist: " + str(0) + "%")

if aantalNegVoorspeld is not 0:
    print('Neg. reviews:  #Neg reviews = ' + str(aantalNeg) + "    aantal negatieve voorspeld: " + str(
        aantalNegVoorspeld) + "    aantal daarvan juist: " + str(aantalNegJuist) + "   #FP = " + str(
        aantalFPNeg) + "   #FN = " + str(aantalFNNeg) + " percentage juist: " + str(
        100 * aantalNegJuist / aantalNegVoorspeld) + "%")
else:
    print('Neg. reviews:  #Neg reviews = ' + str(aantalNeg) + "    aantal negatieve voorspeld: " + str(
        aantalNegVoorspeld) + "    aantal daarvan juist: " + str(aantalNegJuist) + "   #FP = " + str(
        aantalFPNeg) + "   #FN = " + str(aantalFNNeg) + " percentage juist: " + str(0) + "%")

print(str((aantalNegJuist + aantalPosJuist + aantalNeuJuist) / aantalComments))
print('aantal positieve comments voorspeld als negatief: ' + str(aantalPosNegVoorspeld))
print('aantal negatieve comments voorspeld als positief: ' + str(aantalNegPosVoorspeld))

done = time.time()

elapsed = done - start
print(elapsed);
