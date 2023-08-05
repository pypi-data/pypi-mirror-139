import re
from typing import Callable, Dict, List, Optional, Union

from .calculator import Calc
from .errors import InvalidFractionError, InvalidInputError
from .rational_number import RationalNumber


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
                transformed.append(Fractalgebra.parse_input(input_list[i]))
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
            return Fractalgebra.from_mixed_fraction(clean_results)
