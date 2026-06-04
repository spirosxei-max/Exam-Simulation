# questions_pool.py

ALL_QUESTIONS = [
    # --- Manhattan Prep 5 lb. Book ---
    {
        "id": "MP_Q1",
        "book": "Manhattan Prep 5lb",
        "type": "QC",
        "context": "Συγκρίνετε τις δύο ποσότητες:",
        "quantity_a": "0.01410 (με περιοδικό το 410)",
        "quantity_b": "0.0141 (με περιοδικό το 41)",
        "correct_answer": "C",
        "explanation": "Και οι δύο αριθμοί επεκτείνονται ως 0.014101410... επομένως είναι απολύτως ίσοι."
    },
    {
        "id": "MP_Q2",
        "book": "Manhattan Prep 5lb",
        "type": "QC",
        "context": "Ένα βιβλιοπωλείο πουλάει 200 paperbacks από $8 έως $12 το καθένα, και 100 hardbacks από $14 έως $18 το καθένα.",
        "quantity_a": "Η μέση τιμή (average price) όλων των βιβλίων στο κατάστημα",
        "quantity_b": "$9.99",
        "correct_answer": "A",
        "explanation": "Ακόμη και στην ελάχιστη τιμή τους, ο μέσος όρος είναι [(200*8) + (100*14)] / 300 = $10. Το $10 είναι μεγαλύτερο από το $9.99."
    },
    {
        "id": "MP_Q10",
        "book": "Manhattan Prep 5lb",
        "type": "NE",
        "question": "Αν $3x + 6y = 69$ και $2x - y = 11$, ποια είναι η τιμή του $y$;",
        "correct_answer": "7",
        "explanation": "Λύνοντας το σύστημα εξισώσεων: Πολλαπλασιάζουμε τη δεύτερη με 6 -> $12x - 6y = 66$. Προσθέτουμε: $15x = 135 \\Rightarrow x = 9$. Αντικαθιστούμε: $2(9) - y = 11 \\Rightarrow y = 7$."
    },
    {
        "id": "MP_Q11",
        "book": "Manhattan Prep 5lb",
        "type": "MC",
        "question": "Αν $7^9 + 7^9 + 7^9 + 7^9 + 7^9 + 7^9 + 7^9 = 7^x$, ποια είναι η τιμή του $x$;",
        "choices": ["9", "10", "12", "63", "97"],
        "correct_answer": "10",
        "explanation": "Το αριστερό μέλος είναι $7 \\times 7^9$, το οποίο ισούται με $7^{1+9} = 7^{10}$. Επομένως $x = 10$."
    },
    
    # --- Princeton Review ---
    {
        "id": "PR_Q1",
        "book": "Princeton Review",
        "type": "QC",
        "context": "Δίνεται ότι: $y \\neq 0$",
        "quantity_a": "$5y^2$",
        "quantity_b": "$-\\frac{y^2}{7}$",
        "correct_answer": "A",
        "explanation": "Το $y^2$ είναι πάντα θετικό για $y \\neq 0$. Άρα η Ποσότητα Α είναι θετική και η Ποσότητα Β αρνητική."
    },
    {
        "id": "PR_Q3",
        "book": "Princeton Review",
        "type": "QC",
        "context": "Συγκρίνετε τα γινόμενα:",
        "quantity_a": "$35,043 \\times 25,430$",
        "quantity_b": "$35,430 \\times 25,043$",
        "correct_answer": "A",
        "explanation": "Στην Ποσότητα Α ο μεγαλύτερος αριθμός (35k) πολλαπλασιάζεται με το 430, ενώ στη Β με το 43. Άρα η Α είναι μεγαλύτερη."
    },
    {
        "id": "PR_Q5",
        "book": "Princeton Review",
        "type": "QC",
        "context": "Ιδιότητες Πρώτων Αριθμών:",
        "quantity_a": "Ο μικρότερος πρώτος παράγοντας του $7^2$",
        "quantity_b": "Ο μικρότερος πρώτος παράγοντας του $2^7$",
        "correct_answer": "A",
        "explanation": "Ο μικρότερος (και μοναδικός) πρώτος παράγοντας του $7^2$ είναι το 7. Του $2^7$ είναι το 2. Το 7 > 2."
    },
    {
        "id": "PR_Q20",
        "book": "Princeton Review",
        "type": "MC",
        "question": "Αν $x = 3^2$, ποια είναι η τιμή του $x^x$;",
        "choices": ["$3^4$", "$3^8$", "$3^9$", "$3^{12}$", "$3^{18}$"],
        "correct_answer": "$3^{18}$",
        "explanation": "Αντικαθιστούμε το $x$: $x^x = (3^2)^{(3^2)} = (3^2)^9 = 3^{2 \\times 9} = 3^{18}$."
    }
]
