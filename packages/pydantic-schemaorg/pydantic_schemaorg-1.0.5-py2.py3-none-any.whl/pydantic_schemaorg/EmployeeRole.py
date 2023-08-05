from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union
from decimal import Decimal


from pydantic import Field
from pydantic_schemaorg.OrganizationRole import OrganizationRole


class EmployeeRole(OrganizationRole):
    """A subclass of OrganizationRole used to describe employee relationships.

    See: https://schema.org/EmployeeRole
    Model depth: 5
    """
    type_: str = Field(default="EmployeeRole", alias='@type')
    salaryCurrency: Optional[Union[List[Union[str, 'Text']], str, 'Text']] = Field(
        default=None,
        description="The currency (coded using [ISO 4217](http://en.wikipedia.org/wiki/ISO_4217) )"
     "used for the main salary information in this job posting or for this employee.",
    )
    baseSalary: Optional[Union[List[Union[Decimal, 'Number', 'MonetaryAmount', 'PriceSpecification', str]], Decimal, 'Number', 'MonetaryAmount', 'PriceSpecification', str]] = Field(
        default=None,
        description="The base salary of the job or of an employee in an EmployeeRole.",
    )
    

if TYPE_CHECKING:
    from pydantic_schemaorg.Text import Text
    from pydantic_schemaorg.Number import Number
    from pydantic_schemaorg.MonetaryAmount import MonetaryAmount
    from pydantic_schemaorg.PriceSpecification import PriceSpecification
