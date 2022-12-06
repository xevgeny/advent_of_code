#lang racket

(define (all-different? xs)
  (let loop ([xs xs])
    (cond
      [(empty? xs) #t]
      [(member (first xs) (rest xs)) #f]
      [else (loop (rest xs))])))

(define (process-signal xs n)
  (let loop ([xs xs] [pos 0])
    (cond
      [(empty? xs) #f]
      [(all-different? (take xs n)) (+ pos n)]
      [else (loop (rest xs) (+ pos 1))])))

(printf "Part 1: ~a\n" (process-signal (string->list (file->string "input")) 4))
(printf "Part 2: ~a\n" (process-signal (string->list (file->string "input")) 14))