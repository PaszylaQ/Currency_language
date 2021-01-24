import io
import sys

from src.Lexer import Lexer
from src.Parser import Parser
from src.SemanticAnalyzer import SemanticAnalyzer
from src.Source import Source

if __name__ == "__main__":
    # sys.stdin = io.StringIO(
    #     "def func(var name1, var name2) {"
    #     "var sum = 0;"
    #
    #     ""
    #   "return 0;"
    # "}"
    #
    #         "sum = sum + func(param);"
    #         "iter = iter + 1;"
    #
    #     "print(sum);"
    # )
    sys.stdin = io.StringIO(
        #  "PLN wartosc = 8.9;"
        #   " var i = 3;"
        #  "def PLN name1(PLN a,  PLN b) {"
        #    "var luz = 1;"
        #      "  i = 4;"
        #    "name1(a, b);"
        #  "   var luz2 = 2;"
        #      "var luz3 = i + luz;"
        #      "if( luz3 >= luz2){"
        #           "while( i > 2 | i <= 10){"
        #               "print(b);"
        #              "}"
        #  "   return luz3;"
        #  "  }"
        #     "return 5;"
        #  "}"
        # "PLN a = 5;"
        # "PLN b = 4;"

        "def PLN name2(var abc) {"
        # "name1(a , b);"
        "PLN b = 4;"
        "    print(abc);"
        "if (abc > 2){"
        "if (abc > 2){"
        "return b;"
        "}"
        "else{"
        "return b;"

        "}"
        "return b;"
        "}"
        ""
        # "    var a = 2 + 2;"
        # "    return 4;"
        # "name2(2);"
        "return b;"
        "}"
        # "name2(2);"

        # sys.stdin = io.StringIO(
        #     " PLN i = 3;"
        #     # "i = i + 1 ;
        #     "PLN j = 5;"
        #     #     "while( i > j | i<=j){"
        #     #      "i = i+ j ;"
        #     #     "}"
        #     #     "if(j>=i){"
        #     #     "print(i);"
        #     #     "}"
        #     #     "else{"
        #     #     "PLN k = j+i;"
        #     # "}"
        #     "def name1(PLN a,  PLN b) {"
        #     "var luz = 1;"
        #     #        " i= 4;"
        #     #
        #     #     "var luz4 = i + b;"
        #     # "   var luz2 = 2;"
        #     # "var luz3 = i + luz;"
        #     " name1(i, b );"
        #     ""
        #     "return 5;"
        #     "}"

        # "var name = name1(i,i);"

        # "string text = \"cos\";"
        #     "var savings = 3;"
        # "USD savings3 = 5;"
        # #
        #    "PLN savings2 ; "
        # "savings2 = savings;"
        # "savings = 2;"
        # "def func(PLN name1, var name){}"
        # "def func(var name, PLN namez){}"
        # "func();"

        # "savings = savings2;"
        #  "func();"
        #              "if( luz3 >= luz2){"
        #              "while( i >2 | i<=10){"
        #                  "print(\"cos\");"
        #                 "}"
        #     "   return luz3;"
        #     "  }"
        # " return savings;"
        #         "}"

        # "PLN allsavings = savings+ savinf2;"
        # "PLN savings = 23;"
        # "savings2 = 21;"
        #  "print(savings2);"
        # "print(\"\");"

    )
    source = Source()
    lexer = Lexer(source)
    parser = Parser(source, lexer)
    functions = parser.parse()
    # visitor  = getattr(functions[0], 'var_type' )
    # print(visitor)
    # for function in functions:
    #     print(function)
    analyzer = SemanticAnalyzer(functions)
    analyzer.analyze()
    # print(functions)
    # interpreter = Interpreter(functions)
    # interpreter.interpret()

    # while if condition
    #
