from tour import *



class Tournoi:
    def __init__(self, nom, date_debut, date_fin, tour_actuel, liste_joueurs, description):
        self.nom = nom
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nb_tour = 4
        self.tour_actuel = tour_actuel
        self.liste_tour = [] 
        self.liste_joueurs = liste_joueurs
        self.description = description


    def ajouter_tours(self, nom_tour, date_et_heure_debut, date_et_heure_fin):
        nouveau_tour = Tour(nom_tour, date_et_heure_debut, date_et_heure_fin)
        self.liste_tour.append(nouveau_tour)
        return self.liste_tour
    
    def tour_suivant(self):
        if self.tour_actuel < self.nb_tour:
            nom_tour = f"Tour {self.tour_actuel + 1}"
            self.ajouter_tours(nom_tour, self.date_et_heure_debut, self.date_et_heure_fin)
            
            self.tour_actuel += 1
        else:
            print("Tous les tours ont déjà été ajoutés.")
        