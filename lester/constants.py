from lester.synonym import SynonymFinder

__VERB = SynonymFinder.VERB

GO_VERBS = SynonymFinder('go', part_of_speech=__VERB).get()
LOOK_VERBS = SynonymFinder('look', part_of_speech=__VERB).get()
PICKUP_VERBS = SynonymFinder('grab', part_of_speech=__VERB).get()
