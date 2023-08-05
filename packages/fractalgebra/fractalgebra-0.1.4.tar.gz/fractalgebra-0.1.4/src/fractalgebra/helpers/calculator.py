from .rational_number import RationalNumber


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
