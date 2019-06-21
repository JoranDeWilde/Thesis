from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from LanguageDetection import toDutch
import re
from bs4 import BeautifulSoup
from collections import Counter
import kpss_py3 as stemmerKp


def filterOutQuestions(sentence):
    # While er vraagtekens zijn, filter deze eruit

    while sentence.find("?") is not -1:

        Qindex = sentence.find("?")
        index = Qindex-1


        if Qindex is 0:
            if len(sentence) is not 1:
                sentence = sentence[1:]
            else:
                return ""

        while index >= 0:
            if sentence[index] is "?" or sentence[index] is "," or sentence[index] is ";" or sentence[index] is "." or sentence[index] is "!" or sentence[index] is "\n":
                question = sentence[index+1:Qindex+1]
                sentence = sentence.replace(question, "")
                index = -1

            else:
                index = index-1
                if index is 0 or index is -1:
                    question = sentence[index+1:Qindex + 1]
                    sentence = sentence.replace(question, "")
                    index = -1


    return sentence

def afkortingen(x):
    abbrevs={' d.a.v. ': ' daaraanvolgend ', ' d.m.v. ': ' door middel van ', ' d.t.v. ': ' door tussenkomst van ', ' d.w.z. ': ' dat wil zeggen ', ' a ': ' are ',
         ' d.z.z. ': ' dezerzijds ', ' depri ': ' depressief ',' desp. ': ' despotaat ', ' drs. ': ' drams ', ' a.s. ': 'aanstaande',
         ' dwz. ': ' dat wil zeggen ', ' dyn. ': ' dynastie ',' a\'dam ': ' Amsterdam ',  ' a.h.w. ': ' als het ware ',
         ' a.j.b ': ' alsjeblieft ', ' a.m. ': ' ante meridiem ', ' a.u.b. ': ' alstublieft ', ' i.o.v. ': ' in opdracht van ',
         ' aanw.vnw. ': ' aanwijzend voornaamwoord ',' abd. ': ' abdij ', ' abm. ': ' aartsbisdom ', 'a.d.h.v.': 'aan de hand van',
         ' abs. ': ' aartsbisschop ', ' achterv. ': ' achtervolging ',' afl. ': ' aflevering ', ' asa ': ' als en slechts als ',
         ' b. v. ': ' bijvoorbeeld ', ' b.v. ': ' bijvoorbeeld ',' bab. ': ' Babylonisch ', ' bet. ': ' betekenis ',
         ' betr. ': ' betreffende ', ' bib ': ' bibliotheek ',' bijv. ': ' bijvoorbeeld ', ' bijw. ': ' bijwoord ', ' n.a.v. ': ' naar aanleiding van ',
         ' bm. ': ' bisdom ', ' bn. ': ' bijvoeglijk naamwoord ',' bs. ': ' bullshit ', ' bv. ': ' bijvoorbeeld ',
         ' bw. ': ' bijwoord ', ' byz. ': ' byzantijns ',' c.q. ': ' in dat geval ', ' c.s. ': ' cum suis ', ' s.v.p. ': ' alsjeblieft ',
         ' ca. ': ' circa ', ' cgn ': ' gorpus gesproken nederlands ',' e.d. ': ' en dergelijke ', ' e.e.a. ': ' een en ander ',
         ' eil. ': ' eiland ', ' enz. ': ' enzovoorts ',' es. ': ' echtscheiding ', ' evt. ': ' eventueel ',
         ' fed ': ' federatie ', ' ff. ': ' even ',' form. ': ' formeel ', ' fr. ': ' frans ', ' v.v. ': ' vice versa ',
         ' fra. ': ' frans ', ' ft. ': ' fort ',' g ': ' gram ', ' ghert. ': ' groothertogdom ',
         ' gr. ': 'grieks ', ' grs. ': ' graafschap ',' grvm. ': ' grootvorstendom ', ' g.v.d. ': ' godverdomme ',
         ' h.m. ': ' hare majesteit ', ' ha ': ' hectare ', ' hert. ': ' hertogdom ', ' hr. ': ' harer ',
         ' hr.ms. ': ' harer majesteits ', ' i.p.v. ': ' in plaats van ',' i.t.t. ': ' in tegenstelling tot ', ' i.v.m. ': ' in verband met ',
         ' idd ': ' inderdaad ', ' iem. ': ' iemand ',' inf. ': ' informeel ', ' ing. ': ' ingenieur ',
         ' inz. ': ' inzonderheid ', ' ir. ': ' ingenieur ',' jwt ': ' je weet toch ', ' jwz ': ' je weet zelf ',
         ' kg. ': ' koning ', ' ki ': ' kunstmatige intelligentie ',' kilo ': ' kilogram ', ' kk ': ' kanker ',
         ' kkr. ': ' koninkrijk ', ' km/u ': ' kilometer per uur ', ' kvdm. ': ' keurvorstendom ', ' kymr. ': ' kymrisch ',
         ' lat. ': ' latijn ', ' lgrs. ': ' landgraafschap ',' lidw. ': ' lidwoord ', ' lvdh ': ' lees verdomme de handleiding ',
         ' m. ': ' mark ', ' m.a.w. ': ' met andere woorden ',' m.b.t. ': ' met betrekking tot ', ' m.i. ': ' mijns inziens ',
         ' m.i.v. ': ' met ingang van ', ' m.n. ': ' met name ',' m.u.v. ': ' met uitzondering van ', ' m/s' : ' meter per seconde ',
         ' maced. ': ' macedonisch ', ' me. ': ' middelengels ',' mgr. ': ' markgraaf ', ' mgrs. ': ' markgraafschap ',
         ' mhd. ': ' middelhoogduits ', ' mnd. ': ' middelnederduits ',' mr. ': ' meester ', ' ms. ': ' majesteits ',
         ' muz. ': ' muziek ', ' mv. ': ' meervoud ',' n ': ' noord ', ' n. chr. ': ' na Christus ', ' n.chr. ': ' na Christus ',
         ' n.n.b. ': ' nog niet bekend ', ' ngt ': ' nederlandse gebarentaal ',' nhd. ': ' nieuwhoogduits ', ' nieuw arch. wisk. ': ' nieuw archief voor wiskunde ',
         ' nl. ': ' namelijk ', ' nnd. ': ' nieuwnederduits ',' nr. ': ' nummer ', ' ns ': ' nederlandse spoorwegen ',
         ' o ': ' oost ', ' o.a. ': ' onder andere ',' o.c. ': ' opere citato ', ' o.i.d. ': ' of iets dergelijks ',
         ' o.m.' : ' onder meer ', ' o.t.t. ': ' onvoltooid tegenwoordige tijd ',' o.t.t.t. ': ' onvoltooid tegenwoordige toekomende tijd ', ' o.tk.t. ': ' onvoltooid toekomende tijd ',
         ' o.v.t. ': ' onvoltooid verleden tijd ', ' o.v.t.t. ': ' onvoltooid verleden toekomende tijd ',' o.v.tk.t. ': ' onvoltooid verleden toekomende tijd ', ' oe. ': ' oudengels ',
         ' ohd. ': ' oudhoogduits ', ' on.ww. ': ' onovergankelijk werkwoord ',' onfrank. ': ' oudnederfrankisch ', ' onz. ': ' onzijdig ',
         ' orth. ': ' orthodox ', ' os. ': ' oudsaksisch ',' osm. ': ' ottomaans ', ' ov.ww. ': ' overgankelijk werkwoord ',
         ' p.l.o.r.k. ': ' prettig lichaam ontzettende rotkop ', ' prof. ': ' professor ',' prot. ': ' protestants ', ' prov. ': ' provincie. ',
         ' pun. ': ' punisch ', ' r\'dam ': ' rotterdam ',' r.k. ': ' rooms-katholiek ', ' rep. ': ' republiek ',
         ' resp. ': ' respectievelijk ', ' rom. ': ' romeins ',' st. ': ' sint ', ' stu.fi. ': ' studiefinanciering ',
         ' t.g.v. ': ' ten gevolge van ', ' t.w. ': ' te weten ',' t/m ': ' tot en met ', ' taalk. ': ' taalkunde ',
         ' toep. ': ' toepassing ', ' tv ': ' televisie ',' tw. ': ' tussenwerpsel ', ' uitdr. ': ' uitdrukking ', ' v. ': ' van ', ' t.o.v. ': ' ten opzichte van '
         }

    abbrevs2={}
    for w in abbrevs:
        # print(w)
        # print(abbrevs[w])
        abbrevs2[w.replace(".","")]=abbrevs[w]

    # Dictionary with most used abbreviations in the Dutch language
    abbrevs3={**abbrevs,**abbrevs2}

    # Replace all abbreviations with the full-written equivalent
    for w in abbrevs3:
        x = x.replace(w,abbrevs3[w])

    return x

