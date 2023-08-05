from __future__ import annotations


from pydantic import Field
from pydantic_schemaorg.Specialty import Specialty
from pydantic_schemaorg.MedicalEnumeration import MedicalEnumeration


class MedicalSpecialty(Specialty, MedicalEnumeration):
    """Any specific branch of medical science or practice. Medical specialities include clinical"
     "specialties that pertain to particular organ systems and their respective disease"
     "states, as well as allied health specialties. Enumerated type.

    See: https://schema.org/MedicalSpecialty
    Model depth: 5
    """
    type_: str = Field(default="MedicalSpecialty", alias='@type')
    
