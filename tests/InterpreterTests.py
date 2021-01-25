import io
import sys
import unittest

from src.Interpreter import Interpreter
from src.Lexer import Lexer
from src.Parser import Parser
from src.SemanticAnalyzer import SemanticAnalyzer
from src.SemanticError import SemanticError
from src.Source import Source

def buildInterpreter(string):
        sys.stdin = io.StringIO(string)
        source = Source(sys.stdin)
        lexer = Lexer(source)
        parser = Parser(source, lexer)
        functions = parser.parse()
        analyzer = SemanticAnalyzer(functions)
        analyzer.analyze()
        interpreter = Interpreter(functions, analyzer)
        return interpreter.interpret()

class MyTestCase(unittest.TestCase):



    def testDividingByZero(self):
        with self.assertRaises(RuntimeError):
            buildInterpreter("var i = 5.0; var k = 0; var j = i / k;")


    def testAssigningVarToCurrency(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("var i ; PLN k = 5.0; k =  i;")


    def testAssignCurrencyToVar(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("var i ; PLN k = 5.0; k =  i;")


    def testVariableRedeclaration(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("var i ; var i= 5.0;")

    def testCurrencyRedeclaration(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("PLN i ; PLN i= 5.0;")

    def testVariableNotDeclared(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("var i ; k = 5.0;")

    def testMultiplyingCurrencies(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("PLN k = 5.0; EUR p = 5.0; CZK l = l * p;")

    def testDividingCurrencies(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("PLN k = 5.0; EUR p = 5.0; CZK l = l / p;")

    def testAddingDifferentTypes(self):

        with self.assertRaises(SemanticError):
            buildInterpreter("PLN k = 5.0; var p = 5.0; CZK l = k + p;")

    def testSubstractingDifferentTypes(self):

        with self.assertRaises(SemanticError):
            buildInterpreter("PLN k = 5.0; var p = 5.0; CZK l = k - p;")

    def testCallVariableNotDeclared(self):
        with self.assertRaises(SemanticError):
            buildInterpreter(" k = 5;")

    def testCallFuncDeclared(self):
        with self.assertRaises(SemanticError):
            buildInterpreter(" func();")

    def testReturnCurrTypeNotEqualsFuncVarType(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("def var func() { PLN pln = 5.0; return pln;}")

    def testReturnVarTypeNotEqualsFuncCurrType(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("def PLN func() { var pln = 5.0; return pln;}")

    def testFuncRedeclared(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("def var func() { var pln = 5.0; return pln;} def PLN func() {  PLN pln = 5.0; return pln;}")

    def testFuncParametersRedeclaration(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("def var func(PLN curr, var curr) { return 0 ; }")

    def testNotReturnTypeInFunction(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("def var func(PLN curr, var vri) { vri = vri + 2 ; }")

    def testReturnTypeFromIfBlockNotEqualToFuncReturnType(self):
        with self.assertRaises(SemanticError):
            buildInterpreter("def var func(PLN curr, var vri) { if (vri >= 10 ){ return curr;}  vri = vri + 2 ; return vri; }")

    def testReturnTypeFromIfAndElseBlockNotEqualToFuncReturnType(self):
        with self.assertRaises(SemanticError):
            buildInterpreter(
                "def var func(PLN curr, var vri) { if (vri >= 10 ){ return vri ;} else {return curr;}    vri = vri + 2 ; return vri; }")

    def testReturnTypeFromIfElseAndWhileBlockNotEqualToFuncReturnType(self):
        with self.assertRaises(SemanticError):
            buildInterpreter(
                "def var func(PLN curr, var vri) { if (vri >= 10 ){ return vri ;} else {return vri;} while(vri <= 5) { return curr;}   vri = vri + 2 ; return vri; }")

    def testVarAssignement(self):
        iValue = buildInterpreter("var i = 5; return i;")
        self.assertEqual(iValue, 5.0)

    def testCurrAssignement(self):
        plnValue = buildInterpreter("PLN pln = 10.0; return pln; ")
        self.assertEqual(plnValue, '10.00 PLN')
    #sprawdzenie wartosci funkcji zadeklarowanej przez przez iloczyn

    def testCurrDeclaration(self):
        plnValue = buildInterpreter("var i = 2; PLN value1 = 2.0; PLN value2 = i * 2.0; return value2;")
        self.assertEqual(plnValue, '4.00 PLN')

    def testcheckIfVariableOfSameNameLikeInFunctionChanges(self):
        value = buildInterpreter(
        '''
        PLN test = 5.0;

        def PLN funcTest()

        {
        PLN test = 5.0;
        test = test + test;
        return test;
        }
        funcTest();
        return test;'''
        )
        self.assertEqual(value,"5.00 PLN" )

    def testcheckIfVariableOfSameNameLikeInFunctionChanges2(self):
        value = buildInterpreter(
        '''
        PLN test = 5.0;

        def PLN funcTest()

        {
        PLN test2 = 5.0;
        test = test + test2;
        return test;
        }
        funcTest();
        return test;'''
        )
        self.assertEqual(value,"10.00 PLN" )



    #sprawdzenie wartosci zwracanej przez funkcje
    def testcheckVariableValueReturnedByFunc(self):
        varValue = buildInterpreter(
            "var i = 5; "
            "def var func(var j){"
                " j = (j + 2)* 2;"
                "return j;"
            "}"
            "i = func(i);"
            "return i;"

        )
        self.assertEqual(varValue, 14.0)


    #sprawdzenie wartosci zwracanej przez if

    def testCheckIfReturnValue(self):
        ifReturnValue = buildInterpreter(
            "PLN curr = 5.0;"
            "EUR curr2 = 5.0;"
            "def PLN func(){"
                "PLN pln ;"
                "if (curr < curr2){"
                
                "pln =  curr;"
            "}"
            "return pln;"
            "}"
            "return func();"
        )
        self.assertEqual(ifReturnValue, "5.00 PLN")

    #sprawdzenie wartosci zwracanej przez if else
    def testCheckIfElseReturnValue(self):
        ifReturnValue = buildInterpreter(
            "PLN curr = 5.0;"
            "EUR curr2 = 5.0;"
            "def PLN func(){"
            "PLN pln ;"
            "if (curr > curr2){"

            "pln =  curr;"
            "}"
            "else{"
                "pln = curr2;"
            "}"
            "return pln;"
            "}"
            "EUR eur = func();"
            "return eur;"
        )
        self.assertEqual(ifReturnValue, "5.00 EUR")

    #sprawdzenie wartosci zwracanej przez funkcje rekurencyjna
    def testcheckValueFromRevursiveFunction(self):
        returValue = buildInterpreter(
            '''def var fib(var n){
                if (n <= 1)
                {
                    return n;
                }
                else
                {
                    var fib1 = fib(n - 1) + fib(n - 2);

                    return fib1 ;
                }
                return 0;
                }
               var param = 16.0;
            var fib2 = fib(param);
            return fib2; '''
        )
        self.assertEqual(returValue, 987.0)

    #spraedzanie konwersji
    def testcheckCurrConversion(self):
        currency = buildInterpreter(

            '''EUR eur = 1.0;
            PLN pln = eur;
            return pln;'''
        )
        self.assertEqual(currency, "4.54 PLN")









if __name__ == '__main__':
    unittest.main()
