import json
import os 

class Gestion_information_joueur:
    def __init__(self, chemin_fichier_joueur):
        self.chemin_fichier_joueur = chemin_fichier_joueur

    def sauvegarder_fichier(self, filename, data):
        json_data = json.dumps(data)
        with open(filename, "w") as f:
            f.write(json_data)
        

    def charger_fichier(self, filename):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.loads(f.read())
        return None

    def mettre_a_jour_infos_joueur(self, donne, cle, nouvelle_infos):
        if cle in donne:
            donne[cle] = nouvelle_infos


class Gestion_information_tournoi:
    def __init__(self, chemin_fichier_tournoi):
        self.chemin_fichier_tournoi = chemin_fichier_tournoi

    def sauvegarder_fichier(self, filename, data):
        json_data = json.dumps(data)
        with open(filename, "w") as f:
            f.write(json_data)
        

    def charger_fichier(self, filename):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.loads(f.read())
        return None

    def mettre_a_jour_infos_tournoi(self, donne, cle, nouvelle_infos):
        if cle in donne:
            donne[cle] = nouvelle_infos

    
            


liste_joueur = {"nom" : "gerard" , "age" : 34 , "date de naissance" : "30/08/1990"}



fichier = Gestion_information_joueur("C:/Users/Mehdi/Desktop/Formation_Python_OC/Projet_4")

fichier.sauvegarder_fichier("data/liste_de_joueur.json", liste_joueur)

liste_de_joueur =fichier.charger_fichier("data/liste_de_joueur.json")
fichier.mettre_a_jour_infos_joueur(liste_de_joueur, "nom", "jeanne")
fichier.sauvegarder_fichier("data/liste_de_joueur.json", liste_de_joueur)

liste_de_joueur =fichier.charger_fichier("data/liste_de_joueur.json")
fichier.mettre_a_jour_infos_joueur(liste_de_joueur, "date de naissance", "27/12/1991")

fichier.sauvegarder_fichier("data/liste_de_joueur.json", liste_de_joueur)




