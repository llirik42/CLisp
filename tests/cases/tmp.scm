(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

(display (factorial 5))

(define (sum-to-n n)
  (if (= n 0)
      0
      (+ n (sum-to-n (- n 1)))))

(display (sum-to-n 10))
(define dec (lambda (x) (- x 1)))
(display (dec 20))

(define lambda-with-let (lambda () (let ((x 30)) (set! x 60) (+ x 50))))
(display (lambda-with-let))
((lambda x (display x)))
((lambda x (display x)) 1)
((lambda x (display x)) 1 2 3 4 5 6 7)
((lambda (x . y) (display y)) 1)
((lambda (x . y) (display y)) 1 2)
((lambda (x y . z) (display z)) 1 2 3 4 5)
(define (f1) 42)
(display (f1))

(define (f2 x y) (+ x y))
(display (f2 7 8))

(define (f3 . z) z)
(display (f3 1 2 3 4 5 6 7 9))

(define (f4 a1 a2 . z) z)
(display (f4 1 2 3 4 5 6 7 9))

(define (f5 a1 a2 . z) a2)
(display (f5 1 "Hello" 3 4 5 6 7 8 9 10))

(define (f6 a1 a2 . z) a1)
(display (f6 -9 2 3 4 5 6 7 8 9 10))
(define make-adder (lambda (n)
  (lambda (x)
    (+ x n))))

(define add5 (make-adder 5))
(display (add5 1))
(display (add5 2))

(define add7 (make-adder 7))
(display (add7 10))
(display (add7 20))

(define salt 21)

(define make-adder-salt (lambda (n)
  (lambda (x)
    (+ x salt n))))

(define adder-salt (make-adder-salt 10))
(display (adder-salt 10))
(display (adder-salt 20))
(display (if #t 1 2))
(display (if #f 1 2))
(display (if #t (+ 1 1) (+ 2 2)))
(display (if #f (+ 1 1) (+ 2 2)))
(display (if #t (if #t (+ 1 1) (+ 2 2)) (if #t (+ 3 3) (+ 4 4))))
(display (if #t (if #f (+ 1 1) (+ 2 2)) (if #t (+ 3 3) (+ 4 4))))
(display (if #f (if #t (+ 1 1) (+ 2 2)) (if #t (+ 3 3) (+ 4 4))))
(display (if #f (if #t (+ 1 1) (+ 2 2)) (if #f (+ 3 3) (+ 4 4))))
(display (if #t 2 (/ 1 0)))
(display (and 1))
(display (and "#$%"))
(display (and 1 2))
(display (and "a" "b" "c"))
(display (and #t #t "w"))
(display (or 2))
(display (or 3 4))
(display (or 5 6 7))
(display (or #f "kish"))
(display (or #f #f #f -1.5))
(display (and))
(display (and #f))
(display (and #t))
(display (and #f #f))
(display (and #f #t))
(display (and #t #f))
(display (and #t #t))
(display (and #t #t #t #t #f))
(display (and #f #t #t #t #t))
(display (and #t #t #t #t #t))
(display (and #f (/ 1 0)))
(display (or))
(display (or #f))
(display (or #t))
(display (or #f #f))
(display (or #f #t))
(display (or #t #f))
(display (or #t #t))
(display (or #f #f #f #f #t))
(display (or #t #f #f #f #f))
(display (or #f #f #f #f #f))
(display (or #t (/ 1 0)))
(define delayed-value
  (delay (+ 2 3)))
(display (force delayed-value))

(define x 0)
(define lazy-inc
  (delay
    (begin
      (set! x (+ x 1))
      x)))
(display (force lazy-inc))
(display (force lazy-inc))

(define expensive
  (delay
    (begin
      (display "Complex calculations")
      (* 1234 5678))))

(display (force expensive))
(display (force expensive))

(define (lazy-if cond then-expr else-expr)
  (if cond
      (force then-expr)
      (force else-expr)))
(display (lazy-if #t (delay 10) (delay (/ 1 0))))
(display (lazy-if #f (delay 10) (delay 20)))

(define safe (delay (/ 1 0)))

(define (f x) (+ x 100))
(define delayed
  (delay (f 7)))
(force delayed)

(define a (delay (+ 1 2)))
(define b (delay (* (force a) 10)))
(define c (delay (- (force b) 7)))
(display (force c))
(display (*))
(display (* 2))
(display (* -2))
(display (* 1.2))
(display (* 1 2))
(display (* 2 2))
(display (* -2 -2))
(display (* 2 -2))
(display (* -2 2))
(display (* 1 2 3 4 5))
(display (* -2 -2 -2 -2 -2 -2 -2 0))
(display (* 1.5 1.5))
(display (+ 1 0))
(display (+ 2 7))
(display (+ (+ 2 7) 9))
(display (+ (+ 2 7) 0))
(display (+ (+ 7 7) (+ 2 4)))
(display (+))
(display (+ 1))
(display (+ 1.2))
(display (+ 1 1.2))
(display (+ 1.2 1))
(display (+ 1 2 3 4 5 6 7 8 9))
(display (+ 1 2 3 4 5 6 7.0 8 9))
(display (- 2))
(display (- 2 3))
(display (- 3 2))
(display (- 3 3))
(display (- 3.5 3))
(display (- 3 0))
(display (/ 1))
(display (/ 1.0))
(display (/ -1))
(display (/ -1.0))
(display (/ 2))
(display (/ -2))
(display (/ 4 2))
(display (/ 5 2))
(display "hello")
(display "hello \"world\"")
(display "")
(display "hello\nworld")
(display (display 0))
(display #\A )
(display #\a )
(display #\5 )
(display #\ )
(display #\\n )
(display #\" )
(display #\\\ )
(display #\' )
(display -0)
(display 1)
(display -1)
(display 0000000001)
(display 1.2)
(display -1.2)
(display .2)
(display -.2)
(display 0.)
(display -0.)
(display 4.)
(display #t)
(display #f)
(display (let ((x 40)) x))
(display (let ((x 40)) (+ 10 x)))
(display (let ((x 40) (y 60)) (+ x y)))
(display (let ((x 40) (y 60)) (display (+ x y)) x ))
(display (let ((x 10)) (let ((x 100)) (display x)) x ))
(display (let* ((x 10) (y x)) 10))
(display (let* ((x 10) (y x) (z y)) 10))
(display (let ((x 2) (y 3))
         (let* ((x 7)
         (z (+ x y)))
         (* z x))))
(display (letrec ((factorial
           (lambda (n)
             (if (= n 0)
                 1
                 (* n (factorial (- n 1)))))))
  (factorial 5)))

(display (letrec ((even
           (lambda (n)
             (if (= n 0)
                 #t
                 (odd (- n 1)))))
         (odd
           (lambda (n)
             (if (= n 0)
                 #f
                 (even (- n 1))))))
  (even 4)))

(display (letrec ((a (lambda (n) (if (= n 0) 1 (b (- n 1)))))
         (b (lambda (n) (if (= n 0) 0 (a (- n 1))))))
  (a 5)))

(define x 40)

(display x)
(set! x 50)
(display x)

(display (let ((y 10)) (set! y 60) y))
(display (let ((y 10)) (let ((y 100)) (set! y 0) (display y)) y))
(define x 20)
(define increment (lambda (x) (+ x 1)))
(display (increment 10))
(display (increment x))

;; set! and define in lambdas work on global variables if they are not named as local variables.

;; Setting a lambda to a global variable changes the global variable.
(define set-global (lambda () (set! x (+ x 1))))
(set-global)
(display x)

;; Setting a lambda to a argument changes the argument.
(define set-argument (lambda (x) (set! x (+ x 1)) x))
(display (set-argument  5))
(display x)

;; Defining a variable in a lambda creates a local variable.
(define define-in-lambda (lambda () (define x 100) (+ x 20 )))
(display (define-in-lambda))
(display x)

;; Defining a local variable in a lambda redefine a local variable.
(define define-local (lambda () (define x 100) (define x 200) (+ x 20 )))
(display (define-local))
(display x)

;; Defining a variable in a lambda redefine the argument.
(define define-argument (lambda (x) (define x 100) (+ x 0)))
(display (define-argument 213123124))
(display x)

;; Setting a lambda to a local variable changes the local variable.
(define set-local (lambda () (define x 300) (set! x (+ x 1)) x))
(display (set-local))
(display x)

(display (let ((to-zero (lambda (n) 0))) (to-zero 1234)))
(display (let ((calc (lambda (x y) (define sum (+ x y)) (define product (* x y)) (/ sum product)))) (calc 2 2)))

(define return-define (lambda () (define x 300)  x))
(display (return-define))

(define return-let (lambda () (let ((x 50)) x)))
(display (return-let))
(define x 20)

(display x)
(display (+ x 10))

(display (let ((y 40)) (+ x y)))
(display (let ((x 30)) (+ x x)))

(define x 100)

(display x)

;; Defining a local variable in a let redefine a local variable.
(display (let ((x 30)) (define x 10) (+ x x)))

(display x)
(display (= 1 2))
(display (= 2 1))
(display (= 2 2))
(display (= 2.0 2))
(display (= 2 2.0))
(display (= 2 2.1))
(display (= 2.1 2.1))
(display (= #t #t))
(display (= #f #f))
(display (= #t #f))
(display (= "hello" "hello"))
(display (= "hello" "bye"))
(display (= 1 #t))
(display (= 1 "true"))
(display (= #t "true"))
(display (= #\A #\A ))
(display (= #\A #\a ))
(display (= #\A #\B ))
(display (= #\A #\B ))
(display (= #\A "A" ))
(display (> 1 2))
(display (> 2 1))
(display (> 2 2))
(display (>= 1 2))
(display (>= 2 1))
(display (>= 2 2))
(display (< 1 2))
(display (< 2 1))
(display (< 2 2))
(display (<= 1 2))
(display (<= 2 1))
(display (<= 2 2))
;;
(display (> 1.1 2.1))
(display (>= 1.1 2.1))
(display (>= 2.1 2.1))
(display (< 1.1 2.1))
(display (<= 2.1 2.1))
;;
(display (> 2 2.1))
(display (< 2 2.1))
;;
(display (> -2 2))
(display (> 2 -2))
