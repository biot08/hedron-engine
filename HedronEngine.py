from Parser import Parser
from DiceSymbols import dice_symbol_table, dice_token_gen
from Lis import Environment, standard_env, exec
from Roller import Roller

roller = Roller()
parser = Parser(dice_token_gen, dice_symbol_table())
def dice_env():
  env = Environment((), (), standard_env())
  env.update({
    'd': roller.d_roll,
    'z': roller.z_roll,
    '+': lambda left, right: roller.math(left, right, '+'),
    '-': lambda left, right: roller.math(left, right, '-'),
    '*': lambda left, right: roller.math(left, right, '*'),
    '/': lambda left, right: roller.math(left, right, '/'),
    '/+': lambda left, right: roller.math(left, right, '/+'),
    '/-': lambda left, right: roller.math(left, right, '/-'),
    '<': lambda left, right: roller.compare(left, right, '<'),
    '<=': lambda left, right: roller.compare(left, right, '<='),
    '>': lambda left, right: roller.compare(left, right, '>'),
    '>=': lambda left, right: roller.compare(left, right, '>='),
    '=': lambda left, right: roller.compare(left, right, '='),
    '==': lambda left, right: roller.compare(left, right, '=='),
    '!=': lambda left, right: roller.compare(left, right, '!='),
    "H": roller.highest,
    "L": roller.lowest,
    "finalize": roller.finalize
  })
  return env

def engine(input):
  s_exp = str(parser.parse(input))
  s_exp = f"(finalize {parser.parse(input)})"
  return exec(s_exp, dice_env())

if __name__ == "__main__":
  pass