Lisp REPL and Interpreter
Author: Ryan Cebulko
Created: 1/2015

This was a little project written one night when a friend posed me the
challenge of writing a Lisp interpreter in Python. Having no experience
using Python for anything but Hello World, I thought it would be a fun
project. It was.

Data types:
    -integer
    -float
    -symbol
    -list/cons
    -boolean
    -lambda function
Current Features:
    -local bindings with 'let'
    -boolean operators
    -arithmetic operators
    -function currying
    -if branches
    -cond blocks
Missing Features:
    -global definitions
    -recursive bindings without using a Y-combinator
    -lazy evaluation
    -arbitrary number of arguments for functions like + and or
    -tests for the parser (I was tired and lazy writing that bit)
    -parser error handling (same reason as above)
    -(help) and (exit) functions