(clear)


;정삼각형
(deftemplate equilateral-triangle
    (slot id)
    (slot point1)
    (slot point2)
    (slot point3)
    (multislot l-side)
    (multislot r-side)
    (multislot base)
    (slot ls-angle (default 60))
    (slot rs-angle (default 60))
    (slot v-angle (default 60))
    (slot area))

(deftemplate right-triangle
    (slot id)
    (slot point1)
    (slot point2)
    (slot point3)
    (multislot hypothenuse)
    (multislot adjacent)
    (multislot opposite)
    (slot h-value)
    (slot a-value)
    (slot o-value)
    (slot reference-angle (type Float))
    (slot opp-angle (type Float)))

(deftemplate triangle
    (slot id)
    (slot point1)
    (slot point2)
    (slot point3))

(deftemplate quad
    (slot id)
    (slot point1)
    (slot point2)
    (slot point3)
    (slot point4))

(deftemplate angle
    (slot id)
    (slot point1)
    (slot point2)
    (slot point3)
    (slot degree)
    (multislot just (default data)))

(deftemplate line
    (slot id)
    (slot point1)
    (slot point2)
    (slot value))

(deftemplate point-lies-on-line
    (slot id)
    (slot point)
    (slot start-point)
    (slot end-point))

;정삼각형 넓이 공식(변의 길이)
(deffunction equilateral-triangle-area-theorem (?v)
    (return (*(/ (sqrt 3) 4) (* ?v ?v))))

;삼각함수(cos)이용한 빗변의 길이
(deffunction Trigonometric-cos-theorem-1 (?v ?a)
    (return (/ ?v (Math.cos (Math.toRadians ?a)))))

; Symmetry Rule
(defrule symmetry-line
    (line (point1 ?p1) (point2 ?p2) (value ?v&~nil))
    (not (line (point1 ?p2) (point2 ?p1)))
    =>
    (assert (line (point1 ?p2) (point2 ?p1) (value ?v) )))

(defrule symmetry-angle
    ?angle <- (angle (point1 ?p) (point2 ?q) (point3 ?r) (degree ?d&~nil))
    (not (angle (point1 ?r) (point2 ~q) (point3 ~p) (degree ?d&~nil)))
    =>
    ; add new id for the new angle
    (assert (angle (point1 ?r) (point2 ?q) (point3 ?p) (degree ?d)(just symmetry-angle))))


; 정삼각형
(defrule assert-equilateral-triangle-1
    (triangle (point1 ?p1) (point2 ?p2) (point3 ?p3))
    (angle (point1 ?p1) (point2 ?p2) (point3 ?p3) (degree 60))
    (angle (point1 ?p2) (point2 ?p1) (point3 ?p3) (degree 60))
    (not (equilateral-triangle (point1 ?p1) (point2 ?p2) (point3 ?p3)))
    =>
    (assert (equilateral-triangle (point1 ?p1) (point2 ?p2) (point3 ?p3)
            (l-side ?p1 ?p3) (r-side ?p2 ?p3) (base ?p1 ?p2))))
(defrule assert-equilateral-triangle-2
    (triangle (point1 ?p2) (point2 ?p3) (point3 ?p1))
    (angle (point1 ?p1) (point2 ?p2) (point3 ?p3) (degree 60))
    (angle (point1 ?p2) (point2 ?p1) (point3 ?p3) (degree 60))
    (not (equilateral-triangle (point1 ?p2) (point2 ?p3) (point3 ?p1)))
    =>
    (assert (equilateral-triangle (point1 ?p2) (point2 ?p3) (point3 ?p1)
            (l-side ?p1 ?p3) (r-side ?p2 ?p3) (base ?p1 ?p2))))
(defrule assert-equilateral-triangle-3
    (triangle (point1 ?p3) (point2 ?p1) (point3 ?p2))
    (angle (point1 ?p1) (point2 ?p2) (point3 ?p3) (degree 60))
    (angle (point1 ?p2) (point2 ?p1) (point3 ?p3) (degree 60))
    (not (equilateral-triangle (point1 ?p3) (point2 ?p1) (point3 ?p2)))
    =>
    (assert (equilateral-triangle (point1 ?p3) (point2 ?p1) (point3 ?p2)
            (l-side ?p1 ?p3) (r-side ?p2 ?p3) (base ?p1 ?p2))))
