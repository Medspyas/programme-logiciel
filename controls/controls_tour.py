import os
import sys

from models.match import Match

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class ControlsTour:
    # Controleur pour gérer les opérations liées aux tours.
    def __init__(self, tour, tournoi, menu):
        self.tour = tour
        self.tournoi = tournoi
        self.menu = menu
        self.tour_terminer = False

    def verifier_rencontre_joueurs(self, joueur_1, joueur_2):
        # Verifie si deux joueurs ce sont déja rencontrés durant les tours précédent.
        for tour in self.tournoi.liste_tours:
            for match in tour.liste_matches:
                if (
                    match.joueur_1.id_nationale == joueur_1.id_nationale
                    and match.joueur_2.id_nationale == joueur_2.id_nationale
                ) or (
                    match.joueur_1.id_nationale == joueur_2.id_nationale
                    and match.joueur_2.id_nationale == joueur_1.id_nationale
                ):
                    return True
        return False

    def generer_matchs(self):
        # Génère les matchs d'un tour en faisant en sorte que chaque est différent.
        liste_joueurs = self.tournoi.liste_joueurs

        if len(liste_joueurs) % 2 != 0:
            self.menu.afficher_message("Le nombre de joueurs n'est pas pair.")
            return

        liste_joueurs.sort(key=lambda joueur: (joueur.score, joueur.id_nationale), reverse=True)
        matchs_temporaire = []
        joueurs_deja_apparies = set()

        def trouver_appareillements(joueur_disponible):
            # Fonction récursive qui cherche à apparier tous les joueurs.
            # Retourne True si un appariement est complet.
            # Retourne False si un appariement échoue, et réessaye d'autre combinaisons. 
            if len(joueur_disponible) < 2:
                return True

            joueur_1 = joueur_disponible.pop(0)

            for i, joueur_2 in enumerate(joueur_disponible):
                if not self.verifier_rencontre_joueurs(joueur_1, joueur_2):
                    matchs_temporaire.append((joueur_1, joueur_2))
                    joueurs_deja_apparies.add(joueur_1)
                    joueurs_deja_apparies.add(joueur_2)

                    if trouver_appareillements(joueur_disponible[:i] + joueur_disponible[i + 1:]):
                        return True

                    matchs_temporaire.pop()
                    joueurs_deja_apparies.remove(joueur_1)
                    joueurs_deja_apparies.remove(joueur_2)

            joueur_disponible.insert(0, joueur_1)
            return False

        if trouver_appareillements(liste_joueurs[:]):

            for joueur_1, joueur_2 in matchs_temporaire:
                match = Match(joueur_1, joueur_2)
                self.tour.ajouter_match(match)
        else:
            return
