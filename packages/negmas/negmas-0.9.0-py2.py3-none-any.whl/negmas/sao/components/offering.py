from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from attr import define, field

from negmas.common import PreferencesChangeType, Value

from .base import FilterResult, OfferingStrategy

if TYPE_CHECKING:
    from negmas.common import PreferencesChange
    from negmas.outcomes import Outcome
    from negmas.sao import SAOState
    from negmas.sao.negotiators.base import SAONegotiator


__all__ = [
    "LimitedOutcomesOfferingStrategy",
    "NegotiatorOfferingStrategy",
    "ConcensusOfferingStrategy",
    "RandomConcensusOfferingStrategy",
    "UnanimousConcensusOfferingStrategy",
    "UtilBasedConcensusOfferingStrategy",
    "MyBestConcensusOfferingStrategy",
    "MyWorstConcensusOfferingStrategy",
    "NoneOfferingStrategy",
    "RandomOfferingStrategy",
    "OfferTop",
    "OfferBest",
    "NaiveTFTOfferingStrategy",
]


@define
class NaiveTFTOfferingStrategy(OfferingStrategy):
    """
    Offers based on an estimate of the concession made by the opponent as projected in our own utility space.

    """

    _best: Outcome | None = None

    def on_preferences_changed(self, changes: list[PreferencesChange]):
        if not self.negotiator or not self.negotiator.ufun:
            return
        _, self._best = self.negotiator.ufun.extreme_outcomes()

    def propose(self, state: SAOState) -> Outcome | None:
        return self._best


@define
class OfferBest(OfferingStrategy):
    """
    Offers Only the best outcome.

    Remarks:
        - You can pass the  best outcome if you know it as `best` otherwise it will find it.
    """

    _best: Outcome | None = None

    def on_preferences_changed(self, changes: list[PreferencesChange]):
        if not self.negotiator or not self.negotiator.ufun:
            return
        _, self._best = self.negotiator.ufun.extreme_outcomes()

    def propose(self, state: SAOState) -> Outcome | None:
        return self._best


@define
class OfferTop(OfferingStrategy):
    """
    Offers outcomes that are in the given top fraction or top `k`. If neither is given it reverts to only offering the best outcome

    Remarks:
        - The outcome-space is always discretized and the constraints `fraction` and `k` are applied to the discretized space
    """

    fraction: float = 0.0
    k: int = 1

    def on_preferences_changed(self, changes: list[PreferencesChange]):
        if not self.negotiator or not self.negotiator.ufun:
            return
        if any(
            _.type
            not in (
                PreferencesChangeType.Scaled,
                PreferencesChangeType.ReservedOutcome,
                PreferencesChangeType.ReservedValue,
            )
            for _ in changes
        ):
            self.negotiator.ufun.invert().init()

    def propose(self, state: SAOState) -> Outcome | None:
        if not self.negotiator or not self.negotiator.ufun:
            return None
        top_k = self.negotiator.ufun.invert().within_indices((0, self.k))
        top_f = self.negotiator.ufun.invert().within_fractions((0.0, self.fraction))
        top = list(set(top_k + top_f))
        return random.choice(top)


@define
class NoneOfferingStrategy(OfferingStrategy):
    """
    Always offers `None` which means it never gets an agreement.
    """

    def propose(self, state: SAOState) -> Outcome | None:
        return None


@define
class RandomOfferingStrategy(OfferingStrategy):
    """
    Always offers `None` which means it never gets an agreement.
    """

    def propose(self, state: SAOState) -> Outcome | None:
        if not self.negotiator or not self.negotiator.nmi:
            return None
        return self.negotiator.nmi.random_outcomes(1)[0]


@define
class LimitedOutcomesOfferingStrategy(OfferingStrategy):
    """
    Offers from a given list of outcomes
    """

    outcomes: list[Outcome] | None
    prob: list[float] | None = None
    p_ending: float = 0.0

    def propose(self, state: SAOState, retry=False) -> Outcome | None:
        if not self.negotiator or not self.negotiator.nmi:
            return None
        if random.random() < self.p_ending - 1e-7:
            return None
        if not self.prob or not self.outcomes:
            return random.choice(
                self.outcomes
                if self.outcomes
                else list(self.negotiator.nmi.discrete_outcomes())
            )
        r, s = random.random(), 0.0
        for w, p in zip(self.outcomes, self.prob):
            s += p
            if r <= s:
                return w
        if retry:
            return None
        if s > 0.999:
            return self.outcomes[-1]
        self.prob = [_ / s for _ in self.prob]
        return self.propose(state, True)


