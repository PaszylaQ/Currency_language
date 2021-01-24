import io
import sys

from src.Interpreter import Interpreter
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

        #    "i = 16 + 2;"
        #     "print(i);"

        #  "var a = 5.0;"
        "var i = 4.0;"
        # "def var name1(var a,  var b) {"
        #      "i = i - 1;"
        #      "if( i > 0) "
        #  "   { "
        #         "print(i);"
        #           "name1(a , b);"
        #         
        #  "   } "
        #      ""
        #  "   return a + b; "
        #  "}"
        #   "print(name1(a, a));"
        #  "print(i);"
        #      "  i = 4;"
        #    "name1(a, b);"
        #  "   var luz2 = 2;"
        # #      "var luz3 = i + luz;"
        #
        "while ( i > 0) "
        "{"
        " i = i - 1 ;"
        "print(i);"
        "}"

        # " var i = 3 + (1 * 2);"
        # "if( 4 ==   4 | 4 == 5){"
        #     # "while( i > 2 | i <= 10){"
        #         "print(i);"
        # # "}"
        # "}"

        # "def var sum(var a, var b){ return sum(a, b) + sum "
        #    # "}"
        # #  "   return luz3;"
        #  "}"
        #     "return 5;"
        #  "}"
        # "PLN a = 5;"
        #  "PLN b = 4;"
        #
        # "def var name2() {"
        #     "var i = 5;"
        #            "while ( i<10){"
        #                "i = i + 1;"
        #                "return i;"
        #            "}"
        #            "while ( i<10){"
        #                "i = i + 1;"
        # #              "return b;"
        #            "}"
        #
        #        "return i;"
        #        "} "
        #         "name2();"
        # "var i = 5;"
        # "while ( i<10){"
        # "i = i + 1;"

        # "}"

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
    interpreter = Interpreter(functions, analyzer)
    interpreter.interpret()

    # while if condition
    #
