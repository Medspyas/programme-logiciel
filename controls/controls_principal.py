from datetime import datetime 
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.joueur import Joueur, GestionJoueurs
from models.tournois import Tournoi
from models.tour import Tour
from controls_tour import ControlsTour
from controls_joueur import ControlsJoueur
from controls_tournois import ControlsTournois
from view.menu import MenuPrincipal
from controls.gestion import *

class ControlsPrincipal:
    def __init__(self, menu, controls_joueurs, gestion_information_joueur, gestion_information_tournois, gestion_joueur, gestion_rapports, controls_tours, controls_tournois):
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

        while True:
            choix_principal = self.menu.afficher_menu()
            if choix_principal == '1':
                self.gerer_joueur()
            elif choix_principal == '2':
                self.gerer_tournois()
            elif choix_principal == '3':
                self.gerer_rapport()
            elif choix_principal == '4':
                self.menu.afficher_message("Quittez le programme")
                break
            else:
                self.menu.afficher_message("Choix invalide , réessayer")

    def gerer_joueur(self):
        while True:
            choix_joueurs = self.menu.afficher_menu_joueurs()
            if choix_joueurs == '1':
                self.ajouter_joueur()
            elif choix_joueurs == '2':
                self.modifier_joueur()
            elif choix_joueurs == '3':
                self.sauvegarder_joueurs()
            elif choix_joueurs == '4': 
                break
            else:
                self.menu.afficher_message("Choix invalide , réessayer")

    def gerer_rapport(self):
        choix = self.menu.afficher_menu_rapport()
        if choix == "1":
            joueurs = self.gestion_rapports.afficher_joueurs_alphabetique()
            for joueur in joueurs:
                self.menu.afficher_message(joueur)
        elif choix == "2":
            tournois = self.gestion_rapports.afficher_tournois()
            for tournoi in tournois:
                self.menu.afficher_message(tournoi)
        elif choix == "3":
            nom_tournoi = self.menu.demander_information("Entre le nom du tournoi : ")
            details = self.gestion_rapports.afficher_details_tournoi(nom_tournoi, self.gestion_joueur)
            for detail in details:
                self.menu.afficher_message(detail)
        elif choix =="4":
            nom_tournoi = self.menu.demander_information("Entre le nom du tournoi : ")
            tours_et_matchs = self.gestion_rapports.afficher_tours_et_matchs(nom_tournoi)
            for tour in tours_et_matchs:
                self.menu.afficher_message(tour)
        else:
            self.menu.afficher_message("Choix invalide réessayer")
            
        


    def ajouter_joueur(self):
        nom = self.menu.demander_information("Entrez le nom : ")
        prenom = self.menu.demander_information("Entrez le prenom : ")
        date_de_naissance = self.menu.demander_information("Entrez la date de naissance (JJ/MM/AAA) : ")
        id_nationale = self.menu.demander_information("Entre l' ID nationale: ( ex: AA111): ")

        self.controls_joueurs.ajouter_joueur(nom, prenom, date_de_naissance, id_nationale)
        self.sauvegarder_joueurs()
        self.menu.afficher_message("Les information ont bien été pris en comtpe")
        
    def sauvegarder_joueurs(self):
        joueurs = self.gestion_joueur.liste_joueurs
        self.gestion_information_joueur.sauvegarder_joueurs(joueurs)
        self.menu.afficher_message("Les joueurs ont bien été sauvegarder.")

    def sauvegarder_tournoi(self):
        self.gestion_information_tournois.sauvegarder_tous_les_tournois(self.liste_tournois)

    def charger_tournois(self):
        
        tournois = self.gestion_information_tournois.charger_tous_les_tournois(self.gestion_joueur, "tournois.json")
        

        if not tournois:
            self.menu.afficher_message("Aucun tournoi à charger")
            return
        
        for i, tournoi in enumerate(tournois):
            self.menu.afficher_message(f"{i+1}: {tournoi.nom}")

        choix = int(self.menu.demander_information("Selectionner tournoi à charger: "))
        if 1 <= choix <= len(tournois):
            selecion_tournoi = tournois[choix - 1]
            self.controls_tournois = ControlsTournois(selecion_tournoi, self.menu)

            self.controls_tournois.tournoi.tour_en_cours = selecion_tournoi.tour_en_cours

            if selecion_tournoi not in self.liste_tournois:
                self.liste_tournois.append(selecion_tournoi)
            
            self.continuer_tournoi()
        else:
            self.menu.afficher_message("Veuillez choisir un numero parmis la liste ci-dessus.")
            self.charger_tournois()

    def modifier_joueur(self):
        id_nationale = self.menu.demander_information("Entre l' ID nationale: ( ex: AA111)")
        joueur = self.controls_joueurs.trouver_joueur(id_nationale)

        if joueur:
            self.menu.afficher_message(joueur.afficher_informations_joueur())

            nom = self.menu.demander_information("Entrez le nom : ") or joueur.nom
            prenom = self.menu.demander_information("Entrez le prenom : ") or joueur.prenom
            date_de_naissance = self.menu.demander_information("Entrez la date de naissance (JJ/MM/AAA): ") or joueur.date_de_naissance

            nouvel_id = self.menu.demander_information("Entre l' ID nationale: ( ex: AA111)") or joueur.id_nationale
            if nouvel_id != joueur.id_nationale:
                joueur_existant = self.controls_joueurs.trouver_joueur(nouvel_id)
                if joueur_existant:
                    self.menu.afficher_message("L'ID est deja utilisé par un autre joueur. ")
                    return
                else:
                    self.controls_joueurs.mettre_a_jour_infos_joueur(id_nationale, "id_nationale", nouvel_id)
                    joueur = self.controls_joueurs.trouver_joueur(nouvel_id)

            self.controls_joueurs.mettre_a_jour_infos_joueur(id_nationale, "nom", nom)
            self.controls_joueurs.mettre_a_jour_infos_joueur(id_nationale, "prenom", prenom)
            self.controls_joueurs.mettre_a_jour_infos_joueur(id_nationale, "date_de_naissance", date_de_naissance)
            
            self.sauvegarder_joueurs()
            self.menu.afficher_message("L'ID à été modifier avec succès")  
        else:
            self.menu.afficher_message("L'ID n'à pas été trouver")  

    def gerer_tournois(self):
        while True:
            choix_tournoi = self.menu.afficher_menu_tournois()
            if choix_tournoi == "1": 
                self.creer_tournoi()
            elif choix_tournoi == "2":
                self.charger_tournois()    
            elif choix_tournoi == "3":
                self.sauvegarder_tournoi()
            elif choix_tournoi == "4":
                self.menu.afficher_message("Retour au menu principal")
                break
            else: 
                self.menu.afficher_message("Choix invalide, réessayez.")

    def creer_tournoi(self):
        while True:

            nom_tournoi = self.menu.demander_information("Entre le nom du tournoi: ")
            if not nom_tournoi.strip():
                self.menu.afficher_message("Le nom du tournoi ne peut pas être vide.")
                continue
            date_debut_tournoi = self.menu.demander_information("Entre la date du début du tournoi: ") 
            if not date_debut_tournoi.strip():
                self.menu.afficher_message("La date de debut du tournoi ne peut pas être vide.")
                continue
            date_fin_tournoi= self.menu.demander_information("Entre la date de fin du tournoi: ")
            if not date_fin_tournoi.strip():
                self.menu.afficher_message("La date de fin du tournoi ne peut pas être vide.")
                continue
            description = self.menu.demander_information("Entrez la description du tournoi: ")
            if not description.strip():
                self.menu.afficher_message("La description du tournoi ne peut pas être vide.")                
                continue
            break

        joueurs_disponible = self.gestion_joueur.liste_joueurs
        self.afficher_joueur(joueurs_disponible)

        selection_joueur = self.selectionner_joueurs(joueurs_disponible)

        tournoi = Tournoi(nom_tournoi, date_debut_tournoi, date_fin_tournoi, description, selection_joueur, nb_tour=4)

        self.controls_tournois = ControlsTournois(tournoi, self.menu)
        self.liste_tournois.append(tournoi)
        self.lancer_tournoi()

    def afficher_joueur(self, joueurs):
        self.menu.afficher_message("Listes joueur: ")
        for joueur in joueurs:
            self.menu.afficher_message(f"{joueur.id_nationale} - {joueur.nom} {joueur.prenom}")

    def selectionner_joueurs(self, joueurs):
        while True:
            id_joueurs = self.menu.demander_information("Entrez les ID des joueurs participants, séparer les par des virgules :")

            id_joueurs = [id_joueur.strip() for id_joueur in id_joueurs.split(",")]

            if len(id_joueurs) < 8:
                self.menu.afficher_message("Erreur : vous devez entrer au moins 8 ID de joueurs pour créer un tournoi.")
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
        if not self.controls_tournois:
            self.menu.afficher_message("Tournoi non créé")
            return

        date_heure_debut = self.menu.demander_information("Entrez la date et le l'heure du début (JJ/MM/AAA HH:MM): ")

        for i in range(self.controls_tournois.nb_tour):
            self.menu.afficher_message(f"Lancement du tour {i+1}/{self.controls_tournois.nb_tour}")
            self.controls_tournois.lancer_nouveau_tour(date_heure_debut)
            self.entrer_resultats_tour()
            dernier_tour = self.controls_tournois.tournoi.liste_tours[-1]
            dernier_tour.afficher_matchs()
            date_heure_fin = self.menu.demander_information("Entrez la date de fin du tour (JJ/MM/AAA HH:MM): ")
            dernier_tour.date_et_heure_fin = date_heure_fin
            
            self.controls_tournois.tournoi.tour_en_cours += 1
            
            self.sauvegarder_tournoi()
            
            if not self.demander_continuer_ou_quitter():
                break
            date_heure_debut = date_heure_fin 

        if self.controls_tournois.tournoi.tour_en_cours == self.controls_tournois.nb_tour:
            self.generer_classement()

    def continuer_tournoi(self):
            date_heure_debut = self.menu.demander_information("Entrez la date et le l'heure du début (JJ/MM/AAA HH:MM): ")

            for i in range(self.controls_tournois.tournoi.tour_en_cours, self.controls_tournois.tournoi.nb_tour):
                
                self.menu.afficher_message(f"{self.controls_tournois.tournoi.tour_en_cours+1}/{self.controls_tournois.tournoi.nb_tour}")
                self.controls_tournois.lancer_nouveau_tour(date_heure_debut)
                self.entrer_resultats_tour()
                
                dernier_tour = self.controls_tournois.tournoi.liste_tours[-1]
                dernier_tour.afficher_matchs()

                date_heure_fin = self.menu.demander_information("Entrez la date de fin du tour (JJ/MM/AAA HH:MM): ")
                dernier_tour.date_et_heure_fin = date_heure_fin


                self.controls_tournois.tournoi.tour_en_cours += 1
                

                
                self.sauvegarder_tournoi()
                
                
                if not self.demander_continuer_ou_quitter():
                    break

                date_heure_debut = date_heure_fin
                
            if self.controls_tournois.tournoi.tour_en_cours == self.controls_tournois.nb_tour:
                self.generer_classement()

    def generer_classement(self):
        joueurs = self.controls_tournois.tournoi.liste_joueurs

        

        classement = sorted(joueurs, key=lambda joueur: joueur.score, reverse=True)

        self.menu.afficher_message("Classement final du tournoi :")
        for i, joueur in enumerate(classement, start=1):
            self.menu.afficher_message(f"{i}. {joueur.nom} {joueur.prenom}. Score: {joueur.score} points")
        return classement
            
    def entrer_resultats_tour(self):
        
        dernier_tour = self.controls_tournois.tournoi.liste_tours[-1]
      
        for match in dernier_tour.liste_matches:
            if match.score_joueur_1 !=0 or match.score_joueur_2 !=0:
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
                

            elif resultat ==2:
                self.menu.afficher_message(f"{match.joueur_2.nom} a gagné.")
                match.joueur_1.mettre_a_jour_score(0)
                match.joueur_2.mettre_a_jour_score(1)
                match.score_joueur_1 = 0
                match.score_joueur_2 = 1
                

            elif resultat ==3:
                self.menu.afficher_message("Match nul.")
                match.joueur_1.mettre_a_jour_score(0.5)
                match.joueur_2.mettre_a_jour_score(0.5)
                match.score_joueur_1 = 0.5
                match.score_joueur_2 = 0.5
                
            
                

        #self.controls_tournois.terminer_tour()
        

   


    def demander_continuer_ou_quitter(self):
        choix = self.menu.demander_information("Voulez continuer ou quitter ? ")
        if choix == "q":
            print("DEBUG: Appel de la sauvegarde avant de quitter.")
            self.sauvegarder_tournoi()
            self.menu.afficher_message("Vous avez quitté le tournois.")
            return False
        elif choix == "c":
            return True
        else:
            self.menu.afficher_message("Choix invalide, réessayer.")
            return self.demander_continuer_ou_quitter()
        
 
        



def main():
    menu = MenuPrincipal()
    gestion_joueur = GestionJoueurs(menu)
    gestion_information_joueur = Gestion_information_joueur()
    controls_joueur = ControlsJoueur(gestion_joueur)
    gestion_information_tournoi = Gestion_information_tournoi()
    joueurs_charges = gestion_information_joueur.charger_joueurs()
    gestion_joueur.liste_joueurs = joueurs_charges
    gestion_rapports = GestionRapport()
    if not gestion_joueur.liste_joueurs:
        menu.afficher_message("Auncun joueur n'a été trouvé. Ajouter des joueurs.2")
    #controls_tour = ControlsTour(None, None)
    #controls_tournois = ControlsTournois(None)

    controls_principal = ControlsPrincipal(menu, controls_joueur, gestion_information_joueur, gestion_information_tournoi, gestion_joueur, gestion_rapports, None, None)

    controls_principal.lancer_menu_principal()

main()


   
                

            

        
        

   
   



        