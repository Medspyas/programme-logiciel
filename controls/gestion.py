import json
import os
import sys


from models.joueur import Joueur
from models.match import Match
from models.tour import Tour
from models.tournois import Tournoi

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class GestionDeBase:
    # Gere la création de dossier. sauvegarde et charge un fichier.
    def __init__(self, dossier_data="data"):
        self.dossier_data = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", dossier_data))
        if not os.path.exists(self.dossier_data):
            os.makedirs(self.dossier_data)

    def chemin_fichier(self, filename):
        # Crée un dossier et defini un chemin de sauvegarde.
        return os.path.join(self.dossier_data, filename)

    def sauvegarder_fichier(self, filename, data):
        # Sauvegarde un fichier.
        chemin_fichier = self.chemin_fichier(filename)
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def charger_fichier(self, filename):
        # Charge un fichier.
        chemin_fichier = self.chemin_fichier(filename)
        if os.path.exists(chemin_fichier):
            with open(chemin_fichier, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        return None


class Gestion_information_joueur(GestionDeBase):
    # Gère la sauvegarde et chargement des informations joueurs.
    def sauvegarder_joueurs(self, joueurs, filename="joueurs.json"):
        # Sauvegarde les informations joueur.
        joueurs_existants = self.charger_joueurs(filename)

        joueurs_dict = {joueur.id_nationale: joueur for joueur in joueurs_existants}

        for joueur in joueurs:
            joueurs_dict[joueur.id_nationale] = joueur

        listes_joueurs_dict = [
            {
                "nom": joueur.nom,
                "prenom": joueur.prenom,
                "date_de_naissance": joueur.date_de_naissance,
                "id_nationale": joueur.id_nationale,
                "score": joueur.score,
            }
            for joueur in joueurs_dict.values()
        ]
        self.sauvegarder_fichier(filename, listes_joueurs_dict)

    def charger_joueurs(self, filename="joueurs.json"):
        # Charge les informations joueur.
        data = self.charger_fichier(filename)
        if data:
            return [
                Joueur(
                    joueur["nom"],
                    joueur["prenom"],
                    joueur["date_de_naissance"],
                    joueur["id_nationale"],
                    joueur["score"],
                )
                for joueur in data
            ]
        return []


class Gestion_information_tournoi(GestionDeBase):
    # Gère la sauvegarde et chargement des informations tournois.
    def sauvegarder_tous_les_tournois(self, tournois, filename="tournois.json"):
        # Sauvegarde les tournois créer.
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
                        "matches": [
                            {
                                "joueur_1": match.joueur_1.id_nationale,
                                "score_joueur_1": match.score_joueur_1,
                                "joueur_2": match.joueur_2.id_nationale,
                                "score_joueur_2": match.score_joueur_2,
                            }
                            for match in tour.liste_matches
                        ],
                    }
                    for tour in tournoi.liste_tours
                ],
                "nb_tour": tournoi.nb_tour,
                "tour_en_cours": tournoi.tour_en_cours,
                "classement": tournoi.classement,
            }

        self.sauvegarder_fichier(filename, list(tournois_dict.values()))

    def charger_tous_les_tournois(self, gestion_joueurs, filename):
        # Charge les informations des tournois
        data = self.charger_fichier(filename)
        if not data:
            return []
        tournois = []

        if data:
            for tournoi_data in data:
                tournoi = Tournoi(
                    nom=tournoi_data["nom"],
                    date_debut=tournoi_data["date_debut"],
                    date_fin=tournoi_data["date_fin"],
                    description=tournoi_data["description"],
                    liste_joueurs=[],
                    nb_tour=4,
                )

                tournoi.tour_en_cours = tournoi_data.get("tour_en_cours", 0)

                tournoi.classement = tournoi_data.get("classement", [])

                for id_nationale in tournoi_data["joueurs"]:
                    joueur = gestion_joueurs.trouver_joueur_par_id(id_nationale)
                    if joueur:

                        tournoi.liste_joueurs.append(joueur)

                for tour_data in tournoi_data["tours"]:
                    tour = Tour(
                        nom_tour=tour_data["nom_tour"],
                        date_et_heure_debut=tour_data["date_et_heure_debut"],
                        date_et_heure_fin=tour_data["date_et_heure_fin"],
                    )

                    for match_data in tour_data["matches"]:
                        joueur_1 = gestion_joueurs.trouver_joueur_par_id(match_data["joueur_1"])
                        joueur_2 = gestion_joueurs.trouver_joueur_par_id(match_data["joueur_2"])

                        if joueur_1 and joueur_2:
                            match = Match(
                                joueur_1, joueur_2, match_data["score_joueur_1"], match_data["score_joueur_2"]
                            )

                            tour.liste_matches.append(match)
                    tournoi.liste_tours.append(tour)
                tournois.append(tournoi)
            return tournois

        return None


