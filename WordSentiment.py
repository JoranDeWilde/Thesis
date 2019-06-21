class WordSentiment(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, synonyms, weight, role):
        self.synonyms = synonyms
        self.weight = weight
        self.role = role

    def checkword(self,word):
        if word in self.synonyms:

            return self.weight





