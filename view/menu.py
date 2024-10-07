


class MenuPrincipal:
    def __init__(self):
        print("Bienvenue dans le gestionnaire de tournois d'échecs")


    def afficher_menu(self):
        print("\nMenu Principal:")
        print("1. Gérer les Joueurs")
        print("2. Gérer le Tournoi")
        print("3. Afficher les Rapports")
        print("4. Quittez")
        return input("Choisissez une option : ")

    def afficher_menu_joueurs(self):
        print("\nMenu Gestion des Joueurs:")
        print("1. Ajouter un joueur")
        print("2. Modifier un joueur")
        print("3. Sauvegarder les joueurs")
        print("4. Retour au menu principal")
        return  input("Faite votre choix : ")
    


    def afficher_menu_tournois(self):
        print("\nMenu Gestion des Tournois:")
        print("1. Créer un tournois")
        print("2. Lancer un tournois")
        print("3. Sauvegarder tournois")
        print("4. Retour au menu principal")
        return input("Faite votre choix : ")
    

    def afficher_menu_rapport(self):
        print("\nMenu Rapports:")
        print("1. Afficher listes joueurs")
        print("2. Afficher les tournois")
        print("3. Afficher infos tournois")
        print("4. Afficher listes joueurs d'un tournois")
        print("5. Afficher listes tours et matchs d'un tournois")
        print("6. Retour au menu principal")
        return input("Faite votre choix : ")


    def afficher_message(self, message):
        print(message)

    def demander_information(self, element):
        return input(element)

    def demander_les_ids_nationales(self):
        return input("Entrez les ID des joueurs participants, séparer les par des virgules :")
    
    
    

