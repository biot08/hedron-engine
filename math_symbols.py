import re
from parser import SymbolTable

def math_token_gen(program, symbol_table):
  token_pat = re.compile(r"\s*(?:(6a|%{1,3}|F|\d+)|(\*\*|>=|<=|!=|==|.))")
  for number, operator in token_pat.findall(program):
    if number:
      symbol = symbol_table.get("(quote)")
      yield symbol(number)
    elif operator:
      symbol = symbol_table.get(operator)
      if not symbol:
        raise SyntaxError("Unknown operator")
      yield symbol()
  symbol = symbol_table.get("(end)")
  yield symbol()

def math_symbol_table():
  symbol_table = SymbolTable()
  symbol_table.add_infix("+", 10)
  symbol_table.add_prefix("+", 100)
  symbol_table.add_infix("-", 10)
  symbol_table.add_prefix("-", 100)
  symbol_table.add_infix("*", 20)
  symbol_table.add_infix("/", 20)
  symbol_table.add_infix_right("**", 30)
  symbol_table.add_nud("(quote)", lambda self, parser: self)
  symbol_table.add_blank("(", 150)
  def parenthesis_nud(self, parser):
    right = parser.next()
    parser.advance(")")
    return right
  symbol_table.add_nud("(", parenthesis_nud)
  symbol_table.add_blank(")")
  symbol_table.add_blank("(end)")
  return symbol_table