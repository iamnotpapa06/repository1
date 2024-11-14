"""Salut. Nous vous présentons notre code générant notre application de voyage "Horizons Voyage"
                                                                                                 """
""" Bibliothèques utilisées dans notre application Horizons Voyage
                                                                   """
import customtkinter as ctk
import pyodbc
from tkinter import ttk
import tkinter.messagebox as messagebox

""" Configuration de la connexion.
                                  """
server = 'DESKTOP-JEKMIAS\\SQLEXPRESS'
database = 'Voyage'

""" Chaine de connexion.
                        """
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=' + server + ';'
    'DATABASE=' + database + ';'
    'Trusted_Connection=yes;'
    )


""" def connect_to_db():
    - établit une connexion à la base de données.
    - renvoie la connexion et le curseur si la connexion est réussie, 
    sinon renvoie un message d'erreur.    
                                      """
def connect_to_db():
    try:
        conn = pyodbc.connect(conn_str)  # Essaye de se connecter à la base de données
        cursor = conn.cursor()  # Crée un curseur pour exécuter des requêtes
        return conn, cursor  # Renvoie la connexion et le curseur
    except:
        return "Erreur de connexion à la base de données."  # Message d'erreur si la connexion échoue

""" def search_data():
    - recherche toutes les données dans la table Station
    - renvoie les lignes récupérées ou un message d'erreur si la recherche échoue.
                                                                                  """
def search_data():
    conn, cursor = connect_to_db()  # Établit une connexion à la base de données
    if conn:  # Vérifie si la connexion est réussie
        try:
            cursor.execute("SELECT * FROM Station")  # Exécute une requête pour sélectionner toutes les stations
            rows = cursor.fetchall()  # Récupère toutes les lignes résultantes
            return rows  # Renvoie les lignes
        except:
            return "Erreur lors de la recherche des données."  # Message d'erreur générique en cas d'échec
        finally:
            cursor.close()  # Ferme le curseur
            conn.close()  # Ferme la connexion
    return "Erreur de connexion."  # Message d'erreur si la connexion échoue

""" def insert_data():
    - insère une nouvelle station dans la table Station
    - renvoie un message de succès ou d'erreur selon le résultat de l'insertion.
                                                                                """
def insert_data(nom, capacite, lieu, region, tarif):
    conn, cursor = connect_to_db()  # Établit une connexion à la base de données
    if conn:  # Vérifie si la connexion est réussie
        try:
            cursor.execute("""
                INSERT INTO Station (nomStation, capacité, lieu, région, tarif)
                VALUES (?, ?, ?, ?, ?)
            """, (nom, capacite, lieu, region, tarif))  # Exécute une requête d'insertion avec les données fournies
            conn.commit()  # Valide les changements
            return "Données ajoutées avec succès !"  # Message de succès
        except:
            return "Erreur lors de l'insertion des données."  # Message d'erreur générique en cas d'échec
        finally:
            cursor.close()  # Ferme le curseur
            conn.close()  # Ferme la connexion
    return "Erreur de connexion."  # Message d'erreur si la connexion échoue

""" def modify_data():
    - modifie les informations d'une station existante.
    - renvoie un message de succès ou d'erreur selon le résultat de la modification.
                                                                                    """
def modify_data(nomStation, nouveau_nom=None, nouvelle_capacite=None, nouveau_lieu=None, nouvelle_region=None, nouveau_tarif=None):
    conn, cursor = connect_to_db()  # Établit une connexion à la base de données
    if conn:  # Vérifie si la connexion est réussie
        try:
            if nouveau_nom:  # Si un nouveau nom est fourni
                cursor.execute("UPDATE Station SET nomStation = ? WHERE nomStation = ?", (nouveau_nom, nomStation))
            if nouvelle_capacite:  # Si une nouvelle capacité est fournie
                cursor.execute("UPDATE Station SET capacité = ? WHERE nomStation = ?", (nouvelle_capacite, nomStation))
            if nouveau_lieu:  # Si un nouveau lieu est fourni
                cursor.execute("UPDATE Station SET lieu = ? WHERE nomStation = ?", (nouveau_lieu, nomStation))
            if nouvelle_region:  # Si une nouvelle région est fournie
                cursor.execute("UPDATE Station SET région = ? WHERE nomStation = ?", (nouvelle_region, nomStation))
            if nouveau_tarif:  # Si un nouveau tarif est fourni
                cursor.execute("UPDATE Station SET tarif = ? WHERE nomStation = ?", (nouveau_tarif, nomStation))
            conn.commit()  # Valide les changements
            return "Station modifiée avec succès !"  # Message de succès
        except:
            return "Erreur lors de la modification des données."  # Message d'erreur générique en cas d'échec
        finally:
            cursor.close()  # Ferme le curseur
            conn.close()  # Ferme la connexion
    return "Erreur de connexion."  # Message d'erreur si la connexion échoue

