grammar Lisp;

program
    : expression* EOF
    ;

expression
    : constant
    | variable
    | procedureCall
    ;

constant
    : boolConstant
    | stringConstant
    | integerConstant
    ;

variable : IDENTIFIER ;

procedureCall : '(' operator operand* ')' ;
operator : expression ;
operand : expression ;

boolConstant : TRUE | FALSE ;
stringConstant : STRING ;
integerConstant : NUMBER ;

TRUE: '#t' ;
FALSE: '#f' ;
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
