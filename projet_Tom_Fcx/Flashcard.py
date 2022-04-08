import pickle, datetime, random, os, csv
from tkinter import filedialog
from tkinter import *
root = Tk()
root.iconbitmap('iconApp.ico')
root.title('Flashcarding')
root = Tk()


class Fiche(object):
    def __init__(self, face1, face2):
        self.face1 = face1
        self.face2 = face2
        self.position = 0
        self.revoirDrapeau = True #Les cartes sont créées avec la date de la dernière révision comme date de création, mais le drapeau de révision est activé.
        self.derniereRevue = datetime.datetime.now()

class Casier(object):
    def __init__(self, nom, delaiRevue):
        self.nom = nom
        self.delaiRevue = datetime.timedelta(days=delaiRevue)


def sauvegarder():
    pickle_out = open(filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("PICKLE files","*.pickle"),("all files","*.*"))), "wb")
    pickle.dump(FICHES, pickle_out)
    pickle_out.close()

def interfaceCharger():
    #Référencement
    fenetreCharger = Toplevel()
    attention = Label(fenetreCharger, text = "Êtes-vous sûr de vouloir charger ? Cela supprimera les données actuelles.")
    boutonOui = Button(fenetreCharger, text = "Oui", command = lambda: sauvegarder(fenetreCharger))
    boutonNon = Button(fenetreCharger, text = "Non", command = lambda: fenetreCharger.destroy())

    #Matérialisation graphique
    attention.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 10)
    boutonOui.grid(row = 1, column = 0)
    boutonNon.grid(row = 1, column = 1)

def charger(fenetreCharger):
    global FICHES
    importPickle = open(filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("PICKLE files","*.pickle"),("all files","*.*"))), "rb")
    FICHES = pickle.load(importPickle)
    generateStack()
    fichesRestantes.set(len(CASIER))
    totalFiches.set(len(FICHES))

#Boutons du menu
def jeSais():
    if len(CASIER) == 0:
        return
    CASIER[0].revoirDrapeau = False
    CASIER[0].location += 1
    faceArriere.config(text = "")
    CASIER[0].derniereRevue = datetime.datetime.now()
    CASIER.remove(CASIER[0])
    fichesRestantes.set(len(CASIER))
    if len(CASIER) == 0:
        faceArriere.config(text = "N'oublie pas de sauvegarder")
        faceDevant.config(text = "Bien joué ! C'est fini pour aujourd'hui")
        return
    nouvelleInvite = CASIER[0].face1
    faceDevant.config(text = new_prompt)

def Faux():
    if len(CASIER) == 0:
        return
    CASIER[0].location = 0
    faceArriere.config(text = "")
    CASIER[0].derniereRevue = datetime.datetime.now()
    CASIER.remove(study_stack[0])
    fichesRestantes.set(len(study_stack))
    if len(CASIER) == 0:
        face2.config(text = "N'oublie pas de sauvegarder")
        face1.config(text = "Bien joué ! C'est fini pour aujourd'hui")
        return
    nouvelleInvite = CASIER[0].face1
    faceDevant.config(text = nouvelleInvite)

def Reponse():
    if len(CASIER) == 0:
        return
    nouveauTexte = CASIER[0].face2
    faceArriere.config(text = new_text)

def supprimer(fenetre, f):
    FICHES.remove(card)
    CASIER.remove(card)
    fichesRestantes.set(len(CASIER))
    totalFiches.set(len(FICHES))
    fenetre.destroy()
    face2.config(text = "")
    if len(CASIER) == 0:
        face2.config(text = "N'oublie pas de sauvegarder")
        face1.config(text = "Bien joué ! C'est fini pour aujourd'hui")
        return
    else:
        nouvelleInvite = study_stack[0].face_1
        face1.config(text = nouvelleInvite)
        return

def revoir():
    for f in FICHES:
        delaiRevue = CASIERS[f.location].delaiRevue
        derniereRevue = f.derniereRevue
        if derniereRevue + delaiRevue < datetime.datetime.now():
            f.revoirDrapeau = True

def genererCASIER():
    global CASIER
    revoir()
    for f in FICHES:
        if f.revoirDrapeau == True: #
            CASIER.append(f)
    random.shuffle(CASIER)
    if len(CASIER) == 0:
        faceAvant.config(text = "N'oublie pas de sauvegarder")
        faceArriere.config(text = "Bien joué ! C'est fini pour aujourd'hui")
        return
    else:
        nouvelleInvite = CASIER[0].face1
        faceAvant.config(text = nouvelleInvite)

def retourner():
    for f in fiches:
        face, faceRetournee = fiche.face2, fiche.face1

    faceAvant.config(text = CASIER[0].face1)

def completer(inviteFiche, reponseFiche, creation_window): #
    nouvelleFiche = Flash_Card(inviteFiche.get(), reponseFiche.get())
    FICHES.append(new_card)
    creation_window.destroy()
    totalFiches.set(len(all_cards))

