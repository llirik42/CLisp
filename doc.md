# CLisp documentation

The interpreter made according to the R5RS scheme.

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

## Supported data types

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

## Lambdas

Lambda is created by `(lambda (...) ...)`.

### Fixed arguments

```Scheme
((lambda (x) (display x)) 1)
```

```
1
```

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

`to-boolean`
`to-string`
`to-char`
`to-double`
`to-integer`

`promise?`
`procedure?`
`boolean?`
`string?`
`char?`
`double?`
`integer?`
`number?`
`pair?`
`list?`

## If, and, or, not



## Environment

set!
define!


## Native calls

## Platform definition

## Apply

## Begin


## Promises

## Loops

