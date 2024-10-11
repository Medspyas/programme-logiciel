class Match:
    def __init__(self, joueur_1, joueur_2, score_joueur_1=0, score_joueur_2=0):
        self.joueur_1 = joueur_1
        self.joueur_2 = joueur_2
        self.score_joueur_1 = score_joueur_1
        self.score_joueur_2 = score_joueur_2

    def stockage_resultat_joueur(self):
        liste_1 = [f"{self.joueur_1.nom} {self.joueur_1.prenom}", self.score_joueur_1]
        liste_2 = [f"{self.joueur_2.nom} {self.joueur_2.prenom}", self.score_joueur_2]
        return (liste_1, liste_2)
