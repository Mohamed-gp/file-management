from pickle import dumps, loads
from sys import getsizeof
global b #Nombre maximal d'enregistrement dans le buffer ou le bloc
global tnom #La taille du champ Nom
global tprénom #La taille du champ Prénom
global tmat #La taille du champ Matricule
global tniveau #La taille du champ Niveau
global tsupprimer #La taille du champ indiquant l'effacement logique de l'enregistrement
global bufsize #La taille dubfuffer ou du bloc
b = 5
tmat = 20
tnom = 20
tprenom = 20
tniveau = 10
tsupprimer = 1
etud1 = '#' * (tmat + tnom + tprenom + tniveau + tsupprimer)
buf = [0, [etud1] * b] #Utilisé pour le calcul de la taille du buffer
bufsize = getsizeof(dumps(buf)) + (len(etud1) + 1) *  (b - 1) #Formule de calcul de la taille du buffer
print(bufsize)
def resize_chaine(chaine, maxtaille):
    """Fonction de redémentionnement des champs de l'enregistrement afin de ne pas avoir des problèmes de taille"""
    for i in range(len(chaine),maxtaille):
          chaine = chaine + '#'
    return chaine
def Creer_fichier(fn):
    """ Procédure de création d'un fichier binaire"""
    j = 0 #Parcours des enregistrement
    i = 0 #Parcours des blocs
    n = 0 #Nombre des enregistrements
    #initialisation du buffer :
    buf_tab = [etud1]*b
    buf_nb = 0 #buf_nb représente le nombre d'enregistrements dans le bloc
    try:
        f = open(fn, "wb")
    except:
        print("Creation du fichier est impossible ")
    rep = 'O'
    while (rep.upper() == 'O'):
        #Lecture des information :
        Nom = input('Donner le nom : \n')
        Prenom = input('Donner le prenom : \n')
        Matricule = input('Donner le matricule : \n')
        Niveau = input('Donner le niveau : \n')
        #Redémentionnement des informations :
        Matricule = resize_chaine(Matricule, tmat)
        Nom = resize_chaine(Nom, tnom)
        Prenom = resize_chaine(Prenom, tprenom)
        Niveau = resize_chaine(Niveau, tniveau)
        #Enregistrement sous-forme d'une chaine de caractères
        Etud = Matricule + Nom + Prenom + Niveau + '0' #'0' pour non-supprimé
        n += 1 #Augmenter le nombre d'enregistrement
        if(j < b): #bloc non-plain
            buf_tab[j] = Etud
            buf_nb += 1 #Augmenter le nombre d'enregistrement
            j += 1
        else: #bloc plain
            buf=[buf_nb, buf_tab]
            ecrireBloc(f, i, buf) #Ecrire le bloc dans le fichier
            buf_tab=[etud1] * b #Créer un nouveau bloc
            #Mettre dans le bloc le nouveau enregistrement
            buf_nb = 1
            buf_tab[0] = Etud
            j = 1
            i += 1 #Augmenter le nombre de blocs
        rep = input("Un autre étudiant à ajouter O/N ? ")
    buf=[j,buf_tab]
    ecrireBloc(f, i, buf) #Ecrire le dernier bloc
    affecter_entete(f, 0, n) #Ecrire la première caractéristique
    affecter_entete(f, 1, i+1) #Ecrire la deuxième caractéristique
    f.close()

def affecter_entete(f, offset, val):
    """Fonction pour écrire les caractéristiques dans le fichier selon 'offset'"""
    Adr = offset * getsizeof(dumps(0))
    f.seek(Adr, 0)
    f.write(dumps(val))
    return

def ecrireBloc(f, ind, buff):
    """Procédure pour écrire le bloc dans le fichier selon 'ind'"""
    Adr = 2 * getsizeof(dumps(0)) + ind * bufsize
    f.seek(Adr, 0)
    f.write(dumps(buff))
    return

def lirebloc(f, ind) :
    """Fonction pour lire le bloc du fichier selon 'ind'"""
    Adr = 2 * getsizeof(dumps(0)) + ind * bufsize
    f.seek(Adr, 0)
    buf = f.read(bufsize)
    return (loads(buf))

def entete(f, ind):
    """fonction de récupération des caractéristiques selon 'ind'"""
    Adr = ind * getsizeof(dumps(0))
    f.seek(Adr, 0)
    tete = f.read(getsizeof(dumps(0)))
    return loads(tete)

def afficher_fichier():
    """Procédure d'affichage du fichier"""
    fn = input('Entrer le nom du fichier à afficher: ')
    f = open(fn,'rb')
    secondcar = entete(f,1) #Récupération de nombre des blocs
    print(f'votre fichier contient {secondcar} block \n')
    for i in range (0,secondcar):
        buf = lirebloc(f,i)
        buf_nb = buf[0]
        buf_tab = buf[1]
        print(f'Le contenu du block {i+1} est:\n' )
        for j in range(buf_nb):
            if (buf_tab[i][-1] != '1'): #Ne pas affichier les enregistrements supprimés logiquement
                print(afficher_enreg(buf_tab[j]))
        print('\n')
    f.close()
    return

