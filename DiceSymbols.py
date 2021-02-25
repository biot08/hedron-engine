import re
from Parser import SymbolTable

def dice_token_gen(program, symbol_table):
  token_pat = re.compile(r"\s*(?:(6a|%{2,3}|F|\d+)|(/-|/\+|>=|<=|!=|==|.))")
  for number, operator in token_pat.findall(program):
    if number:
      symbol = symbol_table.get("(literal)")
      yield symbol(number)
    elif operator:
      symbol = symbol_table.get(operator)
      if not symbol:
        raise SyntaxError("Unknown operator")
      yield symbol()
  symbol = symbol_table.get("(end)")
  yield symbol()

def dice_symbol_table():
  symbol_table = SymbolTable()
  symbol_table.add_infix("v", 10)
  symbol_table.add_infix("^", 10)
  symbol_table.add_infix("<", 20)
  symbol_table.add_infix("<=", 20)
  symbol_table.add_infix(">", 20)
  symbol_table.add_infix(">=", 20)
  symbol_table.add_infix("==", 20)
  symbol_table.add_infix("=", 20)
  symbol_table.add_infix("!=", 20)
  symbol_table.add_infix("+", 30)
  symbol_table.add_infix("-", 30)
  def minus_nud(self, parser):
    self.first = parser.next(100)
    self.value = f"-{self.first.value}"
    self.id = "(literal)"
    return self
  symbol_table.add_nud("-", minus_nud)
  symbol_table.add_infix("*", 40)
  symbol_table.add_infix("/", 40)
  symbol_table.add_infix("/+", 40)
  symbol_table.add_infix("/-", 40)
  symbol_table.add_infix("H", 55)
  symbol_table.add_infix("L", 55)
  symbol_table.add_infix("#", 55)
  symbol_table.add_infix("d", 60)
  symbol_table.add_infix("z", 60)
  def dz_led(self, left, parser):
    """Note to self: throw SyntaxError if allowed_operators are being used with wrong dice types"""
    """Note to self: z should reject anything other than number dice set"""
    bp = 60
    if self.id == "d":
      allowed_operators = ["+", "-", "*", "."]
    elif self.id == "z":
      allowed_operators = ["+", "-", "*"]
    self.first = left
    operators = set()
    if parser.token.id != "(literal)" or parser.token.id != "(":
      while True:
        if parser.token.id in allowed_operators:
          operators.add(parser.token.id)
          parser.advance()
        else:
          break
    self.third = f"{' '.join([op for op in operators])}"
    self.second = parser.next(bp)
    return self
  symbol_table.add_led("d", dz_led)
  symbol_table.add_led("z", dz_led)
  symbol_table.add_nud("(literal)", lambda self, parser: self)
  symbol_table.add_blank("(", 150)
  def parenthesis_nud(self, parser):
    right = parser.next()
    parser.advance(")")
    return right
  symbol_table.add_nud("(", parenthesis_nud)
  symbol_table.add_blank(")")
  symbol_table.add_blank(".")
  symbol_table.add_blank("(end)")
  return symbol_table