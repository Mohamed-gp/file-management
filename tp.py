from os import write  # Importing the write function from the os module to write in file 

from pickle import dumps, loads  # Importing the dumps and loads functions from the pickle module dumps is used to convert a Python object into a binary string, and loads is used to convert a binary string into a Python object.

from sys import getsizeof  # Importing the getsizeof function from the sys module to get the size of an object in bytes.



global n # nombre max des enreg dans le fichier

global b # taille max enreg dans un bloc

global tnom # taille max du nom

global tprenom # taille max du prenom

global tnum # taille max du numéro d'inscription

global taffiliation  # taille max de l'affiliation

global tefface # taille de l'effacement

global tindex # taille max de table index

global fn # fichier des enregs en zone primaire

global fd # fichier des enregs en zone de débordement

global fi # fichier de la table d'index

global fr # nouveau fichier pour la reoragnisation

global buf # buffer pour un bloc



fn = 'f1.txt'       # fichier des enregs en zone primaire

fd = 'f2.txt'       # fichier des enregs en zone de débordement

fi = 'f3.txt'       # fichier de la table d'index

fr = 'f.txt'        # nouveau fichier pour la reoragnisation



b = 3 

tefface = 1

efface = '0'

tnum = 10

tnom = 20

tprenom = 20

taffiliation = 20

tmax = 100          # taille max de table index  

tindex = [(tnum,0)] * tmax # table index


telement = [(tnum,0)] # taille d'un élément de la table d'index

tbloc_index = [0,[(tnum,0)]* b]  #b = taille max enreg dans un bloc

tetud = tnum + tnom + tprenom + taffiliation + tefface  # taille d'un enreg

tnreg = tetud * '#' # enreg vide

tbloc = [0, [tnreg]*b, 0]   #b = taille max enreg dans un bloc

global blocsize # taille d'un bloc

global blocsize_index # taille d'un bloc de la table d'index

blocsize = getsizeof(dumps(tbloc))+len(tnreg)*(b-1)+(b-1) 

blocsize_index = getsizeof(dumps(tbloc_index))+len(telement)*(b-1)+(b-1) 



def resize_chaine(chaine, maxtaille):

    for i in range (len(chaine), maxtaille):

        chaine = chaine + '#' # ajouter des # à la fin de la chaine

    return chaine 



def affecte_entete(f, of, c):

    dp = of * getsizeof(dumps(0)) #general offset of 0 mean the header of file to write the number of bytes to move the file cursor. It can be a positive or negative integer. A positive value moves the cursor forward, and a negative value moves it backward.to get the size of an object in bytes.
    # we don't put 2 because we are not goint to write in the file we are just going to put taille of blocs or enregistrement ...
# file_object.seek(offset, whence)
# offset: The number of bytes to move the file cursor. It can be a positive or negative integer. A positive value moves the cursor forward, and a negative value moves it backward.
# whence: It specifies the reference point for the offset. It can take one of three values:
# 0 (default): Offset is relative to the beginning of the file.
# 1: Offset is relative to the current position of the file cursor.
# 2: Offset is relative to the end of the file.
    f.seek(dp,0)

    f.write(dumps(c))   #convertir c en binaire

    return



def ecrireBloc(f, i, bf):
# f: file ; i: index ; bf: bloc à écrire
    dp = 2 * getsizeof(dumps(0)) + i * blocsize
# 1 and 0  => for the eregistrement numbers and blocs and 2 => for the enregistrement data and we put 2 to skip the values of the first ones 
# and by doing that we can get the size of how much we will move the file cursor to write the data in the file 
    f.seek(dp,0)

    f.write(dumps(bf))  #convertir bf en binaire

    return 



def lire_bloc(f, i):

    dp = 2 * getsizeof(dumps(0)) + i * blocsize

    f.seek(dp, 0)

    buf = f.read(blocsize)

    return (loads(buf))



def lireBloc_index(f, i):

    dp = 2 * getsizeof(dumps(0)) + i * blocsize_index

    f.seek(dp, 0)

    buf = f.read(blocsize_index)

    return (loads(buf))



def ecrireBloc_index(f, i, bf):

    dp = 2 * getsizeof(dumps(0)) + i * blocsize_index

    f.seek(dp,0)

    f.write(dumps(bf))  #convertir bf en binaire

    return 



def entete(f, of):

    dp = of * getsizeof(dumps(0))

    f.seek(dp, 0)

    c = f.read(getsizeof(dumps(0)))

    return (loads(c))



def creer_fichier():

    j = 0 ; i = 0 ; n = 0

    buf_tab = [tnreg]*b

    buf_nb = 0

    nmb_enregs = 0      # nombre des éléments dans la table d'index

    try :

        f= open(fn, 'rb+')
