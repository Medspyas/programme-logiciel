


class Joueur:
    def __init__(self, nom, prenom, date_de_naissance, id_nationale, score) :
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.id_nationale = id_nationale
        self.score = score

        
        

    def afficher_informations_joueur(self):
        print(f"Nom: {self.nom}; Prenom: {self.prenom}; date_de_naissance: {self.date_de_naissance}; indentifiant nationale: {self.id_nationale}; score: {self.score}") 
    
    def mettre_a_jour_score(self, points):
        self.score += points
        return self.score

    def __str__(self):
        return f"{self.nom} {self.prenom} (ID: {self.id_nationale}, Score: {self.score})"


    

joueur1 = Joueur("Dupont", "Jean", "01/01/1990", "ID001", 0)
joueur2 = Joueur("Martin", "Alice", "15/05/1988", "ID002", 0)
joueur3 = Joueur("Durand", "Pierre", "20/07/1992", "ID003", 0)
joueur4 = Joueur("Leroy", "Sophie", "30/09/1991", "ID004", 0)


print(joueur1)

"""joueur1.afficher_informations_joueur()
joueur2.afficher_informations_joueur()
joueur3.afficher_informations_joueur()
joueur4.afficher_informations_joueur()"""
