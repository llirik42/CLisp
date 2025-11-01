grammar Lisp;

prog
    : sexpr EOF #program
    ;

sexpr : '(' PRINT exprNumber ')' #printExpr ;

exprNumber : NUMBER #number ;

PRINT : 'print' ;
KEYWORD : ':' SYMBOL ;
NUMBER  : '-'? [0-9]+ ('.' [0-9]+)? ;
SYMBOL  : [a-zA-Z_+\-*/?<>=!$%&^~][a-zA-Z0-9_+\-*/?<>=!$%&^~]* ;
WS      : [ \t\r\n,]+ -> skip ;
