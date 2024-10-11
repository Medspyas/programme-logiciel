import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class ControlsJoueur:
    def __init__(self, gestion_joueurs):
        self.gestion_joueurs = gestion_joueurs

    def ajouter_joueur(self, nom, prenom, date_de_naissance, id_nationale, score=0):
        self.gestion_joueurs.ajouter_joueur(nom, prenom, date_de_naissance, id_nationale, score=0)

    def trouver_joueur(self, id_nationale):
        joueur = self.gestion_joueurs.trouver_joueur_par_id(id_nationale)
        if joueur:
            return joueur
        print("Joueur introuvable")
        return None

    def mettre_a_jour_infos_joueur(self, id_nationale, attribut, nouvelle_valeur):
        joueur = self.trouver_joueur(id_nationale)
        if joueur:
            self.gestion_joueurs.mettre_a_jour_infos(joueur, attribut, nouvelle_valeur)

    def mettre_a_jour_score_joueur(self, id_nationale, points):
        joueur = self.trouver_joueur(id_nationale)
        if joueur:
            joueur.mettre_a_jour_score(points)

    def afficher_joueurs(self):
        self.gestion_joueurs.afficher_tous_les_joueurs()
