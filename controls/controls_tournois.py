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
        
        

if __name__ == "__main__":
  
    gestion_joueurs = GestionJoueurs()

  
    gestion_joueurs.ajouter_joueur("Dupont", "Jean", "01/01/1990", "FR12345", 0)
    gestion_joueurs.ajouter_joueur("Martin", "Paul", "02/02/1991", "FR12346", 0)
    gestion_joueurs.ajouter_joueur("Petit", "Luc", "03/03/1992", "FR12347", 0)
    gestion_joueurs.ajouter_joueur("Durand", "Sophie", "04/04/1993", "FR12348", 0)

   
    tournoi = Tournoi(
        nom="Tournoi Test",
        date_debut="24/09/2024",
        date_fin="25/09/2024",
        description="Un tournoi d'échecs de test",
        liste_joueurs=gestion_joueurs.liste_joueurs,
        nb_tour=4
    )

  
    controller_tournois = ControlsTournois(tournoi, gestion_joueurs)

  
    for tour_num in range(1, 5):
        print(f"\nLancement du Tour {tour_num}")
        controller_tournois.lancer_nouveau_tour(f"2024-09-24 {10+tour_num}:00:00", f"2024-09-24 {12+tour_num}:00:00")

       
        tournoi.liste_tour[-1].tour.afficher_matchs()

        
        gestion_joueurs.afficher_tous_les_joueurs()

   
    print("\nRésumé des tours générés :")
    for i, controle_tour in enumerate(tournoi.liste_tour, start=1):
        print(f"Tour {i} : {controle_tour.tour.nom_tour} avec {len(controle_tour.liste_matchs)} matchs")