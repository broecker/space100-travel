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
import random

SAMPLES = 20000

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


def print_percentages(histo: dict[int, Sample]) -> None:
	"""Calculates percentages and prints a histogram for the result."""
	for k in histo:
		# Ignore small sample sizes.
		if histo[k].count < SAMPLES * 0.02:
			continue

		dots = '*' * round(histo[k].absolute_percentage / 10)
		s = '{0:2d} {1:5d} ({2:2d}% / {3:2d}%) {04:20s}'.format(
			k,
			histo[k].count,
			histo[k].absolute_percentage,
			histo[k].running_percentage,
			dots)
		print(s)

	# TODO: resample the resulting table/histogram into a D10 table based on the
	# running_total


def main():
	print('Hello traveller!')

	distance = 4
	total_skill = 50

	print(f'Total skill: {total_skill}, distance {distance}')
	results = cruise_tests(total_skill, distance, SAMPLES)
	histo = make_histogram(results)
	print_percentages(histo)


if __name__ == '__main__':
	main()