""" 
    def delete_data():
    - supprime une station de la table Station
    - renvoie un message de succès ou d'erreur selon le résultat de la suppression.
                                                                                   """
def delete_data(nomStation):
    conn, cursor = connect_to_db()  # Établit une connexion à la base de données
    if conn:  # Vérifie si la connexion est réussie
        try:
            cursor.execute("""
                DELETE FROM Station
                WHERE nomStation = ?
            """, (nomStation,))  # Exécute une requête de suppression pour la station spécifiée
            conn.commit()  # Valide les changements
            return "Station supprimée avec succès !"  # Message de succès
        except:
            return "Erreur lors de la suppression des données."  # Message d'erreur générique en cas d'échec
        finally:
            cursor.close()  # Ferme le curseur
            conn.close()  # Ferme la connexion
    return "Erreur de connexion."  # Message d'erreur si la connexion échoue

""" def update_treeview():
    - met à jour le Treeview avec les données des stations.
    - efface les anciens éléments et insère les nouveaux.
                                                             """
def update_treeview(tree):

    for item in tree.get_children():  # Supprime tous les éléments existants dans le Treeview
        tree.delete(item)
    rows = search_data()  # Récupère toutes les stations
    if isinstance(rows, str):  # Vérifie si une erreur a été renvoyée
        return
    for row in rows:  # Pour chaque ligne récupérée
        tree.insert("", "end", values=(row.nomStation, row.capacité, row.lieu, row.région, row.tarif))  # Insère les données dans le Treeview



""" def show_info_messagebox () crée une boîte de message pour afficher des informations.
                                                             """
def show_info_messagebox(title, message):
    info_messagebox = ctk.CTkToplevel(app)  # Nouvelle fenêtre pour le message
    info_messagebox.title(title)  # Titre de la fenêtre
    
    # Définir la taille de la fenêtre
    info_messagebox.geometry("400x300")

    # Ajouter un label pour le message, centrer le texte
    message_label = ctk.CTkLabel(info_messagebox, text=message, font=('Segoe UI', 20))
    message_label.pack(padx=20, pady=10, expand=True)  # Utiliser expand pour centrer verticalement

    # Ajouter un bouton pour fermer la fenêtre
    close_button = ctk.CTkButton(info_messagebox, text="OK", command=info_messagebox.destroy, font=('Mistral', 40), fg_color="blue")
    close_button.pack(pady=20)  # Pady pour espacer le bouton


""" def show_contact_info() affiche les informations de contact selon l'option choisie.
                                                                                       """
def show_contact_info(option):
    # Si l'option est "phone", afficher le numéro de téléphone
    if option == "phone":
        show_info_messagebox("Contact", "Numéro de téléphone : +221 33 936 54 07")  # Affiche le numéro de téléphone
    
    # Si l'option est "about", afficher les informations sur l'application
    elif option == "about":
        app_info = (
            "Nom de l'application : Horizons Voyage\n"
            "Version : 1.0\n"
            "Développé par :\n"
            "Moussa Niang 👨\n" 
            "Nogaye Ndiaye 👩‍🦱\n"
            "Mariama Foly Diallo 👩\n"
            "Papa Samba Niang 🧑\n"
            "Cette application permet de gérer les informations sur les stations de voyage.\n"
            "Fonctionnalités :\n"
            "- Ajouter, modifier, supprimer et rechercher des stations\n"
            "- Afficher la liste des stations enregistrées"
        )
        # Appeler la fonction pour afficher les informations sur l'application
        show_info_messagebox("À propos", app_info)  # Affiche les informations sur l'application


