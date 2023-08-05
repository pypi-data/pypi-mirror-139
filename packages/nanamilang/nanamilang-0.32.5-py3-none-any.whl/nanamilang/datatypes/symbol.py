"""NanamiLang Symbol Data Type Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base
from .string import String
from ._exports import export


class Symbol(Base):
    """NanamiLang Symbol Data Type"""

    name: str = 'Symbol'
    _expected_type = str
    _python_reference: str
    purpose = 'Encapsulate Python 3 str'

    @export()
    def nominal(self) -> String:
        """NanamiLang Symbol nominal() method implementation"""

        return String(self.name)

    def format(self, **_) -> str:
        """NanamiLang Symbol, format() method implementation"""

        return f'\'{self._python_reference}'

    def to_py_str(self) -> str:
        """NanamiLang Symbol to_py_str() method implementation"""

        return self.reference()

    def _additional_assertions_on_init(self, reference) -> None:
        """NanamiLang Symbol, _additional_assertions_on_init() method implementation"""

        self._init_assert_ref_could_not_be_empty(reference)
        # Since Symbol encapsulates a Python 3 str, ensure that the string is not empty
