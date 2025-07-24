# 📘 Formal Languages and Compiler Design

## Overview

This repository contains all lab assignments and individual projects developed for the *Formal Languages and Compiler Design* course at UBB. The course focused on both theoretical and practical aspects of formal languages, automata theory, and compiler components. It progressed through key compiler phases: lexical analysis, finite automata modeling, grammar parsing, and syntax validation.

## Technologies Used

- **Language**: Python
- **Concepts**: Hash tables, finite automata, context-free grammars, recursive descent parsing
- **Other tools**: Regular expressions, CLI menus, structured text file parsing

## Assignments Summary

### Lab 1 - Custom Language & Syntax Rules
- Defined a minimal programming language with Pascal-like syntax
- Wrote simple programs (e.g. factorial, GCD)
- Designed token and syntax rules manually (`token.in`, `Syntax.in`, `Lexic.txt`)

### Lab 2 - Symbol Table with Hashing
- Implemented a `SymbolTable` using a custom hash table with chaining
- Supported insert, lookup, reverse-position fetch, and collision handling
- Printed internal structure and validated correct indexing

### Lab 3 - Lexical Scanner
- Developed a `Scanner` class to tokenize custom source programs
- Detected and reported lexical errors (invalid identifiers, literals)
- Produced `PIF.out` (Program Internal Form) and `ST.out` (Symbol Table)

### Lab 4 - Finite Automaton (FA)
- Built a FA simulator (DFA/NFA)
- Parsed automata from file and printed transitions, states, and determinism
- Checked whether input strings are accepted by a given automaton

### Lab 5 - Context-Free Grammar & Parser
- Loaded grammars from file and validated CFG structure
- Implemented a recursive descent parser
- Parsed token sequences and confirmed compliance with the grammar
