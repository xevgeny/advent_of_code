;; part 1

(defun get-input (filename)
  (with-open-file (stream filename)
    (loop for line = (read-line stream nil)
          while line
          collect (parse-integer line))))

(defun find-pair (preamble sum)
  "finds pair with the given sum in a list for O(N)"
  (let ((ht (make-hash-table)))
    (loop for x in preamble
          when (gethash (- sum x) ht)
          do (return t)
          do (setf (gethash x ht) t))))

(defun inspect-preamble (filename preamble-len)
  (let ((preamble (get-input filename)))
    (loop for i from preamble-len below (list-length preamble)
          with sub-preamble = (subseq preamble (- i preamble-len) i)
          when (not (find-pair
                      (subseq preamble (- i preamble-len) i)
                      (nth i preamble)))
          do (progn
               (format t "number ~D violates preamble properties, pos ~D~%" (nth i preamble) i)
               (return (nth i preamble))))))

(inspect-preamble "./test_input" 5)
(inspect-preamble "./input" 25)

;; part 2

(defun find-seq (preamble sum pos)
  (loop for i from pos below (list-length preamble)
        maximize (nth i preamble) into max
        minimize (nth i preamble) into min
        sum (nth i preamble) into n
        when (<= n sum)
        do (if (= n sum)
             (progn
                (format t "encryption weakness is ~D~%" (+ min max))
                (return)))))

(defun find-weakness (filename preamble-len)
  (let ((preamble (get-input filename))
        (sum (inspect-preamble filename preamble-len)))
    (loop for pos from 0 below (list-length preamble)
        do (find-seq preamble sum pos))))

(find-weakness "./test_input" 5)
(find-weakness "./input" 25)
