import array
import functools
import operator
from collections import Counter, defaultdict
from functools import cached_property
from pathlib import Path
from typing import Callable, Dict, List, NamedTuple, Union

import numpy as np
import scipy.sparse as sp
import srsly
from spacy.language import Language
from spacy.tokens import Doc

from .corpustypes import CorpusVocabulary, VocabElement
from .dispersion_functions import calculate_all_stats


def require_frozen(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.frozen:
            raise ValueError("Must call freeze() before use")
        return func(self, *args, **kwargs)

    return wrapper


@Language.factory("corpus_statistics", default_config={"lowercase": False})
def create_corpus_statistics_component(nlp: Language, name: str, lowercase: bool):
    return CorpusStatistics(nlp, lowercase=lowercase)


class CorpusAggregates(NamedTuple):
    vocab_size: int
    token_count: int
    corpus_length: int
    doc_lengths: List[int]


class CorpusStatistics:
    def __init__(self, nlp: Language, lowercase: bool):
        self.corpus_counter: Counter = Counter()
        self.lowercase = lowercase

        self.vocabulary: Dict[str, int] = defaultdict()
        self.vocabulary.default_factory = self.vocabulary.__len__

        self._j_indices: List[int] = []
        self._indptr: List[int] = [0]
        self._values = array.array("i")

        self.frozen: bool = False

    def __call__(self, doc: Doc) -> Doc:
        # TODO: Raise Error if Frozen
        feature_counter: Dict[int, int] = {}
        for token in doc:
            token_text = token.text if not self.lowercase else token.text.lower()
            feature_idx = self.vocabulary[token_text]
            if feature_idx not in feature_counter:
                feature_counter[feature_idx] = 1
            else:
                feature_counter[feature_idx] += 1
        self._j_indices.extend(feature_counter.keys())
        self._values.extend(feature_counter.values())
        self._indptr.append(len(self._j_indices))
        return doc

    def freeze(self) -> None:
        j_indices = np.asarray(self._j_indices, dtype=np.int64)
        indptr = np.asarray(self._indptr, dtype=np.int64)
        values = np.frombuffer(self._values, dtype=np.intc)
        _X = sp.csr_matrix(
            (values, j_indices, indptr),
            shape=(len(indptr) - 1, len(self.vocabulary)),
            dtype=np.int64,
        )
        _X.sort_indices()
        _X = _X.tocsc()

        # freeze vocabulary: convert from defaultdict
        self.vocabulary = dict(self.vocabulary)
        self.aggregates = CorpusAggregates(
            vocab_size=len(self.vocabulary),
            token_count=_X.sum(),
            corpus_length=_X.shape[0],
            doc_lengths=_X.sum(axis=1).ravel().tolist(),
        )

        self.data = calculate_all_stats(_X, self.vocabulary)
        self.frozen = True

    @require_frozen
    def __getitem__(self, key: str) -> VocabElement:
        element = [v for v in self.data if v.token == key]
        if element:
            return element[0]
        else:
            raise KeyError(f"{key} not in vocabulary.")

    @require_frozen
    def __contains__(self, key: str) -> int:
        return key in self.vocabulary

    def __len__(self):
        raise ValueError(
            "Length is ambiguous. "
            "Do you mean vocab_size, token_count, or corpus_length?"
        )

    @cached_property  # type: ignore
    @require_frozen
    def vocab_size(self) -> int:
        return self.aggregates.vocab_size

    @cached_property  # type: ignore
    @require_frozen
    def token_count(self) -> int:
        return self.aggregates.token_count

    @cached_property  # type: ignore
    @require_frozen
    def corpus_length(self) -> int:
        return self.aggregates.corpus_length

    @cached_property  # type: ignore
    @require_frozen
    def doc_lengths(self) -> List[int]:
        return self.aggregates.doc_lengths

    @cached_property  # type: ignore
    @require_frozen
    def type_token_ratio(self) -> float:
        return self.aggregates.vocab_size / self.aggregates.token_count

    @require_frozen
    def query(
        self,
        attribute: str,
        op: Callable[[float, float], bool],
        value: Union[float, int],
    ) -> CorpusVocabulary:
        return [v for v in self.data if op(getattr(v, attribute), value)]

    @cached_property  # type: ignore
    @require_frozen
    def hapax_legomena(self) -> CorpusVocabulary:
        return self.query("frequency", operator.eq, 1)

    @cached_property  # type: ignore
    @require_frozen
    def dis_legomena(self) -> CorpusVocabulary:
        return self.query("frequency", operator.eq, 2)

    @require_frozen
    def to_disk(self, path, exclude=tuple()):
        if not isinstance(path, Path):
            path = Path(path)
        if not path.exists():
            path.mkdir()
        srsly.write_msgpack(path / "vocabulary.msgpack", self.vocabulary)
        srsly.write_msgpack(path / "dispersion_data.msgpack", self.data)
        srsly.write_msgpack(path / "aggregates.msgpack", self.aggregates)

    def from_disk(self, path, exclude=tuple()):
        self.vocabulary = srsly.read_msgpack(path / "vocabulary.msgpack")
        self.data = srsly.read_msgpack(path / "dispersion_data.msgpack")
        self.aggregates = srsly.read_msgpack(path / "aggregates.msgpack")
        self.frozen = True
        return self
