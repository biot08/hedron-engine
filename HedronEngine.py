from Parser import Parser
from DiceSymbols import dice_symbol_table, dice_token_gen

def test():
  parser = Parser(dice_token_gen, dice_symbol_table())
  test1_value = "-1 + 2 * 3 / 4 + 1 * 2 + (1 + 2) /+ 5 /- 2"
  print(f"Test1 value: {test1_value}")
  print(parser.parse(test1_value))

  test2_value = r"-3 + 3d6 + 2d6a + 1d%%% + 2d%% + 3z*6H3 + 2d(3 + 4)L4 + 2d+-.6 - 2d*6a - 2d*(2+2) > 3 >= 2 == 1 = 2 != 3"
  print(f"Test2 value: {test2_value}")
  print(parser.parse(test2_value))

if __name__ == "__main__":
  test()