# -----------------------------------------------------   MAIN   -------------------------------------------------------------




def noiseRemoval(commentList):

    # translatedComments=toDutch(commentList)
    translatedComments=[]
    tokenizedComments= []
    tokenizedStemComments=[]

    i = 0
    nn=0
    # alle_woorden = []

    for comment in commentList:



        if not isinstance(comment, str):
                translatedComments.append(comment)
        else:
            # Automatisch uitfilteren van html zaken zoals <p>, <br>,...
            # cleanr = re.compile('<.*?>')
            # w = re.sub(cleanr, '', comment.lower())

            # Hyperlinks eruit filteren
            soup = BeautifulSoup(comment,features="lxml")
            for m in soup.find_all('a'):
                m.replaceWithChildren()

            w = re.sub(r'^https?:\/\/.*[\r\n]*', '', str(soup), flags=re.MULTILINE)
            w = re.sub(r'http\S+', '', w)

            # Automatisch uitfilteren van html zaken zoals <p>, <br>,...
            cleanr = re.compile('<.*?>')
            w = re.sub(cleanr, '', w.lower())


        # Translate all the sentences to Dutch

        #TODO: Zet onderstaande lijn in commentaar wanneer er veel commentaren (5000+) beoordeeld moeten worden. Dit kan niet allemaal tegelijk vertaald worden
        #w = toDutch(w)
        i=i+1
        # print(translated)


        # Add abbreviations to sentence
        w = afkortingen(w)

        #Uitfilteren van vragen
        temp=w
        w = filterOutQuestions(w)
        # Tokenize sentence
        tokenizer = RegexpTokenizer(r'\w+')
        w = w.replace("ste ", " ")
        w = w.replace("tje", " ")

        words = tokenizer.tokenize(w)
        tokenizedComments.append(words)


        # Stemming all words


        stemmer = SnowballStemmer("dutch")


        gestemde_woorden = []

        filtered_sentence = []

        # Filtering stopwords
        stop_words = set(stopwords.words("dutch"))
        stop_words.remove("geen")
        stop_words.remove("niet")
        #stop_words.remove("veel")



        for w in words:
            if w not in stop_words:
                filtered_sentence.append(w)

        for w in filtered_sentence:

            # print(w)
            a = stemmer.stem(w)


            #a = stemmerKp.stem(w)

            if a[len(a)-1] == a[len(a)-2]:
                a = a[:-1]

            # alle_woorden.append(a)


            gestemde_woorden.append(a)


            # w = stemmer.stem(w)
            # gestemde_woorden.append(stemmer.stem(w))

        tokenizedStemComments.append(gestemde_woorden)


    '''
    # print(alle_woorden)
    print(len(alle_woorden))
    counts = Counter(alle_woorden)
    mostcommon = counts.most_common(200)

    for mc in mostcommon:
        print(mc)
    '''
    return tokenizedStemComments

