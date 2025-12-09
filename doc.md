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

```
(display 5)
(display 0)
(display -13)
```

```
5
0
-13
```

### Lambdas

### Promises

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

