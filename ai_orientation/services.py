"""
Module d'orientation médicale intelligente.
Approche : TF-IDF + similarité cosinus (scikit-learn) — cahier des charges §7.2
Le système suggère une spécialité à partir du texte libre du patient.
Il ne fait PAS de diagnostic médical.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------------------------------------------------
# Base de connaissances : spécialité → mots-clés / descriptions médicales
# -----------------------------------------------------------------------
SPECIALITY_CORPUS = {
    "Cardiologie": (
        "douleur poitrine coeur palpitation essoufflement tachycardie "
        "hypertension tension pression artérielle infarctus arythmie "
        "battements irreguliers souffle cardiaque fatigue effort"
    ),
    "Dermatologie": (
        "peau bouton acné rougeur démangeaison eczéma psoriasis urticaire "
        "tache grain de beauté verrue mycose champignon cheveux chute "
        "prurit éruption cutanée brulure peau sèche"
    ),
    "Dentisterie": (
        "dent dentaire douleur molaire gencive saignement carie "
        "extraction couronne bridge implant orthodontie appareil "
        "sensibilité froid chaud machoire abcès"
    ),
    "Pédiatrie": (
        "enfant bébé nourrisson fièvre vaccination croissance "
        "otite angine bronchite pédiatrique poids taille développement "
        "alimentation allaitement nouveau-né"
    ),
    "Ophtalmologie": (
        "oeil vue vision trouble myopie presbytie astigmatisme "
        "lunettes lentilles rougeur larmes irritation cataracte "
        "glaucome fond oeil mal tête lecture écran"
    ),
    "ORL": (
        "oreille nez gorge sinusite rhume rhinite otite angine "
        "amygdales toux mal gorge enrouement perte voix vertige "
        "acouphène surdité audition congestion nasale"
    ),
    "Gynécologie": (
        "grossesse contraception cycle menstruation règles douleur "
        "pelvienne ovaire kyste fibrome col utérus frottis "
        "ménopause fertilité suivi gynécologique"
    ),
    "Neurologie": (
        "mal tête migraine céphalée vertige étourdissement tremblements "
        "paralysie engourdissement fourmillements épilepsie convulsion "
        "mémoire concentration sclérose parkinson"
    ),
    "Radiologie": (
        "radio radiographie scanner irm echographie imagerie bilan "
        "résultat examen radiologique"
    ),
    "Médecine générale": (
        "fatigue fièvre grippe rhume toux mal dos courbature "
        "bilan sanguin tension suivi traitement médicament ordonnance "
        "certificat médical vaccination adulte"
    ),
}

# Construire le vecteur TF-IDF une seule fois au chargement du module
_speciality_names = list(SPECIALITY_CORPUS.keys())
_corpus_texts = list(SPECIALITY_CORPUS.values())

_vectorizer = TfidfVectorizer(analyzer="word", ngram_range=(1, 2))
_corpus_matrix = _vectorizer.fit_transform(_corpus_texts)


def suggest_speciality(symptoms_text: str, top_n: int = 3) -> list[dict]:
    """
    Analyse le texte libre du patient et retourne les spécialités les plus
    pertinentes triées par score de similarité cosinus.

    Retourne une liste de dicts :
        [{"speciality": "Cardiologie", "score": 0.87}, ...]

    La liste contient au maximum top_n résultats avec score > 0.
    Si aucune correspondance, retourne Médecine générale par défaut.
    """
    if not symptoms_text or not symptoms_text.strip():
        return [{"speciality": "Médecine générale", "score": 0.0}]

    query_vector = _vectorizer.transform([symptoms_text.lower()])
    similarities = cosine_similarity(query_vector, _corpus_matrix).flatten()

    # Associer chaque score à sa spécialité
    scored = [
        {"speciality": _speciality_names[i], "score": round(float(similarities[i]), 3)}
        for i in range(len(_speciality_names))
    ]

    # Trier par score décroissant
    scored.sort(key=lambda x: x["score"], reverse=True)

    # Garder uniquement les résultats avec un score > 0
    results = [s for s in scored if s["score"] > 0][:top_n]

    if not results:
        return [{"speciality": "Médecine générale", "score": 0.0}]

    return results
