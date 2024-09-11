import random
from joueur import*


class Match:
    def __init__(self, joueur_1, joueur_2, score_joueur_1, score_joueur_2):
        self.joueur_1 = joueur_1
        self.joueur_2 = joueur_2
        self.score_joueur_1 = score_joueur_1
        self.score_joueur_2 = score_joueur_2


    def obtenir_résultats_possibles(self):
        return ["Joueur 1 gagne", "Joueur 2 gagne", "Match nul"]
    
    def attribuer_resultat(self):
        resultats = self.obtenir_résultats_possibles()

        resultat_match = random.choice(resultats)

        return resultat_match
        

    def calculer_score(self):
        resultat_match = self.attribuer_resultat()
        if resultat_match == "Joueur 1 gagne":
            self.score_joueur_1 += 1
        elif resultat_match == "Joueur 2 gagne":
            self.score_joueur_2 +=1
        else: 
            self.score_joueur_1 += 0.5
            self.score_joueur_2 += 0.5

    def stockage_resulat_joueur(self, joueur_1, joueur_2, score_joueur_1, score_joueur_2):
        liste_1 = [joueur_1, score_joueur_1]
        liste_2 = [joueur_2, score_joueur_2]
        return (liste_1, liste_2)
    

    def __str__(self):
        return f"Match entre {self.joueur_1} et {self.joueur_2}: Score {self.score_joueur_1}-{self.score_joueur_2}"

        


match1 = Match(joueur1, joueur2, 1, 0)  
match2 = Match(joueur3, joueur4, 0, 1) 

