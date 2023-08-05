import re
from dataclasses import dataclass
from typing import Callable, Dict, List,  Optional, Union


@dataclass
class RationalNumber:
    numerator: int
    denominator: int

    @staticmethod
    # uses the regex to parse a string into a RationalNumber
    def parse_input(input_string: str) -> "RationalNumber":
        # TODO make better regex that will validate edge cases
        pattern: re.Pattern = re.compile(
            r"(?P<whole>-?\d+_)?(?P<numer>-?\d+)(?P<denom>/-?\d+)?$"
        )
        match: Optional[re.Match] = pattern.match(input_string)
        if match is None:
            # TODO: make this a custom exception
            raise ValueError(f"Invalid input: {input_string}")
        else:
            match_results: Dict[str, Optional[str]] = match.groupdict()
            RationalNumber.clean_match_results(match_results)
            clean_results: Dict[str, int] = RationalNumber.clean_match_results(
                match_results
            )
            return RationalNumber.from_mixed_fraction(clean_results)

    @staticmethod
    # simplifies a RationalNumber with negative values and reduces it to lowest terms
    # TODO: make this an automatic validation when initializing a RationalNumber
    def reduced(rn: "RationalNumber") -> "RationalNumber":
        new_n: int = rn.numerator
        new_d: int = rn.denominator
        if new_d == 0:
            raise ZeroDivisionError("Parsing the input revealed a division by zero")
        if rn.numerator < 0 and rn.denominator < 0:
            new_n, new_d = rn.numerator * -1, rn.denominator * -1
        elif rn.numerator < 0 or rn.denominator < 0:
            new_n, new_d = abs(rn.numerator) * -1, abs(rn.denominator)
        greatest_common_factor: int = rn.gcf(new_n, new_d)
        reduced_n = new_n // greatest_common_factor
        reduced_d = new_d // greatest_common_factor
        return RationalNumber(numerator=reduced_n, denominator=reduced_d)

    @staticmethod
    # returns a mixed fraction string representation of a RationalNumber
    def as_mixed_fraction(rational_number: "RationalNumber") -> str:
        is_negative: bool = rational_number.numerator < 0
        whole: int = abs(rational_number.numerator) // rational_number.denominator
        numerator: int = abs(rational_number.numerator) % rational_number.denominator
        return_str = ""
        negative_part = "-" if is_negative else ""
        whole_part = f"{whole}" if whole > 0 else ""
        mixed_part = "_" if numerator > 0 and whole > 0 else ""
        fraction_part = (
            f"{numerator}/{rational_number.denominator}" if numerator > 0 else ""
        )
        return_str = negative_part + whole_part + mixed_part + fraction_part
        return return_str if len(return_str) > 0 else "0"

    @staticmethod
    # uses the Euclidean algorithm to find the greatest common factor of two numbers
    def gcf(x: int, y: int) -> int:
        while y != 0:
            x, y = y, abs(x - y)
        return x

    @staticmethod
    def clean_match_results(match_results: Dict[str, Optional[str]]) -> Dict[str, int]:
        """checks for nonsensical mixed numbers and reformats the results if valid"""

        # remove '/' and '_' from raw strings TODO: turn into dict comprehension
        ds: Dict[str, Optional[str]] = {"numer": match_results["numer"]}
        if match_results["denom"] is not None:
            ds["denom"] = match_results["denom"][1:]
        if match_results["whole"] is not None:
            ds["whole"] = match_results["whole"][:-1]

        int_d: Dict[str, int] = {k: int(v) for k, v in ds.items() if v is not None}
        if len(int_d) == 1:  # regex should only allow this if numer was passed
            if "numer" in int_d:
                int_d = {"whole": int_d["numer"]}
            elif "denom" in int_d:
                raise Exception(f"Unexpected input {str(match_results)}")
        if len(int_d) == 2:
            if "numer" not in int_d:
                raise InvalidFractionError(str(match_results), "numerator is missing!")
            if "denom" not in int_d:
                raise InvalidFractionError(
                    str(match_results), "denominator is missing!"
                )
        return int_d

    @staticmethod
    def from_mixed_fraction(mf_dict: Dict[str, int]) -> "RationalNumber":
        """ensures mixed number doesn't have wonky denominators or negative values"""
        if len(mf_dict) == 1:
            return RationalNumber(numerator=mf_dict["whole"], denominator=1)
        numer, denom = mf_dict["numer"], mf_dict["denom"]
        if denom == 0:
            raise ZeroDivisionError("Denominator cannot be zero!")
        if len(mf_dict) == 2:
            return RationalNumber(numerator=numer, denominator=denom)
        # TODO: possibly allow `whole -numer/-denom` but it's not really standard
        if numer < 0 or denom < 0:
            raise InvalidFractionError(
                str(mf_dict), "mixed fractions can't have a negative fraction part"
            )
        whole = mf_dict["whole"]
        is_negative: bool = whole < 0
        if is_negative:
            abs_whole = RationalNumber(numerator=abs(whole), denominator=1)
            positive_sum = Calc.add(
                abs_whole, RationalNumber(numerator=numer, denominator=denom)
            )
            return RationalNumber(
                numerator=positive_sum.numerator * -1,
                denominator=positive_sum.denominator,
            )
        return Calc.add(
            RationalNumber(numerator=whole, denominator=1),
            RationalNumber(numerator=numer, denominator=denom),
        )


