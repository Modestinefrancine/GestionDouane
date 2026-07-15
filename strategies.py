# strategies.py
from abc import ABC, abstractmethod
from fpdf import FPDF
from database import recuperer_tous_les_dossiers

class StrategieRapport(ABC):
    @abstractmethod
    def generer(self, dossiers):
        pass

class GenerateurPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "AGENCE EN DOUANE - MAVIC SERVICE S.A.", ln=True, align="C")
        self.set_font("Helvetica", "I", 10)
        self.cell(0, 10, "Rapport d'Activités de Dédouanement", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

class RapportPDFStrategy(StrategieRapport):
    def generer(self, dossiers):
        pdf = GenerateurPDF()
        pdf.add_page()
        
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "Liste des Dossiers Traités :", ln=True)
        pdf.ln(5)
        
        # En-têtes du tableau
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(15, 8, "ID", border=1)
        pdf.cell(55, 8, "Client", border=1)
        pdf.cell(55, 8, "Marchandise", border=1)
        pdf.cell(30, 8, "Statut", border=1)
        pdf.cell(35, 8, "Valeur ($)", border=1, ln=True)
        
        # Remplissage du tableau
        pdf.set_font("Helvetica", size=10)
        for d in dossiers:
            pdf.cell(15, 8, str(d.id_dossier), border=1)
            pdf.cell(55, 8, d.client, border=1)
            pdf.cell(55, 8, d.type_marchandise, border=1)
            pdf.cell(30, 8, d.statut, border=1)
            pdf.cell(35, 8, f"{d.valeur_declaration:,.2f}", border=1, ln=True)
            
        pdf.output("rapport.pdf")

class ContexteRapport:
    def __init__(self, strategie: StrategieRapport):
        self._strategie = strategie

    def executer_generation(self):
        dossiers = recuperer_tous_les_dossiers()
        self._strategie.generer(dossiers)

def generer_le_rapport_pdf():
    contexte = ContexteRapport(RapportPDFStrategy())
    contexte.executer_generation()