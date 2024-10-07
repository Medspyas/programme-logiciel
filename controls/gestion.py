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

    
            



if __name__ == "__main__":
    gestion_joueurs = GestionJoueurs()

    
    gestion_joueurs.ajouter_joueur("Dupont", "Jean", "01/01/1980", "FR12345", 0)
    gestion_joueurs.ajouter_joueur("Martin", "Paul", "02/02/1990", "FR12346", 0)

    
    gestion_joueurs.afficher_tous_les_joueurs()

    tournoi = Tournoi(
        nom="Tournoi de Paris",
        date_debut="2024-01-01",
        date_fin="2024-01-05",
        description="Un tournoi prestigieux.",
        liste_joueurs=gestion_joueurs.liste_joueurs,
        nb_tour=4
    )

    
    tour_1 = Tour("Round 1", "2024-01-02 10:00", "2024-01-02 12:00")

  
    match_1 = Match(joueur_1=gestion_joueurs.liste_joueurs[0], joueur_2=gestion_joueurs.liste_joueurs[1], score_joueur_1=1, score_joueur_2=0)
    tour_1.ajouter_match(match_1.joueur_1, match_1.joueur_2)
    print(f"Match ajouté: {tour_1.liste_matches[0].joueur_1.nom} vs {tour_1.liste_matches[0].joueur_2.nom}")
    
   
    tournoi.liste_tours.append(tour_1)
    print(f"Nombre de tours dans le tournoi : {len(tournoi.liste_tours)}")
    print(f"Nombre de matchs dans le tour : {len(tour_1.liste_matches)}")

   
    gestion_information_tournoi = Gestion_information_tournoi()

    
    gestion_information_tournoi.sauvegarder_tournois(tournoi, filename="test_tournoi.json")
    print("Tournoi sauvegardé avec les tours et matchs.")

    
    tournoi_charge = gestion_information_tournoi.charger_tournoi(gestion_joueurs=gestion_joueurs, filename="test_tournoi.json")
    if tournoi_charge:
        print("Tournoi chargé avec succès.")
        print(f"Nom du tournoi : {tournoi_charge.nom}")
        print(f"Description : {tournoi_charge.description}")
        print(f"Date de début : {tournoi_charge.date_debut}")
        print(f"Date de fin : {tournoi_charge.date_fin}")
        print(f"Nombre de joueurs : {len(tournoi_charge.liste_joueurs)}")

        
        for idx, tour in enumerate(tournoi_charge.liste_tours):
            print(f"\nTour {idx + 1}: {tour.nom_tour}")
            print(f"Début: {tour.date_et_heure_debut}, Fin: {tour.date_et_heure_fin}")
            for match in tour.liste_matches:
                print(f"Match: {match.joueur_1.nom} vs {match.joueur_2.nom} | Score: {match.score_joueur_1} - {match.score_joueur_2}")
    else:
        print("Le tournoi n'a pas pu être chargé.")

    


   
    gestion_information_tournoi.sauvegarder_tournois(tournoi_charge, filename="test_tournoi.json")
    





