


class Joueur:
    def __init__(self, nom, prenom, date_de_naissance) :
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance

    def afficher_informations_joueur(self):
        print(f"Nom: {self.nom} ; Prenom: {self.prenom} ; date_de_naissance: {self.date_de_naissance}") 



    

joueur = Joueur("delabe", "jean", "30/03/1996")

joueur.afficher_informations_joueur()
