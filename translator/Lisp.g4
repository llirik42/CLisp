grammar Lisp;

program
    : expression* EOF
    ;

expression
    : constant
    | variable
    | procedureCall
    ;

procedureCall : '(' operator operand* ')' ;
operator : expression ;
operand : expression ;

constant
    : boolConstant
    | stringConstant
    | integerConstant
    ;

boolConstant : true | false;

true : TRUE;
false : FALSE;

stringConstant : STRING ;

integerConstant : NUMBER;

variable : IDENTIFIER;

TRUE: '#t';
FALSE: '#f';
IDENTIFIER : (LETTER|EXTENDED_CHAR) (LETTER|EXTENDED_CHAR|DIGIT)* ;
NUMBER: SIGN? DIGIT+;
STRING : '"' (~'\\' | ESCAPED_DOUBLEQUOTE | ESCAPED_BACKSLASH | '\\n')* '"';
WS : [ \t\r\n,]+ -> skip ;

fragment DIGIT : [0-9] ;
fragment LETTER : [a-zA-Z] ;
fragment EXTENDED_CHAR : [!$%&*+-./:<=>?@^_~] ;
fragment ESCAPED_DOUBLEQUOTE : '\\"';
fragment ESCAPED_BACKSLASH : '\\\\';
fragment SIGN : [+-];
