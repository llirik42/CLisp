# CLisp documentation

The interpreter made according to the R5RS scheme.

* [IO](#io)
* [Data types](#data-types)
* [Arithmetic operations](#arithmetic-operations)
* [Logical operations](#logical-operations)
* [Procedures](#procedures)
* [Promises](#promises)
* [Apply](#apply)
* [Begin](#begin)
* [Environments](#environments)
* [Loops](#loops)
* [Native calls](#native-calls)
* [Plaftorm definitions](#platform-definitions)
* [Other standard library functions](#other-standard-library-functions)

## IO

### display

```Scheme
(display "Hello, world!")
```

```
Hello, world!
```

Function accepts only one argument and prints it on stdout.

> Unlike the R5RS, `display` adds \n. 

### newline

```Scheme
(newline)
```

> `(newline)` is equivalent to `(display "\n")`.

### read-line

```Scheme
(display (read-line))
```

Function reads the input until it encounters \n, then it returns string containing user input. For example, if user inputs "Hello, clisp!", then the code above will print

```
Hello, clisp!
```

## Data types

### Primitives

**Integers**

```Scheme
(display 5)
(display 0)
(display -13)
```

```
5
0
-13
```

**Doubles**

```Scheme
(display 5.2)
(display -3.5)
(display .5)
(display -3.)
```

```
5.2
-3.5
0.5
-3
```

**Booleans**

```Scheme
(display #t)
(display #f)
```

```
true
false
```

**Characters**

```Scheme
(display #\A )
(display #\a )
(display #\5 )
(display #\\\ )
(display #\" )
```

```
A
a
5
\
"
```

> Special values: `#\\n`, `#\\r`, `#\\t`, `#\ ` (space).

**Strings**

```Scheme
(display "Test")
(display "\"")
(display "\\")
```

```
Test
"
\
```

> Special values: `"\n"`, `"\r"`, `"\t"`.

### Pairs

Pair is creates by `(cons ... ...)`.

```Scheme
(display (cons 1 2))
```

```
(1 . 2)
```

### Lists

List is created by `(list ...)`.

```Scheme
(display (list))
(display (list 1 2 3 4))
```

```
()
(1 2 3 4 )
```

## Arithmetic operations

```Scheme
(+ ... ... ...)
(* ... ... ...)
```

> accept any number of arguments.

```Scheme
(- ... ... ...)
(/ ... ... ...)
```

> accept any number of arguments, but uses only first 2.

```Scheme
(> ... ...)
(>= ... ...)
(< ... ...)
(<= ... ...)
(= ... ...)
```

> accept only 2 arguments.

## Logical operations

**if**

```Scheme
(if x y z)
```

> Operation is lazy, so it won't evaluate `y` if `x` is false (similarly for `z`, if `x` is true).


**and, or**

```Scheme
(and ... ... ...)
(or ... ... ...)
```

> Operations are lazy and accept any number of arguments. 

```Scheme
(and)          =>    true
(and 1)        =>    1
(and 1 2 3)    =>    3
(or)           =>    false
(or 1)         =>    1
(or 1 2 3)     => 1
```

**not**

```Scheme
(not ...)
```

> Operation accepts only 1 argument.

## Procedures

Procedure is created by `(lambda (...) ...)`.

### Fixed arguments

**Example 1**

```Scheme
((lambda (x) (display x)) 1)
```

```
1
```

**Example 2**

```Scheme
((lambda (x y z) (display x) (display y) (display z)) 1 2 3)
```

```
1
2
3
```

### Variadic argument

```Scheme
((lambda x (display x)))
((lambda x (display x)) 1)
((lambda x (display x)) 1 2 3)
```

```
()
(1)
(1 2 3)
```

### Mixed arguments

```Scheme
((lambda (x y . z) (display x) (display y) (display z) 1 2 3 4)
```

```
1
2
(3 4)
```

## Promises

Promise is created by `(delay <expression>)`. Passed expression doesn't evaluate until `(force <promise>`. Expression evaluates only once.

```Scheme
(delay 5)            =>    promise
(force (delay 5))    =>    5
```

## Apply

`Apply` puts given list into procedure arguments.

```Scheme
(apply + 1 2 (list 3 4))    =>    10
```

> In example above it transforms into `(+ 1 2 3 4 )`.

## Begin

`Begin` evaluates all given expressions and returns values of the last one.

**Example 1**

```Scheme
(begin (display 1) (display "abc") (display #t))
```

```
1
abc
true
```

**Example 2**

```Scheme
(begin (+ 1 2) (+ 3 4) (+ 5 6))    => 11
```

## Environments

### let, let*, letrec

Environment represents variables with their values. At the very beginning, there is a global one. Environment is created by `let`, `let*` or `letrec`. 

```Scheme
(let ((x 5))
	(display x))
```

### define, set!

`Define` creates a new variable in the current environment, `set!` changes variables values. 

```Scheme
(define x "Old")
(display x)
(set! x "New")
(display x)
```

```
Old
New
```

## Loops

Loops is organized by `do`.

```Scheme
(do ((i 0 (+ i 1))) 
  ((> i 5))
  (display i))
```

```
0
1
2
3
4
5
```

## Native calls

**Supported native types**:

* `integer`
* `double`
* `char`
* `string`
* `void`

## Platform definitions

## Other standard library functions

* `car`, `cdr`, `set-cdr!`, `set-car!`;
* `length`, `list-ref`;
* `integer?`, `double?`, `number?`, `boolean?`, `char?`, `string?`, `pair?`, `list?`, `procedure?`, `promise?`;
* `to-integer`, `to-double`, `to-boolean`, `to-char`, `to-string`.
