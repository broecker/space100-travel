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

import random

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
			if random.randint(1, 100) <= target_roll:
				d -= 1
			pl += 1

		results.append(pl)
	return sorted(results)


def calculate_percentages(results: list[int]) -> None:
	"""Calculates percentages and prints a histogram for the result."""
	counts = {}
	for r in results:
		try:
			counts[r] += 1
		except KeyError:
			counts[r] = 1

	running_total = 0
	for k in counts.keys():
		rel_val = float(counts[k]) / len(results)
		dots = '*' * int(rel_val * 20)

		# Ignore all results below 1%
		if rel_val < 0.01:
			continue

		absolute_percentage = round(rel_val*100)
		running_total += absolute_percentage
		s = '{0:2d} {1:5d} ({2:2d}% / {3:2d}%) {04:20s}'.format(
			k,
			counts[k],
			absolute_percentage,
			running_total,
			dots)
		print(s)

	# TODO: resample the resulting table/histogram into a D10 table based on the
	# running_total


def main():
	print('Hello traveller!')

	intelligence = 30
	cruise_mod = 10
	pilot_skill = 0
	distance = 5
	print(f'Testing for: INT {intelligence} CM {cruise_mod} pilot {pilot_skill}')
	print(f'Travelling {distance} areas.')

	results = cruise_tests(intelligence + cruise_mod + pilot_skill, distance, 100000)
	calculate_percentages(results)


if __name__ == '__main__':
	main()