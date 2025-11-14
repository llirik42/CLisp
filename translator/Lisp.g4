grammar Lisp;

program
    : expression* EOF
    ;

body : expression+ ;

expression
    : literal
    | variable
    | condition
    | and
    | or
    | procedureCall
    | procedure
    | assignment
    ;

literal
    : constant
    ;

variable : IDENTIFIER ;

condition : LBRACKET IF test consequent alternate? RBRACKET ;
and : LBRACKET AND test* RBRACKET ;
or : LBRACKET OR test* RBRACKET ;
test : expression ;
consequent : expression ;
alternate : expression ;

procedureCall : LBRACKET operator operand* RBRACKET ;
operator : expression ;
operand : expression ;

procedure : LBRACKET LAMBDA formals body RBRACKET ;
formals
    : fixedFormals
    | variadicFormals
    | periodFormals
    ;

fixedFormals : LBRACKET variable* RBRACKET ;
variadicFormals : variable ;
periodFormals : LBRACKET variable+ PERIOD variable RBRACKET ;

assignment : LBRACKET SET variable expression RBRACKET ;

constant
    : boolConstant
    | stringConstant
    | integerConstant
    ;
boolConstant : TRUE | FALSE ;
stringConstant : STRING ;
integerConstant : NUMBER ;

TRUE: '#t' ;
FALSE: '#f' ;
LAMBDA : 'lambda' ;
PERIOD : '.' ;
IF : 'if' ;
AND : 'and' ;
OR : 'or' ;
SET : 'set!';
NUMBER: SIGN? DIGIT+ ;
IDENTIFIER : (LETTER|EXTENDED_CHAR) (LETTER|EXTENDED_CHAR|DIGIT)* ;
STRING : '"' (~('\\' | '"') | ESCAPED_DOUBLEQUOTE | ESCAPED_BACKSLASH | ESCAPE_SEQUENCE)* '"' ;
WS : [ \t\r\n,]+ -> skip ;
COMMENT : ';' ~[\r\n]* -> skip ;
LBRACKET : '(' ;
RBRACKET : ')' ;

fragment DIGIT : [0-9] ;
fragment LETTER : [a-zA-Z] ;
fragment EXTENDED_CHAR : [!$%&*+-./:<=>?@^_~] ;
fragment ESCAPED_DOUBLEQUOTE : '\\"';
fragment ESCAPED_BACKSLASH : '\\\\';
fragment ESCAPE_SEQUENCE :  '\\' ('t' | 'n' | 'r') ;
fragment SIGN : [+-];