(defrule assert-equilateral-triangle-4
    (triangle (point1 ?p3) (point2 ?p2) (point3 ?p1))
    (angle (point1 ?p1) (point2 ?p2) (point3 ?p3) (degree 60))
    (angle (point1 ?p2) (point2 ?p1) (point3 ?p3) (degree 60))
    (not (equilateral-triangle (point1 ?p3) (point2 ?p2) (point3 ?p1)))
    =>
    (assert (equilateral-triangle (point1 ?p3) (point2 ?p2) (point3 ?p1)
            (l-side ?p1 ?p3) (r-side ?p2 ?p3) (base ?p1 ?p2))))
(defrule assert-equilateral-triangle-5
    (triangle (point1 ?p2) (point2 ?p1) (point3 ?p3))
    (angle (point1 ?p1) (point2 ?p2) (point3 ?p3) (degree 60))
    (angle (point1 ?p2) (point2 ?p1) (point3 ?p3) (degree 60))
    (not (equilateral-triangle (point1 ?p2) (point2 ?p1) (point3 ?p3)))
    =>
    (assert (equilateral-triangle (point1 ?p2) (point2 ?p1) (point3 ?p3)
            (l-side ?p1 ?p3) (r-side ?p2 ?p3) (base ?p1 ?p2))))
(defrule assert-equilateral-triangle-6
    (triangle (point1 ?p1) (point2 ?p3) (point3 ?p2))
    (angle (point1 ?p1) (point2 ?p2) (point3 ?p3) (degree 60))
    (angle (point1 ?p2) (point2 ?p1) (point3 ?p3) (degree 60))
    (not (equilateral-triangle (point1 ?p1) (point2 ?p3) (point3 ?p2)))
    =>
    (assert (equilateral-triangle (point1 ?p1) (point2 ?p3) (point3 ?p2)
            (l-side ?p1 ?p3) (r-side ?p2 ?p3) (base ?p1 ?p2))))
(defrule assert-equilateral-triangle-7
    "세 변의 길이가 같은 삼각형은 정삼각형"
    (triangle (point1 ?p1) (point2 ?p3) (point3 ?p2))
    (line (point1 ?p1) (point2 ?p2) (value ?v1&~nil))
   (line (point1 ?p2) (point2 ?p3) (value ?v2&~nil))
    (line (point1 ?p3) (point2 ?p1) (value ?v3&~nil))
    (test (eq ?v1 ?v2 ?v3))
    (not (equilateral-triangle (point1 ?p1) (point2 ?p3) (point3 ?p2)))
    =>
    (assert (equilateral-triangle (point1 ?p1) (point2 ?p3) (point3 ?p2)
            (l-side ?p1 ?p3) (r-side ?p2 ?p3) (base ?p1 ?p2))))

; 직각삼각형
(defrule assert-right-triangle-1
    (triangle (point1 ?p1) (point2 ?p2) (point3 ?p3))
    (angle (point1 ?p1) (point2 ?p2) (point3 ?p3) (degree 90))
    (not (right-triangle (point1 ?p1) (point2 ?p2) (point3 ?p3)))
    =>
    (assert (right-triangle (point1 ?p1) (point2 ?p2) (point3 ?p3)
            (hypothenuse ?p1 ?p3) (adjacent ?p2 ?p3) (opposite ?p1 ?p2))))
(defrule assert-right-triangle-2
    (triangle (point1 ?p2) (point2 ?p3) (point3 ?p1))
    (angle (point1 ?p1) (point2 ?p2) (point3 ?p3) (degree 90))
    (not (right-triangle (point1 ?p2) (point2 ?p3) (point3 ?p1)))
    =>
    (assert (right-triangle (point1 ?p2) (point2 ?p3) (point3 ?p1)
            (hypothenuse ?p1 ?p3) (adjacent ?p2 ?p3) (opposite ?p1 ?p2))))
