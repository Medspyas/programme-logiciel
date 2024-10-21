import os
import sys

from controls_joueur import ControlsJoueur
from controls_tournois import ControlsTournois

from controls.gestion import Gestion_information_joueur, Gestion_information_tournoi, GestionRapport
from models.joueur import GestionJoueurs
from models.tournois import Tournoi
from view.menu import MenuPrincipal


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class ControlsPrincipal:
    def __init__(
        self,
        menu,
        controls_joueurs,
        gestion_information_joueur,
        gestion_information_tournois,
        gestion_joueur,
        gestion_rapports,
        controls_tours,
        controls_tournois,
    ):

        # Initialisation du contrôleur principal avec les modules nécessaires.

        self.menu = menu
        self.controls_joueurs = controls_joueurs
        self.gestion_information_joueur = gestion_information_joueur
        self.gestion_information_tournois = gestion_information_tournois
        self.gestion_joueur = gestion_joueur
        self.gestion_rapports = gestion_rapports
        self.controls_tours = controls_tours
        self.controls_tournois = controls_tournois
        self.liste_tournois = []

    def lancer_menu_principal(self):
        # Lancer le menu principal et gérer les choix utilisateur.
        while True:
            choix_principal = self.menu.afficher_menu()

            if choix_principal == "1":
                self.gerer_joueur()
            elif choix_principal == "2":
                self.gerer_tournois()
            elif choix_principal == "3":
                self.gerer_rapport()
            elif choix_principal == "4":
                self.menu.afficher_message("Quittez le programme")
                break
            else:
                self.menu.afficher_message("Choix invalide , réessayer")

    def gerer_joueur(self):
        # Affiche le menu joueur et ses choix.
        while True:
            choix_joueurs = self.menu.afficher_menu_joueurs()
            if choix_joueurs == "1":
                self.ajouter_joueur()
            elif choix_joueurs == "2":
                self.modifier_joueur()
            elif choix_joueurs == "3":
                break
            else:
                self.menu.afficher_message("Choix invalide , réessayer")

    def gerer_tournois(self):
        # Affiche le menu tournoi et ses choix.
        while True:
            choix_tournoi = self.menu.afficher_menu_tournois()
            if choix_tournoi == "1":
                self.creer_tournoi()
            elif choix_tournoi == "2":
                self.charger_tournois()
            elif choix_tournoi == "3":
                self.menu.afficher_message("Retour au menu principal")
                break
            else:
                self.menu.afficher_message("Choix invalide, réessayez.")

    def gerer_rapport(self):
        # Affiche le menu rappor et ses choix.
        while True:
            choix = self.menu.afficher_menu_rapport()
            if choix == "1":
                self.afficher_joueurs_alphabetique()
            elif choix == "2":
                self.afficher_tournois()
            elif choix == "3":
                self.afficher_details_tournoi()
            elif choix == "4":
                self.afficher_tours_et_matchs()
            elif choix == "5":
                self.menu.afficher_message("Retour au menu principal")
                break
            else:
                self.menu.afficher_message("Choix invalide réessayer")

    def afficher_joueurs_alphabetique(self):

        joueurs_trier = self.gestion_rapports.afficher_joueurs_alphabetique()
        if not joueurs_trier:
            self.menu.afficher_message("Auncun joueur disponible.")
            return

        titres = ["ID Nationale", "Nom", "prenom", "Date de naissance"]
        largeurs = [len(titre) + 7 for titre in titres]
        self.menu.afficher_message(
            f"{titres[0]:<{largeurs[0]}} {titres[1]:<{largeurs[1]}}"
            f"{titres[2]:<{largeurs[2]}} {titres[3]:<{largeurs[3]}}"
        )
        for joueur in joueurs_trier:
            self.menu.afficher_message(
                f"{joueur['id_nationale']:<{largeurs[0]}} {joueur['nom']:<{largeurs[1]}}"
                f"{joueur['prenom']:<{largeurs[2]}} {joueur['date_de_naissance']:<{largeurs[3]}}"
            )

    def afficher_tournois(self):
        tournois = self.gestion_rapports.afficher_tournois()
        if not tournois:
            self.menu.afficher_message("Auncun tournoi disponible.")
            return
        for tournoi in tournois:
            self.menu.afficher_message(tournoi)

    def afficher_details_tournoi(self):
        tournois = self.gestion_rapports.afficher_tounois_noms()
        if not tournois:
            self.menu.afficher_message("Auncun tournoi disponible.")
            return

        self.menu.afficher_message("Liste de tournois :")
        for tournoi in tournois:
            self.menu.afficher_message(tournoi)

        while True:
            nom_tournoi = self.menu.demander_information("Entre le nom du tournoi : ")
            if not nom_tournoi:
                self.menu.afficher_message("Choix invalide.")
                continue

            details = self.gestion_rapports.afficher_details_tournoi(nom_tournoi, self.gestion_joueur)
            if not details:
                self.menu.afficher_message(f"Le tournoi {nom_tournoi} n'a pas été trouvé.")
            else:
                for detail in details:
                    self.menu.afficher_message(detail)
                break

    def afficher_tours_et_matchs(self):
        tournois = self.gestion_rapports.afficher_tounois_noms()

        if not tournois:
            self.menu.afficher_message("Auncun tournoi disponible.")
            return

        self.menu.afficher_message("Liste de tournois :")
        for tournoi in tournois:
            self.menu.afficher_message(tournoi)
        while True:
            nom_tournoi = self.menu.demander_information("Entre le nom du tournoi : ")
            if not nom_tournoi:
                self.menu.afficher_message("Choix invalide.")
                continue

            tours_et_matchs = self.gestion_rapports.afficher_tours_et_matchs(nom_tournoi, self.gestion_joueur)
            if not tours_et_matchs:
                self.menu.afficher_message(f"Aucun tour et match trouvé pour le tournoi {nom_tournoi}.")
            else:
                for tour in tours_et_matchs:
                    self.menu.afficher_message(tour)
                break

    def valider_champ(self, message):
        # Vérifie que le nom/prenom contient uniquement des lettres et n'est pas vide.
        while True:
            valeur = self.menu.demander_information(message).strip().lower()
            if valeur.isalpha():
                return valeur
            else:
                self.menu.afficher_message("Le champ ne doit contenir que des lettres et ne doit pas être vide.")

    def valider_date(self, message):
        # Vérifie que la date est au foramt JJ/MM/AAAA et est valide.
        while True:
            date_str = self.menu.demander_information(message).strip()
            try:
                jour, mois, annee = map(int, date_str.split("/"))
                if 1 <= jour <= 31 and 1 <= mois <= 12 and 1900 <= annee <= 2100:
                    return date_str
                else:
                    self.menu.afficher_message("La date être valide.")
            except ValueError:
                self.menu.afficher_message("La date doit être au format JJ/MM/AAAA.")

    def valider_date_et_heure(self, message):
        # Vérifie que la date et heure d'un tour est au format JJ/MM/AAA HH:MM
        while True:
            date_heure_str = self.menu.demander_information(message).strip()

            if (
                len(date_heure_str) == 16
                and date_heure_str[2] == "/"
                and date_heure_str[5] == "/"
                and date_heure_str[10] == " "
                and date_heure_str[13] == ":"
            ):
                try:
                    date_partie, heure_partie = date_heure_str.split(" ")

                    jour, mois, annee = date_partie.split("/")
                    heure, minute = heure_partie.split(":")

                    if jour.isdigit() and mois.isdigit() and annee.isdigit() and heure.isdigit() and minute.isdigit():
                        jour, mois, annee = int(jour), int(mois), int(annee)
                        heure, minute = int(heure), int(minute)

                        if (
                            1 <= jour <= 31
                            and 1 <= mois <= 12
                            and 1900 <= annee <= 2100
                            and 0 <= heure <= 23
                            and 0 <= minute <= 59
                        ):
                            return date_heure_str
                except ValueError:
                    pass

            self.menu.afficher_message(
                "Format invalide. Veuillez entrer un date et une heure au format JJ/MM/AAA HH:MM."
            )

    def ajouter_joueur(self):
        # Ajoute les joueurs crées.
        while True:
            nom = self.valider_champ("Nom du joueur : ")
            prenom = self.valider_champ("Prénom du joueur : ")
            date_de_naissance = self.valider_date("Date de naissance (JJ/MM/AAA) :")

            while True:
                id_nationale = self.menu.demander_information("ID nationale: ( ex: AA111) :").strip()
                if len(id_nationale) == 5 and id_nationale[:2].isalpha() and id_nationale[2:].isdigit():
                    break
                else:
                    self.menu.afficher_message(
                        "l'ID nationale doit au format deux lettres suivi de trois chiffres \
                                                (ex: AA111)."
                    )

            self.controls_joueurs.ajouter_joueur(nom, prenom, date_de_naissance, id_nationale)
            self.sauvegarder_joueurs()
            choix_continuer = self.menu.demander_information(
                "Continuez ? o(oui),ou n'importe quelle touche pour quitter."
            )
            if choix_continuer.lower() != "o":
                break

        self.menu.afficher_message("Les information ont bien été pris en comtpe")

    def sauvegarder_joueurs(self):
        # Sauvegarde les joueurs ajoutés.
        joueurs = self.gestion_joueur.liste_joueurs
        self.gestion_information_joueur.sauvegarder_joueurs(joueurs)
        self.menu.afficher_message("Les joueurs ont bien été sauvegarder.")

    def sauvegarder_tournoi(self):
        # Sauvegarde les tournois crées.
        self.gestion_information_tournois.sauvegarder_tous_les_tournois(self.liste_tournois)

    def charger_tournois(self):
        # Charge les tournois sauvegardés.
        tournois = self.gestion_information_tournois.charger_tous_les_tournois(self.gestion_joueur, "tournois.json")
        if not tournois:
            self.menu.afficher_message("Aucun tournoi à charger")
            return

        for i, tournoi in enumerate(tournois):
            self.menu.afficher_message(f"{i+1}: {tournoi.nom}")

        while True:
            try:
                choix = int(self.menu.demander_information("Selectionner tournoi à charger: "))
                if 1 <= choix <= len(tournois):
                    break
                else:
                    self.menu.afficher_message("Veuillez entrer un numéro valide parmis la liste.")
            except ValueError:
                self.menu.afficher_message("Veuillez entrer un nombre entier valide.")
        selecion_tournoi = tournois[choix - 1]
        self.controls_tournois = ControlsTournois(selecion_tournoi, self.menu)

        self.controls_tournois.tournoi.tour_en_cours = selecion_tournoi.tour_en_cours

        if selecion_tournoi not in self.liste_tournois:
            self.liste_tournois.append(selecion_tournoi)

        self.continuer_tournoi()

    def modifier_joueur(self):
        # Modifie les informations d'un joueur ajoutés.
        self.menu.afficher_message("Liste de joueurs disponibles :")
        self.controls_joueurs.afficher_joueurs()

        id_nationale = self.menu.demander_information("Entre l' ID nationale: ( ex: AA111)")
        joueur = self.controls_joueurs.trouver_joueur(id_nationale)

        if joueur:
            self.menu.afficher_message(joueur.afficher_informations_joueur())

            nom = self.menu.demander_information("Entrez le nom : ") or joueur.nom
            prenom = self.menu.demander_information("Entrez le prenom : ") or joueur.prenom
            date_de_naissance = (
                self.menu.demander_information("Entrez la date de naissance (JJ/MM/AAA): ") or joueur.date_de_naissance
            )

            nouvel_id = self.menu.demander_information("Entre l' ID nationale: ( ex: AA111)") or joueur.id_nationale
            joueur_existant = self.controls_joueurs.trouver_joueur(nouvel_id)
            if joueur_existant and nouvel_id != joueur.id_nationale:
                self.menu.afficher_message("L'ID est deja utilisé par un autre joueur. ")
                return

            self.controls_joueurs.mettre_a_jour_infos_joueur(id_nationale, "nom", nom)
            self.controls_joueurs.mettre_a_jour_infos_joueur(id_nationale, "prenom", prenom)
            self.controls_joueurs.mettre_a_jour_infos_joueur(id_nationale, "date_de_naissance", date_de_naissance)

            if nouvel_id != joueur.id_nationale:
                self.controls_joueurs.mettre_a_jour_infos_joueur(id_nationale, "id_nationale", nouvel_id)

            self.sauvegarder_joueurs()
            self.menu.afficher_message("L'ID à été modifier avec succès")
        else:
            self.menu.afficher_message("L'ID n'à pas été trouver")

    def creer_tournoi(self):
        # Crée un tournoi

        joueurs_disponible = self.gestion_joueur.liste_joueurs

        if len(joueurs_disponible) < 8:
            self.menu.afficher_message("Erreur : vous devez crée au moins 8 joueurs pour crée un tournois.")
            return

        while True:
            nom_tournoi = self.menu.demander_information("Entre le nom du tournoi: ").strip()
            if nom_tournoi:
                break
            else:
                self.menu.afficher_message("Le nom du tournois ne peut pas être vide.")

        date_debut_tournoi = self.valider_date("Entre la date du début du tournoi: ")

        date_fin_tournoi = self.valider_date("Entre la date de fin du tournoi: ")

        while True:
            description = self.menu.demander_information("Entre le nom de la description: ").strip()
            if description:
                break
            else:
                self.menu.afficher_message("Le nom de la description ne peut pas être vide.")

        self.afficher_joueur()

        selection_joueur = self.selectionner_joueurs(joueurs_disponible)

        for joueur in selection_joueur:
            joueur.score = 0

        tournoi = Tournoi(nom_tournoi, date_debut_tournoi, date_fin_tournoi, description, selection_joueur, nb_tour=4)

        self.controls_tournois = ControlsTournois(tournoi, self.menu)
        self.liste_tournois.append(tournoi)
        self.sauvegarder_tournoi()
        self.lancer_tournoi()

    def afficher_joueur(self):
        # Affiche la liste de tous les joueurs.
        self.menu.afficher_message("Listes joueur: ")
        self.controls_joueurs.afficher_joueurs()

    def selectionner_joueurs(self, joueurs):
        # Sélectionne parmi la liste de joueurs les joueurs qui vont participer au tournoi.

        while True:
            id_joueurs = self.menu.demander_information(
                "Entrez les ID des joueurs participants, séparer les par des virgules :"
            )

            id_joueurs = [id_joueur.strip() for id_joueur in id_joueurs.split(",")]

            if len(id_joueurs) < 8:
                self.menu.afficher_message(
                    "Erreur : vous devez entrer au moins 8 ID de joueurs pour créer un tournoi."
                )
                continue

            joueurs_selectionnes = []
            ids_deja_selectionnes = set()
            erreur_detectee = False

            for id_joueur in id_joueurs:
                if id_joueur in ids_deja_selectionnes:
                    self.menu.afficher_message(f"l'ID {id_joueur} a déja été sélectionné.")
                    erreur_detectee = True
                    break

                joueur_trouver = False
                for joueur in joueurs:
                    if joueur.id_nationale == id_joueur:
                        joueurs_selectionnes.append(joueur)
                        ids_deja_selectionnes.add(id_joueur)
                        joueur_trouver = True
                        break
                if not joueur_trouver:
                    self.menu.afficher_message("l'ID n'éxiste pas.")
                    erreur_detectee = True
                    break
            if erreur_detectee:
                self.menu.afficher_message("Veuillez recommencer")
                continue
            return joueurs_selectionnes

    def lancer_tournoi(self):
        # Lance un tournois crée.
        if not self.controls_tournois:
            self.menu.afficher_message("Tournoi non créé")
            return

        if self.controls_tournois.tournoi.tour_en_cours >= self.controls_tournois.nb_tour:
            self.menu.afficher_message("Tous les tours sont terminés.")
            return

        date_heure_debut = self.valider_date_et_heure("Entrez la date et le l'heure du début (JJ/MM/AAA HH:MM): ")

        for i in range(self.controls_tournois.tournoi.tour_en_cours, self.controls_tournois.nb_tour):
            self.menu.afficher_message(f"Tour {i+1}/{self.controls_tournois.nb_tour}")

            self.controls_tournois.lancer_nouveau_tour(date_heure_debut)
            self.entrer_resultats_tour()

            dernier_tour = self.controls_tournois.tournoi.liste_tours[-1]
            resultats_matchs = dernier_tour.afficher_matchs()
            for resultat in resultats_matchs:
                self.menu.afficher_message(resultat)
                self.menu.afficher_message("")

            date_heure_fin = self.valider_date_et_heure("Entrez la date de fin du tour (JJ/MM/AAA HH:MM): ")
            dernier_tour.date_et_heure_fin = date_heure_fin

            self.controls_tournois.tournoi.tour_en_cours += 1

            if self.controls_tournois.tournoi.tour_en_cours == self.controls_tournois.nb_tour:
                self.generer_classement()
                self.sauvegarder_tournoi()
                self.menu.afficher_message("Le tournois est terminé.")
                return

            if not self.demander_continuer_ou_quitter():
                self.sauvegarder_tournoi()
                return
            date_heure_debut = date_heure_fin

    def continuer_tournoi(self):
        # Poursuis un tournoi arrêté avant la fin.

        if not self.controls_tournois:
            self.menu.afficher_message("Auncun tournoi à continuer.")
            return

        if self.controls_tournois.tournoi.tour_en_cours >= self.controls_tournois.nb_tour:
            self.menu.afficher_message("Tous les tours sont terminés.")
            return

        date_heure_debut = self.valider_date_et_heure("Entrez la date et le l'heure du début (JJ/MM/AAA HH:MM): ")

        for i in range(self.controls_tournois.tournoi.tour_en_cours, self.controls_tournois.tournoi.nb_tour):

            self.menu.afficher_message(
                f"Tour {self.controls_tournois.tournoi.tour_en_cours+1}/{self.controls_tournois.tournoi.nb_tour}"
            )
            self.controls_tournois.lancer_nouveau_tour(date_heure_debut)
            self.entrer_resultats_tour()

            dernier_tour = self.controls_tournois.tournoi.liste_tours[-1]
            resultats_matchs = dernier_tour.afficher_matchs()
            for resultat in resultats_matchs:
                self.menu.afficher_message(resultat)
                self.menu.afficher_message("")

            date_heure_fin = self.valider_date_et_heure("Entrez la date de fin du tour (JJ/MM/AAA HH:MM): ")
            dernier_tour.date_et_heure_fin = date_heure_fin

            self.controls_tournois.tournoi.tour_en_cours += 1

            if self.controls_tournois.tournoi.tour_en_cours == self.controls_tournois.nb_tour:
                self.generer_classement()
                self.sauvegarder_tournoi()
                self.menu.afficher_message("Le tournois est terminé.")
                return

            if not self.demander_continuer_ou_quitter():
                self.sauvegarder_tournoi()
                return

            date_heure_debut = date_heure_fin

    def generer_classement(self):
        # Génère le classement final d'un tournoi.
        joueurs = self.controls_tournois.tournoi.liste_joueurs

        classement = sorted(joueurs, key=lambda joueur: joueur.score, reverse=True)
        self.controls_tournois.tournoi.classement = [
            (joueur.nom, joueur.prenom, joueur.score) for joueur in classement
        ]

        self.menu.afficher_message("Classement final du tournoi :")
        for i, joueur in enumerate(classement, start=1):
            self.menu.afficher_message(f"{i}. {joueur.nom} {joueur.prenom}. Score: {joueur.score} points")
        return classement

    def entrer_resultats_tour(self):
        # Enregistre les résultats des matches d'un tour et mets à jour les scores des joueurs.
        dernier_tour = self.controls_tournois.tournoi.liste_tours[-1]

        for match in dernier_tour.liste_matches:
            if match.score_joueur_1 != 0 or match.score_joueur_2 != 0:
                continue

            self.menu.afficher_message(f"{match.joueur_1.nom} contre {match.joueur_2.nom}")
            self.menu.afficher_message("1: Joueur 1 gagne")
            self.menu.afficher_message("2: Joueur 2 gagne")
            self.menu.afficher_message("3: Nul")

            while True:
                try:
                    resultat = int(self.menu.demander_information("Entrez le resultat (1, 2 ou 3): "))

                    if resultat in [1, 2, 3]:
                        break
                    else:
                        self.menu.afficher_message("Résultat invalide, veuillez réessayez;")
                except ValueError:
                    self.menu.afficher_message("Erreur : veuillez entrer un nombre entier.")
                    continue

            if resultat == 1:
                self.menu.afficher_message(f"{match.joueur_1.nom} a gagné.")
                match.joueur_1.mettre_a_jour_score(1)
                match.joueur_2.mettre_a_jour_score(0)
                match.score_joueur_1 = 1
                match.score_joueur_2 = 0

            elif resultat == 2:
                self.menu.afficher_message(f"{match.joueur_2.nom} a gagné.")
                match.joueur_1.mettre_a_jour_score(0)
                match.joueur_2.mettre_a_jour_score(1)
                match.score_joueur_1 = 0
                match.score_joueur_2 = 1

            elif resultat == 3:
                self.menu.afficher_message("Match nul.")
                match.joueur_1.mettre_a_jour_score(0.5)
                match.joueur_2.mettre_a_jour_score(0.5)
                match.score_joueur_1 = 0.5
                match.score_joueur_2 = 0.5
        self.sauvegarder_joueurs()

    def demander_continuer_ou_quitter(self):
        # Permet de quitter a la fin d'un tour.
        choix = self.menu.demander_information("Voulez continuer ou quitter ? (q) pour quitter/ (c) pour continuer: ")
        if choix == "q":
            self.menu.afficher_message("Vous avez quitté le tournois.")
            return False
        elif choix == "c":
            return True
        else:
            self.menu.afficher_message("Choix invalide, réessayer.")
            return self.demander_continuer_ou_quitter()


def main():
    # Réunis tous les modules nécessaires au lancement du programme.
    menu = MenuPrincipal()
    gestion_information_joueur = Gestion_information_joueur()
    gestion_joueur = GestionJoueurs(menu, gestion_information_joueur)
    controls_joueur = ControlsJoueur(gestion_joueur, menu)
    gestion_information_tournoi = Gestion_information_tournoi()
    joueurs_charges = gestion_information_joueur.charger_joueurs()
    gestion_joueur.liste_joueurs = joueurs_charges
    gestion_rapports = GestionRapport()
    if not gestion_joueur.liste_joueurs:
        menu.afficher_message("Auncun joueur n'a été trouvé. Ajouter des joueurs.")
    controls_principal = ControlsPrincipal(
        menu,
        controls_joueur,
        gestion_information_joueur,
        gestion_information_tournoi,
        gestion_joueur,
        gestion_rapports,
        None,
        None,
    )

    controls_principal.lancer_menu_principal()


if __name__ == "__main__":
    main()
