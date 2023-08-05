from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic import Field
from pydantic_schemaorg.Intangible import Intangible


class Grant(Intangible):
    """A grant, typically financial or otherwise quantifiable, of resources. Typically a"
     "[[funder]] sponsors some [[MonetaryAmount]] to an [[Organization]] or [[Person]],"
     "sometimes not necessarily via a dedicated or long-lived [[Project]], resulting in"
     "one or more outputs, or [[fundedItem]]s. For financial sponsorship, indicate the [[funder]]"
     "of a [[MonetaryGrant]]. For non-financial support, indicate [[sponsor]] of [[Grant]]s"
     "of resources (e.g. office space). Grants support activities directed towards some"
     "agreed collective goals, often but not always organized as [[Project]]s. Long-lived"
     "projects are sometimes sponsored by a variety of grants over time, but it is also common"
     "for a project to be associated with a single grant. The amount of a [[Grant]] is represented"
     "using [[amount]] as a [[MonetaryAmount]].

    See: https://schema.org/Grant
    Model depth: 3
    """
    type_: str = Field(default="Grant", alias='@type')
    fundedItem: Optional[Union[List[Union['Thing', str]], 'Thing', str]] = Field(
        default=None,
        description="Indicates an item funded or sponsored through a [[Grant]].",
    )
    sponsor: Optional[Union[List[Union['Organization', 'Person', str]], 'Organization', 'Person', str]] = Field(
        default=None,
        description="A person or organization that supports a thing through a pledge, promise, or financial"
     "contribution. e.g. a sponsor of a Medical Study or a corporate sponsor of an event.",
    )
    

if TYPE_CHECKING:
    from pydantic_schemaorg.Thing import Thing
    from pydantic_schemaorg.Organization import Organization
    from pydantic_schemaorg.Person import Person
