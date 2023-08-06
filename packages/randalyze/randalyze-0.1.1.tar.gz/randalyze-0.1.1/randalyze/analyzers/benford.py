from math import log10, floor, ceil
from typing import Sequence


class BenfordAnalyzer:

    def __init__(self):
        self._first_digit_counts = list(0 for i in range(10))
        self._second_digit_counts = list(0 for i in range(10))

        self._expected_distribution = None

    @staticmethod
    def digit_probability(digit: int) -> float:
        if digit < 1 or digit > 9:
            raise ValueError('digit must be in the range [1..9]')

        return log10(1 + (1 / digit))

    @property
    def expected_distribution(self) -> Sequence[float]:
        if not self._expected_distribution:
            self._expected_distribution = [0.0] + [log10(1 + (1 / d)) for d in range(1, 10)]

        return self._expected_distribution

    def add_number(self, number: float) -> None:
        """
        Add a number to the analyzer.
        :param number:
        :return:
        """
        number_string = str(number).replace('0', '').replace('.', '')
        first_digit = int(number_string[0]) if number_string else None
        second_digit = int(number_string[1]) if number_string and len(number_string) > 1 else None

        if first_digit:
            self._first_digit_counts[first_digit] = self._first_digit_counts[first_digit] + 1

        if second_digit:
            self._second_digit_counts[second_digit] = self._second_digit_counts[second_digit] + 1

    def add_numbers(self, numbers: Sequence[float]) -> None:
        """
        Add a collection of numbers to the analyzer.
        :param numbers:
        :return:
        """
        if numbers:
            for number in numbers:
                self.add_number(number)

    @property
    def first_digit_counts(self) -> Sequence[int]:
        """
        The counts of each of the first digits from 0..9 for all of the numbers added to the analyzer.
        :return: A list of ten integers, representing the total counts of each first digit from 0.9
        respectively.
        """
        return [d for d in self._first_digit_counts]

    @property
    def first_digit_distribution(self) -> Sequence[float]:
        """
        The proportions of the total count of first digits for all of the numbers added to the analyzer.
        :return: A list of ten floating point numbers, representing the proportion of the total
        count represented by each digit.
        """
        total = sum(self._first_digit_counts)
        return [count / total if total else 1 for count in self._first_digit_counts]

    @property
    def second_digit_counts(self) -> Sequence[int]:
        return [d for d in self._second_digit_counts]

    def matches_distribution(self, tolerance_percent: float = 5.0) -> bool:
        """
        Returns true if the distribution matches Benford's law.
        :param tolerance_percent:
        :return:
        """
        total_numbers = sum(self.first_digit_counts)
        expected_counts = [c * total_numbers for c in self.expected_distribution]

        matches = True

        for d in range(1, 9):
            digit_count = 1.0 * self._first_digit_counts[d]
            min_digit_count = floor(expected_counts[d] * (1 - (tolerance_percent / 100.0)))
            max_digit_count = ceil(expected_counts[d] * (1 + (tolerance_percent / 100.0)))

            # print(f'{min_digit_count} <= {digit_count} <= {max_digit_count} -> {expected_counts[d]}')
            if not (min_digit_count <= digit_count <= max_digit_count):
                matches = False

        return matches
