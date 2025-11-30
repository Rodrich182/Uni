#lang racket

;;  FUNCIONES AUXILIARES 
;; Obtener la lista de vecinos de un nodo
(define (vecinos grafo nodo)
  (hash-ref grafo nodo '()))

;; Calcular el grado de un nodo
(define (grado grafo nodo)
  (length (vecinos grafo nodo)))

;; Eliminar una arista no dirigida (u -- v) del grafo
(define (eliminar-arista grafo u v)
  (let* ([vecinos-u (vecinos grafo u)]
         [vecinos-v (vecinos grafo v)]
         [nuevos-u (remove v vecinos-u)]
         [nuevos-v (remove u vecinos-v)])
    (hash-set (hash-set grafo u nuevos-u) v nuevos-v)))

;; Determinar el nodo de inicio correcto
;; - Si hay nodos de grado impar, DEBE empezar en uno de ellos (camino euleriano).
;; - Si todos son pares, puede empezar en cualquiera (circuito euleriano).
(define (encontrar-nodo-inicial grafo)
  (define nodos (hash-keys grafo))
  (define impares (filter (lambda (n) (odd? (grado grafo n))) nodos))
  (if (null? impares)
      (first nodos)      ; Caso circuito: cualquiera sirve
      (first impares)))  ; Caso camino: obligado uno impar


;; 1. LÓGICA DE PUENTES 
;; Cuenta cuántos nodos son alcanzables desde un nodo 'inicio' usando BFS
;; Sirve para saber si el grafo sigue conectado o se ha roto.
(define (contar-alcanzables grafo inicio)
  (let loop ((cola (list inicio))
             (visitados (set)))
    (if (null? cola)
        (set-count visitados)
        (let* ((u (first cola))
               (resto (rest cola)))
          (if (set-member? visitados u)
              (loop resto visitados)
              (loop (append resto (vecinos grafo u)) 
                    (set-add visitados u)))))))

;; Determina si la arista u-v es un "puente".
;; Una arista es puente si al quitarla, el número de nodos alcanzables disminuye.
(define (es-puente? grafo u v)
  (define n-antes (contar-alcanzables grafo u))
  (define grafo-sin (eliminar-arista grafo u v))
  (define n-despues (contar-alcanzables grafo-sin u))
  (< n-despues n-antes))

;; Elige el siguiente paso.
;; Regla de Fleury: Elige una arista que NO sea puente, a menos que no haya otra opción.
(define (mejor-vecino grafo u candidatos)
  (cond
    [(null? candidatos) #f]
    ;; Si solo hay un camino, no hay elección: hay que tomarlo
    [(null? (rest candidatos)) (first candidatos)]
    [else
     ;; Filtramos los vecinos que NO provocan un puente
     (define no-puentes (filter (lambda (v) (not (es-puente? grafo u v))) candidatos))
     (if (null? no-puentes)
         (first candidatos) ; Si todos son puentes, tomamos el primero (no queda otra)
         (first no-puentes))])) ; Si hay opciones seguras, tomamos la primera


;; 2. ALGORITMO DE FLEURY
;; Función recursiva que construye el camino paso a paso
(define (fleury-rec grafo u camino)
  (define ady (vecinos grafo u))
  (if (null? ady)
      (reverse (cons u camino)) ;; Base: No hay más aristas, devolvemos el camino
      (let* ([v (mejor-vecino grafo u ady)]
             [nuevo-g (eliminar-arista grafo u v)])
        (fleury-rec nuevo-g v (cons u camino)))))

;; Función de entrada solicitada por el enunciado
(define (Fleury grafo)
  (define inicio (encontrar-nodo-inicial grafo))
  (fleury-rec grafo inicio '()))

;; EJEMPLO DE PRUEBA

(define G
  (hash
   'A '(B)
   'B '(A C D)
   'C '(B D)
   'D '(B C)))

(displayln "Buscando camino Euleriano con Fleury en el grafo G:")
(displayln (Fleury G))
