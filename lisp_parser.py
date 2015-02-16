from lisp_exceptions import LispParsingException
from ast import *
import re

class Parser:
    """Parses string into abstract syntax tree"""

    @staticmethod
    def tokenize(stx):
        # Pad parentheses for convenient tokenizing by whitespace
        stx = re.sub(r"([\(\)])", r" \1 ", stx)
        parts = re.split(r"\s+", stx)

        if parts[0] == "":
            parts = parts[1:]
        if parts[-1] == "":
            parts = parts[:-1]

        return parts

    @staticmethod
    def lex(tkns):
        if len(tkns) == 1:
            return tkns[0]
        elif tkns[0] != "(" or tkns[-1] != ")":
            raise LispParsingException(
                "lex",
                "expected atomic or s-expression; got " + str(tkons)
            )
        else:
            stack = [[]]
            topExpr = stack[0]
            for token in tkns[1:]:
                currExpr = stack[-1]

                if token == "(":
                    currExpr = []
                    stack.append(currExpr)
                elif token == ")":
                    if currExpr == topExpr:
                        break
                    else:
                        stack[-2].append(currExpr)
                        stack = stack[:-1]
                else:
                    currExpr.append(token)
            return topExpr

    @staticmethod
    def interpret(expr):
        if type(expr) is list:
            ast = map(Parser.interpret, expr)

            if expr[0] == "if":
                return ASTIf(
                    ast[1],
                    ast[2],
                    ast[3]
                )
            elif expr[0] == "cond":
                return ASTCond(
                    map(lambda b: map(Parser.interpret, b), expr[1:])
                )
            elif expr[0] == "cons":
                return ASTCons(ast[1], ast[2])
            elif expr[0] == "car":
                return ASTCar(ast[1])
            elif expr[0] == "cdr":
                return ASTCdr(ast[1])
            elif expr[0] == "list":
                return ASTList(ast[1:])
            elif expr[0] == "lambda":
                return ASTFun(
                    map(Parser.interpret, expr[1]),
                    Parser.interpret(expr[2])
                )
            elif expr[0] == "let":
                bindings = expr[1]
                values, names = \
                    map(list, zip(*[
                        [Parser.interpret(str(e))
                            for e in bind]
                        for bind in bindings
                    ]))

                return ASTWith(
                    values,
                    names,
                    Parser.interpret(expr[2])
                )
            else:
                return ASTCall(
                    ast[0],
                    ast[1:]
                )
        else:
            if expr == "t":
                return ASTBool(True)
            elif expr == "nil":
                return ASTBool(False)
            elif expr == "nil":
                return ASTBool(False)
            elif expr[0] == "'":
                return ASTSym(expr[1:])
            else:
                try:
                    return ASTNum(int(expr))
                except ValueError:
                    try:
                        return ASTNum(float(expr))
                    except ValueError:
                        return ASTId(expr)

    @staticmethod
    def parse(stx):
        return Parser.interpret(Parser.lex(Parser.tokenize(stx)))