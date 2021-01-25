import io
import sys

from src.CurrencyReader import CurrencyReader
from src.Interpreter import Interpreter
from src.Lexer import Lexer
from src.Parser import Parser
from src.SemanticAnalyzer import SemanticAnalyzer
from src.Source import Source
from src.Token import Characters

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

        #  "PLN wartosc = 8.9;"

        #    "i = 16 + 2;"
        #     "print(i);"

        #  "var a = 5.0;"
       # "var i = 4.0;"
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
     #    #
     #    "while ( i > 0) "
     #    "{"
     #    " i = i - 1 ;"
     #    "print(i);"
     # "}"
       # "print(\"dkckk\");"

        # " var i = 3 + (1 * 2);"
        # "if( 4 ==   4 | 4 == 5){"
        #     # "while( i > 2 | i <= 10){"
        #         "print(i);"
        # # "}"
        # "}"
        #  "EUR i = 4.0;"
        # "def PLN sum(EUR eur){"

        #" eur = 5.0;"
        # "return eur;"
        # "}"
        # "PLN num ;"
        # "PLN pln = sum(i);"
        # "GBP gbp = sum(i);"
        # "var i = 5.0 ;"
        # " var j = 4.0 ;"
        # "var k = (1 / 2 ) / 3;"
        #  "print(k);"


        # "def var sum(var a, var b){ return sum(a, b) "}"
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
       # "GBP i = 5.0;"
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

    #sys.stdin = io.StringIO()

  #   "def USD savingsInUsdCurrency(PLN currency1, EUR currency2, USD currency3)"
  #   "{"
  #   "USD savings = 0 ;"
  #   "savings = currency1 + currency2  ;"
  #   "savings = savings + currency3 ;"
  #   "return savings;"
  #   "}"
  #  "PLN złote = 200.0 ;"
  #  "EUR euro = 10.0 ;"
  #  "USD dolary = 342.0 ;"
  #  "CZK mySavings = savingsInUsdCurrency(złote, euro, dolary) ;"
  #  "print(mySavings) ;"
  #   "EUR mySavings = 1.0 ;"
  #   "EUR mySavings2 =  mySavings * 2;"
  #   "print(mySavings2);"
  #
  #   "def var fib(var n){"
  #   "if (n == 1 | n == 2)"
  #  " {"
  #
  #
  #       "return 1 ;"
  #   "}"
  #   "else"
  #   "{"
  #       "return  fib(n - 1) + fib(n - 2);"
  #   "}"
  #   "return 0;"
  #   "}"
  #  " var sum = 0 ;"
  #  " var iter = 0 ;"
  #   "var param = 1;"
  # " while ( iter < 30 )"
  #      " {"
  #         "sum = sum + fib(param);"
  #          " iter = iter + 1;"
  #       "}"
  #   "print(sum);"
  #
  #       "def var func()"
  #       " {"
  #           "var i = 4 ;"
  #       " return i ;"
  #       " }"
#     source = Source(io.StringIO(     "def USD savingsInUsdCurrency(PLN currency1, EUR currency2, USD currency3)"
#     "{"
#     "USD savings = 0 ;"
#     "savings = currency1 + currency2  ;"
#     "savings = savings + currency3 ;"
#     "return savings;"
#     "}"
#    "PLN złote = 200.0 ;"
#    "EUR euro = 10.0 ;"
#    "USD dolary = 342.0 ;"
#    "CZK mySavings = savingsInUsdCurrency(złote, euro, dolary) ;"
#    "print(mySavings) ;"
#
#     "EUR mySavings2 =  mySavings * 2;"
#     "print(mySavings2);"
#
#     "def var fib(var n){"
#     "if (n == 1 | n == 2)"
#    " {"
#
#
#         "return 1 ;"
#     "}"
#     "else"
#     "{"
#         "return  fib(n - 1) + fib(n - 2);"
#     "}"
#     "return 0;"
#     "}"
#    " var sum = 0 ;"
#    " var iter = 0 ;"
#     "var param = 1;"
#   " while ( iter < 30 )"
#        " {"
#           "sum = sum + fib(param);"
#            " iter = iter + 1;"
#         "}"
#     "print(sum);"
# ))
    source = Source(sys.stdin)
    lexer = Lexer(source)
    parser = Parser(source, lexer)
    functions = parser.parse()

    analyzer = SemanticAnalyzer(functions)
    analyzer.analyze()
    interpreter = Interpreter(functions, analyzer)
    interpreter.interpret()
    # visitor  = getattr(functions[0], 'var_type' )
    # print(visitor)
    # for function in functions:
    #     print(function)
    # while if condition
    #
