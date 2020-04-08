from enum import Enum

"""
Liste de tous les types de contraintes actuellement identifiees et utilisees
IBS =
IBD =
IBHD =
GBHD =
"""
class ConstraintType(Enum):
    # From TTModel
    # TECHNICAL
    IBS_SUP = "IBS supérieur"
    IBS_INF = "IBS inférieur"
    IBD_INF = "IBD inférieur"
    IBD_EQ = "IBD égal"
    IBHD_INF = "IBHD_inférieur"
    IBHD_EQ = "IBHD_égal"
    IBHD_SUP = "IBHD_supérieur"
    GBHD_INF = "GBHD_inférieur"
    GBHD_SUP = "GBHD_supérieur"
    CONJONCTION = "Conjonction"
    SEUIL = "Seuil"
    SI_A_ALORS_NON_B = "Si a alors non b"

    # CORE
    PAS_PLUS_1_COURS_PAR_CRENEAU = "Pas plus d'un cours par créneau"
    COURS_DOIT_ETRE_PLACE = "Le cours doit être placé"
    COURS_DOIT_AVOIR_PROFESSEUR = "Le cours doit avoir un professeur"
    PROFESSEUR_NE_PEUT_DONNER_2_COURS_EN_MEME_TEMPS = "Le professeur ne peut pas donner 2 cours en même temps"
    SALLE_NE_PEUT_ACCEPTER_2_COURS_EN_MEME_TEMPS = "Une salle ne peut pas être disponible pour 2 cours à un même moment"
    UN_COURS_POUR_UN_TYPE_DE_SALLE = "Chaque cours doit être assigné à un type de salle"
    SALLE_DISPO_AU_PLUS_1_FOIS = "Chaque salle ne peut être utilisée qu'une seule fois"

    # SPECIFIC
    PAS_DE_COURS_DE_DEMI_JOURNEE = "Pas de cours de demi-journée"
    PAS_DE_PROFESSEUR_DISPONIBLE = "Pas de professeur disponible"
    SIMUL_SLOT = "Simul slot"
    SALLE_PAS_DISPONIBLE = "La salle n'est pas disponible"
    SALLE_PREFEREE_NON_DISPONIBLE = "La salle préférée n'est pas disponible"
    DEPENDANCE = "Problème de dépendance"
    DEPENDANCE_SALLE = "Problème de dépendance entre les salles"
    DEPARTEMENT_BLOQUE_SLOT = "Les autres départements bloquent le slot"
    PROFESSEUR_A_DEJA_COURS_EN_AUTRE_DEPARTEMENT = "Le professeur a déjà un cours dans un autre département"
    PROFESSEUR_A_DEJA_COURS_EN_AUTRE_DEPARTEMENT_IBD = "Le professeur a déjà un cours dans un autre département IBD"

    # From iut
    BOUND_HOURS_PER_DAY = "Bound_hours per day"
    PAS_COURS_JEUDI_APREM = "Pas_de_cours_le_jeudi_aprem"
    PAS_SPORT_SAUF_LUNDI_ET_MARDI = "Pas de sport sauf lundi et mardi"
    PAS_COURS_PROMO1_SPORT = "pas de cours de promo1 sur un creneau de sport"
    CONF_SATELLITES = "Conference sattelites"
    B219_TO_LP = "B219 to LP"
    QUATRE_JOURS_AU_MOINS_POUR_IC = "4 jours au moins pour IC"
    SPECIFICITE_PDU = "spécificites PDU"
    REU_PEDA = "reu peda"
    SI_AJ_A_PLUS_DE_3_CRENEAUX_IL_PREFERE_VENIR_2_JOURS_DIFFERENT = "Si AJ a plus de 3 creneaux, il préfère venir 2 jours differents"
    VG_ET_AO_SONT_TOUJOURS_DANS_LA_MEME_SALLE = "VG et AO sont toujours dans la même salle"
    SEMAINE_REU_PEDAGOGIQUE_OU_EQUIPE = "Semaine de réunion pédagogique ou d'équipe"
    CDU_VEUT_VENIR_1_JOUR_ENTIER_QUAND_6_CRENEAUX = "CDU veut venir une journée entière quand il a 6 créneaux"
    CDU_VEUT_VENIR_1_JOUR_ENTIER_QUAND_7_CRENEAUX = "CDU veut venir une journée entière quand il a 7 créneaux"
    SEMAINE_3_EXAM_ISI = "Semaine 3 exam d'ISI"
    SEMAINE_5_MODULE_PR_GROUPE_1_4 = "Semaine 5 module PR groupe 1 et 4"
    PTUT_NO_COURSES = "PTUT_no_Courses"
    SEMAINE_6_JURY_VENDREDI = "Semaine 6, Jury le vendredi"
    JURY = "Jury"
    SEMAINE_FLOP = "Semaine FLOP"
    VACATAIRE_FAIT_TP240_ALORS_TITULAIRE_FAIT_TP_EN_MEME_TEMPS_MEME_MATIERE = "Si un vacataire fait un TP240, un titulaire fait un TP en même temps de la même matière"
    VACACATAIRE_SANS_PERMANENTS = "Vacataires_sans_permanents"
    PAS_PLUS_1_TD_PAR_DEMI_JOURNEE = "Pas plus d'un TD par demie-journee"
    MIN_HALF_DAYS = "Min half days"
    PAS_PLUS_4_COURS_PAR_DEMI_JOURNEE = "Pas plus de 4 heures par demie_journee"
    PAS_COURS_LUNDI_8H_POUR_RT2 = "Pas de cours lundi 8h pour RT2"
    SIMUL_FAKE = "Simul fake"
    PAS_COURS_LUNDI_8H_GIM2 = "pas de cours lundi 8h pour GIM2"
    PAS_PLUS_SEANCE_MEME_MODULE_PAR_JOUR = "Pas plus de seance du meme module par jour"
    SEMAINE_2_COURS_NBE_PPP3_VENDREDI = "semaine 2 Les cours de NBE de PPP3 sont le vendredi"
    SEMAINE_6_COURS_DBE_PPP2_LUNDI_MATIN = "semaine 6 Les cours de DBE et PPP2 sont le lundi matin"
    SEMAINE_6_COURS_CPR_PPP2_LUNDI_MATIN = "semaine 6 Les cours de CPR et PPP2 sont le lundi matin"
    SEMAINE_6_COURS_MPH_PPP2_JEUDI_APRES_MIDI = "semaine 6 Les cours de MPH et PPP2 sont le jeudi après-midi"
    SEMAINE_6_COURS_EPI_PPP2_MARDI_MATIN = "semaine 6 Les cours de EPI et PPP2 sont le mardi matin"
    TECH_MARDI_APREM = "Tech le mardi aprem"
    PAS_PLUS_5_CRENEAU = "Pas_plus_de_5_creneau"
    G1_G2_COURS_MEME_JOUR = "G1 et G2 ont cours le meme jour"

    # From TTApp/models.py
    MAX_HOURS = "Max hours"
    STABILIZE_ENRICH_MODEL = "Stabilize : enrich model"

    #minhalfdays
    MIN_HALF_DAYS_LIMIT = "Min Half Days limit"
    MIN_HALF_DAYS_LOCAL = "Min Half Days local"
    MIN_HALF_DAYS_JOIN_AM = "Min Half Days join AM"
    MIN_HALF_DAYS_JOIN_PM = "Min Half Days join PM"