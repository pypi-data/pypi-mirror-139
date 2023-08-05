from dataclasses import dataclass
from typing import Dict, Optional

from .errors import InvalidFractionError


@dataclass
class RationalNumber:
    numerator: int
    denominator: int

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
