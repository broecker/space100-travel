# Copyright 2024 Markus Broecker
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""This is a small tool to improve D100 Space's intra-system travel.

Rather than having to roll for success/failure and power loss for every area
travelled, this tool precalculates tables for the current total abilitiy level
and distance travelled. To retain some kind of variation, it creates smaller
D10 lookup tables that return the total power loss (PL) for this distance
travelled.
"""

import dataclasses
import math
import random

# The number of Monte-Carlo samples to run per table entry. Higher-values yield
# statistically better results but is much slower to calculate.
SAMPLES = 50000

@dataclasses.dataclass
class Sample:
	# How many samples were counted.
	count:								int
	# This sample's percentage of the whole.
	absolute_percentage:	int = 0
	# How many other samples came before.
	running_percentage:   int = 0


def cruise_tests(target_roll: int, distance: int, rolls: int = 100) -> list[int]:
	"""Performs successive cruise tests until the ship arrives at the distance.

		target_roll = Int + CM + Pilot skill
		distance: distance to travel
		rolls: how many rolls to perform
		Returns a list of PL /losses/. It will always return /rolls/ results.
	"""
	results = []

	for _ in range(0, rolls):
		d = distance

		pl = 0
		while d > 0:
			roll = random.randint(1, 100)
			if roll  <= target_roll or roll == 1:
				d -= 1
			pl += 1

		results.append(pl)
	return sorted(results)


def make_histogram(results: list[int]) -> dict[int, Sample]:
	"""Returns a dict of Samples, keyed by PL."""
	counts = {}
	for r in results:
		try:
			counts[r].count += 1
		except KeyError:
			counts[r] = Sample(count=1)


	running_total = 0
	for k in counts:
		rel_val = float(counts[k].count) / SAMPLES

		counts[k].absolute_percentage = round(rel_val*100)
		running_total += counts[k].absolute_percentage
		counts[k].running_percentage = running_total

	return counts


def resample_into_d9(histo: dict[int, Sample]) -> list[int]:
	"""Resamples a histogram into a D9 table."""

	# Invert the histogram, to be keyed by running percentage.
	pl_by_running_total = {}
	for k in histo:
		pl_by_running_total[histo[k].running_percentage] = k

	# The index into the result is found by dividing by 11, yielding 9 results.
	# We can overwrite the last results, yielding always the highest cost.
	results = [0] * 9
	for k in pl_by_running_total:
		idx = math.floor(k/11) - 1
		results[idx] = pl_by_running_total[k]

	# We now have to fill in the 0's in the list by copying over values from the
	# left until all empty pockets are filled. These 0s can happen when there are
	# gaps in the results.
	for i in range(1, 9):
		if results[i] == 0:
			results[i] = results[i-1]

	for i in range(8, -1, -1):
		if results[i] == 0:
			results[i] = results[i+1]

	return results


def print_percentages(histo: dict[int, Sample]) -> None:
	"""Calculates percentages and prints a histogram for the result."""

	d9 = resample_into_d9(histo)

	for k in histo:
		# Ignore small sample sizes.
		if histo[k].count < SAMPLES * 0.02:
			continue

		dots = '*' * round(histo[k].absolute_percentage / 10)
		s = '{0:2d} {1:5d} ({2:2d}% / {3:2d}%) {4:20s}'.format(
			k,
			histo[k].count,
			histo[k].absolute_percentage,
			histo[k].running_percentage,
			dots)
		print(s)


def print_table(table: dict[tuple[int, int], list[int]]) -> None:
	"""Prints a table of D9s, indexed by skill and distance."""


	print(' Skill                                 Distance')
	print('          2          3          4          5          6          7          8          9')

	for k in range(20, 110, 10):
		# We need 3 prints for every line, due to D9, as we split it into 3 lines
		# of 3 entries each.
		line0 = '      '
		line1 = ' {0:3d}  '.format(k)
		line2 = '      '

		for d in range(2, 10):
			d9 = table[(k, d)]
			def make_table_row(row: int) -> str:
				assert row >= 0 < 3
				k = row*3
				return '{0:2d} {1:2d} {2:2d}'.format(d9[k+0], d9[k+1], d9[k+2])

			line0 += make_table_row(0) + '   '
			line1 += make_table_row(1) + '   '
			line2 += make_table_row(2) + '   '

		print(line0)
		print(line1)
		print(line2)

		print()	


def main():
	print('Hello traveller!')

	# D9s for the whole table.
	table = {} #: dict[tuple[2], list[int]] = {}
	for distance in range(2, 10):
		for skill in range(20, 110, 10):
			# print(f'Total skill: {skill}, distance {distance}')
			results = cruise_tests(skill, distance, SAMPLES)
			histo = make_histogram(results)
			d9 = resample_into_d9(histo)
			table[(skill, distance)] = d9

	print_table(table)


if __name__ == '__main__':
	main()