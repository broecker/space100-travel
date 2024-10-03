# space100-travel
Better in-system travel for the D100 Space Tabletop RPG

## About
This little tool creates a table that replaces the repetitive roll, then check
for success rule when travelling within a star system in D100:Space. Instead,
you roll cross reference your skill with the requested distance once on the
generated table, roll once and read back the cost required.

The numbers are derived by simulating travel for each skill/distance
combination ten thousand times, then simplifying the results.

## How to use the generated tables

1. Determine the /Total Skill/ of your ship: Int + CM + Pilot skill. If your
   Total Skill falls between two rows, select the lower row.

1. Determine the Distance you want to travel.

1. Cross reference the Total Skill and Distance on the table, this will show a
   3x3 subtable. Roll a D9 (or D10, ignoring 0s) and read the value, top-left
   to bottom-right. This is the PL you expend travelling to your destination.

1. Arrive at the destination and pay the cost. The usual rules apply: if your
   PL drops below 0, you need to take it out of the life support. You /cannot/
   generate power during this travel. If your life support drops to 0, you are
   stranded in space.

### Example

1. Your captain has an Int of 50, no pilot skill and the ship's CM is -5. The
   Total Skill is 45 (50 -5 +0). You will use the 40 row in the table.

1. In the Floxtar System (base game) you want to travel from Horus Station\
   (Zone 3) to Draymo (Zone 10). The Distance is 7.

1. Cross-referencing 40 and 7 on the table gives you the following subtable:
   > 10 12 14  
   > 15 16 18  
   > 20 22 29 

   You roll a 4 on the D10 and read 15. This is the number of PL you have to
   pay. If you only had 12 PL left, the remaining 3 PL would have been drawn
   from the life support.


## Hacking

This script can easily be extended to any game situation or rule that asks you
to roll repeatedly with success.

I've not seen the multi-dimensional matrices (i.e. a table within a table)
often before. Mythic Gamemaster Emulator uses just three values, not the full
nine. However, I think this can be reused for other situations, as long as the
inner table is not too large or complicated. Ten values is already getting too
crowded, hence the D9 roll. 

## Developer Notes

Developing this small script was fun and followed in three stages:

1. Sampling the results; i.e. playing the game and collecting the results for
   each skill/distance combination. This was the easy part and already included
   some debugging prints that show the result distribution. 

1. The next step was resampling each generated distribution. I defined the
   number of buckets (initially ten) first, then accumulated results until I
   hit the desired bucket number. There are probably smarter ways and/or use
   numpy, but this is nice and quick for the data I'm working with.

1. Finally, printing and formatting everything nicely was the last step. The
   major insight was that I could stack tables within tables by keeping the
   second one small enough.

   Formatting itself reminded me of the enormous effort put into the printer of
   the Difference Engine nobody talks about but added so much additional
   complexity.
