import sys
import operator
from random import choices, seed

class Roller:
  dice_sets = {
    "%": { f"{x}":x for x in range(0,10) },
    "%%": { f"{x}0":(x * 10) for x in range(0,10) },
    "%%%": { f"{x}00":(x * 100) for x in range(0,10) },
    "6a": [2, 3, 3, 4, 4, 5],
    "F": {'+': 1, '-': -1, ' ': 0}
  }

  def __init__(self, seed_value=None):
    if seed_value:
      seed(seed_value)

  def d_roll(self, quantity, dice_set, *modifiers):
    """Returns the results of rolling a (quantity) number of (sides)-sided dice"""
    quantity = self.get_value(quantity)
    set_name = dice_set = self.get_value(dice_set)
    if '%' in str(dice_set):
      return self.percentile_roll(quantity, dice_set)
    elif dice_set in self.dice_sets:
      dice_set = self.dice_sets[dice_set]
    else:
      dice_set = list(range(1, dice_set+1))
    (values, report) = self.general_roll(quantity, dice_set, modifiers)
    return (values, f"rolled {quantity}d{''.join(modifiers)}{set_name}: {report}")

  def z_roll(self, quantity, sides, *modifiers):
    """Returns the results of rolling a (quantity) number of (sides)-sided dice, numbered 0 to sides-1"""
    quantity = self.get_value(quantity)
    set_name = sides = self.get_value(sides)
    (values, report) = self.general_roll(quantity, list(range(0, sides)), modifiers)
    return (values, f"rolled {quantity}d{''.join(modifiers)}{set_name}: {report}")

  def highest(self, dice_result, amount):
    """Returns the highest (amount) number of results in dice_result"""
    dice_values = self.get_list(dice_result)
    amount = self.get_value(amount)
    highest = sorted(dice_values)[-amount:]
    return (highest, f"{self.get_report(dice_result)}; highest {amount}: {self.dice_reporter(highest)}")

  def lowest(self, dice_result, amount):
    """Returns the highest (amount) number of results in dice_result"""
    dice_values = self.get_list(dice_result)
    amount = self.get_value(amount)
    lowest = sorted(dice_values)[:amount]
    return (lowest, f"{self.get_report(dice_result)}; lowest {amount}: {self.dice_reporter(lowest)}")

  def compare(self, dice_result, value, comparator):
    comp = {
      '>': operator.gt,
      '>=': operator.ge,
      '<': operator.lt,
      '<=': operator.le,
      '=': operator.eq,
      '==': operator.eq,
      '!=': operator.ne
    }
    comp_strings = {
      '>': "greater than",
      '>=': "greater than or equal",
      '<': "less than",
      '<=': "less than or equal",
      '=': "equal",
      '==': "equal",
      "!=": "not equal"
    }
    dice_values = self.get_list(dice_result)
    value = self.get_value(value)
    result = [x for x in dice_values if comp[comparator](x, value)]
    report = f"{len(result) if len(result) > 0 else 'None'} were {comp_strings[comparator]} to {value}"
    if len(result) > 0:
      report += f" ({self.get_report(result)})"
    return (result, f"{self.get_report(dice_result)}; {report}")

  def math(self, dice_result, value, math_op):
    def ceildiv(a, b):
      "This works because Python's division is true floor division. This preserves integer accuracy without resorting to floats"
      return -(-a // b)

    def truncdiv(a, b):
      "For the default C-Style division"
      return int(a / b)

    ops = {
      '*': operator.mul,
      '/': truncdiv,
      '/-': operator.floordiv,
      '/+': ceildiv,
      '+': operator.add,
      '-': operator.sub,
    }
    dice_value = self.get_value(dice_result)
    value = self.get_value(value)
    result = ops[math_op](dice_value, value)
    return ([result], f"{self.get_report(dice_result)}; {dice_value} {math_op} {value} = {result}")
    
  def percentile_roll(self, quantity, dice_set):
    """For when you want that authentic percentile dice experience"""
    values = []
    report = []
    for _ in range(0, quantity):
      sub_set = dice_set
      rolled_faces = []
      while sub_set:
        rolled_faces += choices(list(self.dice_sets[sub_set]))
        sub_set = sub_set[:-1]
      value = sum(int(x) for x in rolled_faces)
      if (value == 0):
        value = 10 ** len(dice_set)
      values += [value]
      report += [f"{'+'.join(rolled_faces)}={value}"]
    dice_text = f"{self.dice_reporter(report)}"
    return (values, dice_text)

  def detonate(self, value, seq, modifiers):
    """Handles dice explosions and implosions, penetrating and non-penetrating (the .,-,+,* modifiers)"""
    acc = [value]
    report = [f"{value}"]
    min_val = min(list(seq))
    max_val = max(list(seq))

    "Note that (if *) returns early, while (if +) falls through to (if -); this is intentional"
    if '*' in modifiers:
      while acc[-1] == max_val:
        new_value = self.general_roll(1,seq)[0][0]
        acc += [new_value]
        report.append(f"{new_value}")
      return(acc, report)

    if '+' in modifiers and acc[0] == max_val:
      while acc[-1] >= max_val - 1 if '.' in modifiers else acc[-1] == max_val:
        new_value = self.general_roll(1,seq)[0][0]
        new_value = new_value - 1 if '.' in modifiers else new_value
        acc += [new_value]
      report = [f"{'+'.join(str(x) for x in acc)}={sum(acc)}"]
      acc = [sum(acc)]
    if '-' in modifiers and acc[0] == min_val:
      acc = [0]
      acc.append(self.general_roll(1,seq)[0][0])
      while acc[-1] >= max_val -1 if '.' in modifiers else acc[-1] == max_val:
        new_value = self.general_roll(1,seq)[0][0]
        new_value = new_value - 1 if '.' in modifiers else new_value
        acc += [new_value]
      acc = [(-1 * x) for x in acc]
      "Creates the dice text report for imploding dice, such that imploding 4s resulting in 1,4,4,2 will become 0-4-4-2=-10"
      report = [f"{acc[0]}" + f"{''.join(str(x) if x != 0 else '-0' for x in acc[1:])}={sum(acc)}"]
      acc = [sum(acc)]
    return (acc, report)

  def get_value(self, input):
    """If given a tuple of (dice-value-sequence, str) returns sum(dice-value-sequence); else just returns the input unmodified"""
    return sum(input[0]) if isinstance(input, tuple) else input
    
  def get_list(self, input):
    """If given a tuple of (dice-value-sequence, str) returns dice-value-sequence; else returns the input in a single-item list"""
    return input[0] if isinstance(input, tuple) else [input]

  def get_report(self, input):
    """If given a tuple of (dice-value-sequence, str) returns str; else returns input as string"""
    return input[1] if isinstance(input, tuple) else f"{input}"

  def general_roll(self, quantity, seq, modifiers=None):
    """Returns an array of the results of picking a (quantity) number of random values from the given sequence"""
    rolled_faces = choices(list(seq), k=quantity)

    if modifiers and ('+' or '*' or '-' in modifiers):
      values = []
      dice_text = []
      for die in rolled_faces:
        value, report = self.detonate(die, seq, modifiers)
        values += value
        dice_text += report
      report = f"{self.dice_reporter(dice_text)}"
      return (values, report)

    if isinstance(seq, dict):
      values = [seq[x] for x in rolled_faces]
    else:
      values = rolled_faces
    dice_text = f"{self.dice_reporter(rolled_faces)}"
    return (values, dice_text)
  
  def dice_reporter(self, rolled_faces):
    return f"{' '.join([f'[{x}]' for x in rolled_faces])}"

if __name__ == "__main__":
  roller = Roller(1)
  print("Percentile:")
  print(roller.d_roll(10, "%%"))
  print(roller.d_roll(5, "%%%"))
  print("General:")
  print(roller.d_roll(5,6))
  print("FATE:")
  print(roller.d_roll(4, 'F'))
  print("Averaging:")
  print(roller.d_roll(10,'6a'))
  print("Explosion test:")
  print(roller.d_roll(40,4,'+'))
  print("Dot explosion test:")
  print(roller.d_roll(40,4,'+','.'))
  print("Star explosion test:")
  print(roller.d_roll(40,4,'*'))
  print("Implosion test:")
  print(roller.d_roll(40,4,'-'))
  print("Dot implosion test:")
  print(roller.d_roll(40,4,'.', '-'))
  print("Z rolls")
  print("General:")
  print(roller.z_roll(10,4))
  print("Explosion:")
  print(roller.z_roll(10,4,'+'))
  print("Star explosion:")
  print(roller.z_roll(10,4, '*'))
  print("Implosion:")
  print(roller.z_roll(10,4, '-'))

  print("Operations")
  res = roller.d_roll(10,10)
  print(res)
  print("Highest:")
  print(roller.highest(res, 3))
  print(roller.highest(5,2))
  print("Lowest:")
  print(roller.lowest(res, 3))
  print(roller.lowest(5,2))
  print("GTE:")
  print(roller.compare(res, 6, '>='))
  print(roller.compare(5,2, '>='))
  print(roller.compare(3,5, '>='))
  print("Addition")
  print(roller.math(res, 3, '+'))
  print(roller.math(5,3, '+'))
