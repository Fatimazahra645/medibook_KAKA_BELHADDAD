def suggest_speciality(text):
    text = text.lower()

    if "poitrine" in text or "coeur" in text:
        return "Cardiologie"

    if "peau" in text or "bouton" in text:
        return "Dermatologie"

    if "dent" in text:
        return "Dentisterie"

    if "enfant" in text or "fièvre" in text:
        return "Pédiatrie"

    return "Médecine générale"