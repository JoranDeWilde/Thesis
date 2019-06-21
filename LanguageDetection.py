from googletrans import Translator

import translate
from langdetect import detect


def toDutch(w):

    # translator = Translator()
    # translations =translator.translate(w,dest='nl')

    # translatedComments=[]

    try:
        k = detect(w)
    except:
        # print(w+ " |ERROR")

        return w


    if k != 'nl':
        # k = detect(w)
        # print(translate.google(w, str(detect(w)), 'nl'))

        return translate.google(w, str(detect(w)), 'nl')


    else:
        return w





    # detection= translator.detect(w)



'''
    if detection.lang == "en":
        # print("De engelse taal is gedetecteerd.")
        t = translator.translate(w, dest='nl')
        return t.text;

    elif detection.lang == "fr":
        # print("Franse taal gedetecteerd.")
        t = translator.translate(w, dest='nl')
        return t.text;
    elif detection.lang == "de":
        # print("Duitse taal gedetecteerd.")
        t = translator.translate(w, dest='nl')
        return t.text
    else:
        # print(detection.lang + " taal gedetecteerd.")
        t = translator.translate(w, dest='nl')
        return t.text

'''