""" def show_user_info() affiche les informations sur l'utilisateur sélectionné.
                                                                                 """
def show_user_info(user):
        # Dictionnaire contenant les informations des utilisateurs
        user_info = {
        "👨": (
            "Nom: Moussa Niang\n"
            "Email: moussaniang@gmail.com\n"
            "Rôle: Administrateur\n"
            "Expérience: 5 ans dans la gestion de projets\n"
            "Responsabilités: Supervise la gestion de l'application,\n"
            "assure la sécurité des données et coordonne les équipes."
        ),
        "👩‍🦱": (
            "Nom: Nogaye Ndiaye\n"
            "Email: nogayendiaye@gmail.com\n"
            "Rôle: Gestionnaire\n"
            "Expérience: 3 ans dans la gestion opérationnelle\n"
            "Responsabilités: Gère les opérations quotidiennes,\n"
            "s'assure de la satisfaction des utilisateurs et\n "
            "analyse les performances."
        ),
        "👩": (
            "Nom: Mariama Foly Diallo\n"
            "Email: mariamafolydiallo@gmail.com\n"
            "Rôle: Gestionnaire\n"
            "Expérience: 4 ans dans la gestion de projets\n"
            "Responsabilités: Coordonne les activités de l'équipe,\n"
            "suit les indicateurs de performance et\n"
            "élabore des rapports."
        ),
        "🧑": (
            "Nom: Papa Samba Niang\n"
            "Email: papasambaniang@gmail.com\n"
            "Rôle: Employé\n"
            "Expérience: 2 ans dans le service client\n"
            "Responsabilités: Assiste les utilisateurs,\n"
            "et assure le support technique."
        )
    }
        # Affiche les informations sur l'utilisateur sélectionné
        show_info_messagebox("Personnel", user_info[user])  # Affiche les informations sur l'utilisateur


""" def create_contact_window() crée une fenêtre de contact avec des informations utiles.
                                                                                         """
def create_contact_window():
    # Création d'une nouvelle fenêtre de contact
    contact_window = ctk.CTkToplevel(app)  
    contact_window.geometry("800x600") # Définition de la taille de la fenêtre

    # Frame pour les boutons en haut à gauche
    button_frame = ctk.CTkFrame(contact_window)
    button_frame.pack(side="top", anchor="nw", padx=10, pady=10)

    # Boutons pour afficher les informations de contact
    ctk.CTkButton(button_frame, text="🔍", command=lambda: show_contact_info("about"), font=('Segoe UI', 45), width=30, text_color="yellow", fg_color="blue").pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="📞", command=lambda: show_contact_info("phone"), font=('Segoe UI', 45), width=30, text_color="red", fg_color="blue").pack(side="left", padx=5)
    
    # Frame pour les icônes de l'application, positionnée en haut à droite
    iconapp_frame = ctk.CTkFrame(contact_window)
    iconapp_frame.pack(side="top", anchor="ne", padx=10, pady=10)

    # Bouton pour revenir à la fenêtre principale
    ctk.CTkButton(iconapp_frame, text="🛩️", command=lambda: app.deiconify(), font=('Segoe UI', 45), width=30, text_color="blue", fg_color="white", anchor="ne").pack(side="right", padx=5)

    # Frame pour le titre de la fenêtre
    title_frame = ctk.CTkFrame(contact_window)
    title_frame.pack(pady=20)

    # Titre de la fenêtre
    ctk.CTkLabel(title_frame, text="Horizons Voyage", font=('Mistral', 60)).pack(pady=10)

    # Frame en bas à gauche pour le copyright
    copyright_frame = ctk.CTkFrame(contact_window)
    copyright_frame.pack(side="bottom", anchor="sw", padx=10, pady=(5, 5))
    
    # Label pour afficher le texte du copyright
    copyright_label = ctk.CTkLabel(copyright_frame, text="© Octobre 2024.", font=('Segoe UI', 20))
    copyright_label.pack()

    # Frame en bas à droite pour les icônes utilisateur
    user_icon_frame = ctk.CTkFrame(contact_window)
    user_icon_frame.pack(side="bottom", anchor="se", padx=10, pady=10)

    # Création des boutons pour chaque utilisateur
    user_buttons = [
        ("👨", "Moussa"),
        ("👩‍🦱", "Nogaye"),
        ("👩", "Mariama"),
        ("🧑", "Papa Samba")
    ]

    for icon, name in user_buttons:
        ctk.CTkButton(user_icon_frame, text=icon, command=lambda u=icon : show_user_info(u), font=('Segoe UI', 45), width=30, text_color="blue", fg_color="white").pack(side="left", padx=5)

