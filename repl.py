from lisp_exceptions import *
from interpreter import Interpreter

'''
REPL interface for interacting with the interpreter
'''

class REPL:
    """Lisp read-eval-print loop class"""

    def __init__(self):
        interpreter = Interpreter()

        print("""
///////////////////////////////////////////////////////////////////////////////
//                                                                           //
//  Lisp REPL and Interpreter                                                //
//  Author: Ryan Cebulko                                                     //
//  Created: 1/2015                                                          //
//                                                                           //
//  This was a little project written one night when a friend posed me the   //
//  challenge of writing a Lisp interpreter in Python. Having no experience  //
//  using Python for anything but Hello World, I thought it would be a fun   //
//  project. It was.                                                         //
//                                                                           //
//  Data types:                                                              //
//      -integer                                                             //
//      -float                                                               //
//      -symbol                                                              //
//      -list/cons                                                           //
//      -boolean                                                             //
//      -lambda function                                                     //
//  Current Features:                                                        //
//      -local bindings with 'let'                                           //
//      -boolean operators                                                   //
//      -arithmetic operators                                                //
//      -function currying                                                   //
//      -if branches                                                         //
//      -cond blocks                                                         //
//  Missing Features:                                                        //
//      -global definitions                                                  //
//      -recursive bindings without using a Y-combinator                     //
//      -lazy evaluation                                                     //
//      -arbitrary number of arguments for functions like + and or           //
//      -tests for the parser (I was tired and lazy writing that bit)        //
//      -parser error handling (same reason as above)                        //
//      -(help) and (exit) functions                                         //
//                                                                           //
///////////////////////////////////////////////////////////////////////////////
            """)

        while True:
            try:
                print(interpreter.run(raw_input("\n>>> ")))
            except LispParsingException, e:
                print("LispParsingException in " + str(e))
            except LispCompilationException, e:
                print("LispCompilationException in " + str(e))
            except LispRuntimeException, e:
                print("LispRuntimeException in " + str(e))
            except LispRuntimeException, e:
                print("LispRuntimeException in " + str(e))
            except Exception, e:
                print(e)


if __name__ == '__main__':
    REPL()