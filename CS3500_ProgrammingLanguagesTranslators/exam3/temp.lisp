(setq g1 '((1 2) (2 3) (3 1) (3 4) (4 2) (4 5)))
(setq g2 '((2 1) (2 4) (1 3) (1 4) (3 2) (3 5) (5 6) (6 3) (4 2)))
(setq counter 0)


(defun countTrianglesWrap (graph)
  (loop for i in graph do
    (loop for j in graph do ;These two loops loop through all possible 'pairs' of edges in order to determine if the pair that would make them a triangle exists
      (progn
        (if (and (not (equal i j)) (= (nth 1 i) (nth 0 j))) ;Two of the same edges together cannot form a valid triangle so pass and the 2nd element of i must be the 1st element of j to avoid repeat edges
          (if (or (member (nth 0 i) j) (member (nth 1 i) j)) ;A single element from I must also appear in J to be a triangle to satisfy the relation
            (if (exists graph (nth 1 j) (nth 0 i)) ;If the valid pair we're looking for exists in the set g1/g2 that forms a triangle
              (progn
                (setq counter (+ 1 counter))            
              )
            )
          )
        )
      )
    )
  )
)

;Wrapper for count triangles to reset counter
(defun countTriangles (graph)
  (setq counter 0)
  (countTrianglesWrap graph)
  (print (/ counter 3)) ;divide by 3 because we're looking only for triangles in a directed graph
)


(defun exists (graph edgeA edgeB)
  (if (myFind graph (list edgeA edgeB)) 
    (return-from exists t)
  )
)

(defun myFind (graph element)
  (loop for i in graph doing
    (progn
      (if (= (nth 0 element) (nth 0 i))
        (if (= (nth 1 element) (nth 1 i))
          (return-from myFind t)
        )
      )
    )
  )
)