""" Variables globales.
                       """
current_user = None
user_roles = {
    "Moussa": "Admin",
    "Nogaye": "Gestionnaire",
    "Mariama": "Gestionnaire",
    "Papa Samba": "Employé"
    }


""" def login_callback(): callback pour gérer la connexion de l'utilisateur.
                                                                            """
def login_callback():
    global current_user
    username = username_entry.get()  # Récupère le nom d'utilisateur
    
    if username in user_roles:
        current_user = username  # Définit l'utilisateur courant
        login_frame.destroy()  # Supprime le cadre de connexion
        create_widgets()  # Crée les widgets principaux
    
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur non reconnu.")  # Affiche une erreur si l'utilisateur n'est pas reconnu


""" Création de la fenêtre principale
                                         """
app = ctk.CTk()  # Création de la fenêtre principale
app.geometry("800x600")  # Définition de la taille de la fenêtre

# Création d'un cadre pour l'écran de connexion
login_frame = ctk.CTkFrame(app)
login_frame.pack(pady=200)

# Création d'un label pour le champ de saisie du nom d'utilisateur
ctk.CTkLabel(login_frame, text="Nom d'utilisateur :", font=('Segoe UI', 24)).grid(row=0, column=0, padx=10, pady=10)
username_entry = ctk.CTkEntry(login_frame, font=('Segoe UI', 24), width=200)
username_entry.grid(row=0, column=1)

# Création d'un bouton pour se connecter
ctk.CTkButton(login_frame, text="Se connecter", font=('Mistral', 40), width=10, command=login_callback).grid(row=1, column=0, columnspan=2, pady=10)


""" def create_widgets() crée les onglets principaux de l'application.
                                                                      """
def create_widgets():
    global info_frame, tree

    button_frame = ctk.CTkFrame(app)  # Création d'un cadre pour les boutons
    button_frame.pack(side="top", fill="x", padx=10, pady=10)

    # Remplacement des icônes des boutons par les emojis spécifiés selon l'utilisateur
    if current_user == "Moussa":
        user_icon = "👨"
    elif current_user == "Nogaye":
        user_icon = "👩‍🦱"
    elif current_user == "Mariama":
        user_icon = "👩"
    elif current_user == "Papa Samba":
        user_icon = "🧑"

    # Création du bouton pour l'utilisateur actuel
    ctk.CTkButton(button_frame, text=user_icon, command=None, font=('Segoe UI', 45), width=30, text_color="black", fg_color="white").pack(side="left", padx=5)

    # Cadre d'information pour le message de bienvenue
    info_frame = ctk.CTkFrame(app)
    info_frame.pack(pady=20)

    # Labels de bienvenue
    ctk.CTkLabel(info_frame, text=f"Bienvenue, {current_user}!", font=('Mistral', 60)).pack(pady=10)
    ctk.CTkLabel(info_frame, text="Bonne journée !", font=('Mistral', 40), text_color="grey").pack(pady=10)

    create_manager_tabs()  # Création des onglets pour le gestionnaire

    # Cadre pour afficher les stations
    display_frame = ctk.CTkFrame(app)
    display_frame.pack(side="right", fill="both", expand=True)

    # Label pour les stations disponibles
    stations_label = ctk.CTkLabel(display_frame, text="Stations disponibles", font=('Mistral', 40, 'bold'))
    stations_label.pack(pady=5)

    # Création de la Treeview pour afficher les stations
    tree = ttk.Treeview(display_frame, columns=("Nom", "Capacité", "Lieu", "Région", "Tarif"), show='headings')
    tree.heading("Nom", text="Nom")
    tree.heading("Capacité", text="Capacité")
    tree.heading("Lieu", text="Lieu")
    tree.heading("Région", text="Région")
    tree.heading("Tarif", text="Tarif")

    # Configuration des colonnes de la Treeview
    tree.column("Nom", width=150, anchor="w")
    tree.column("Capacité", width=100, anchor="w")
    tree.column("Lieu", width=150, anchor="w")
    tree.column("Région", width=150, anchor="w")
    tree.column("Tarif", width=100, anchor="w")

    tree.pack(fill="both", expand=True)  # Ajout de la Treeview au cadre

    update_treeview(tree)  # Mise à jour de la Treeview avec les données
    
    # Configuration du style pour la Treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Helvetica', 14))
    style.configure("Treeview", font=('Helvetica', 13))