# The code you provided is calling the `open()` function in Python. The `open()` function is used to open a file and returns a file object that can be used to read from or write to the file.

# In the code snippet you provided, the `open()` function is called with two arguments: `fn` and `'rb+'`. The first argument, `fn`, is the file name or path of the file to be opened. The second argument, `'rb+'`, specifies the mode in which the file should be opened.

# The mode `'rb+'` indicates that the file should be opened in binary mode for both reading and writing. In binary mode, the file is treated as a sequence of bytes rather than a sequence of characters. The `'r'` indicates that the file should be opened for reading, and the `'b'` indicates that it should be opened in binary mode. The `'+'` indicates that the file should be opened for both reading and writing.

# So, the code is opening the file specified by `fn` in binary mode for both reading and writing.

    except:

        print("impossible d\'ouvrir le fichier en mode d\'écriture")

    rep = 'O'

    while(rep == 'o' or rep =='O'):

        print("entrez les informations de l\'étudiant : ")

        num = input("entrez le numéro d\'inscription : ")

        nom = input("entrez le nom : ")

        prenom = input("entrez le  prenom : ")

        affiliation = input("entrez l\'affiliation : ")

        num = resize_chaine(num, tnum)

        nom = resize_chaine(nom, tnom)

        prenom = resize_chaine(prenom, tprenom) 

        affiliation = resize_chaine(affiliation, taffiliation)

        etud = num + nom + prenom + affiliation + efface

        n = n + 1   # nombre des enregs

        if(j<b):

            buf_tab[j]=etud

            buf_nb += 1

            j += 1

            n += 1

        else:

            nmb_enregs += 1

            cle = buf_tab[j-1][:tnum].replace('#','')

            tindex[i] = [(cle,i)] #####


            buf = [buf_nb, buf_tab, -1]

            ecrireBloc(f, i, buf)

            buf_tab = [tnreg]*b

            buf_nb = 1

            buf_tab[0] = etud

            n += 1

            j = 1 

            i += 1

        rep = input("avez vous un autre element a entrer (O/N) : ")

    nmb_enregs += 1

    cle = buf_tab[j-1][:tnum].replace('#','')

    tindex[i] = [(cle,i)]

    buf =[j, buf_tab, -1]

    ecrireBloc(f, i, buf)

    sauvegarde_index(tindex ,nmb_enregs)    # sauvegarde le contenu de la table d'index dans le fichier 'fi'

    print("<-- Affichage de contenu de la table d'index -->")

    for k in range (nmb_enregs):
        print(tindex[k])

    affecte_entete(f, 0, n)           

    affecte_entete(f, 1, i+1)

    f.close()

    return 



def affichage(fname):

    f = open(fname, 'rb')

    secondcar = entete(f, 1)

    print(f'votre fichier contient {secondcar} block \n')

    for i in range (0, secondcar):

        buf = lire_bloc(f, i)

        buf_nb = buf[0]

        buf_tab = buf[1]

        print(f'le contenu du block {i+1} est : \n')

        for j in range(buf_nb):

            print(afficher_enreg(buf_tab[j]))

        print('\n')

    f.close()

    return



def afficher_enreg(e):

    num = e[0:tnum].replace('#','')

    nom = e[tnum:tnum+tnom].replace('#','')

    prenom = e[tnum+tnom:tnum+tnom+tprenom].replace('#','')

    affiliation = e[tnum+tnom+tprenom:len(e)-1].replace('#','')

    efface = e[len(e)-1:]

    return (num+' '+nom+' '+prenom+' '+affiliation+' '+efface)



def reoragnisation():
    buf_tab = [tnreg]*b

    buf_nb = 0

    T = [tnreg] * tmax #table d'index i think

    f1= open(fn, 'rb')

    f2= open(fd, 'rb')

    f3= open(fr, 'wb')
# fn = 'f1.txt'       # fichier des enregs en zone primaire

# fd = 'f2.txt'       # fichier des enregs en zone de débordement

# fi = 'f3.txt'       # fichier de la table d'index

