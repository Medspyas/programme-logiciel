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

        

    




            


        

    