""" def show_custom_messagebox() crée une boîte de message personnalisée pour afficher des résultats.
                                                                                                     """
def show_custom_messagebox(title, message):
    custom_messagebox = ctk.CTkToplevel(app)  # Nouvelle fenêtre pour le message
    custom_messagebox.title(title)  # Titre de la fenêtre
    
    # Définir la taille de la fenêtre
    custom_messagebox.geometry("400x300")

    # Ajouter un label pour le message
    message_label = ctk.CTkLabel(custom_messagebox, text=message, font=('Segoe UI', 20))
    message_label.pack(padx=20, pady=20, expand=True)  # Utiliser expand pour centrer verticalement

    # Ajouter un bouton pour fermer la fenêtre
    close_button = ctk.CTkButton(custom_messagebox, text="OK", command=custom_messagebox.destroy, font=('Mistral', 40), fg_color="black")
    close_button.pack(pady=20)  # Pady pour espacer le bouton


""" def create_manager_tabs() crée les onglets pour l'interface utilisateur en fonction du rôle de l'utilisateur actuel.
                                                                                             """
def create_manager_tabs():
    tabview = ctk.CTkTabview(app)  # Crée un nouvel onglet dans l'application
    tabview.pack(side="left", fill="both", expand=True)  # Ajoute l'onglet à l'interface

    if current_user == "Papa Samba":  # Vérifie si l'utilisateur est Papa Samba
        info_tab = tabview.add("Information")  # Ajoute un onglet pour les informations
        ctk.CTkLabel(info_tab, text="Vous avez un accès limité à cette application.", font=('Mistral', 40)).pack(pady=20)  # Affiche un message d'accès limité
        search_tab = tabview.add("Rechercher une station")  # Ajoute un onglet pour rechercher une station
        create_search_tab_content(search_tab)  # Crée le contenu de l'onglet de recherche

    elif current_user == "Moussa":  # Vérifie si l'utilisateur est Moussa
        insert_tab = tabview.add("Ajouter une station")  # Ajoute un onglet pour ajouter une station
        create_insert_tab_content(insert_tab)  # Crée le contenu de l'onglet d'insertion
        modify_tab = tabview.add("Modifier une station")  # Ajoute un onglet pour modifier une station
        create_modify_tab_content(modify_tab)  # Crée le contenu de l'onglet de modification
        delete_tab = tabview.add("Supprimer une station")  # Ajoute un onglet pour supprimer une station
        create_delete_tab_content(delete_tab)  # Crée le contenu de l'onglet de suppression
        search_tab = tabview.add("Rechercher une station")  # Ajoute un onglet pour rechercher une station
        create_search_tab_content(search_tab)  # Crée le contenu de l'onglet de recherche

    elif current_user in ["Nogaye", "Mariama"]:  # Vérifie si l'utilisateur est Nogaye ou Mariama
        insert_tab = tabview.add("Ajouter une station")  # Ajoute un onglet pour ajouter une station
        create_insert_tab_content(insert_tab)  # Crée le contenu de l'onglet d'insertion
        delete_tab = tabview.add("Supprimer une station")  # Ajoute un onglet pour supprimer une station
        create_delete_tab_content(delete_tab)  # Crée le contenu de l'onglet de suppression
        search_tab = tabview.add("Rechercher une station")  # Ajoute un onglet pour rechercher une station
        create_search_tab_content(search_tab)  # Crée le contenu de l'onglet de recherche


""" def create_insert_tab_content crée le contenu de l'onglet pour ajouter une station.
                                                                                       """