def interfaceCreation():
    fenetreCrea = Toplevel()
    inviteFace1 = Label(fenetreCrea, text = "Invite ")
    inviteFace2 = Label(fenetreCrea, text = "Réponse: ")
    inviteFiche = StringVar()
    reponseFiche = StringVar()
    Face1entree = Entry(creation_window, textvariable = card_prompt)
    Face2entree = Entry(creation_window, textvariable = card_response)
    boutonCrea = Button(creation_window, text = "Finalize Card", command = lambda: finalizeCard(card_prompt, card_response, creation_window))

    inviteFace1.grid(row = 0, column = 0)
    inviteFace2.grid(row = 1, column = 0)
    entreeFace1.grid(row = 0, column = 1, columnspan = 3)
    entreeFace2.grid(row = 1, column = 1, columnspan = 3)
    boutonCrea.grid(row = 2, column = 0, columnspan = 2)

def interfaceSuppression():
    fenetreSuppression = Toplevel()
    attention = Label(deletion_window, text = "Etes-vous sûr?")
    boutonOui = Button(deletion_window, text = "Oui", command = lambda: deleteCard(fenetreSuppression, study_stack[0]))
    boutonNon = Button(deletion_window, text = "Non", command = lambda: fenetreSuppression.destroy())

    attention.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 10)
    boutonOui.grid(row = 1, column = 0)
    boutonNon.grid(row = 1, column = 1)

def importer():
    fichierTXT = open(filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("TEXT files","*.txt"),("all files","*.*"))))
    lecture = csv.reader(fichierTXT )
    donneesFichierTXT = []
    for donnee in lecteur:
        donneesFichierTXT.append(donnee)
    for fiche in donneesFichierTXT:
        FICHES.append(Fiche(card[0], card[1]))
    generateStack()
    fichesRestantes.set(len(study_stack))
    totalFiches.set(len(FICHES))

def exporter():
    export = open(filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("TEXT files","*.txt"),("all files","*.*"))), 'w', newline='')
    donneesFiche = []
    for f in FICHES:
        donneesFiche.append([fiche.face1, card.face2])
    ecriture = csv.writer(outputFile)
    for f in donneesFiche:
        ecriture.writerow(f)
    outputFile.close()

#Création des variables de base

CASIERS = []

for i in range(1, 7):
    CASIERS.append(Casier(i, (2 ** (i-1)) )) #créer des casiers à revoir tous les 2 puis 4 puis ... jours

FICHES = []
CASIER = []

try:
    imageMenu = PhotoImage(file = "index_card.gif")
except:
    imageErreurInvite = Toplevel()
    attention = Label(imageErreurInvite, text = "I couldn't find index_card.gif. Could you please find it for me?")
    attention.pack()
    imageMenu = PhotoImage(file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("GIF files","*.gif"),("all files","*.*"))))
    imageErreurInvite.destroy()

fichesRestantes = IntVar()
fichesRestantes.set(len(CASIER))
totalFiches = IntVar()
totalFiches.set(len(FICHES))

#Création des éléments du menu
ficheFace = Label(root, text = "", wraplength = 350, font = ("Arial", 24, "bold"), image = imageMenu, compound = CENTER)
ficheDerriere = Label(root, text = "", wraplength = 350, font = ("Arial", 24, "bold"), image = imageMenu, compound = CENTER)
vrai = Button(root, text = "Je sais", command = jeSais)
faux = Button(root, text = "Faux", command = Faux)
reponse = Button(root, text = "Réponse", command = Reponse)
retourne = Button(root, text = "Retourner", command = retourner)
creaFiche = Button(root, text = "Nouvelle fiche", command = interface_Creation)
resteFiches = Label(root, text = "Nombre total de fiches:")
fichesentout = Label(root, text = "Total number of cards:")
compteurFichesRestantes = Label(root, textvariable = cards_left_count)
compteurTotalFiches = Label(root, textvariable = cards_total_count)
supFiche = Button(root, text = "Supprimer cette fiche", command = Supprimer)
sauvegarde = Button(root, text = "Sauvegarder", command = sauvegarder)
boutonCharger = Button(root, text = "Charger", command = interfaceCharger)
Import = Button(root, text = "Importer", command = importer)
export = Button(root, text = "Exporter", command = exporter)

#TODO: arrange GUI elements
ficheFace.grid(row = 0, column = 0, rowspan = 6)
ficheDerriere.grid(row = 0, column = 1, rowspan = 6)
supFiche.grid(row = 4, column = 3)
creaFiche.grid(row = 4, column = 2)
cards_left.grid(row = 2, column = 2)
reponse.grid(row = 0, column = 2)
retourner.grid(row = 0, column = 3)
cards_left_counter.grid(row = 2, column = 3)
total_cards_counter.grid(row = 3, column = 3)
vrai.grid(row = 1, column = 2)
faux.grid(row = 1, column = 3)
fichesEnTout.grid(row = 3, column = 2)
sauvegarder.grid(row = 5, column = 2)
charger.grid(row = 5, column = 3)
export.grid(row = 6, column = 2)
Import.grid(row = 6, column = 3)

root.mainloop()
