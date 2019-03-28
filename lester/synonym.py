from nltk.corpus import wordnet


class SynonymFinder:
    """
    Used to generate synonyms for an iterable of words
    """
    NOUN = 'n'
    VERB = 'v'

    def __init__(self, *words, part_of_speech=None):
        if part_of_speech is None:
            part_of_speech = self.NOUN

        self.part_of_speech = part_of_speech
        self.words = words

    def get(self):
        synonyms = {
            lemma.name().replace('_', ' ')
            for word in self.words
            for synset in wordnet.synsets(word)
            if synset.pos() == self.part_of_speech
            for lemma in synset.lemmas()
        }

        return synonyms
