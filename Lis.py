import math
import operator as op
import sys

class environment(dict):
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
    return eval(self.body, environment(self.params, args, self.env))

def standard_env():
  env = environment()
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
    "symbol?": lambda x: isinstance(x, str),
    "quit": lambda: sys.exit(0)
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

def eval(s_exp, env=global_env):
  if isinstance(s_exp, str):        # variable
    return env.find(s_exp)[s_exp]
  elif not isinstance(s_exp, list): # constant
    return s_exp
  op, *args = s_exp
  if op == "quote":                 # quotation
    return args[0]
  elif op == "if":                  # conditional
    (test, true_res, false_res) = args
    exp = (true_res if eval(test, env) else false_res)
    return eval(exp, env)
  elif op == "define":              # definition
    (symbol, exp) = args
    env[symbol] = eval(exp, env)
  elif op == "set!":                # assignment
    (symbol, exp) = args
    env.find(symbol)[symbol] = eval(exp, env)
  elif op == "lambda":              # procedure
    (params, body) = args
    return Procedure(params, body, env)
  else:
    proc = eval(op, env)
    vals = [eval(arg, env) for arg in args]
    return proc(*vals)

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

def exec(s_exp, env=global_env):
  """Wraps read-eval for external client convenience"""
  return eval(read(s_exp), env)

if __name__ == "__main__":
  repl()
