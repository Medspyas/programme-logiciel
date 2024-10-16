class Joueur:
    # Représente un joueur.
    def __init__(self, nom, prenom, date_de_naissance, id_nationale, score):
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.id_nationale = id_nationale
        self.score = score

    def afficher_informations_joueur(self):
        # Affiche tous les informations d'un joueur.
        return f"{self.id_nationale} - {self.nom} - {self.prenom} - {self.date_de_naissance}"

    def mettre_a_jour_score(self, points):
        # Met à jour le score d'un joueur.
        self.score += points
        return self.score


class GestionJoueurs:
    # Gère plusieurs joueurs.
    def __init__(self, menu, gestion_information_joueur):
        self.liste_joueurs = []
        self.menu = menu
        self.gestion_information_joueur = gestion_information_joueur

    def ajouter_joueur(self, nom, prenom, date_de_naissance, id_nationale, score=0):
        # Ajoute un joueur à la liste.
        nouveau_joueur = Joueur(nom, prenom, date_de_naissance, id_nationale, score)
        self.liste_joueurs.append(nouveau_joueur)

    def obtenir_tous_les_joueurs(self):
        # Renvoi une liste de tous les joueurs ajoutés.
        if not self.liste_joueurs:
            print("Aucun joueur en mémoire, tentative de chargement depuis le fichier JSON.")
            joueur_charges = self.gestion_information_joueur.charger_joueurs()
            if joueur_charges:
                print(f"{len(self.liste_joueurs)} joueurs chargés en mémoire.")
                self.liste_joueurs = joueur_charges
        return self.liste_joueurs

    def trouver_joueur_par_id(self, id_nationale):
        # Trouve un joueur par son ID nationale.
        for joueur in self.liste_joueurs:
            if joueur.id_nationale == id_nationale:
                return joueur
        return None

    def mettre_a_jour_infos(self, joueur, attribut, nouvelle_valeur):
        # Met à jour une information d'un joueur.
        setattr(joueur, attribut, nouvelle_valeur)
