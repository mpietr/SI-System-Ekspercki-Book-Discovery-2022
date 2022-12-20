(deftemplate message
    (slot name (type STRING))
    (slot question (type STRING))
    (multislot answers (type STRING))
)

(deftemplate book
    (slot author (type STRING))
    (slot title (type STRING))
)



(defrule genre
    =>
    (assert (message (name "genre") (question "Which type of book are you looking for?") (answers "Fantasy" "Sci-fi" "Both")))
)


(defrule fairy-tale
    ?f <- (genre "Fantasy")
    ?id <- (message (name ?x))
    =>
    (retract ?id)
    (retract ?f)
    (assert (message (name "fairy-tale") (question "Up for a fairy tale?") (answers "Yes, why mess with classic formula" "No, something more gritty")))
)
