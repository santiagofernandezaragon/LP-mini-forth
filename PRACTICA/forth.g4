grammar forth;

// --- PARSER RULES (SINTAXI) ---

// El punt d'entrada: un programa és una llista de definicions o instruccions soltes.
root : (definition | instruction)* EOF ;

// Definició de funció: comença per ':', té un nom, un bloc de codi i acaba amb ';'
definition : COLON ID block SEMICOLON # DefFunction ;

// Un bloc és una seqüència de comandes vàlides dins d'una estructura
block : (instruction | control_structure)* ;

// Estructura condicional (IF/ELSE)
// Nota: Com que 'control_structure' està dins de 'block' i 'block' està dins de 'definition',
// això permet IFs dins de funcions. Per impedir-los al 'root' directament,
// 'root' utilitza 'instruction' (que no inclou IF) i 'definition'.
control_structure : IF block (ELSE block)? ENDIF # IfStatement ;

// Instruccions simples (que poden anar tant al root com dins de funcions)
instruction
    : NUMBER      # PushNumber
    | ID          # CallFunction
    | RECURSE     # RecursiveCall
    // Operacions Aritmètiques
    | PLUS        # Add
    | MINUS       # Sub
    | MULT        # Mul
    | DIV         # Div
    | MOD         # Mod
    // Operacions de Pila
    | DUP         # StackDup
    | SWAP        # StackSwap
    | DROP        # StackDrop
    | OVER        # StackOver
    | ROT         # StackRot
    | TWODUP      # Stack2Dup
    | TWOSWAP     # Stack2Swap
    | TWODROP     # Stack2Drop
    | TWOOVER     # Stack2Over
    // Operacions d'E/S
    | DOT         # PrintTop
    | DOTS        # PrintStack
    // Operacions Relacionals i Booleanes
    | EQ          # Equal
    | NEQ         # NotEqual
    | LT          # Less
    | GT          # Greater
    | AND         # LogicAnd
    | OR          # LogicOr
    | NOT         # LogicNot
    ;

// --- LEXER RULES (TOKENS) ---

// Paraules clau (Keywords) - Han d'anar abans de ID
COLON     : ':' ;
SEMICOLON : ';' ;
IF        : 'if' ;
ELSE      : 'else' ;
ENDIF     : 'endif' ;
RECURSE   : 'recurse' ;

// Operadors Aritmètics
PLUS      : '+' ;
MINUS     : '-' ;
MULT      : '*' ;
DIV       : '/' ;
MOD       : 'mod' ;

// Operadors de Pila
DUP       : 'dup' ;
SWAP      : 'swap' ;
DROP      : 'drop' ;
OVER      : 'over' ;
ROT       : 'rot' ;
TWODUP    : '2dup' ;
TWOSWAP   : '2swap' ;
TWODROP   : '2drop' ;
TWOOVER   : '2over' ;

// E/S
DOT       : '.' ;
DOTS      : '.s' ;

// Relacionals i Booleans
EQ        : '=' ;
NEQ       : '<>' ;
LT        : '<' ;
GT        : '>' ;
AND       : 'and' ;
OR        : 'or' ;
NOT       : 'not' ;

// Identificadors i Literals
// Un ID és qualsevol paraula que no sigui una keyword (per noms de funcions)
ID        : [a-zA-Z_][a-zA-Z0-9_]* ;

// Números enters (positius i negatius).
// Compte: El '-' pot ser resta o part d'un número. 
// ANTLR intenta fer el match més llarg. '-2' serà NUMBER, '- 2' serà MINUS NUMBER.
NUMBER    : '-'? [0-9]+ ;

// Comentaris: Delimitats per ( i ). Els ignorem (skip).
COMMENT   : '(' ~')'* ')' -> skip ;

// Espais en blanc: Els ignorem.
WS        : [ \t\r\n]+ -> skip ;