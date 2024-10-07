import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.joueur import Joueur , GestionJoueurs
from models.tournois import Tournoi
from models.tour import Tour
from models.match import Match
from view.menu import MenuPrincipal


class ControlsTour:
    def __init__(self, tour, tournoi):
        self.tour = tour
        self.tournoi = tournoi
        self.menu = MenuPrincipal()
        self.tour_terminer = False
        
        

    def verifier_rencontre_joueurs(self, joueur_1, joueur_2):
        for tour in self.tournoi.liste_tours:
            for match in tour.liste_matches:
                if (match.joueur_1 == joueur_1) and (match.joueur_2 == joueur_2) or (match.joueur_1 == joueur_2) and (match.joueur_2 == joueur_1):
                    return True
        return False

    def generer_matchs(self):
        liste_joueurs = self.tournoi.liste_joueurs

        if len(liste_joueurs) % 2 != 0:
            return 

        nb_match = len(liste_joueurs) //2 
        match_crees = 0 
        liste_joueurs_appariement = liste_joueurs[:]

        while match_crees < nb_match:
            joueur_1 = liste_joueurs_appariement.pop(0)

            for i , joueur_2 in enumerate(liste_joueurs_appariement):
                if not self.verifier_rencontre_joueurs(joueur_1, joueur_2): 
                    match = Match(joueur_1, joueur_2)
                    self.tour.ajouter_match(match)
                    del liste_joueurs_appariement[i]
                    match_crees+=1
                    break
            if len(liste_joueurs_appariement) < 2 and match_crees < nb_match: 
                self.menu.afficher_message("Erreur: Plus de joueur disponible.")
                return

        

    

if __name__ == "__main__":
    
    gestion_joueurs = GestionJoueurs()
    gestion_joueurs.ajouter_joueur("Dupont", "Jean", "01/01/1990", "FR12345", 0)
    gestion_joueurs.ajouter_joueur("Martin", "Paul", "02/02/1991", "FR12346", 0)
    gestion_joueurs.ajouter_joueur("Petit", "Luc", "03/03/1992", "FR12347", 0)  

   
    tour_test = Tour("Round 1", "2023-09-21 10:00", "2023-09-21 12:00")

    
    controle_tour = ControlsTour(tour_test, gestion_joueurs)
    controle_tour.generer_matchs()

    
    print("\nMatchs générés :")
    for match in controle_tour.liste_matchs:
        print(f"{match.joueur_1.nom} vs {match.joueur_2.nom}")

   
    controle_tour.terminer_tour()

    
    print("\nÉtat du tour après avoir terminé :")
    if controle_tour.tour_terminer:
        print(f"Le tour {tour_test.nom_tour} est bien terminé.")
    else:
        print(f"Le tour {tour_test.nom_tour} n'est pas terminé.")


            


        

    