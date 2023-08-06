"""NanamiLang String Data Type CLass"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base
from ._exports import export


class String(Base):
    """NanamiLang String Data Type"""

    name: str = 'String'
    _expected_type = str
    _python_reference: str
    purpose = 'Encapsulate Python 3 str'
    __reference_helpers = (0, '', )

    def truthy(self) -> bool:
        """NanamiLang String, truthy() method implementation"""

        return True

    def format(self, **_) -> str:
        """NanamiLang String, format() method implementation"""

        return f'"{self._python_reference}"'

    @export()
    def nominal(self) -> Base:
        """NanamiLang String, nominal() method implementation"""

        return String(self.name)

    def to_py_str(self) -> str:
        """NanamiLang String, to_py_str() method implementation"""

        return self._python_reference

    def reference(self) -> str:
        """NanamiLang String, reference() method implementation"""

        idx, retval = self.__reference_helpers

        while idx < len(self._python_reference):
            if self._python_reference[idx] == '\\':
                idx += 1
                escaped = self._python_reference[idx]
                # TODO:: handle more escape sequences
                if escaped == '"':
                    retval += '"'   # string boundary
                if escaped == 'n':
                    retval += '\n'  # a new-line char
                # Leave an escape seq as is otherwise
                idx += 1
            else:
                retval += self._python_reference[idx]
                idx += 1

        return retval

    # We redefine self.reference() to handle the escape sequences
    # We redefine self.truthy() to validate empty strings as well
