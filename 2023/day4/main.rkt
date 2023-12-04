#lang racket

(define (score-1 xs ys)
  (let ([score (foldl (λ (x score) (if (member x ys) (* score 2) score)) 1 xs)]) 
    (floor (/ score 2))))

(define (score-2 xs ys)
  (foldl (λ (x score) (if (member x ys) (+ score 1) score)) 0 xs))

(define (parse-line line)
  (let* ([numbers (string-split line "|")]
         [xs (filter-map string->number (string-split (first numbers)))]
         [ys (map string->number (string-split (second numbers)))])
    (list xs ys)))

(define (score-card-2 lines)
  (let* ([vec (make-vector (length lines) 0)])
    (for ([(it i) (in-indexed lines)])
      (let ([score (apply score-2 it)])
        (when (> score 0)
          (for ([ii (in-range (+ i 1) (+ i score 1))])
            (vector-set! vec ii (+ (vector-ref vec ii) (vector-ref vec i) 1))))))
    (+ (length lines) (foldl + 0 (vector->list vec)))))

(let ([lines (map parse-line (file->lines "input"))])
  (printf "Part: 1: ~a\n" (apply + (map (λ (it) (apply score-1 it)) lines)))
  (printf "Part: 2: ~a\n" (score-card-2 lines)))
