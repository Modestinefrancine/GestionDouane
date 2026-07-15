# gui.py
import tkinter as tk
from tkinter import messagebox
from database import inserer_nouveau_dossier
from strategies import generer_le_rapport_pdf
from exceptions import AgenceDouaneException

def calculer_et_enregistrer():
    client = entry_client.get().strip()
    marchandise = entry_marchandise.get().strip()
    valeur_str = entry_valeur.get().strip()
    
    if not client or not marchandise or not valeur_str:
        messagebox.showwarning("Champs vides", "Veuillez remplir le client, la marchandise et la valeur.")
        return
    
    try:
        valeur_fob = float(valeur_str)
        
        # --- LOGIQUE DE CALCUL DE L'AGENCE ---
        droits_douane = valeur_fob * 0.20  # Exemple : Taux de douane à 20%
        tva = (valeur_fob + droits_douane) * 0.16  # Exemple : TVA à 16%
        total_taxes = droits_douane + tva
        
        
        # Affichage du résultat instantané sur l'interface
        label_resultat_douane.config(text=f"{droits_douane:,.2f} $")
        label_resultat_tva.config(text=f"{tva:,.2f} $")
        label_resultat_total.config(text=f"{total_taxes:,.2f} $")
        
        # Enregistrement du dossier avec le montant total calculé
        statut = "Calculé"
        inserer_nouveau_dossier(client, marchandise, statut, total_taxes)
        
        messagebox.showinfo("Calcul Terminé", f"Calcul réussi et enregistré pour {client} !")
        
    except ValueError:
        messagebox.showerror("Erreur de format", "La valeur de la marchandise doit être un nombre valide.")
    except AgenceDouaneException as ae:
        messagebox.showerror("Erreur Base", str(ae))

def declencher_rapport():
    try:
        generer_le_rapport_pdf()
        messagebox.showinfo("Succès", "Le rapport PDF contenant tous les calculs a été généré !")
    except AgenceDouaneException as ae:
        messagebox.showerror("Alerte Rapport", str(ae))

def lancer_interface():
    global entry_client, entry_marchandise, entry_valeur
    global label_resultat_douane, label_resultat_tva, label_resultat_total
    
    fenetre = tk.Tk()
    fenetre.title("Calculateur de Taxes - MAVIC SERVICE S.A.")
    fenetre.geometry("500x520")
    fenetre.config(bg="#f5f5f5")
    
    # --- SECTION SAISIE ---
    tk.Label(fenetre, text="SAISIE DES DONNÉES", font=("Helvetica", 12, "bold"), bg="#f5f5f5", fg="#333").pack(pady=10)
    
    tk.Label(fenetre, text="Nom du Client :", bg="#f5f5f5").pack(anchor="w", padx=40)
    entry_client = tk.Entry(fenetre, width=50)
    entry_client.pack(padx=40, pady=2)
    
    tk.Label(fenetre, text="Type de Marchandise :", bg="#f5f5f5").pack(anchor="w", padx=40)
    entry_marchandise = tk.Entry(fenetre, width=50)
    entry_marchandise.pack(padx=40, pady=2)
    
    tk.Label(fenetre, text="Valeur de la Marchandise ($) :", bg="#f5f5f5").pack(anchor="w", padx=40)
    entry_valeur = tk.Entry(fenetre, width=50)
    entry_valeur.pack(padx=40, pady=2)
    
    # Bouton de calcul
    btn_calculer = tk.Button(fenetre, text="1. Calculer les Taxes & Enregistrer", command=calculer_et_enregistrer, bg="#2196F3", fg="white", font=("Helvetica", 10, "bold"), pady=5)
    btn_calculer.pack(pady=15)
    
    # --- SECTION RÉSULTATS VISUELS ---
    cadre_resultat = tk.LabelFrame(fenetre, text=" RÉSULTATS DU CALCUL INSTATANÉ ", font=("Helvetica", 10, "bold"), bg="#e3f2fd", bd=2, padx=15, pady=10)
    cadre_resultat.pack(fill="x", padx=40, pady=10)
    
    tk.Label(cadre_resultat, text="Droits de Douane (20%) :", font=("Helvetica", 10), bg="#e3f2fd").grid(row=0, column=0, sticky="w", pady=2)
    label_resultat_douane = tk.Label(cadre_resultat, text="0.00 $", font=("Helvetica", 10, "bold"), bg="#e3f2fd", fg="#0d47a1")
    label_resultat_douane.grid(row=0, column=1, sticky="e", padx=20)
    
    tk.Label(cadre_resultat, text="TVA (16%) :", font=("Helvetica", 10), bg="#e3f2fd").grid(row=1, column=0, sticky="w", pady=2)
    label_resultat_tva = tk.Label(cadre_resultat, text="0.00 $", font=("Helvetica", 10, "bold"), bg="#e3f2fd", fg="#0d47a1")
    label_resultat_tva.grid(row=1, column=1, sticky="e", padx=20)
    
    tk.Label(cadre_resultat, text="TOTAL À PAYER :", font=("Helvetica", 10, "bold"), bg="#e3f2fd").grid(row=2, column=0, sticky="w", pady=5)
    label_resultat_total = tk.Label(cadre_resultat, text="0.00 $", font=("Helvetica", 11, "bold"), bg="#e3f2fd", fg="#d32f2f")
    label_resultat_total.grid(row=2, column=1, sticky="e", padx=20)
    
    # Separateur
    tk.Frame(fenetre, height=2, bg="#ccc").pack(fill="x", padx=40, pady=10)
    
    # --- SECTION EXPORT ---
    btn_pdf = tk.Button(fenetre, text="2. Sortir le Rapport PDF Global", command=declencher_rapport, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"), pady=5)
    btn_pdf.pack(pady=5)
    
    fenetre.mainloop()