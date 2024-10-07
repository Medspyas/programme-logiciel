from datetime import datetime 
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.joueur import Joueur, GestionJoueurs
from models.tournois import Tournoi
from models.tour import Tour
from controls_tour import ControlsTour 
from view.menu import MenuPrincipal     

class ControlsTournois:
    def __init__(self, tournoi):
        self.tournoi = tournoi
        self.nb_tour= tournoi.nb_tour
       
        

    def lancer_tournois(self):
        if not self.tournoi.liste_joueurs:
            print("Impossible de  lancer le tounois : aucun joueur n'est incrit")
            return
        print(f"Lancement du tournois {self.tournoi.nom}")
        self.lancer_nouveau_tour(self.date_heure_debut)


    def lancer_nouveau_tour(self, date_heure_debut):
        nb_tour_actuel = len(self.tournoi.liste_tours)

        if nb_tour_actuel >= self.nb_tour:
            print("Tournois terminer. tous les tours ont été joués.")
            return
        
        
        nouveau_tour = Tour(f"Tour {nb_tour_actuel + 1}", date_heure_debut)
        print(f"Appel de generer_matchs() pour le tour {nouveau_tour.nom_tour}")
        controls_nouveau_tour = ControlsTour(nouveau_tour, self.tournoi)
        
        controls_nouveau_tour.generer_matchs()
        print(f"Nombre de matchs générés: {len(nouveau_tour.liste_matches)}")
        self.tournoi.liste_tours.append(nouveau_tour)


    def terminer_tour(self):
        if self.tournoi.tour_en_cours < self.tournoi.nb_tour:
            self.tournoi.tour_en_cours +=1
        
        

