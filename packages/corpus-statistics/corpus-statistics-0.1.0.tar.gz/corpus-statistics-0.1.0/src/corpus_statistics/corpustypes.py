from typing import List, NamedTuple


class VocabElement(NamedTuple):
    token: str
    frequency: int
    proportion: float
    range: int
    stdev: float
    vc: float
    juilland_d: float
    carroll_d2: float
    rosengren_sadj: float
    dp: float
    dp_norm: float
    kl_divergence: float


CorpusVocabulary = List[VocabElement]
