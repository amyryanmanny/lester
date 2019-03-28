from collections import defaultdict

from nltk.corpus import brown

from nltk.tokenize import word_tokenize
from nltk.tag import UnigramTagger


class Parser:
    NOUN = 'NN'
    VERB = 'VB'

    class TooManyNounsError(ValueError):
        pass

    class TooManyVerbsError(ValueError):
        pass

    class NoVerbsError(ValueError):
        pass

    def __init__(self, rooms):
        self.__sentences = list(brown.tagged_sents(categories=['adventure']))

        for room in rooms:
            """
            This will only really work with UnigramTagger, since there's no context 
            """
            self.__sentences.append(
                [(name, 'NN') for name in room.names]
            )
            self.__sentences.append(
                [(noun, 'NN') for noun in room.noun_to_item.keys()]
            )
            for item in room:
                for i in range(1000):  # TODO: Weight less hackily
                    self.__sentences.append(
                        [(verb, 'VB') for verb in item.verb_to_action.keys()]
                    )

        self.tokenize = word_tokenize
        self.__tagger = UnigramTagger(train=self.__sentences)
        self.tag = self.__tagger.tag

        self.tokens = []
        self.tagged = []

    def parse(self, s):
        """
        Parses a command into three parts:
            1) Verb
            2) Subject (noun)
            3) Object (noun)
        """
        self.tokens = self.tokenize(s)
        self.tagged = self.tag(self.tokens)

        if len(self.tokens) == 1:
            # Assume one-word commands are always a verb
            return self.tokens[0], []

        print(self.tagged)

        classified_tokens = defaultdict(list)
        for i, (token, tag) in enumerate(self.tagged):
            if tag is None:
                if i == 0:
                    tag = 'VB'  # Assume verb (for funny print-statements)
                else:
                    tag = 'NN'  # Assume noun
            classified_tokens[tag[:2]].append(token)

        verbs = classified_tokens[self.VERB]
        nouns = classified_tokens[self.NOUN]

        if len(verbs) > 1:
            raise self.TooManyVerbsError
        elif not verbs:
            raise self.NoVerbsError

        if len(nouns) > 2:
            # raise self.TooManyVerbsError
            pass  # We'll see if this causes any problems

        return verbs[0], nouns
