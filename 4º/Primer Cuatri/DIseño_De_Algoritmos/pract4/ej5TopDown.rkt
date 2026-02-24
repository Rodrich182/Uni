#lang racket
;; Top-down con memoización.
;; Devuelve p(n) usando una tabla (n+1) x (n+1) inicializada a #f.

(define (p-top n)
  (let* ([memo (make-vector (+ n 1) #f)])
    (do ([i 0 (+ i 1)])
        [(> i n)]
      (vector-set! memo i (make-vector (+ n 1) #f)))

    (define (memo-ref n k) (vector-ref (vector-ref memo n) k))
    (define (memo-set! n k v) (vector-set! (vector-ref memo n) k v))

    (define (p-act-m n k)
      (cond
        [(or (< n 0) (< k 0)) 0] ; fuera de dominio útil
        [else
         (let ([cached (memo-ref n k)])
           (if cached
               cached
               (let ([v
                      (cond
                        [(and (= n 0) (= k 0)) 1]
                        [(and (>= n 0) (>= k 1))
                         (+ (p-act-m n (- k 1))
                            (p-act-m (- n k) k))]
                        [else 0])])
                 (memo-set! n k v)
                 v)))]))

    (p-act-m n n)))
