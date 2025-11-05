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

;; Utilidades con listas (sin sets)
(define (miembro? x xs) (and (member x xs) #t))
(define (union-uniqs a b)
  (foldl (lambda (x acc) (if (miembro? x acc) acc (cons x acc))) a b))
(define (diff a b) ;; a \ b
  (filter (lambda (x) (not (miembro? x b))) a))

(define (todas-habs datos)
  (foldl (lambda (h acc) (union-uniqs acc h)) '() datos))

(define (nuevas-habs habs-sel cand) (diff cand habs-sel))

;; Elige el índice del mejor candidato (máximo aporte nuevo); en empate, el menor índice
(define (elige-mejor-idx datos habs-sel)
  (let loop ((i 0) (best-i #f) (best-k -1) (rest datos))
    (cond
      [(null? rest) best-i]
      [else
       (define cand (car rest))
       (define k (length (nuevas-habs habs-sel cand)))
       (if (> k best-k)
           (loop (add1 i) i k (cdr rest))
           (loop (add1 i) best-i best-k (cdr rest)))])))

;; Voraz que devuelve los índices (etiquetas) de los candidatos seleccionados
(define (Parcial-voraz-indices datos)
  (let* ((objetivo (todas-habs datos))
         (n-total (length objetivo)))
    (let loop ((sel-idx '()) (cubiertas '()) (act datos))
      (if (>= (length cubiertas) n-total)
          (reverse sel-idx)
          (let ((i (elige-mejor-idx act cubiertas)))
            (if (not i) ;; sin mejoras posibles
                (reverse sel-idx)
                (let* ((cand (list-ref act i))
                       (aporta (nuevas-habs cubiertas cand))
                       (cubiertas2 (union-uniqs cubiertas aporta)))
                  ;; avanzamos en la lista para que no se re-seleccione el mismo candidato
                  ;; y mantenemos índices relativos al original a través de acumulación
                  (loop (cons i sel-idx) cubiertas2 act))))))))

;; En caso de que quieras también la “representación tipo Python” (etiquetas y tamaño):
(define (Seleccion-voraz datos)
  (let ((idx (Parcial-voraz-indices datos)))
    (values idx (length idx))))

;;Ejemplos:
(define datos-ej '((0 1 2) (2 3) (3 4) (4 5) (5 6)))
(Parcial-voraz-indices datos-ej)        ; => '(0 1 3) por ejemplo (según empates)
(call-with-values (lambda () (Seleccion-voraz datos-ej)) list)
;; Con tu fichero:
(Parcial-voraz-indices entrada)         ; etiquetas de candidatos seleccionados
(call-with-values (lambda () (Seleccion-voraz entrada)) list)
(length (Parcial-voraz-indices entrada)) ; esperado: 20