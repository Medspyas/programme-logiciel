import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class ControlsJoueur:
    def __init__(self, gestion_joueurs, menu):
        self.gestion_joueurs = gestion_joueurs
        self.menu = menu

    def ajouter_joueur(self, nom, prenom, date_de_naissance, id_nationale, score=0):
        self.gestion_joueurs.ajouter_joueur(nom, prenom, date_de_naissance, id_nationale, score=0)

    def trouver_joueur(self, id_nationale):
        return self.gestion_joueurs.trouver_joueur_par_id(id_nationale)

    def mettre_a_jour_infos_joueur(self, id_nationale, attribut, nouvelle_valeur):
        joueur = self.trouver_joueur(id_nationale)
        if joueur:
            self.gestion_joueurs.mettre_a_jour_infos(joueur, attribut, nouvelle_valeur)

    def afficher_joueurs(self):
        joueurs = self.gestion_joueurs.obtenir_tous_les_joueurs()
        if not joueurs:
            self.menu.afficher_message("Aucun joueur")
        else:
            for joueur in joueurs:
                self.menu.afficher_message(joueur.afficher_informations_joueur())
