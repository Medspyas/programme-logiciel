from match import *


class Tour:
    def __init__(self, nom_tour, date_et_heure_debut, date_et_heure_fin):
        self.nom_tour = nom_tour
        self.liste_matches = []
        self.date_et_heure_debut = date_et_heure_debut
        self.date_et_heure_fin = date_et_heure_fin
        self.score_match = None
        

    def ajouter_match(self, joueur_1, joueur_2):
        nouveau_match = Match(joueur_1, joueur_2, 0, 0)
        nouveau_match.calculer_score()
        self.liste_matches.append(nouveau_match)
        return self.liste_matches
    
    def afficher_matchs(self):
        for match in self.liste_matches:
            print(match)


tour1 = Tour("round1" , "02/02/2024  10:00" , "02/02/2024 14:00")

tour1.ajouter_match(joueur1, joueur2)
tour1.ajouter_match(joueur3, joueur4)

tour1.afficher_matchs()



