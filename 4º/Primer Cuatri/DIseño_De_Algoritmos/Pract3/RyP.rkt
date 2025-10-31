#lang racket
(define (leer-fichero-listas-sin-indice ruta)
  (call-with-input-file ruta
    (lambda (in)
      (let loop ((linea (read-line in 'any))
                 (acumulador '()))
        (if (eof-object? linea)
            (reverse acumulador)
            (let* ((partes (string-split linea ":"))
                   (numeros-str (if (> (length partes) 1)
                                    (cadr partes)
                                    ""))
                   (numeros (filter number?
                                    (map string->number
                                         (string-split numeros-str))))
                   (ordenados (sort numeros <)))
              (loop (read-line in 'any) (cons ordenados acumulador))))))))

(define entrada (leer-fichero-listas-sin-indice "04_dat_01.txt"))

(define (Parcial-RyP datos)
  ; Complete todo el código que se necesite.
  ; Al final, debe devolver una lista de listas con las 
  ; habilidades de los individuos seleccionados.
)

(length (Parcial-RyP entrada)) ; deberia devolver 20
