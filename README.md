# LogicTableauConstructor
This code implements a propositional and first order logic tableau using Python. The program can be run on an input file to get the result. The program correctly identifies the type of a propositional/first order logic formula, and identifies whether it is satisfiable or not satisfiable. In the case of FOL tableau, satisfiablility cannot be determined after introducing 10 new constants in the δ-expansions on any given open branch.

<br/>
Below we define both the language of propositional and first order logic. We limit our propositional letters to p,q,r,s, and our binary connectives to conjunctions, disjunctions, and implications. White space or extra brackets are not allowed in formulas.

```
FMLA := PROP (Proposition)
        | -FMLA (Negation)
        | (FMLA*FMLA) (Binary Connective)
      
PROP := p|q|r|s
* := ^|v|> (and, or, implies)
```

<br/>
Similarly, for FOL, we limit our variables to x, y, z, and w, with no function symbols and only binary predicates P, Q, R, and S.

```
FMLA := PRED(var,var) (Atom)
        | -FMLA (Negation)
        | EvarFMLA (Existentially Quantified)
        | AvarFMLA (Universally Quantified)
        | (FMLA*FMLA) (Binary Connective)
        
var := x|y|z|w
PRED := P|Q|R|S
* := ^|v|>
```

<br/>
To see some examples, see the sample input file. The input file should have the first line containing PARSE in order for the program to produce parser output, or SAT to produce satisfiability output (or both). The remaining lines should be propositional or first order formulas.

If a formula is parsed as a formula, a tableau is constructed and checked to see if it has an open branch. For propositional formulas, the program determines whether or not it is satisfiable. For first order logic formulas, we assume there are no free variables. We try to determine satisfiability; however, the tableau may never close. Thus, if the program is required to add more than 10 new constants to all open branches under some reasonable and fair schedule, it leaves satisfiability undetermined.

## Running the code
* Clone the repo
* `cd` into to the directory
* Run `python3 tableau.py`
