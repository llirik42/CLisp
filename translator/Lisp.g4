grammar Lisp;

program : programElement* EOF ;

programElement
    : expression
    | environmentBodyDefinition ;

expression
    : literal
    | variable
    | condition
    | and
    | or
    | procedureCall
    | procedure
    | assignment
    | let
    | letAsterisk
    | letRec
    ;

literal : constant ;

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

procedure : LBRACKET LAMBDA formals procedureBody RBRACKET ;
formals
    : fixedFormals
    | variadicFormal
    | mixedFormals
    ;
fixedFormals : LBRACKET variable* RBRACKET ;
variadicFormal : variable ;
mixedFormals : LBRACKET variable+ PERIOD variable RBRACKET ;
procedureBody : procedureBodyDefinition* expression+ ;
procedureBodyDefinition : definition ;

assignment : LBRACKET SET variable expression RBRACKET ;

let : LBRACKET LET bindingList environmentBody RBRACKET ;
letAsterisk : LBRACKET LET_ASTERISK bindingList environmentBody RBRACKET ;
letRec : LBRACKET LET_REC bindingList environmentBody RBRACKET ;
bindingList : LBRACKET binding* RBRACKET ;
binding : LBRACKET variable expression RBRACKET ;
environmentBody : environmentBodyDefinition* expression+ ;
environmentBodyDefinition : definition ;

constant
    : boolConstant
    | characterConstant
    | stringConstant
    | integerConstant
    | floatConstant
    ;
boolConstant : TRUE | FALSE ;
characterConstant : CHARACTER ;
stringConstant : STRING ;
integerConstant : INTEGER ;
floatConstant : FLOAT ;

definition : variableDefinition ;
variableDefinition : LBRACKET DEFINE variable expression RBRACKET ;

TRUE: '#t' ;
FALSE: '#f' ;
LAMBDA : 'lambda' ;
PERIOD : '.' ;
IF : 'if' ;
AND : 'and' ;
OR : 'or'  ;
SET : 'set!' ;
DEFINE : 'define' ;
LET : 'let' ;
LET_ASTERISK : 'let*' ;
LET_REC : 'letrec' ;
INTEGER : SIGN? DIGIT+ ;
FLOAT : SIGN?  ((DIGIT* '.' DIGIT+) | (DIGIT+ '.' DIGIT*)) ;
IDENTIFIER : (LETTER|EXTENDED_CHAR) (LETTER|EXTENDED_CHAR|DIGIT)* ;
CHARACTER : '#\\' (~'\\' | ESCAPED_QUOTE | ESCAPED_BACKSLASH | ESCAPE_SEQUENCE) ;
STRING : '"' (~('\\' | '"') | ESCAPED_DOUBLEQUOTE | ESCAPED_BACKSLASH | ESCAPE_SEQUENCE)* '"' ;
WS : [ \t\r\n,]+ -> skip ;
COMMENT : ';' ~[\r\n]* -> skip ;
LBRACKET : '(' ;
RBRACKET : ')' ;

fragment DIGIT : [0-9] ;
fragment LETTER : [a-zA-Z] ;
fragment EXTENDED_CHAR : [!$%&*+-./:<=>?@^_~] ;
fragment ESCAPED_DOUBLEQUOTE : '\\"';
fragment ESCAPED_QUOTE : '\\\'';
fragment ESCAPED_BACKSLASH : '\\\\';
fragment ESCAPE_SEQUENCE :  '\\' ('t' | 'n' | 'r') ;
fragment SIGN : [+-];
