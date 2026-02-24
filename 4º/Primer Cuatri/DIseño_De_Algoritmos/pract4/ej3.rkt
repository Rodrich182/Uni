#lang racket
;; p(n): número de particiones de n
(define (p n)
  (p-act n n))

;; p-act(n,k): número de particiones de n con longitud <= k
(define (p-act n k)
  (cond
    [(and (= n 0) (= k 0)) 1]
    [(and (>= n 0) (>= k 1))
     (+ (p-act n (- k 1))
        (p-act (- n k) k))]
    [else 0]))

;; Ejemplos:
(p 0)   ; => 1
(p 1)   ; => 1
(p 2)   ; => 2
(p 3)   ; => 3
(p 4)   ; => 5
(p 5)   ; => 7
(p 6)   ; => 11
(p 10)  ; => 42

