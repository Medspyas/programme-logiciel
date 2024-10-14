class Joueur:
    def __init__(self, nom, prenom, date_de_naissance, id_nationale, score):
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.id_nationale = id_nationale
        self.score = score

    def afficher_informations_joueur(self):
        return f"{self.id_nationale} - {self.nom} - {self.prenom} - {self.date_de_naissance}"

    def mettre_a_jour_score(self, points):
        self.score += points
        return self.score


class GestionJoueurs:
    def __init__(self, menu):
        self.liste_joueurs = []
        self.menu = menu

    def ajouter_joueur(self, nom, prenom, date_de_naissance, id_nationale, score=0):
        nouveau_joueur = Joueur(nom, prenom, date_de_naissance, id_nationale, score)
        self.liste_joueurs.append(nouveau_joueur)

    def obtenir_tous_les_joueurs(self):
        return self.liste_joueurs

    def trouver_joueur_par_id(self, id_nationale):
        for joueur in self.liste_joueurs:
            if joueur.id_nationale == id_nationale:
                return joueur
        return None

    def mettre_a_jour_infos(self, joueur, attribut, nouvelle_valeur):
        setattr(joueur, attribut, nouvelle_valeur)
