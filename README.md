# THE HEDRON ENGINE

The Hedron Engine is a full-featured dice rolling engine, meant to be flexible enough to be useful for most gaming systems.

## Usage

Import 'engine' from HedronEngine.py. If you give it a syntactically correct dice request (a string), it will return a tuple of (value, report), where value is the the final result of the dice roll and report will show the operations and results of running the request. For example, if you run engine("3d6") you will get back a number that is the result of summing those three values, and the report will be a string displaying each of the dice values rolled.

## Request Syntax

### The basic rolls
ndX: Rolls n number of dice, each with X number of sides, numbered 1 to X.

nzX: Rolls n number of dice, each with X number of sides, numbered 0 to X-1.

ndF: Rolls FATE/FUDGE dice

nd6a: Rolls n number of 'averaging' dice. An averaging die is a six-sided die where the faces read 2, 3, 3, 4, 4, 5

nd%%: Rolls n number of percentile pairs, each pair containing the tens and ones place

nd%%%: Rolls n number of percentile triads, each triad consisting of the thousands place, the tens place, and the ones place.

### Math
The engine supports the basic math operators of + - * / as well as grouping using open and closed parenthesis. If a math operator is applied to multiple dice being rolled, such as 3d6, the dice will be summed before performing the math operation.

Division by default truncates the decimal part. This behaviour can be shifted by following it with a + or - symbol. /+ will always round up (towards positive infinity), while /- will always round down (towards negative infinity)

Division by zero will return zero.

### Comparators
The engine supports > >= <= < != and == operations. If used between two values, for example 1 > 0, the engine will return 1 for true or 0 for false.

If used against a dice roll, for example 3d6, the comparison will be done against all the results of the dice roll, and will return the number of dice meeting the condition. For exampe, if you run '3d6 > 2', and the dice values are 3,1,6 the result will be 2, the number of dice which are greater than two.

### Other Operators
Hn: Will pick the n number of highest values. Used after a dice roll, e.g. '3d6H1' will return the highest value rolled. '4d6H3' is popular for rolling DnD attribute values for chargen.

Ln: Will pick the n number of lowest values. Used afte ra dice roll, e.g. '3d6L1' will return the lowest value rolled.

### Advanced rolls
nd+X: Rolls n number of exploding X-sided dice. If a die rolls its maximum value, it is rolled again, and that result is added to the value for that die. This can happen multiple times. For example, if 3d+6 results in an initial run of 3,1,6, the six will be re-rolled, and the new result added to it. So if the re-roll is, for example, 5, the final result will be 3,1,6+5=11.

nd.+X: Rolls n number of penetrating exploding X-sided dice. If a die rolls its maximum value, it is rolled again. The result - 1 is added to the value for that die. This can happen multiple times. For example, if 3d.+6 results in an initial run of 3,1,6, the six will be re-rolled, and the new result - 1 will be added to it. So if the re-roll is, for example, 5, the final result will be 3,1,6+5-1=10.

nd*X: Rolls n number of exploding X-sided dice. If a die rolls its maximum value, it is rolled again. This result is treated as a new die, and can also explode. So for example, for 3d6, if the result is 3,1,6, the six will be rolled again to produce a new value. In this example, if that new die roll results in a 5, the end result will be 3,1,6,5.

nd-X: Rolls n number of imploding X-sided dice. If a die rolls its minimum value, it is treated as a zero, and rolled again. That new result is subtracted from the value of that die. If on the re-roll, the die rolls its maximum value, it will be rolled again, continuing to subtract from the value until the die rolls a value besides its maximum. So for example, for 3d6, if the result is 3,1,6, the 1 will be treated as a zero and rolled again. If the new value is a five, the final result will be 3,0-5=-5,6.

nd.-X: Rolls n number of penetrating imploding X-sided dice. If a die rolls its minimum value, it is treated as a zero, and rolled again. That new result + 1 is subtracted from the value of that die. If on the re-roll, the die rolls its maximum value, it will be rolled again, continuing to subtract from the value until the die rolls a value besides its maximum. So for example, for 3d6, if the result is 3,1,6, the 1 will be treated as a zero and rolled again. If the new value is a five, the final result will be 3,0-(5+1)=-4,6.
