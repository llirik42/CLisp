grammar Lisp;

program : programElement* EOF ;

programElement
    : platformDefinition
    | definition
    | expression ;

platformDefinition : LBRACKET DEFINE_PLATFORM LBRACKET variable RBRACKET platformBodyLines+ RBRACKET ;
platformBodyLines : PLATFORM_BODY_LINE ;

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

expression
    : constant
    | variable
    | procedureCall
    | apply
    | procedure
    | condition
    | and
    | or
    | let
    | letAsterisk
    | letRec
    | assignment
    | delay
    | force
    | nativeCall
    | do
    | begin
    ;

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

variable : IDENTIFIER ;

procedureCall : LBRACKET operator operand* RBRACKET ;
apply : LBRACKET APPLY operator operand+ RBRACKET ;
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

condition : LBRACKET IF test consequent alternate? RBRACKET ;
and : LBRACKET AND test* RBRACKET ;
or : LBRACKET OR test* RBRACKET ;
test : expression ;
consequent : expression ;
alternate : expression ;

let : LBRACKET LET bindingList environmentBody RBRACKET ;
letAsterisk : LBRACKET LET_ASTERISK bindingList environmentBody RBRACKET ;
letRec : LBRACKET LET_REC bindingList environmentBody RBRACKET ;
bindingList : LBRACKET binding* RBRACKET ;
binding : LBRACKET variable expression RBRACKET ;
environmentBody : definition* expression+ ;

assignment : LBRACKET SET variable expression RBRACKET ;

delay : LBRACKET DELAY expression RBRACKET ;
force : LBRACKET FORCE expression RBRACKET ;

nativeCall : LBRACKET NATIVE nativeFunction nativeType+ RBRACKET ;
nativeFunction : IDENTIFIER ;
nativeType : IDENTIFIER ;

do : LBRACKET DO LBRACKET doVariable* RBRACKET LBRACKET doTest doExpression* RBRACKET doCommand* RBRACKET ;
doVariable : LBRACKET doVariableName doVariableInit doVariableStep? RBRACKET ;
doVariableName : variable ;
doVariableInit : expression ;
doVariableStep : expression ;
doTest : expression ;
doExpression : expression ;
doCommand : expression ;

begin : LBRACKET BEGIN expression+ RBRACKET ;

DEFINE_PLATFORM : 'define-platform' ;
DEFINE : 'define' ;
TRUE: '#t' ;
FALSE: '#f' ;
APPLY : 'apply' ;
LAMBDA : 'lambda' ;
IF : 'if' ;
AND : 'and' ;
OR : 'or'  ;
LET : 'let' ;
LET_ASTERISK : 'let*' ;
LET_REC : 'letrec' ;
SET : 'set!' ;
DELAY : 'delay' ;
FORCE : 'force' ;
NATIVE : 'native' ;
DO : 'do' ;
BEGIN : 'begin' ;
PERIOD : '.' ;
INTEGER : SIGN? DIGIT+ ;
FLOAT : SIGN?  ((DIGIT* '.' DIGIT+) | (DIGIT+ '.' DIGIT*)) ;
IDENTIFIER : (LETTER|EXTENDED_CHAR) (LETTER|EXTENDED_CHAR|DIGIT)* ;
CHARACTER : '#\\' (~'\\' | ESCAPED_QUOTE | ESCAPED_BACKSLASH | ESCAPE_SEQUENCE) ;
STRING : '"' (~('\\' | '"') | ESCAPED_DOUBLEQUOTE | ESCAPED_BACKSLASH | ESCAPE_SEQUENCE)* '"' ;
PLATFORM_BODY_LINE : '`' (~'`')* '`' ;

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
