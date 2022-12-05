#lang racket

;             [G] [W]         [Q]
; [Z]         [Q] [M]     [J] [F]
; [V]         [V] [S] [F] [N] [R]
; [T]         [F] [C] [H] [F] [W] [P]
; [B] [L]     [L] [J] [C] [V] [D] [V]
; [J] [V] [F] [N] [T] [T] [C] [Z] [W]
; [G] [R] [Q] [H] [Q] [W] [Z] [G] [B]
; [R] [J] [S] [Z] [R] [S] [D] [L] [J]
;  1   2   3   4   5   6   7   8   9
(define stack (vector (list "Z" "V" "T" "B" "J" "G" "R")
                      (list "L" "V" "R" "J")
                      (list "F" "Q" "S")
                      (list "G" "Q" "V" "F" "L" "N" "H" "Z")
                      (list "W" "M" "S" "C" "J" "T" "Q" "R")
                      (list "F" "H" "C" "T" "W" "S")
                      (list "J" "N" "F" "V" "C" "Z" "D")
                      (list "Q" "F" "R" "W" "D" "Z" "G" "L")
                      (list "P" "V" "W" "B" "J")))

(define (display-stack stack)
  (for ([i (in-range (vector-length stack))])
    (printf "~a: ~a\n" (+ i 1) (vector-ref stack i))))

(define (get-answer stack)
  (let ([top (map (λ (blocks) (first blocks)) (vector->list stack))])
    (apply string-append top)))

(define (parse-line str)
  (let ([split (string-split str " ")])
    (values (string->number (list-ref split 1))
            (string->number (list-ref split 3))
            (string->number (list-ref split 5)))))

; move n blocks from src to dst
(define (move stack n src dest reverse?)
  (let ([top (take (vector-ref stack src) n)]
        [bottom (drop (vector-ref stack src) n)])
    (vector-set! stack dest (append (if reverse? (reverse top) top) (vector-ref stack dest)))
    (vector-set! stack src bottom)))

(define (run-command stack line reverse?)
  (cond [(string-prefix? line "move")
         (let-values ([(n src dest) (parse-line line)])
           (move stack n (- src 1) (- dest 1) reverse?))]))

(define (solve reverse?)
  (let ([stack (vector-copy stack)])
    (for-each (λ (line) (run-command stack line reverse?)) (file->lines "input"))
    (get-answer stack)))

(printf "part 1: ~a\n" (solve #t))
(printf "part 2: ~a\n" (solve #f))
