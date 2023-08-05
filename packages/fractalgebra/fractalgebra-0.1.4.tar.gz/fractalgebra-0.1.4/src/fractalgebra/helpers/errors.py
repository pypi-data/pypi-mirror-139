from typing import Optional, Union


class InvalidFractionError(Exception):
    """Raised when a fraction is invalid
    Attributes:
        infraction -- the bad thing
        message -- explanation of the error
        suggestion -- a suggestion for how to fix the error
    """

    def __init__(
        self,
        infraction: Union[int, str],
        message: str,
        suggestion: Optional[str] = None,
    ):
        self.infraction = infraction
        self.message = message
        self.suggestion = suggestion
        super().__init__(self.message)

    def __str__(self) -> str:
        base_string = f"{self.message}: {self.infraction}"
        if self.suggestion is not None:
            base_string = f"{base_string} ({self.suggestion})"
        return base_string


class InvalidInputError(Exception):
    """indicates to the user an invalid input"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
