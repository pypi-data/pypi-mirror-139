"""NanamiLang Boolean Data Type Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base
from .string import String
from ._exports import export


class Boolean(Base):
    """NanamiLang Boolean Data Type"""

    name: str = 'Boolean'
    _expected_type = bool
    _python_reference: bool
    purpose = 'Encapsulate Python 3 bool'

    @export()
    def nominal(self) -> String:
        """NanamiLang Boolean, nominal() method implementation"""

        return String(self.name)

    def to_py_str(self) -> str:
        """NanamiLang Boolean, to_py_str() method implementation"""

        return self.format()

    def format(self, **_) -> str:
        """NanamiLang Boolean, format() method re-implementation"""

        return f'{"true" if self.reference() is True else "false"}'
