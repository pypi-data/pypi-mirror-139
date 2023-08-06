"""NanamiLang Numeric Data Type Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base
from .string import String
from .boolean import Boolean
from ._exports import export


class Numeric(Base):
    """NanamiLang Numeric Type"""

    name = 'Numeric'

    @export()
    def even(self) -> Boolean:
        """NanamiLang Numeric, even?"""

        return Boolean(self._python_reference % 2 == 0)

    @export()
    def abs(self) -> Base:
        """NanamiLang Numeric, abs value"""

        return self.__class__(abs(self._python_reference))

    @export()
    def odd(self) -> Boolean:
        """NanamiLang Numeric, number is odd?"""

        return Boolean(not self._python_reference % 2 == 0)

    @export()
    def nominal(self) -> String:
        """NanamiLang Numeric, nominal() method implementation"""

        return String(self.name)

    # We could implement other builtin numeric-specific methods :)
