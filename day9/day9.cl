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
          when (not (find-pair
                        (subseq preamble (- i preamble-len) i)
                        (nth i preamble)))
          do (format t "number ~D violates preamble properties, pos ~D~%" (nth i preamble) i))))

(inspect-preamble "./test_input" 5)
(inspect-preamble "./input" 25)