def afficher_enreg(e):
    """Fonction de mise en forme des enregistrements
    Retourne une chaine de caractères sans le '#'"""
    Matricule = e[0:tmat].replace('#',' ')
    Nom = e[tmat:tmat+tnom].replace('#',' ')
    Prenom = e[tmat+tnom:tmat+tnom+tprenom].replace('#',' ')
    Niveau = e[tmat+tnom+tprenom:len(e) - 1].replace('#',' ')
    Supprimer = e[-1]
    return Matricule + ' ' + Nom + ' ' + Prenom + ' ' + Niveau+ ' ' + Supprimer

def recherche():
    nom_fichier = input("entrer le nom du fichier \n")
    f = open(nom_fichier, 'rb')
    matricule = input("entrer le matricule pour la recherche \n")
    nb_bloc = entete(f, 1)
    for i in range(0, nb_bloc):
        buf = lirebloc(f, i)
        nb_enreg = buf[0]
        buf_tab = buf[1]
        for j in range(0, nb_enreg):
            enreg_mat = buf_tab[j][:tmat].replace('#', ' ').strip()
            if matricule == enreg_mat:
                i = str(i + 1)
                j = str(j + 1)
                print("Matricule existe")
                print("La position du bloc est " + i)
                print("La position dans le bloc est " + j)
                f.close()
                return
    print("Matricule n'existe pas ")
    f.close()
    return


def suppression_physique():
    nom_fichier = input("entrer le nom du fichier pour la suppression \n")
    f = open(nom_fichier,"rb+")
    matricule = input("entrer le matricule pour supprimer \n")
    nb_bloc = entete(f, 1)
    dernier_buf = lirebloc(f,nb_bloc-1)
    dernier_buf_tab = dernier_buf[1]
    e = dernier_buf_tab[dernier_buf[0]-1]
    for i in range(0, nb_bloc):
        buf = lirebloc(f, i)
        nb_enreg = buf[0]
        buf_tab = buf[1]
        for j in range(nb_enreg):
            enreg_mat = buf_tab[j][:tmat].replace('#', ' ').strip()
            if matricule == enreg_mat:
                buf_tab[j]= e
                affecter_entete(f,0,entete(f,0)-1)
                if dernier_buf[0] == 1 :
                    affecter_entete(f,1,nb_bloc-1)
                else :
                    if nb_bloc != 1 :
                        buf = [nb_enreg, buf_tab]
                        dernier_buf = [dernier_buf[0]-1, dernier_buf_tab]
                        ecrireBloc(f, nb_bloc-1,dernier_buf)
                        ecrireBloc(f, i,buf)
                        f.close()
                    else :
                        buf = [nb_enreg - 1,buf_tab]
                        ecrireBloc(f,i,buf)
                        f.close()
                    return
    print("le matricule n'existe pas")
    f.close()
    return
def insertion():
    nom_fichier = input("entrez le nom de fichier pour l'insertion \n")
    f = open(nom_fichier, "rb+")
    Nom = input('Donner le nom : \n')
    Prenom = input('Donner le prenom : \n')
    Matricule = input('Donner le matricule : \n')
    Niveau = input('Donner le niveau : \n')
    Matricule = resize_chaine(Matricule, tmat)
    Nom = resize_chaine(Nom, tnom)
    Prenom = resize_chaine(Prenom, tprenom)
    Niveau = resize_chaine(Niveau, tniveau)
    Etud = Matricule + Nom + Prenom + Niveau + '0' 
    nb_bloc = entete(f , 1) 
    buf = lirebloc(f, nb_bloc - 1)
    nb_enreg = buf[0]
    buf_tab = buf[1]
    if nb_enreg < b:
        buf_tab[nb_enreg] = Etud
        buf = [nb_enreg+1 , buf_tab]
        ecrireBloc(f  , nb_bloc - 1 , buf)
    else:
        buf_tab=[etud1] * b 
        buf_nb = 1
        buf_tab[0] = Etud
        buf = [buf_nb , buf_tab]
        affecter_entete(f , 1 , nb_bloc + 1 )
        ecrireBloc(f , nb_bloc  , buf)
    affecter_entete(f , 0 , entete(f , 0) + 1)

    f.close()
    return 


if __name__ == "__main__": ## bdlou les nom de variables +=+
    achraf =  input("Donner le nom du fichier : ")
    Creer_fichier(achraf)
    recherche()
    suppression_physique()
    afficher_fichier()
    insertion()
    afficher_fichier()