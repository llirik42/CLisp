grammar Lisp;

program
    : expression* EOF
    ;

body : expression+ ;

expression
    : literal
    | variable
    | condition
    | procedureCall
    | procedure
    | assignment
    ;

literal
    : constant
    ;

variable : IDENTIFIER ;

condition : '(' IF test consequent alternate? ')' ;
test : expression ;
consequent : expression ;
alternate : expression ;

procedureCall : '(' operator operand* ')' ;
operator : expression ;
operand : expression ;

procedure : '(' LAMBDA formals body  ')' ;
formals
    : fixedFormals
    | variadicFormals
    | periodFormals
    ;

fixedFormals : '(' variable* ')' ;
variadicFormals : variable ;
periodFormals : '(' variable+ PERIOD variable ')' ;

assignment : '(' SET variable expression ')' ;

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
SET : 'set!';
NUMBER: SIGN? DIGIT+ ;
IDENTIFIER : (LETTER|EXTENDED_CHAR) (LETTER|EXTENDED_CHAR|DIGIT)* ;
STRING : '"' (~'\\' | ESCAPED_DOUBLEQUOTE | ESCAPED_BACKSLASH | '\\n')* '"' ;
WS : [ \t\r\n,]+ -> skip ;
COMMENT : ';' ~[\r\n]* -> skip ;

fragment DIGIT : [0-9] ;
fragment LETTER : [a-zA-Z] ;
fragment EXTENDED_CHAR : [!$%&*+-./:<=>?@^_~] ;
fragment ESCAPED_DOUBLEQUOTE : '\\"';
fragment ESCAPED_BACKSLASH : '\\\\';
fragment SIGN : [+-];