class GestionRapport(GestionDeBase):
    # Gère les rapports des différentes inforamtions joueurs et tournois.
    def afficher_joueurs_alphabetique(self, filename="joueurs.json"):
        # Renvoie la liste de tous les joueurs sauvegardés trier.
        joueurs = self.charger_fichier(filename)
        if not joueurs:
            return None

        joueurs_trier = sorted(joueurs, key=lambda joueur: joueur["nom"])
        return joueurs_trier

    def afficher_tournois(self, filename="tournois.json"):
        # Renvoie la liste des tournois sauvegardés.
        tournois = self.charger_fichier(filename)
        if not tournois:
            return []

        return [
            f"{tournoi['nom']}, du {tournoi['date_debut']} au {tournoi['date_fin']}; "
            f"{tournoi['description']}; {tournoi['nb_tour']} tours"
            for tournoi in tournois
        ]

    def afficher_tounois_noms(self, filename="tournois.json"):
        # Renvoie le nom des différents tournois.
        tournois = self.charger_fichier(filename)

        if not tournois:
            return []

        return [tournoi["nom"] for tournoi in tournois]

    def afficher_details_tournoi(self, nom_tournoi, gestion_joueur, filename="tournois.json"):
        # Renvoie les informations d'un tournois
        tournois = self.charger_fichier(filename)
        tournoi = next((t for t in tournois if t["nom"] == nom_tournoi), None)
        if tournoi:
            details = [
                f"Nom du tournoi: {tournoi['nom']}",
                f"Dates: {tournoi['date_debut']} ; {tournoi['date_fin']}",
                f"Description: {tournoi['description']}",
            ]
            details.append("Liste joueurs :")
            for id_joueur in tournoi["joueurs"]:
                joueur = gestion_joueur.trouver_joueur_par_id(id_joueur)
                if joueur:
                    details.append(f"{joueur.nom}; {joueur.prenom}")
                else:
                    details.append(f"Joueur avec ID {id_joueur} non trouvé.")

            details.append("Classement final :")
            if "classement" in tournoi:
                for i, (nom, prenom, score) in enumerate(tournoi["classement"], start=1):
                    details.append(f"{i}. {nom} {prenom}. Score: {score} points")
            else:
                details.append("Classement non disponible.")

            return details
        return ["Tournoi non trouvé."]

    def afficher_tours_et_matchs(self, nom_tournoi, gestion_joueur, filename="tournois.json"):
        # Renvoie les informations des différents tours et matchs d'un tournois.
        tournois = self.charger_fichier(filename)
        tournoi = next((t for t in tournois if t["nom"] == nom_tournoi), None)
        if tournoi:
            details = []
            for tour in tournoi["tours"]:
                details.append(
                    f"{tour['nom_tour']}; Début: {tour['date_et_heure_debut']}; Fin: {tour['date_et_heure_fin']}"
                )

                for match in tour["matches"]:
                    joueur_1 = gestion_joueur.trouver_joueur_par_id(match["joueur_1"])
                    joueur_2 = gestion_joueur.trouver_joueur_par_id(match["joueur_2"])

                    match_info = (
                        f"{joueur_1.nom} {joueur_1.prenom} vs {joueur_2.nom} {joueur_2.prenom}; "
                        f"Score {match['score_joueur_1']} - {match['score_joueur_2']}"
                    )
                    details.append(match_info)
                details.append("")
            return details
        return ["Tournoi non trouvé"]
