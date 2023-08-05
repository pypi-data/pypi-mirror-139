from __future__ import annotations

from typing import TYPE_CHECKING, Any

from negmas.common import PreferencesChange
from negmas.helpers import snake_case
from negmas.helpers.types import get_full_type_name
from negmas.outcomes import Outcome
from negmas.outcomes.common import check_one_at_most, os_or_none
from negmas.serialization import PYTHON_CLASS_IDENTIFIER, deserialize, serialize
from negmas.types import NamedObject

from .protocols import BasePref, HasReservedOutcome

__all__ = ["Preferences"]

if TYPE_CHECKING:
    from negmas import Rational
    from negmas.outcomes.base_issue import Issue
    from negmas.outcomes.common import Outcome
    from negmas.outcomes.protocols import OutcomeSpace


class Preferences(NamedObject, HasReservedOutcome, BasePref):
    """
    Base class for all preferences.

    Args:
        outcome_space: The outcome-space over which the preferences are defined
    """

    outcome_space: OutcomeSpace | None
    reserved_outcome: Outcome
    owner: Rational | None = None

    def __init__(
        self,
        *args,
        outcome_space: OutcomeSpace | None = None,
        issues: tuple[Issue] = None,
        outcomes: tuple[Outcome] | int | None = None,
        reserved_outcome: Outcome = None,
        **kwargs,
    ) -> None:
        self.owner = None
        check_one_at_most(outcome_space, issues, outcomes)
        super().__init__(*args, **kwargs)
        self.outcome_space = os_or_none(outcome_space, issues, outcomes)
        self.reserved_outcome = reserved_outcome  # type: ignore
        self._changes: list[PreferencesChange] = []

    def to_dict(self) -> dict[str, Any]:
        d = {PYTHON_CLASS_IDENTIFIER: get_full_type_name(type(self))}
        return dict(
            **d,
            outcome_space=serialize(self.outcome_space),
            reserved_outcome=self.reserved_outcome,
            name=self.name,
            id=self.id,
        )

    @classmethod
    def from_dict(cls, d):
        d.pop(PYTHON_CLASS_IDENTIFIER, None)
        d["outcome_space"] = deserialize(d.get("outcome_space", None))
        return cls(**d)

    def changes(self) -> list[PreferencesChange]:
        if self.is_stationary():
            return []
        return [PreferencesChange()]

    @property
    def type(self) -> str:
        """Returns the utility_function type.

        Each class inheriting from this ``UtilityFunction`` class will have its own type. The default type is the empty
        string.

        Examples:
            >>> from negmas.preferences import *
            >>> from negmas.outcomes import make_issue
            >>> print(LinearAdditiveUtilityFunction((lambda x:x, lambda x:x), issues=[make_issue((0, 1), (0, 1))]).type)
            linear_additive
            >>> print(MappingUtilityFunction([lambda x: x], issues=[make_issue((0.0, 1.0))]).type)
            mapping

        Returns:
            str: utility_function type
        """
        return snake_case(
            self.__class__.__name__.replace("Function", "").replace("Utility", "")
        )

    @property
    def base_type(self) -> str:
        """Returns the utility_function base type ignoring discounting and similar wrappings."""
        from .discounted import DiscountedUtilityFunction

        u = self
        while isinstance(u, DiscountedUtilityFunction):
            u = u.ufun
        return self.type