# fr = 'f.txt'        # nouveau fichier pour la reoragnisation

    nmb_enregs = 0      # nombre des éléments dans la table d'index

    i1 = 0  ; i = 0    ; j = 0

    while (i1 < entete(f1,1)):

        buf1 = lire_bloc(f1, i1)

        buf1_nb = buf1[0]

        buf1_tab = buf1[1]

        j1 = 0 

        while(j1 < buf1_nb):

            if (buf1_tab[j1][tetud-1:] == '0'):

                if (j < b):

                    buf_tab[j] = buf1_tab[j1]

                    j += 1 

                    j1 += 1

                    buf_nb += 1

                else : 

                    cle = int(buf_tab[j-1][:tnum].replace('#',''))

                    tindex[nmb_enregs] = [(cle,i)]

                    nmb_enregs += 1     # nombre des éléments dans la table d'index

                    buf = [buf_nb, buf_tab, -1]

                    ecrireBloc(f3, i, buf)

                    i += 1

                    buf_tab = [tnreg]*b

                    buf_nb = 1

                    buf_tab[0] = buf1_tab[j1]

                    j1 += 1

                    j = 1 

        if (buf1 [2] != -1):

            k = 0

            i2 = buf1 [2]

            while (i2 != -1):

                buf2 = lire_bloc(f2, i2)

                buf2_nb = buf2[0]

                buf2_tab = buf2[1]

                j2 = 0

                while (j2 < buf2_nb):

                    if(buf2_tab[j2][tetud-1:] == '0'):

                        T[k] = buf2_tab[j2]

                        k += 1

                    j2 += 1

                i2 = buf2 [2]

            # trier les k enregs dans T

            for x in range (0,k):

                for y in range (0,k):

                    cle1 = int(T[x][:tnum].replace('#',''))

                    cle2 = int(T[y][:tnum].replace('#',''))

                    if (cle1 > cle2):

                        enreg_tmp = T[x]

                        T[x] = T[y]

                        T[y] = enreg_tmp

            for j2 in range (0,k):

                if (j<b):

                    buf_tab[j] = T[j2]

                    buf_nb += 1

                    j += 1

                else: 

                    cle = int(buf_tab[j-1][:tnum].replace('#',''))

                    tindex[nmb_enregs] = [(cle,i)] 

                    buf = [buf_nb,buf_tab,-1]

                    ecrireBloc(f3, i, buf)

                    i += 1

                    buf_tab = [tnreg]*b

                    buf_nb = 1

                    buf_tab[0] = T[j2]

                    j = 1

                    nmb_enregs += 1

        cle = int(buf_tab[j-1][:tnum].replace('#',''))

        tindex[nmb_enregs] = [(cle,i)]

        buf =[buf_nb, buf_tab, -1]

        ecrireBloc(f3, i, buf)

        i1 += 1 

    affecte_entete(f3,1,i+1)

    print("<-- Affichage de contenu de la table d'index -->")

    for k in range (nmb_enregs):

        print(tindex[k])

    f1.close()

    f2.close()

    f3.close()



    return



def recherche(c):

    trouv = False   ; continu = True

    T = chargement_index()

    t_index = T[0]

    nmb_enregs = T[1]

    inf = 1 ; sup = nmb_enregs 

    while ( inf < sup and not(trouv)):

        j = (inf + sup)//2

        cle = t_index[j][0] 

        if (cle == int(c)):

            trouv = True

            k = j

        elif (int (c) > cle):

            inf = j + 1

        else :

            sup = j - 1

    if (not(trouv)):

        if (inf <= nmb_enregs):

            j = inf

        else: 

            j = nmb_enregs ; continu = False  

    k = j

    f = open (fn, 'rb')

    f2 = open (fd ,'rb')

    i = t_index[j][1] ; trouv = False ; debord = False

    buf1 = lire_bloc(f, i)

    buf1_nb = buf1[0]

    buf1_tab = buf1[1]

    cle = int(buf1_tab[buf1_nb-1][:tnum].replace('#',''))

    if (c <= cle):

        bi = 1 ; bs = buf1_nb

        while ( not(trouv) and bi <= bs):

            j = (bi + bs)//2

            if (c < int(buf1_tab[j][:tnum].replace('#',''))):   

                bs = j + 1

            elif (c < int(buf1_tab[j][:tnum].replace('#',''))):

                bi = j - 1

            else :      # c == int(buf1_tab[j][:tnum].replace('#',''))

                if (buf1_tab[j][tetud-1:] == '0'):

                    trouv = True

        if (not (trouv)):

            j = bi

    else :      # c > cle

        if (buf1[2] != -1):

            debord = True ; i = buf1[2] ; i0 = -1

            if (continu) : 

                while (not(trouv) and i!= -1):

                    buf2 = lire_bloc(f2,i)

                    buf2_nb = buf2[0]

                    buf2_tab = buf2[1]

                    j = 0

                    while (j < buf2_nb and not(trouv)):

                        if (c == int(buf2_tab[j][:tnum].replace('#','')) and buf2_tab[j][tetud-1:] == '0'):

                            trouv = True

                        else : 

                            j += 1

                    if (not(trouv)):

                        i0 = i 

                        i = buf2[2]

                if (not(trouv)):

                    i = i0

    f.close()

    f2.close()

    return [trouv,i,j,debord,k]