def create_insert_tab_content(tab):
    
    ctk.CTkLabel(tab, text="Nom :", font=('Segoe UI', 24)).grid(row=0, column=0, padx=10, pady=10)  # Label pour le nom
    nom_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour le nom
    nom_entry.grid(row=0, column=1)

    ctk.CTkLabel(tab, text="Capacité :", font=('Segoe UI', 24)).grid(row=1, column=0, padx=10, pady=10)  # Label pour la capacité
    capacite_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour la capacité
    capacite_entry.grid(row=1, column=1)

    ctk.CTkLabel(tab, text="Lieu :", font=('Segoe UI', 24)).grid(row=2, column=0, padx=10, pady=10)  # Label pour le lieu
    lieu_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour le lieu
    lieu_entry.grid(row=2, column=1)

    ctk.CTkLabel(tab, text="Région :", font=('Segoe UI', 24)).grid(row=3, column=0, padx=10, pady=10)  # Label pour la région
    region_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour la région
    region_entry.grid(row=3, column=1)

    ctk.CTkLabel(tab, text="Tarif :", font=('Segoe UI', 24)).grid(row=4, column=0, padx=10, pady=10)  # Label pour le tarif
    tarif_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour le tarif
    tarif_entry.grid(row=4, column=1)
    
    """ def insert_data_callback(): callback pour ajouter une station. 
                                                                      """
    def insert_data_callback():
        nom = nom_entry.get()  # Récupère le nom
        capacite = capacite_entry.get()  # Récupère la capacité
        lieu = lieu_entry.get()  # Récupère le lieu
        region = region_entry.get()  # Récupère la région
        tarif = tarif_entry.get()  # Récupère le tarif
        message = insert_data(nom, capacite, lieu, region, tarif)  # Ajoute la station
        show_custom_messagebox("Ajout de Station", message)  # Affiche un message
        update_treeview(tree)  # Met à jour l'affichage des stations

    # Bouton pour ajouter la station
    ctk.CTkButton(tab, text="Ajouter", command=insert_data_callback, fg_color="green", font=('Mistral', 40)).grid(row=5, column=0, columnspan=2, pady=10)

""" def create_modify_tab_content() crée le contenu de l'onglet pour modifier une station.
                                                                                          """
def create_modify_tab_content(tab):
    ctk.CTkLabel(tab, text="Nom de la station à modifier :", font=('Segoe UI', 24)).grid(row=0, column=0, padx=10, pady=10)  # Label pour le nom de la station à modifier
    modify_nom_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour le nom
    modify_nom_entry.grid(row=0, column=1)

    ctk.CTkLabel(tab, text="Nouveau nom :", font=('Segoe UI', 24)).grid(row=1, column=0, padx=10, pady=10)  # Label pour le nouveau nom
    nouveau_nom_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour le nouveau nom
    nouveau_nom_entry.grid(row=1, column=1)

    ctk.CTkLabel(tab, text="Nouvelle capacité :", font=('Segoe UI', 24)).grid(row=2, column=0, padx=10, pady=10)  # Label pour la nouvelle capacité
    nouvelle_capacite_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour la nouvelle capacité
    nouvelle_capacite_entry.grid(row=2, column=1)

    ctk.CTkLabel(tab, text="Nouveau lieu :", font=('Segoe UI', 24)).grid(row=3, column=0, padx=10, pady=10)  # Label pour le nouveau lieu
    nouveau_lieu_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour le nouveau lieu
    nouveau_lieu_entry.grid(row=3, column=1)

    ctk.CTkLabel(tab, text="Nouvelle région :", font=('Segoe UI', 24)).grid(row=4, column=0, padx=10, pady=10)  # Label pour la nouvelle région
    nouvelle_region_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour la nouvelle région
    nouvelle_region_entry.grid(row=4, column=1)

    ctk.CTkLabel(tab, text="Nouveau tarif :", font=('Segoe UI', 24)).grid(row=5, column=0, padx=10, pady=10)  # Label pour le nouveau tarif
    nouveau_tarif_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour le nouveau tarif
    nouveau_tarif_entry.grid(row=5, column=1)
    
    """ def modify_data_callback(): callback pour modifier une station.
                                                                       """
    def modify_data_callback():
        nomStation = modify_nom_entry.get()  # Récupère le nom de la station à modifier
        nouveau_nom = nouveau_nom_entry.get()  # Récupère le nouveau nom
        nouvelle_capacite = nouvelle_capacite_entry.get()  # Récupère la nouvelle capacité
        nouveau_lieu = nouveau_lieu_entry.get()  # Récupère le nouveau lieu
        nouvelle_region = nouvelle_region_entry.get()  # Récupère la nouvelle région
        nouveau_tarif = nouveau_tarif_entry.get()  # Récupère le nouveau tarif

        message = modify_data(nomStation, nouveau_nom, nouvelle_capacite, nouveau_lieu, nouvelle_region, nouveau_tarif)  # Modifie la station
        show_custom_messagebox("Modification de Station", message)  # Affiche un message
        update_treeview(tree)  # Met à jour l'affichage des stations

    # Bouton pour modifier la station
    ctk.CTkButton(tab, text="Modifier", command=modify_data_callback, fg_color="blue", font=('Mistral', 40)).grid(row=6, column=0, columnspan=2, pady=10)

