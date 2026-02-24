#lang racket
;; Bottom-up: construye pk[n][k] para 0<=n<=N y 0<=k<=N y devuelve pk[N][N].

(define (p-bottom N)
  (let ([pk (make-vector (+ N 1) #f)])
    ;; pk[n] será un vector de k=0..N
    (do ([n 0 (+ n 1)])
        [(> n N)]
      (vector-set! pk n (make-vector (+ N 1) 0)))

    ;; caso base pk[0][0] = 1 (partición vacía)
    (vector-set! (vector-ref pk 0) 0 1)

    ;; rellenar por k=0..N, n=0..N
    (do ([k 0 (+ k 1)])
        [(> k N)]
      (do ([n 0 (+ n 1)])
          [(> n N)]
        (cond
          [(and (= n 0) (= k 0))
           (void)] ; ya está
          [(and (>= n 0) (>= k 1))
           (let* ([a (vector-ref (vector-ref pk n) (- k 1))]
                  [b (if (>= (- n k) 0)
                         (vector-ref (vector-ref pk (- n k)) k)
                         0)])
             (vector-set! (vector-ref pk n) k (+ a b)))]
          [else
           (vector-set! (vector-ref pk n) k 0)])))

    (vector-ref (vector-ref pk N) N)))


(for ([n (in-range 0 11)])
  (printf "p(~a) = ~a\n" n (p-bottom n)))