from WordSentiment import WordSentiment
from nltk.stem.snowball import SnowballStemmer
import kpss_py3 as stemmerKp

spreuken = {
    'niet te doen': [],
    'de moeite': [],
    'klopt niet': [],
    '5 sterren waard': []
}

synonyms = {

    'goed': ['goed', 'nice', 'betrouwbaar', 'bruikbaar', 'degelijk', 'tevredenstellend', 'juist', 'correct', 'prima',
              'interessant', 'top', 'plezant', 'tof',],
    'slecht': ['slecht', 'gebrekkig', 'inferieur', 'onvoldoende', 'onplezierig', 'zwak', 'dom', 'stom'],
    'schitterend': ['schitterend', 'blinkend', 'briljant', 'glansrijk', 'stralend', 'grandioos', 'magnifiek', 'subliem',
                    'oogverblindend', 'fascinerend'],
    'fantastisch': ['fantastisch', 'buitengewoon', 'ongelooflijk', 'prachtig', 'toverachtig', 'geweldig'],
    'saai': ['saai', 'doods', 'doorsnee', 'duf', 'eentonig', 'oninteressant', 'slaapverwekkend', 'vervelend'],
    'genot': ['genot', 'heerlijkheid', 'plezier', 'vreugde', 'wellust', 'leuk'],
    'perfect': ['perfect', 'ideaal', 'uitmuntend', 'uitstekend', 'best', 'excellent'],
    'privé': ['privé', 'privéterrein', 'Privédomein', 'privÃ©', 'verboden','privã'],
    'spectaculair': ['spectaculair', 'adembenemend', 'sensationeel', 'opzienbarend', 'fenomenaal'],
    'dank': ['danku', 'dankje', 'bedankt', 'dank', 'merci', 'thanks'],
    'helaas': ['helaas', 'jammer', 'ongelukkigerwijs'],
    'onmogelijk': ['onmogelijk', 'ondoenbaar', 'onberijdbaar'],
    'geschikt': ['geschikt', 'adequaat', 'gelegen', 'passend'],
    'afwijken': ['afwijken', 'verschillen'],
    'toegankelijk': ['toegankelijk', 'bereikbaar', 'openbaar'],
    'kut': ['kut', 'shit', 'klote', 'verdomme'],
    'fijn': ['fijn', 'aangenaam', 'behaaglijk', 'gezellig'],
    'teleurstelling': ['teleurstelling', 'afknapper', 'anticlimax', 'domper', 'flop', 'ontgoocheling', 'tegenvaller',
                       'teleurstellende', 'tijdsverspilling', 'weghalen'],
    'herbekijken': ['herbekijken', 'aanpassen', 'herevalueren', 'herbekeken'],
    'ramp': ['ramp', 'drama', 'tragedie', 'schande'],
    'vervanging': ['vervanging', 'vergoeding', 'vernieuwing'],
    'mooi': ['mooi', 'bevallig', 'fraai', 'knap', 'schoon', 'aantrekkelijk', 'aardig','fietspad','rustig'],
    'aanrader': ['aanrader'],
    'snelweg': ['snelweg'],
    'verdwijn': ['verdwijn'],
    'afrader': ['afrader'],
    'parel': ['parel'],
    'onverhard': ['onverhard'],
    'verhard': ['verhard'],
    'merkwaardig': ['merkwaardig', 'bijzonder', 'curieus', 'notabel', 'wonderlijk'],
    'doodlopen': ['doodlopen'],
    'ok': ['ok', 'oké'],
    'heerlijk': ['heerlijk'],
    'fout': ['verkeerd', 'fout', 'incorrect', 'onaanvaardbaar'],
    'verwarrend': ['verwarrend'],
    'lelijk': ['lelijk', 'druk']

}

modifiers = {
    'zeer': ['zeer', 'extra', 'veel', 'erg', 'heel'],
    'weinig': ['weinig', 'amper', 'gering', 'minder'],
    'zelden': ['zelden'],
    'enorm': ['enorm', 'super', 'reuze', 'uiterst', 'ultra'],
    'helemaal': ['helemaal', 'volkomen', 'totaal'],
    'beetje': ['beetje', 'enigszins', 'ietwat', 'tikkeltje', 'tikje'],
    'niet': ['niet', 'geen'],
    'zo': ['zo'],

}

# Modifiers geven weer met hoeveel procent de woorden moeten versterkt worden --> Voelt intuitiever aan
weightOfWords = {
    'goed': [1], 'schitterend': [2], 'fantastisch': [2], 'saai': [-1], 'genot': [2], 'perfect': [2], 'privé': [-1],
    'spectaculair': [2], 'dank': [1], 'helaas': [-1],
    'onmogelijk': [-1], 'geschikt': [1], 'afwijken': [-1], 'toegankelijk': [1], 'kut': [-2], 'fijn': [1],
    'teleurstelling': [-2], 'herbekijken': [-1], 'ramp': [-2],
    'vervanging': [-1], 'mooi': [1], 'aanrader': [2], 'snelweg': [-1], 'verdwijn': [-1], 'afrader': [-2], 'parel': [2],
    'onverhard': [0], 'verhard': [0],
    'doodlopen': [-2], 'zeer': [0.5], 'weinig': [-0.5], 'zelden': [-0.8], 'enorm': [1], 'helemaal': [0.7],
    'beetje': [-0.25], 'niet': [-2], 'merkwaardig': [1],
    'slecht': [-1], 'ok': [0.5], 'heerlijk': [2], 'zo': [0], 'fout': [-1], 'verwarrend': [-0.5], 'lelijk': [-1]
}

