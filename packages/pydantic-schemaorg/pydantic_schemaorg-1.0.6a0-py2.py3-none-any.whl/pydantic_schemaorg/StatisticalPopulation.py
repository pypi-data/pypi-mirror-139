from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic import Field
from pydantic_schemaorg.Intangible import Intangible


class StatisticalPopulation(Intangible):
    """A StatisticalPopulation is a set of instances of a certain given type that satisfy some"
     "set of constraints. The property [[populationType]] is used to specify the type. Any"
     "property that can be used on instances of that type can appear on the statistical population."
     "For example, a [[StatisticalPopulation]] representing all [[Person]]s with a [[homeLocation]]"
     "of East Podunk California, would be described by applying the appropriate [[homeLocation]]"
     "and [[populationType]] properties to a [[StatisticalPopulation]] item that stands"
     "for that set of people. The properties [[numConstraints]] and [[constrainingProperty]]"
     "are used to specify which of the populations properties are used to specify the population."
     "Note that the sense of \"population\" used here is the general sense of a statistical"
     "population, and does not imply that the population consists of people. For example,"
     "a [[populationType]] of [[Event]] or [[NewsArticle]] could be used. See also [[Observation]],"
     "and the [data and datasets](/docs/data-and-datasets.html) overview for more details.

    See: https://schema.org/StatisticalPopulation
    Model depth: 3
    """
    type_: str = Field(default="StatisticalPopulation", alias='@type', constant=True)
    numConstraints: Optional[Union[List[Union[int, 'Integer', str]], int, 'Integer', str]] = Field(
        default=None,
        description="Indicates the number of constraints (not counting [[populationType]]) defined for"
     "a particular [[StatisticalPopulation]]. This helps applications understand if they"
     "have access to a sufficiently complete description of a [[StatisticalPopulation]].",
    )
    constrainingProperty: Optional[Union[List[Union[int, 'Integer', str]], int, 'Integer', str]] = Field(
        default=None,
        description="Indicates a property used as a constraint to define a [[StatisticalPopulation]] with"
     "respect to the set of entities corresponding to an indicated type (via [[populationType]]).",
    )
    populationType: Optional[Union[List[Union['Class', str]], 'Class', str]] = Field(
        default=None,
        description="Indicates the populationType common to all members of a [[StatisticalPopulation]].",
    )
    

if TYPE_CHECKING:
    from pydantic_schemaorg.Integer import Integer
    from pydantic_schemaorg.Class import Class
