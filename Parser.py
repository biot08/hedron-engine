import re

class parser:
  def __init__(self, token_generator, symbol_table):
    self.token_generator = token_generator
    self.symbol_table = symbol_table
    self.tokenizer = None
    self.token = None
    
  def parse(self, program):
    self.tokenizer = self.token_generator(program, self.symbol_table)
    self.advance()
    return self.next()

  def next(self, rbp=0):
    "Consumes and processes the next symbol"
    current_token = self.token
    self.advance()
    left = current_token.nud(self)
    while self.token.lbp > rbp:
      current_token = self.token
      self.advance()
      left = current_token.led(left, self)
    return left
  
  def advance(self, id=None):
    if id and self.token.id != id:
      raise SyntaxError(f"Expected {id}")
    self.token = next(self.tokenizer)

class AbstractSymbol:
  id = ""
  value = None
  first = second = third = ""
  def __init__(self, value = None):
    if value:
      self.value = value

  def nud(self, parser):
    raise SyntaxError(f"Syntax error on {self.id}")

  def led(self, left, parser):
    raise SyntaxError(f"Unknown operator {self.id}")

  def __repr__(self):
    if self.id == "(quote)":
      return f"(quote {self.value})"
    if self.id == "(name)":
      return f"({self.id[1:-1]} {self.value})"
    out = [self.id, self.first, self.second, self.third]
    out = map(str, filter(None, out))
    return f"({' '.join(out)})"

class SymbolTable:
  def __init__(self):
    self.symbol_table = {}

  def __symbol__(self, id, bp=0):
    if id in self.symbol_table:
      Symbol = self.symbol_table[id]
      Symbol.lbp = max(bp, Symbol.lbp)
    else:
      class Symbol(AbstractSymbol):
       pass
      Symbol.__name__ = f"symbol:'{id}'"
      Symbol.id = id
      Symbol.lbp = bp
      self.symbol_table[id] = Symbol
    return Symbol

  def get(self, id):
    return self.symbol_table.get(id)
    
  def add_prefix(self, id, bp):
    def nud(self, parser):
      self.first = parser.next(bp)
      self.second = ""
      return self
    self.__symbol__(id, bp).nud = nud

  def add_infix(self, id, bp):
    def led(self, left, parser):
      self.first = left
      self.second = parser.next(bp)
      return self
    self.__symbol__(id, bp).led = led
  
  def add_infix_right(self, id, bp):
    def led(self, left, parser):
      self.first = left
      self.second = parser.next(bp - 1)
      return self
    self.__symbol__(id, bp).led = led

  def add_nud(self, id, nud):
    self.__symbol__(id).nud = nud
    
  def add_led(self, id, led):
    self.__symbol__(id).led = led

  def add_blank(self, id, bp=0):
    self.__symbol__(id, bp)

if __name__ == "__main__":
  pass