used = []


def RateTokenizedSentence(tokSent):
    totalScore = 0
    wordsentimenten = []


    stemmer = SnowballStemmer("dutch")

    for key in synonyms:

        gestemde_syn = []

        for w in synonyms[key]:
            w = w.replace("tje", " ")
            a = stemmer.stem(w)


            #a = stemmerKp.stem(w)

            if a[len(a) - 1] == a[len(a) - 2]:
                a = a[:-1]

            gestemde_syn.append(a)

        ws1 = WordSentiment(gestemde_syn, weightOfWords[key][0], 'synonym')
        wordsentimenten.append(ws1)

    for key in modifiers:

        gestemde_mod = []

        for w in modifiers[key]:
            w = w.replace("tje", " ")
            a = stemmer.stem(w)


            #a = stemmerKp.stem(w)

            if a[len(a) - 1] == a[len(a) - 2]:
                print("Oh-Ow")
                a = a[:-1]

            gestemde_mod.append(a)

        ws1 = WordSentiment(gestemde_mod, weightOfWords[key][0], 'modifier')
        wordsentimenten.append(ws1)

    for x in range(len(tokSent)):

        ws1 = checkIfWeight(wordsentimenten, tokSent[x])
        totalmod = 0

        if ws1 is not None and x not in used:

            # print(tokSent[x] + " has weight: " + str(ws1.checkword(tokSent[x])))

            index = x
            totalmod = ws1.checkword(tokSent[x])
            used.append(x)
            stop = True

            if index + 1 < len(tokSent):
                if checkIfWeight(wordsentimenten, tokSent[index + 1]) is None:

                    if ws1.checkword(tokSent[index]) >= 0 or ws1.role is 'synonym':
                        # print('hierin')
                        totalScore += ws1.checkword(tokSent[index])
            else:
                if ws1.role is 'modifier':
                    if ws1.weight > 0:
                        totalScore += ws1.checkword(tokSent[index])
                else:
                    totalScore += ws1.checkword(tokSent[index])
                # print(tokSent)
                # print('index is '+str(index)+ ' en lengte is '+str(len(tokSent)))

            while index + 1 < len(tokSent) and stop is True:

                ws2 = checkIfWeight(wordsentimenten, tokSent[index + 1])

                if ws2 is not None and index + 1 not in used:

                    # print(tokSent[index + 1] + " has weight: " + str(ws2.checkword(tokSent[index+1])))


                    if ws1.role is 'synonym':

                        totalScore += ws1.checkword(tokSent[index])
                        stop = False
                    else:
                        used.append(index + 1)
                        if ws2.role is 'synonym':
                            totalScore += ws2.checkword(tokSent[index + 1]) + totalmod * ws2.checkword(tokSent[index + 1])
                            # print(tokSent[x] + " has weight: " + str(ws2.checkword(tokSent[x])))
                            stop = False

                        else:
                            totalmod = totalmod + ws2.checkword(tokSent[index + 1])
                            # print(tokSent[x] + " has weight: " + str(ws2.checkword(tokSent[x])))
                            # print(str(totalmod))
                            if index + 2 >= len(tokSent):
                                totalScore += totalmod
                else:
                    stop = False
                index = index + 1
        else:

            if tokSent[x].startswith('top') or tokSent[x].startswith('super'):
                totalScore += 1

    used.clear()
    return totalScore


def stemSynonyms(synonyms):
    stemSyn = []
    stemmer = SnowballStemmer("dutch")

    for syn in synonyms:
        k = stemmer.stem(syn)

        #a = stemmerKp.stem(syn)

        stemSyn.append(k)


def checkIfWeight(wordsentimenten, word):
    hasWeight = None

    for y in range(len(wordsentimenten)):
        if wordsentimenten[y].checkword(word) is not None:
            hasWeight = wordsentimenten[y]

    return hasWeight


def checkScore(wordsentimenten, tokenizedSentence, index, score):
    ws = checkIfWeight(wordsentimenten, tokenizedSentence[index])
    # print('checkIfWeight(wordsentimenten, tokenizedSentence[index]) met waarden: ')
    # print(tokenizedSentence[index])

    if ws is None:
        # print(tokenizedSentence[index]+ ' is none')
        return score

    if ws.role is 'modifier':
        # print(tokenizedSentence[index] + ' is modifier')
        used.append(index)
        return checkScore(wordsentimenten, tokenizedSentence, index + 1, score + ws.weight)

    if ws.role is 'synonym':
        # print(tokenizedSentence[index] + ' is synonym')
        used.append(index)
        return score + score * ws.weight