class Calc:
    """Contains various utilities for fractalgebra"""

    @staticmethod
    def add(a: RationalNumber, b: RationalNumber) -> RationalNumber:
        """adds two rational numbers"""
        new_numerator = a.numerator * b.denominator + b.numerator * a.denominator
        new_denominator = a.denominator * b.denominator
        new_rational = RationalNumber(
            numerator=new_numerator, denominator=new_denominator
        )
        new_reduced = RationalNumber.reduced(new_rational)
        return new_reduced

    @staticmethod
    def subtract(a: RationalNumber, b: RationalNumber) -> RationalNumber:
        """subtracts two rational numbers"""
        return Calc.add(
            a, RationalNumber(numerator=-b.numerator, denominator=b.denominator)
        )

    @staticmethod
    def multiply(a: RationalNumber, b: RationalNumber) -> RationalNumber:
        """multiplies two rational numbers"""
        return RationalNumber.reduced(
            RationalNumber(
                numerator=(a.numerator * b.numerator),
                denominator=(a.denominator * b.denominator),
            )
        )

    @staticmethod
    def divide(a: RationalNumber, b: RationalNumber) -> RationalNumber:
        """divides two rational numbers"""
        return RationalNumber.reduced(
            RationalNumber(
                numerator=(a.numerator * b.denominator),
                denominator=(a.denominator * b.numerator),
            )
        )


class Fractalgebra:
    """top-level class for parsing the input string and returning the answer"""

    # TODO: make a fancier typing.Literal type for better validation
    op_dict: Dict[str, Callable[[RationalNumber, RationalNumber], RationalNumber]] = {
        "*": Calc.multiply,
        "+": Calc.add,
        "-": Calc.subtract,
        "/": Calc.divide,
    }

    @staticmethod
    # parse, validate, and return the answer as a mixed Fraction
    def solve(input_list: List[str]) -> str:
        """
        Parses the input list and returns the answer as a mixed fraction
        """
        is_empty_input = len(list(filter(lambda x: len(x) > 0, input_list))) == 0
        if is_empty_input:
            return ""
        transformed_list = Fractalgebra.transform_input(input_list)
        final_rational = Fractalgebra.reduce_list(transformed_list)
        return RationalNumber.as_mixed_fraction(final_rational)

    @staticmethod
    # returns a List[Union[RationalNumber, AllowedOps]];
    # raises InvalidInputError if the input doesn't follow a parseable pattern
    def transform_input(input_list: List[str]) -> List[Union[RationalNumber, str]]:
        transformed: List[Union[RationalNumber, str]] = []
        for i in range(len(input_list)):
            if i % 2 == 0:
                transformed.append(RationalNumber.parse_input(input_list[i]))
            else:
                if input_list[i] not in Fractalgebra.op_dict:
                    raise InvalidInputError(
                        f"""Operator {input_list[i]} is not a valid operator"""
                    )
                transformed.append(input_list[i])
        if not isinstance(transformed[-1], RationalNumber):
            raise InvalidInputError(
                "Last argument should be a fraction, not an operator"
            )
        return transformed

    @staticmethod
    # reduces the list of rational numbers and operators to a single rational number
    # using order of operations
    def reduce_list(input_list: List[Union[RationalNumber, str]]) -> RationalNumber:
        pemdas: List[str] = ["*", "/", "+", "-"]
        updated_list: List[Union[RationalNumber, str]] = input_list.copy()
        for op in pemdas:
            temp_list = updated_list.copy()
            i = 0
            while i < len(temp_list) - 1:
                if temp_list[i] == op:
                    prev_rational = temp_list[i - 1]
                    next_rational = temp_list[i + 1]
                    assert isinstance(prev_rational, RationalNumber)
                    assert isinstance(next_rational, RationalNumber)
                    new_rational = Fractalgebra.op_dict[op](
                        prev_rational, next_rational
                    )
                    temp_list = temp_list[: i - 1] + [new_rational] + temp_list[i + 2 :]
                else:
                    i += 1
            updated_list = temp_list.copy()
            if len(updated_list) == 1:
                break
        if isinstance(updated_list[0], RationalNumber):
            return updated_list[0]
        else:
            raise Exception("Unexpected error parsing :(")


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