def requete_intervalle(A,B):

    result = recherche(A)

    trouv = result[0]

    T = [tnreg] * tmax

    k = 0

    if(trouv == False):

        print('La clé ',A," n\'existe pas dans le fichier")

    else:

        f1 = open(fn,'rb')

        f2 = open(fd,'rb')

        i1 = result[1]

        debord = result[3]

        while (i1 < entete(f1,1)):

            buf1 = lire_bloc(f1,i1)

            buf1_nb = buf1[0]

            buf1_tab = buf1[1]

            if (debord == True):

                buf2 = buf1[2]

                while (buf2 != -1):

                    buf2_nb = buf2[0]

                    buf2_tab = buf2[1]

                    j = 0

                    while (j < buf2_nb):

                        if (buf2_tab[j] >= A and buf2_tab[j] <= B):

                            T[k] = buf2_tab[j]

                            k += 1

                        else:

                            j += 1

                    buf2 = buf2[2]

            else : 

                buf1 = lire_bloc(f1,i1)

                buf1_nb = buf1[0]

                buf1_tab = buf1[1]

                j = 0

                while (j < buf1_nb):

                    if (buf1_tab[j] >= A and buf1_tab[j] <= B):

                        T[k] = buf2_tab[j]

                        k += 1

                    else:

                        j += 1

                buf2 = buf1[2]

                while (buf2 != -1):

                    buf2_nb = buf2[0]

                    buf2_tab = buf2[1]

                    j = 0

                    while (j < buf2_nb):

                        if (buf2_tab[j] >= A and buf2_tab[j] <= B):

                            T[k] = buf2_tab[j]

                            k += 1

                        else:

                            j += 1

                        buf2 = buf2[2]

            i1 += 1                

        f1.close()

        f2.close()

    return



# def insertion():



#     return



def suppression(c):

    result = recherche(c)

    trouv = result[0]

    debord = result[3]

    if(trouv == False):

        print("L'élement n\'existe pas !")

    else:

        if (debord == False):

            f1 = open(fn,'rb')

            i1 = result[1]

            buf1 = lire_bloc(f1,i1)

            buf1_nb = buf1[0]

            buf1_tab = buf1[1]

            j = 0

            while (j < buf1_nb):

                if (int(buf1_tab[j][0:tnum].replace('#','') == c)):

                    buf1_tab[j] = buf1_tab[j][:(tetud)-2] + '1'

                    buf1 = [buf1_nb, buf1_tab,buf1[2]]

                    ecrireBloc(f1,i1,buf1)

                    break

                else: 

                    j += 1

            f1.close()

        else : 

            f1 = open(fn,'rb')

            f2 = open(fd,'rb')

            i1 = result[1]

            buf1 = lire_bloc(f1,i1)

            buf2 = buf1[2]

            while (buf2 != -1):

                buf2_nb = buf2[0]

                buf2_tab = buf2[1]

                j = 0

                while (j < buf2_nb):

                    if (int(buf2_tab[j][0:tnum].replace('#','')) == c ):

                        buf2_tab[j] = buf2_tab[j][:(tetud)-2] + '1'

                        buf2 = [buf2_nb, buf2_tab,buf2[2]]

                        ecrireBloc(f1,i1,buf2) ###

                        break

                    else:

                        j += 1

                buf2 = buf2[2]

                i1 = buf2

            f1.close()

            f2.close()

    return



def chargement_index():

    f = open(fi,'rb')

    k = 0

    t_index =[(tnum,0)] * tmax

    for i in  range(0,entete(f,1)):

        buf = lireBloc_index(f,i)

        buf_nb = buf[0]

        buf_tab = buf[1]

        for j in  range(buf_nb):

            t_index[k] = buf_tab[j]

            k += 1

    f.close()

    return [t_index , k]



def sauvegarde_index(t_index ,nmb_elements):

    f = open(fi,'wb')

    i = 0

    j = 0

    buf_tab = [(tnum,0)]* b

    buf_nb = 0

    for k in range (nmb_elements):

        if (j<b):

            buf_tab[j] = t_index[k]

            buf_nb += 1

            j += 1

        else: 

            buf = [buf_nb,buf_tab]

            ecrireBloc_index(f, i, buf)

            i += 1

            buf_tab = [(tnum,0)]* b

            buf_tab[0] = t_index[k]

            buf_nb = 1

            j = 1

    buf = [buf_nb,buf_tab]

    ecrireBloc_index(f, i, buf)

    affecte_entete(f,0,nmb_elements)

    affecte_entete(f,1,i+1)

    f.close()

    return


creer_fichier()
affichage("f1.txt")
recherche(2)