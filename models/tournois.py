class Tournoi:
    # Rprésente un tournois
    def __init__(self, nom, date_debut, date_fin, description, liste_joueurs, nb_tour):
        self.nom = nom
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nb_tour = nb_tour
        self.liste_joueurs = liste_joueurs
        self.liste_tours = []
        self.description = description
        self.tour_en_cours = 0
        self.classement = []

    def ajouter_tour(self, tour):
        # Ajoute un tour dans une lsite
        self.liste_tours.append(tour)
        return self.liste_tours
