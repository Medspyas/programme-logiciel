from models.tour import Tour
from models.joueur import Joueur , GestionJoueurs



class Tournoi:
    def __init__(self, nom, date_debut, date_fin, description, liste_joueurs, nb_tour):
        self.nom = nom
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nb_tour = nb_tour
        self.liste_joueurs = liste_joueurs
        self.liste_tours = [] 
        self.description = description
        self.tour_en_cours = 0


    def ajouter_tour(self, nom_tour, date_et_heure_debut, date_et_heure_fin):
        nouveau_tour = Tour(nom_tour, date_et_heure_debut, date_et_heure_fin)
        self.liste_tours.append(nouveau_tour)
        return self.liste_tours
    
    
        