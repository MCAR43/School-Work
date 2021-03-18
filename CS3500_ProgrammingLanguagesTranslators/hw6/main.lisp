(setq counter 0)
(defun isPrime (num &optional (divisor (- num 1)))
  (if (= divisor 1) t (if (= (mod num divisor) 0) nil (isPrime num (- divisor 1))))
)

(defun toList (num)
  (map 'list #'digit-char-p (prin1-to-string num))  
)


(defun rotate (str places)
  (concatenate 'string (subseq str places) (subseq str 0 places))
)

(defun countSpecialPrimes (num)
   (setq numDigits (list-length (toList num)))
   (if (isSpecial num numDigits 0) 
     (setq counter (+ counter 1)) 
   )

   (if (<= num 2)
    counter
    (countSpecialPrimes (- num 1))
   )
)

(defun isSpecial (num maxRots index)
  (if (<= index (- maxRots 1))
    (setq newnum (rotate (write-to-string num) index))
    (return-from isSpecial t)
  )
  (if (isPrime (parse-integer newnum))
    (isSpecial num maxRots (+ index 1))
    nil
  )
)

;97 89 83 79 73
