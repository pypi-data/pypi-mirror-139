from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterable

from attr import define, field

from negmas.common import PreferencesChange, PreferencesChangeType
from negmas.sao.common import ResponseType

from .base import AcceptanceStrategy, FilterResult

if TYPE_CHECKING:
    from negmas.common import PreferencesChange
    from negmas.outcomes import Outcome
    from negmas.sao import SAOState
    from negmas.sao.negotiators.base import SAONegotiator

__all__ = [
    "LimitedOutcomesAcceptanceStrategy",
    "NegotiatorAcceptanceStrategy",
    "ConcensusAcceptanceStrategy",
    "AllAcceptanceStrategies",
    "AnyAcceptanceStrategy",
    "AcceptImmediately",
    "RejectAlways",
    "EndImmediately",
    "AcceptAbove",
    "RandomAcceptanceStrategy",
    "AcceptTop",
    "AcceptBest",
]


@define()
class RandomAcceptanceStrategy(AcceptanceStrategy):
    p_acceptance: float = 0.15
    p_rejection: float = 0.25
    p_ending: float = 0.1

    def respond(self, state: SAOState, offer: Outcome) -> ResponseType:
        r = random.random()
        if r <= self.p_acceptance + 1e-8:
            return ResponseType.ACCEPT_OFFER
        if r <= self.p_acceptance + self.p_rejection + 1e-8:
            return ResponseType.REJECT_OFFER
        if r <= self.p_acceptance + self.p_rejection + self.p_ending + 1e-8:
            return ResponseType.END_NEGOTIATION
        return ResponseType.NO_RESPONSE


@define
class AcceptBest(AcceptanceStrategy):
    """
    Accepts Only the best outcome.

    Remarks:
        - You can pass the  utility of the best outcome if you know it as `best_util` otherwise it will find it.
        - If the best possible utility cannot be found, nothing will be accepted
    """

    _best_util: float = float("inf")

    def on_preferences_changed(self, changes: list[PreferencesChange]):
        if not self.negotiator or not self.negotiator.ufun:
            return
        _, self._best_util = self.negotiator.ufun.minmax()

    def respond(self, state: SAOState, offer: Outcome) -> ResponseType:
        if not self.negotiator or not self.negotiator.ufun:
            return ResponseType.REJECT_OFFER
        if self.negotiator.ufun(offer) >= self._best_util - 1e-10:
            return ResponseType.ACCEPT_OFFER
        return ResponseType.REJECT_OFFER


