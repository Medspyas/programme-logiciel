from datetime import datetime 
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.joueur import Joueur, GestionJoueurs
from models.tournois import Tournoi
from models.tour import Tour
from controls_tour import ControlsTour 
from view.menu import MenuPrincipal     

class ControlsTournois:
    def __init__(self, tournoi, menu):
        self.tournoi = tournoi
        self.nb_tour= tournoi.nb_tour
        self.menu = menu
       
        

    


    def lancer_nouveau_tour(self, date_heure_debut):
        nb_tour_actuel = len(self.tournoi.liste_tours)

        if nb_tour_actuel >= self.nb_tour:
          
            self.menu.afficher_message("Tournois terminer. tous les tours ont été joués.")
            return
        
        
        nouveau_tour = Tour(f"Tour {nb_tour_actuel + 1}", date_heure_debut)
        controls_nouveau_tour = ControlsTour(nouveau_tour, self.tournoi, self.menu)
        
        controls_nouveau_tour.generer_matchs()
        self.tournoi.liste_tours.append(nouveau_tour)


   
        
        

