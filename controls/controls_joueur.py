import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class ControlsJoueur:

    # Controleur pour gérer les opérations liées aux joueurs.

    def __init__(self, gestion_joueurs, menu):
        self.gestion_joueurs = gestion_joueurs
        self.menu = menu

    def ajouter_joueur(self, nom, prenom, date_de_naissance, id_nationale):
        # Ajoute un joueur à la liste.
        self.gestion_joueurs.ajouter_joueur(nom, prenom, date_de_naissance, id_nationale, score=0)

    def trouver_joueur(self, id_nationale):
        # Trouver un joueur par son ID nationale;
        return self.gestion_joueurs.trouver_joueur_par_id(id_nationale)

    def mettre_a_jour_infos_joueur(self, id_nationale, attribut, nouvelle_valeur):
        # Mets à jour une information d'un joueur
        joueur = self.trouver_joueur(id_nationale)
        if joueur:
            self.gestion_joueurs.mettre_a_jour_infos(joueur, attribut, nouvelle_valeur)

    def afficher_joueurs(self):
        # Affiche la liste de tous les joueurs
        joueurs = self.gestion_joueurs.obtenir_tous_les_joueurs()
        if not joueurs:
            self.menu.afficher_message("Aucun joueur")
        else:
            for joueur in joueurs:
                self.menu.afficher_message(joueur.afficher_informations_joueur())