(defrule assert-right-triangle-3
    (triangle (point1 ?p3) (point2 ?p1) (point3 ?p2))
    (angle (point1 ?p1) (point2 ?p2) (point3 ?p3) (degree 90))
    (not (right-triangle (point1 ?p3) (point2 ?p1) (point3 ?p2)))
    =>
    (assert (right-triangle (point1 ?p3) (point2 ?p1) (point3 ?p2)
            (hypothenuse ?p1 ?p3) (adjacent ?p2 ?p3) (opposite ?p1 ?p2))))
(defrule assert-right-triangle-4
    (triangle (point1 ?p1) (point2 ?p3) (point3 ?p2))
    (angle (point1 ?p1) (point2 ?p2) (point3 ?p3) (degree 90))
    (not (right-triangle (point1 ?p1) (point2 ?p3) (point3 ?p2)))
    =>
    (assert (right-triangle (point1 ?p1) (point2 ?p3) (point3 ?p2)
            (hypothenuse ?p1 ?p3) (adjacent ?p2 ?p3) (opposite ?p1 ?p2))))
(defrule assert-right-triangle-5
    (triangle (point1 ?p3) (point2 ?p2) (point3 ?p1))
    (angle (point1 ?p1) (point2 ?p2) (point3 ?p3) (degree 90))
    (not (right-triangle (point1 ?p3) (point2 ?p2) (point3 ?p1)))
    =>
    (assert (right-triangle (point1 ?p3) (point2 ?p2) (point3 ?p1)
            (hypothenuse ?p1 ?p3) (adjacent ?p2 ?p3) (opposite ?p1 ?p2))))
(defrule assert-right-triangle-6
    (triangle (point1 ?p2) (point2 ?p1) (point3 ?p3))
    (angle (point1 ?p1) (point2 ?p2) (point3 ?p3) (degree 90))
    (not (right-triangle (point1 ?p2) (point2 ?p1) (point3 ?p3)))
    =>
    (assert (right-triangle (point1 ?p2) (point2 ?p1) (point3 ?p3)
            (hypothenuse ?p1 ?p3) (adjacent ?p2 ?p3) (opposite ?p1 ?p2))))


;피타고라스 정리
(defrule pythagoras-1
    ?right-triangle <- (right-triangle (hypothenuse ?p1&~nil ?p3&~nil) (h-value nil))
    (line (point1 ?p1) (point2 ?p3) (value ?v&~nil))
    =>
    (modify ?right-triangle (h-value ?v)))
(defrule pythagoras-2
    ?right-triangle <- (right-triangle (adjacent ?p1&~nil ?p3&~nil) (a-value nil))
    (line (point1 ?p1) (point2 ?p3) (value ?v&~nil))
    =>
    (modify ?right-triangle (a-value ?v)))
(defrule pythagoras-3
    ?right-triangle <- (right-triangle (opposite ?p1&~nil ?p3&~nil) (o-value nil))
    (line (point1 ?p1) (point2 ?p3) (value ?v&~nil))
    =>
    (modify ?right-triangle (o-value ?v)))
(defrule pythagoras-4
    ?right-triangle <- (right-triangle (h-value nil) (a-value ?a&~nil)(o-value ?o&~nil))
    =>
    (modify ?right-triangle (h-value (sqrt (+ (* ?a ?a) (* ?o ?o))))))
(defrule pythagoras-5
    ?right-triangle <- (right-triangle (h-value ?h&~nil) (a-value nil)(o-value ?o&~nil))
    =>
    (modify ?right-triangle (a-value (sqrt (- (* ?h ?h) (* ?o ?o))))))
(defrule pythagoras-6
    ?right-triangle <- (right-triangle (h-value ?h&~nil) (a-value ?a&~nil)(o-value nil))
    =>
    (modify ?right-triangle (o-value (sqrt (- (* ?h ?h) (* ?a ?a))))))
