def preprocess(code: str) -> str:
    additional_standard_functions_code = """
(define (abs x)
  (if (>= x 0)
    x
    (- x)))

(define (zero? x) (= x 0))

(define (negative? x) (< x 0))

(define (positive? x) (> x 0))

(define (empty? coll) (= (length coll) 0))

(define (member? coll el)
  (if (> (length coll) 0)
    (if (= (car coll) el)
      #t
      (member? (cdr coll) el))
    #f))

(define (append coll el)
  (define (_append _coll _res)
    (if (> (length _coll) 0)
      (cons (car _coll) (_append (cdr _coll) el _res))
      (list el)))
  (_append coll (list)))

(define (map f coll)
  (letrec ((_map (lambda (_coll _res)
                   (if (> (length _coll) 0)
                     (_map (cdr _coll) (append _res (f (car _coll))))
                     _res))))
    (_map coll (list))))

(define (filter pred coll)
  (letrec ((_filter (lambda (_coll _res)
                   (if (> (length _coll) 0)
                     (let ((el (car _coll)))
                       (if (pred el)
                         (_filter (cdr _coll) (append _res el))
                         (_filter (cdr _coll) _res)))
                     _res))))
    (_filter coll (list))))

(define (quotient n1 n2)
  (to-integer(/ n1 n2)))

(define (remainder n1 n2)
  (- n1 (* n2 (quotient n1 n2))))

(define _floor (native cmath/floor double double))

(define (modulo n1 n2)
  (if (< n2 0)
    (- (modulo (- n1) (- n2)))
    (if (>= n1 0)
      (remainder n1 n2)
      (+ n1 (- (* n2 (to-integer (_floor (to-double (/ n1 n2))))))))))\n\n"""

    return additional_standard_functions_code + code
