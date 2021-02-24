import math
import operator as op
# these two are just for initial testing and should be removed later
from Parser import Parser
from MathSymbols import math_symbol_table, math_tokenize

class Environment(dict):
  def __init__(self, params=(), args=(), outer=None):
    self.update(zip(params, args))
    self.outer = outer
  
  def find(self, var):
    return self if (var in self) else self.outer.find(var)

class Procedure(object):
  def __init__(self, params, body, env):
    self.params = params
    self.body = body
    self.env = env
  
  def __call__(self, *args):
    return eval(self.body, Environment(self.params, args, self.env))


def standard_env():
  env = {}
  env.update(vars(math)) # sin, cos, sqrt, pi, others
  env.update({
    "+": op.add,
    "-": op.sub,
    "*": op.mul,
    "/": op.truediv,
    "**": op.pow,
    "=": op.eq,
    "append": op.add,
    "apply": lambda proc, args: proc(*args),
    "car": lambda x: x[0],
    "cdr": lambda x: x[1:],
    "cons": lambda x,y: [x] + y,
    "eq?": op.is_,
    "equal?": op.eq,
    "length": len,
    "list": lambda *x: list(x),
    "list?": lambda x: isinstance(x, list),
    "map": map,
    "min": min,
    "not": op.not_,
    "null?": lambda x: x == [],
    "number?": lambda x: isinstance(x, (float, int)),
    "print": print,
    "procedure?": callable,
    "round": round,
    "symbol?": lambda x: isinstance(x, str)
  })
  return env

global_env = standard_env()

def tokenize(program):
  return program.replace("(", " ( ").replace(")", " ) ").split()

def read(program):
  return read_from_tokens(tokenize(program))

def read_from_tokens(tokens):
  if len(tokens) == 0:
    return
  token = tokens.pop(0)
  if token == "(":
    L = []
    while tokens[0] != ")":
      L.append(read_from_tokens(tokens))
    tokens.pop(0)
    return L
  elif token == ")":
    raise SyntaxError("unexpected )")
  else:
    return atom(token)

def eval(exp, env = global_env):
  if exp is None:
    return
  elif isinstance(exp, str):
    return env[exp]
  elif isinstance(exp, (float, int)):
    return exp
  elif exp[0] == "if":
    (_, test, conseq, alt) = exp
    if_exp = (conseq if eval(test, env) else alt)
    return eval(if_exp, env)
  elif exp[0] == "define":
    (_, symbol, def_exp) = exp
    env[symbol] = eval(def_exp, env)
  else:
    proc = eval(exp[0], env)
    args = [eval(arg, env) for arg in exp[1:]]
    return proc(*args)

def atom(token):
  try: return int(token)
  except ValueError:
    try: return float(token)
    except ValueError:
      return token

def scheme_str(exp):
  if isinstance(exp, list):
    return f"( {' '.join(map(scheme_str, exp))} )"
  else:
    return str(exp)

def repl(prompt="lis.py>"):
  while True:
    val = eval(read(input(prompt)))
    if val is not None:
      print(scheme_str(val))

def test(program):
  math_tokenizer = math_tokenize(program, math_symbol_table())
  parser = Parser(math_tokenizer)
  sexp = str(parser.process_next_symbol())
  print(read(sexp))
  print(eval(read(sexp)))

if __name__ == "__main__":
  repl()