(defrule pythagoras-7
    ?right-triangle <- (right-triangle (hypothenuse ?p1 ?p2) (h-value ?v&~nil))
    ?line <-(line (point1 ?p1) (point2 ?p2) (value nil))
    =>
    (modify ?line (value ?v)))
(defrule pythagoras-7-1
    ?right-triangle <- (right-triangle (hypothenuse ?p1 ?p2) (h-value ?v&~nil))
    ?line <-(line (point1 ?p2) (point2 ?p1) (value nil))
    =>
    (modify ?line (value ?v)))
(defrule pythagoras-8
    ?right-triangle <- (right-triangle (adjacent ?p1 ?p2) (a-value ?v&~nil))
    ?line <-(line (point1 ?p1) (point2 ?p2) (value nil))
    =>
    (modify ?line (value ?v)))
(defrule pythagoras-8-1
    ?right-triangle <- (right-triangle (adjacent ?p1 ?p2) (a-value ?v&~nil))
    ?line <-(line (point1 ?p2) (point2 ?p1) (value nil))
    =>
    (modify ?line (value ?v)))
(defrule pythagoras-9
    ?right-triangle <- (right-triangle (opposite ?p1 ?p2) (o-value ?v&~nil))
    ?line <-(line (point1 ?p1) (point2 ?p2) (value nil))
    =>
    (modify ?line (value ?v)))
(defrule pythagoras-9-1
    ?right-triangle <- (right-triangle (opposite ?p1 ?p2) (o-value ?v&~nil))
    ?line <-(line (point1 ?p2) (point2 ?p1) (value nil))
    =>
    (modify ?line (value ?v)))

;정삼각형 넓이 공식(변의 길이를 알 때)
(defrule equilateral-triangle-area-1
    ?et <- (equilateral-triangle (r-side ?p1&~nil ?p2&~nil)(area ?a&nil))
    (line (point1 ?p1) (point2 ?p2) (value ?v&~nil))
    =>
    (modify ?et (area (equilateral-triangle-area-theorem ?v))))
(defrule equilateral-triangle-area-2
    ?et <- (equilateral-triangle (l-side ?p1&~nil ?p2&~nil)(area ?a&nil))
    (line (point1 ?p1) (point2 ?p2) (value ?v&~nil))
    =>
    (modify ?et (area (equilateral-triangle-area-theorem ?v))))
(defrule equilateral-triangle-area-3
    ?et <- (equilateral-triangle (base ?p1&~nil ?p2&~nil)(area ?a&nil))
    (line (point1 ?p1) (point2 ?p2) (value ?v&~nil))
    =>
    (modify ?et (area (equilateral-triangle-area-theorem ?v))))

(defrule point-lies-on-line-lengh
    (point-lies-on-line (point ?p)(start-point ?s)(end-point ?e))
    ?line <- (line (point1 ?s)(point2 ?e)(value ?v&nil))
    (line (point1 ?s)(point2 ?p)(value ?v1&~nil))
    (line (point1 ?p)(point2 ?e)(value ?v2&~nil))
    =>
    (modify ?line (value (+ ?v1 ?v2))))


(defquery q-1
    (declare (variables ?p1 ?p2 ?p3))
    (right-triangle (hypothenuse ?p1 ?p2)(h-value ?v1)))

(defquery q-6
    (declare (variables ?p1 ?p2 ?p3))
    (equilateral-triangle (point1 ?p1) (point2 ?p2)(point3 ?p3)(area ?v)))
   ;(line (point1 ?p1) (point2 ?p2)(value ?v)))

(defquery q-11
    (declare (variables ?p1 ?p2 ?p3))
    (right-triangle (hypothenuse ?p1 ?p2)(h-value ?v1))
    (right-triangle (hypothenuse ?p3 ?p2)(h-value ?v2)))

(defquery q-line
    (declare (variables ?p1 ?p2))
    (line (point1 ?p1) (point2 ?p2) (value ?v))

(defquery q-21
    (declare (variables ?p1 ?p2))
    (point-lies-on-line (start-point ?p1)(end-point ?p2))
    (line (point1 ?p1)(point2 ?p2)(value ?v)))
