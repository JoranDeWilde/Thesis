# Nieuwe zinnen klasse
# Hier kan een excel meegegeven worden met
# niet gelabelede data, waarna dit door het RB model gelabeled wordt
import pandas
from NoiseRemoval import noiseRemoval
from WordRater import RateTokenizedSentence as rate

class Comment(object):

    def __init__(self, id, text):
        self.id = id
        self.text = text


naam_excel='testzinnen.xlsx'

df = pandas.read_excel(naam_excel)
df_id = df["id"]
df_text = df["text"]

commentlijst = []
comments=[]

for x in range(df_id.size):
    c = Comment(df_id.get(x), df_text.get(x))
    commentlijst.append(c.text)
    comments.append(c)

vertalingsLijst = noiseRemoval(commentlijst)

labels=[]

for y in range(len(vertalingsLijst)):

   score2 = rate(vertalingsLijst[y])

   if score2 > 0:
        labels.append("Positief")

   elif score2 is 0:
       labels.append("Neutraal")

   else:
       labels.append("Negatief")

df['Sentiment']=labels

df.to_excel(naam_excel)
