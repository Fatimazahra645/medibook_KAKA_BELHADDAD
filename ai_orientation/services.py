def suggest_speciality(text):
    text = text.lower()

    if "poitrine" in text or "coeur" in text or "palpitation" in text:
        return "Cardiologie"

    if "peau" in text or "bouton" in text or "rougeur" in text:
        return "Dermatologie"

    if "dent" in text or "dentaire" in text:
        return "Dentisterie"

    if "enfant" in text or "fièvre" in text or "pédiatrie" in text:
        return "Pédiatrie"

    if "oeil" in text or "vue" in text or "vision" in text:
        return "Ophtalmologie"

    if "oreille" in text or "nez" in text or "gorge" in text:
        return "ORL"

    return "Médecine générale"