@define
class NegotiatorOfferingStrategy(OfferingStrategy):
    """
    Uses a negotiator as an offering strategy
    """

    proposer: SAONegotiator = field(kw_only=True)

    def propose(self, state: SAOState) -> Outcome | None:
        return self.proposer.propose(state)


@define
class ConcensusOfferingStrategy(OfferingStrategy, ABC):
    """
    Offers based on concensus of multiple strategies
    """

    strategies: list[OfferingStrategy]

    def filter(self, indx: int, offer: Outcome | None) -> FilterResult:
        """
        Called with the decision of each strategy in order.


        Remarks:
            - Two decisions need to be made:

              1. Should we continue trying other strategies
              2. Should we save this result.
        """
        return FilterResult(True, True)

    @abstractmethod
    def decide(
        self, indices: list[int], responses: list[Outcome | None]
    ) -> Outcome | None:
        """
        Called to make a final decsision given the decisions of the stratgeis with indices `indices` (see `filter` for filtering rules)
        """

    def propose(self, state: SAOState) -> Outcome | None:
        selected, selected_indices = [], []
        for i, s in enumerate(self.strategies):
            response = s.propose(state)
            r = self.filter(i, response)
            if not r.next:
                break
            if r.save:
                selected.append(response)
                selected_indices.append(i)

        return self.decide(selected_indices, selected)


@define
class UnanimousConcensusOfferingStrategy(ConcensusOfferingStrategy):
    """
    Offers only if all offering strategies gave exactly the same outcome
    """

    def decide(
        self, indices: list[int], responses: list[Outcome | None]
    ) -> Outcome | None:
        outcomes = set(responses)
        if len(outcomes) != 1:
            return None
        return list(outcomes)[0]


@define
class RandomConcensusOfferingStrategy(ConcensusOfferingStrategy):
    """
    Offers a random response from the list of stratgies (different strategy every time).
    """

    prob: list[float] | None = None

    def __attrs_post_init__(self):
        if not self.prob:
            return
        s = sum(self.prob)
        self.prob = [_ / s for _ in self.prob]

    def decide(
        self, indices: list[int], responses: list[Outcome | None]
    ) -> Outcome | None:
        if not self.prob:
            return random.choice(responses)

        r, s = random.random(), 0.0
        for i, p in enumerate(self.prob):
            s += p
            if r <= s:
                return responses[i]
        if s > 0.999:
            return responses[-1]
        raise ValueError(f"sum of probabilities is less than 1: {s}")


@define
class UtilBasedConcensusOfferingStrategy(ConcensusOfferingStrategy, ABC):
    """
    Offers from the list of stratgies (different strategy every time) based on outcome utilities
    """

    @abstractmethod
    def decide_util(self, utils: list[Value]) -> int:
        """
        Returns the index to chose based on utils
        """

    def decide(
        self, indices: list[int], responses: list[Outcome | None]
    ) -> Outcome | None:
        if not self.negotiator.ufun:
            raise ValueError(f"Cannot decide because I have no ufun")
        return responses[
            self.decide_util([self.negotiator.ufun(_) for _ in set(responses)])
        ]


@define
class MyBestConcensusOfferingStrategy(UtilBasedConcensusOfferingStrategy):
    """
    Offers my best outcome from the list of stratgies (different strategy every time).
    """

    def decide_util(self, utils: list[Value]) -> int:
        return max(range(len(utils)), key=lambda x: utils[x])


@define
class MyWorstConcensusOfferingStrategy(UtilBasedConcensusOfferingStrategy):
    """
    Offers my worst outcome from the list of stratgies (different strategy every time) based on outcome utilities
    """

    def decide_util(self, utils: list[Value]) -> int:
        return min(range(len(utils)), key=lambda x: utils[x])