@define
class AcceptTop(AcceptanceStrategy):
    """
    Accepts outcomes that are in the given top fraction or top `k`. If neither is given it reverts to accepting the best outcome only.

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

    def respond(self, state: SAOState, offer: Outcome) -> ResponseType:
        if not self.negotiator or not self.negotiator.ufun:
            return ResponseType.REJECT_OFFER
        top_k = self.negotiator.ufun.invert().within_indices((0, self.k))
        if offer in top_k:
            return ResponseType.ACCEPT_OFFER
        top_f = self.negotiator.ufun.invert().within_fractions((0.0, self.fraction))
        if offer in top_f:
            return ResponseType.ACCEPT_OFFER
        return ResponseType.REJECT_OFFER


@define
class AcceptAbove(AcceptanceStrategy):
    """
    Accepts outcomes with utilities in the given top fraction.
    """

    limit: float
    _min: float = field(init=False, default=float("inf"))

    def on_preferences_changed(self, changes: list[PreferencesChange]):
        if not self.negotiator or not self.negotiator.ufun:
            return
        _min, _max = self.negotiator.ufun.minmax(above_reserve=True)
        self._min = self.limit * (_max - _min) + _min

    def respond(self, state: SAOState, offer: Outcome) -> ResponseType:
        if not self.negotiator or not self.negotiator.ufun:
            return ResponseType.REJECT_OFFER
        if self.negotiator.ufun(offer) >= self._min:
            return ResponseType.ACCEPT_OFFER
        return ResponseType.REJECT_OFFER


@define
class EndImmediately(AcceptanceStrategy):
    """
    Rejects immediately anything
    """

    def respond(self, state: SAOState, offer: Outcome) -> ResponseType:
        return ResponseType.END_NEGOTIATION


@define
class RejectAlways(AcceptanceStrategy):
    """
    Rejects everything
    """

    def respond(self, state: SAOState, offer: Outcome) -> ResponseType:
        return ResponseType.REJECT_OFFER


@define
class AcceptImmediately(AcceptanceStrategy):
    """
    Accepts immediately anything
    """

    def respond(self, state: SAOState, offer: Outcome) -> ResponseType:
        return ResponseType.ACCEPT_OFFER


@define
class LimitedOutcomesAcceptanceStrategy(AcceptanceStrategy):
    """
    Accepts from a list of predefined outcomes


    Remarks:
        - if `prob` is a number, it is taken as the probability of aceptance for any outcome.
        - if `prob` is `None`, the probability of acceptance of any outcome will be set to the relative time
    """

    prob: dict[Outcome, float] | float | None
    p_ending: float = 0.0

    @classmethod
    def from_outcome_list(
        cls,
        outcomes: list[Outcome],
        prob: list[float] | float = 1.0,
        p_ending: float = 0.0,
    ):
        if not isinstance(prob, Iterable):
            prob = [prob] * len(outcomes)
        return LimitedOutcomesAcceptanceStrategy(
            prob=dict(zip(outcomes, prob)), p_ending=p_ending
        )

    def respond(self, state: SAOState, offer: Outcome) -> ResponseType:
        if random.random() < self.p_ending - 1e-12:
            return ResponseType.END_NEGOTIATION
        if self.prob is None:
            prob = state.relative_time
        elif isinstance(self.prob, float):
            prob = self.prob
        else:
            prob = self.prob.get(offer, 0.0)
        if random.random() <= prob:
            return ResponseType.ACCEPT_OFFER
        return ResponseType.REJECT_OFFER


@define
class NegotiatorAcceptanceStrategy(AcceptanceStrategy):
    """
    Uses a negotiator as an offering strategy
    """

    acceptor: SAONegotiator

    def respond(self, state: SAOState, offer: Outcome) -> ResponseType:
        return self.acceptor.respond(state, offer)


@define
class ConcensusAcceptanceStrategy(AcceptanceStrategy, ABC):
    """
    Accepts based on concensus of multiple strategies
    """

    strategies: list[AcceptanceStrategy]

    def filter(self, indx: int, response: ResponseType) -> FilterResult:
        """
        Called with the decision of each strategy in order.


        Remarks:
            - Two decisions need to be made:

              1. Should we continue trying other strategies
              2. Should we save this result.
        """
        return FilterResult(True, True)

    @abstractmethod
    def decide(self, indices: list[int], responses: list[ResponseType]) -> ResponseType:
        """
        Called to make a final decsision given the decisions of the stratgeis with indices `indices` (see `filter` for filtering rules)
        """

    def respond(self, state: SAOState, offer: Outcome) -> ResponseType:
        selected, selected_indices = [], []
        for i, s in enumerate(self.strategies):
            response = s.respond(state, offer)
            r = self.filter(i, response)
            if not r.next:
                break
            if r.save:
                selected.append(response)
                selected_indices.append(i)

        return self.decide(selected_indices, selected)


@define
class AllAcceptanceStrategies(ConcensusAcceptanceStrategy):
    """Accept only if all children accept, end only if all of them end, otherwise reject"""

    def filter(self, indx: int, response: ResponseType) -> FilterResult:
        if response == ResponseType.REJECT_OFFER:
            return FilterResult(False, True)
        if response == ResponseType.END_NEGOTIATION:
            return FilterResult(False, True)
        return FilterResult(True, False)

    def decide(self, indices: list[int], responses: list[ResponseType]) -> ResponseType:
        if not responses:
            return ResponseType.ACCEPT_OFFER
        return responses[0]


@define
class AnyAcceptanceStrategy(ConcensusAcceptanceStrategy):
    """Accept any children accept, end or reject only if all of them end or reject"""

    def filter(self, indx: int, response: ResponseType) -> FilterResult:
        if response == ResponseType.ACCEPT_OFFER:
            return FilterResult(False, True)
        if response == ResponseType.END_NEGOTIATION:
            return FilterResult(False, True)
        return FilterResult(True, False)

    def decide(self, indices: list[int], responses: list[ResponseType]) -> ResponseType:
        if not responses:
            return ResponseType.REJECT_OFFER
        return responses[0]
