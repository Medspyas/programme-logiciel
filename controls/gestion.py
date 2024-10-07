import json
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.joueur import Joueur , GestionJoueurs
from models.tournois import Tournoi
from models.tour import Tour
from models.match import Match
from controls.controls_tournois import ControlsTournois
from controls.controls_tour import ControlsTour



class GestionDeBase:
    def __init__(self, dossier_data= 'data'):
        self.dossier_data = dossier_data
        if not os.path.exists(self.dossier_data):
            os.makedirs(self.dossier_data)
    
    def chemin_fichier(self, filename):
        return os.path.join(self.dossier_data, filename)

    def sauvegarder_fichier(self, filename, data):
        chemin_fichier = self.chemin_fichier(filename)

        with open(chemin_fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def charger_fichier(self, filename):
        chemin_fichier = self.chemin_fichier(filename)
        if os.path.exists(chemin_fichier):
            with open(chemin_fichier, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        return None

class Gestion_information_joueur(GestionDeBase):
    def sauvegarder_joueurs(self, joueurs, filename="joueurs.json"):

        joueurs_existants = self.charger_joueurs(filename)


        joueurs_dict = {joueur.id_nationale: joueur for joueur in joueurs_existants}

        for joueur in joueurs:
            joueurs_dict[joueur.id_nationale] = joueur


        listes_joueurs_dict= [
            {
            "nom": joueur.nom,
            "prenom": joueur.prenom,
            "date_de_naissance": joueur.date_de_naissance,
            "id_nationale": joueur.id_nationale,
            "score":joueur.score
            
            }
            for joueur in joueurs_dict.values()
        ]
        self.sauvegarder_fichier(filename, listes_joueurs_dict)

    def charger_joueurs(self, filename="joueurs.json"):
        data = self.charger_fichier(filename)
        if data:
            return [
                   Joueur(joueur["nom"], joueur["prenom"], joueur["date_de_naissance"], 
                          joueur["id_nationale"], joueur["score"]
                          )
                    for joueur in data
            ]
        return []


    def mettre_a_jour_infos_joueur(self, joueurs, id_nationale, attribut, nouvelle_valeur):
        joueur_trouver = False
        for joueur in joueurs:
            if joueur.id_nationale == id_nationale:
                setattr(joueur, attribut, nouvelle_valeur)
                joueur_trouver = True
                print("l'information a bien été mis à jour.")
        if not joueur_trouver:
            print("Joueur non trouvé.")
        return joueurs

class Gestion_information_tournoi(GestionDeBase):
    def sauvegarder_tous_les_tournois(self, tournois, filename= "tournoi.json"):
        
        tournois_existants = self.charger_fichier(filename) or []

        tournois_dict = {t_existant["nom"]: t_existant for t_existant in tournois_existants}

        for tournoi in tournois:
            tournois_dict[tournoi.nom] = {
                "nom": tournoi.nom,
                "date_debut": tournoi.date_debut,
                "date_fin": tournoi.date_fin,
                "description": tournoi.description,
                "joueurs": [joueur.id_nationale for joueur in tournoi.liste_joueurs],
                "tours": [
                    {
                        "nom_tour": tour.nom_tour,
                        "date_et_heure_debut": tour.date_et_heure_debut,
                        "date_et_heure_fin": tour.date_et_heure_fin,
                        "matches":[
                            {
                                "joueur_1": match.joueur_1.id_nationale,
                                "score_joueur_1": match.score_joueur_1,
                                "joueur_2": match.joueur_2.id_nationale,
                                "score_joueur_2": match.score_joueur_2
                                
                                
                            }
                            for match in tour.liste_matches

                        ]            
                    }
                    for tour in tournoi.liste_tours                  
                ],
                "tour_en_cours" : tournoi.tour_en_cours
                
            }
        
        
        self.sauvegarder_fichier(filename, list(tournois_dict.values()))

    
    def charger_tous_les_tournois(self, gestion_joueurs, filename):
        data = self.charger_fichier(filename)
        print(f"Fichier JSON chargé : {data}")
        tournois = []

        if data:
            for tournoi_data in data:
                tournoi = Tournoi(
                    nom = tournoi_data["nom"],
                    date_debut = tournoi_data["date_debut"],
                    date_fin = tournoi_data["date_fin"],
                    description = tournoi_data["description"],
                    liste_joueurs = [],
                    nb_tour = 4
                )

                tournoi.tour_en_cours = tournoi_data.get("tour_en_cours", 0)

                for id_nationale in tournoi_data["joueurs"]:
                    joueur = gestion_joueurs.trouver_joueur_par_id(id_nationale)
                    if joueur:
                        print(f"Joueur trouvé : {joueur.nom} (ID : {id_nationale})")
                        tournoi.liste_joueurs.append(joueur)
                    else:
                        print(f"Joueur avec ID {id_nationale} introuvable.")

                for tour_data in tournoi_data["tours"]:
                    tour = Tour(
                        nom_tour = tour_data["nom_tour"],
                        date_et_heure_debut = tour_data["date_et_heure_debut"],
                        date_et_heure_fin = tour_data["date_et_heure_fin"]
                    )
                    print(f"Chargement du {tour_data['nom_tour']}") 
                    for match_data in tour_data["matches"]:
                        joueur_1 = gestion_joueurs.trouver_joueur_par_id(match_data["joueur_1"])
                        joueur_2 = gestion_joueurs.trouver_joueur_par_id(match_data["joueur_2"])
                        

                        if joueur_1 and joueur_2:
                            match = Match(joueur_1 , joueur_2, match_data["score_joueur_1"], match_data["score_joueur_2"])
                            print(f"Match chargé : {joueur_1.nom} vs {joueur_2.nom}")
                            
                            tour.liste_matches.append(match)
                    tournoi.liste_tours.append(tour)
                tournois.append(tournoi)
            return tournois
        
             
        return None

 

    
    def mettre_a_jour_infos_tournoi(self, tournoi, attribut, nouvelle_valeur):
        if hasattr(tournoi , attribut):
            setattr(tournoi, attribut, nouvelle_valeur)
            print("L'information à bien été mis à jour")
        else:
            print("L'information est introuvable")
        return tournoi

    
            




    