""" def create_delete_tab_content() crée le contenu de l'onglet pour supprimer une station.
                                                                                           """
def create_delete_tab_content(tab):
    ctk.CTkLabel(tab, text="Nom de la station à supprimer :", font=('Segoe UI', 24)).grid(row=0, column=0, padx=10, pady=10)  # Label pour le nom de la station à supprimer
    delete_nom_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour le nom
    delete_nom_entry.grid(row=0, column=1)
    
    """ def delete_data_callback(): callback pour supprimer une station.
                                                                        """
    def delete_data_callback():
        nomStation = delete_nom_entry.get()  # Récupère le nom de la station à supprimer
        message = delete_data(nomStation)  # Supprime la station
        show_custom_messagebox("Suppression de Station", message)  # Affiche un message
        update_treeview(tree)  # Met à jour l'affichage des stations

    # Bouton pour supprimer la station
    ctk.CTkButton(tab, text="Supprimer", command=delete_data_callback, fg_color="red", font=('Mistral', 40)).grid(row=1, column=0, columnspan=2, pady=10)

""" def create_search_tab_content() crée le contenu de l'onglet pour rechercher une station.
                                                                                            """
def create_search_tab_content(tab):
    ctk.CTkLabel(tab, text="Nom de la station à rechercher :", font=('Segoe UI', 24)).grid(row=0, column=0, padx=10, pady=10)  # Label pour le nom de la station à rechercher
    search_nom_entry = ctk.CTkEntry(tab, font=('Segoe UI', 24))  # Champ de saisie pour le nom
    search_nom_entry.grid(row=0, column=1)

    result_label = ctk.CTkLabel(tab, text="", font=('Segoe UI', 24))  # Label pour afficher le résultat
    result_label.grid(row=2, column=0, columnspan=2, pady=10)
    
    """ def search_data_callback(): callback pour rechercher une station.
                                                                       """
    def search_data_callback():
        nomStation = search_nom_entry.get()  # Récupère le nom de la station à rechercher
        rows = search_data()  # Récupère toutes les stations
        found = None  # Initialisation de la variable pour stocker la station trouvée
        
        for row in rows:
            if row.nomStation.lower() == nomStation.lower():  # Comparer sans tenir compte de la casse
                found = row  # Si trouvé, stocke la station
                break  # Sort de la boucle

        if found:
            # Affiche toutes les données de la station trouvée
            message = (f"Station trouvée : {found.nomStation}\n"
                       f"Capacité: {found.capacité}\n"
                       f"Lieu: {found.lieu}\n"
                       f"Région: {found.région}\n"
                       f"Tarif: {found.tarif}")
            show_custom_messagebox("Résultat de la recherche", message)  # Affiche le résultat
        else:
            show_custom_messagebox("Résultat de la recherche", "Aucune station trouvée.")  # Affiche un message si rien trouvé

    # Bouton pour lancer la recherche
    ctk.CTkButton(tab, text="Rechercher", command=search_data_callback, fg_color="chocolate", font=('Mistral', 40)).grid(row=1, column=0, columnspan=2, pady=10)

app.withdraw()  # Masque l'application principale
create_contact_window()  # Crée la fenêtre de contact
app.mainloop()  # Démarre la boucle principale de l'application
