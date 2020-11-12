__name__ = "conll"
__author__ = "Paul McCann <polm@dampfkraft.com>"
__version__ = "0.1.0"

from visidata import *

@VisiData.api
def open_conll(p):
    return ConllSheet(p.name, source=p)

@VisiData.api
def open_conllu(p):
    return ConllSheet(p.name, source=p)


class ConllSheet(TableSheet):
    rowtype='tokens'
    # see here for reference:
    # https://universaldependencies.org/format.html
    columns=[
        # Usually an integer, but can be prefixed like "dev-s1"
        ColumnItem('sent_id', 0, type=str),
        # token ID is almost always an integer, but can be technically be a decimal between 0 and 1.
        # starts from 1 for each sentence.
        ColumnItem('token_id', 1, type=int),
        # form from the raw input, aka surface
        ColumnItem('form', 2, type=str),
        ColumnItem('lemma', 3, type=str),
        ColumnItem('upos', 4, type=str),
        ColumnItem('xpos', 5, type=str),
        ColumnItem('feats', 6, type=dict),
        ColumnItem('head', 7, type=int),
        ColumnItem('deprel', 8, type=str),
        # possibly list of pairs, but often? unused
        ColumnItem('deps', 9),
        # empty or a dictionary
        ColumnItem('misc', 10, type=dict),
    ]
    def iterload(self):
        import pyconll

        # sent_id + token_id will be unique
        self.setKeys([self.columns[0], self.columns[1]])

        with self.source.open(encoding='utf-8') as fp:
            for sent in pyconll.load.iter_sentences(fp):
                sent_id = sent.id
                for token in sent:
                    yield [sent_id, token.id, token._form, token.lemma, token.upos, 
                            token.xpos, token.feats, token.head, token.deprel, token.deps, token.misc]


vd.addGlobals(globals())
