grammar Lisp;

program : programElement* EOF ;

programElement
    : expression
    | definition ;

expression
    : literal
    | delay
    | force
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

delay : LBRACKET DELAY expression RBRACKET ;
force : LBRACKET FORCE expression RBRACKET ;

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

procedure : LBRACKET LAMBDA procedureFormals procedureBody RBRACKET ;
procedureFormals
    : procedureFixedFormals
    | procedureVariadicFormal
    | procedureMixedFormals
    ;
procedureFixedFormals : LBRACKET variable* RBRACKET ;
procedureVariadicFormal : variable ;
procedureMixedFormals : LBRACKET variable+ PERIOD variable RBRACKET ;
procedureBody : definition* expression+ ;

assignment : LBRACKET SET variable expression RBRACKET ;

let : LBRACKET LET bindingList environmentBody RBRACKET ;
letAsterisk : LBRACKET LET_ASTERISK bindingList environmentBody RBRACKET ;
letRec : LBRACKET LET_REC bindingList environmentBody RBRACKET ;
bindingList : LBRACKET binding* RBRACKET ;
binding : LBRACKET variable expression RBRACKET ;
environmentBody : definition* expression+ ;

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

definition : variableDefinition | procedureDefinition;
variableDefinition : LBRACKET DEFINE variable expression RBRACKET ;
procedureDefinition : LBRACKET DEFINE LBRACKET variable procedureDefinitionFormals RBRACKET procedureBody RBRACKET ;

procedureDefinitionFormals
    : procedureDefinitionFixedFormals
    | procedureDefinitionVariadicFormal
    | procedureDefinitionMixedFormals
    ;
procedureDefinitionFixedFormals : variable* ;
procedureDefinitionVariadicFormal : PERIOD variable ;
procedureDefinitionMixedFormals : variable+ PERIOD variable ;

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
DELAY : 'delay' ;
FORCE : 'force' ;
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
