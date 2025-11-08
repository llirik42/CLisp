grammar Lisp;

program
    : expression* EOF
    ;

expression
    : IDENTIFIER #variable
    | constantExpression #constant
    | procedureCallExpression #procedureCall
    ;

procedureCallExpression : '(' operator operand* ')' ;
operator : expression ;
operand : expression ;

constantExpression
    : boolConstant
    | stringConstant
    | integerConstant
    ;

boolConstant : BOOLEAN;

stringConstant : STRING ;

integerConstant : NUMBER;

BOOLEAN : '#t' | '#f';
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
