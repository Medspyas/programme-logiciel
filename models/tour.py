class Tour:
    # Représente un tour pendant un tournois.
    def __init__(self, nom_tour, date_et_heure_debut, date_et_heure_fin=None):
        self.nom_tour = nom_tour
        self.liste_matches = []
        self.date_et_heure_debut = date_et_heure_debut
        self.date_et_heure_fin = date_et_heure_fin
        self.score_match = None

    def ajouter_match(self, match):
        # Ajoute un match dans une lite.
        self.liste_matches.append(match)

    def afficher_matchs(self):
        # Renvoie les informations d'un match
        resultats = []
        for match in self.liste_matches:
            resultat = match.stockage_resultat_joueur()
            resultats.append(resultat)
        return resultats
