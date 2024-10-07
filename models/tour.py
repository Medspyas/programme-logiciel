from models.match import Match


class Tour:
    def __init__(self, nom_tour, date_et_heure_debut, date_et_heure_fin=None):
        self.nom_tour = nom_tour
        self.liste_matches = []
        self.date_et_heure_debut = date_et_heure_debut
        self.date_et_heure_fin = date_et_heure_fin
        self.score_match = None
        

    def ajouter_match(self, match):
        self.liste_matches.append(match)
        
        
    
    def afficher_matchs(self):
        for match in self.liste_matches:
            resultat = match.stockage_resultat_joueur()
            print(resultat)


tour1 = Tour("round1" , "02/02/2024  10:00" , "02/02/2024 14:00")







