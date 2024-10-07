


class Joueur:
    def __init__(self, nom, prenom, date_de_naissance, id_nationale, score):
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.id_nationale = id_nationale
        self.score = score

        
        

    def afficher_informations_joueur(self):
        return f"Nom: {self.nom}; Prenom: {self.prenom}; date_de_naissance: {self.date_de_naissance}; indentifiant nationale: {self.id_nationale}; score: {self.score}"
    
    def mettre_a_jour_score(self, points):
        self.score += points
        return self.score
    
    

class GestionJoueurs:
    def __init__(self):
        self.liste_joueurs = []

    def ajouter_joueur(self, nom, prenom, date_de_naissance, id_nationale, score=0):
        nouveau_joueur = Joueur(nom, prenom, date_de_naissance, id_nationale, score)
        self.liste_joueurs.append(nouveau_joueur)
    
    def afficher_tous_les_joueurs(self):
        if not self.liste_joueurs:
            print("Aucun joueur")
        else:
            for joueur in self.liste_joueurs:
                print(joueur.afficher_informations_joueur())

    def trouver_joueur_par_id(self, id_nationale):
        for joueur in self.liste_joueurs:
            if joueur.id_nationale == id_nationale:
                return joueur
        print("Joueur introuvable.")
        return None
    
    def mettre_a_jour_infos(self, joueur, attribut, nouvelle_valeur):
        if hasattr(joueur, attribut):
            setattr(joueur, attribut, nouvelle_valeur)
            print(f"{attribut} de {joueur.nom} à bien été mis à jour.")
        else:
            print(f"L'attribut {attribut} n'existe pas.")
    

    
    

  


    


