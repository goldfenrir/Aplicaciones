import unicodedata
import re
from nltk.stem.snowball import SnowballStemmer
from textblob import TextBlob
from textblob import Word
from nltk.corpus import stopwords

import codecs
import math
import string
#definiciones
def noComillas(campo):    
    for c in campo:
        if (c=="\""):
            return False
    return True
def quitarComilla(campo):  #quitar comas dentro de un campo con comillas
    #if (campo==""): campo
    if (noComillas(campo)):
        return campo
    flagComilla=0
    campoS=campo.strip() #campo sin espacios
    if (campoS[0]=="\"" and campoS[len(campoS)-1]=="\""):
        campoS=campoS[1:-1]
        
        
        wordList = re.sub("[^\w]", " ",  campoS).split()
        campoS=""
        for word in wordList:
            if (existeNumero(word)==False):
                campoS+=word
                campoS+=" "
                
        campoS = campoS.translate(None, ',\"')        
        return campoS
    else:
        return -1
    return -1
def validarComillas(linea):
    nComillas=0
    comillasPares=True
   
    #omillasValidas=True
    for c in linea:
        if (c=="\""):
            nComillas+=1
        
    if ((nComillas%2)==0): comillasPares=True
    else: comillasPares=False
    return  (comillasPares)
    
def quitarComillasPuestoClase(linea):   
    nLinea=""
    clase=""
    puesto=""
    if (linea[0]=="\""):
        clase=linea[1]  
        linea=linea[4:]
    else:
        clase=linea[0]
        linea=linea[2:]
        
    if (linea[0]=="\""):
        puesto=linea[1:linea.find("\"")]  
        linea=linea[linea.find(",")+1:]
    else:
        puesto=linea[0:linea.find(",")]
        linea=linea[linea.find(",")+1:]
        
    nLinea+=clase
    nLinea+=","
    nLinea+=puesto   
    nLinea+=","
    nLinea+=linea
    return nLinea
def stopWordStem(linea):
    blob=TextBlob(linea.decode('utf-8'))
    words=blob.words
    comentarios=""
    stemmer = SnowballStemmer("spanish")
    primero=True
    for word in words:    
        if word not in (stopwords.words('spanish')):#Elimnimar Stop words
            w=Word(word)        
            if (primero):
                comentarios+=(stemmer.stem(w.lower()))
                primero=False
            else:
                comentarios+=" "
                comentarios+=(stemmer.stem(w.lower()))
            
    
    
    return comentarios
    
    
def quitarDobleComa(linea):
    return linea.replace(",,", ",")  

def existeNumero(lin):
    for a in lin:
        if (a.isdigit()):
            return True;
        
    return False
def  limpiarLinea(linea,numeroCampos,lineasIngles): #se limpia una linea
    linea=quitarDobleComa(linea)
    #print linea
    linea=quitar_campo1_2(linea,lineasIngles)
    if linea==-1: # si contiene ingles se elimina
        return -1
    
    #print linea
    linea=quitarComillasPuestoClase(linea)
    #print linea
    nuevaLinea=""
    nCampos=0
    primero=True
    
    linea=linea.strip() #campo sin espacios
    
    
   
    linea=strip_accents(linea) #linea = linea sin acentos
  
    
    linea = quitar_puntuacion(linea)
    
    linea=linea.translate(None, '\n')
    
    if(validarComillas(linea)==False):
        
        #print "cayo validarComillas"
        return -1
    i=0
    f=0
    #print len(linea)
    while (f<len(linea)):
        
        
        #print f
        if (linea[f]=="," and ((nCampos==2 and 
        (noComillas(linea[f:] or f+2==len(linea)) )) or linea[f+1]=="\"" or nCampos<2)):
            nCampos+=1
            campo=linea[i:f]
            #print campo
            
            if (quitarComilla(campo)!=-1):
                campo=quitarComilla(campo)
                campo=stopWordStem(campo)
            else:
                #print "callo"
                return -1
            if (primero==False):
                nuevaLinea+=","
                nuevaLinea+=campo
            else:
                nuevaLinea+=campo
                primero=False
            #print campo
            #print nuevaLinea
            i=f+1
        f+=1
    
    f+=1
    nCampos+=1
    campo=linea[i:f]
    #print campo
    if (quitarComilla(campo)!=-1):
        campo=quitarComilla(campo)
        campo=stopWordStem(campo)
    else:
        #print "cayo ultima validacion"
        return -1
    nuevaLinea+=","
    nuevaLinea+=campo
    #print campo
    #print nuevaLinea
    if (nCampos==numeroCampos):
        return nuevaLinea
    else:
        return -1
    return nuevaLinea


def arreglo_ofertas(archLectura):
	lineas = archLectura.readlines()
	nuevaLinea = ""
	nuevaLinea += lineas[0]
	arregloLineas = []
	count = 1
	while count < len(lineas):
		puesto = lineas[count].split(',')
		#if puesto[0].isdigit() and puesto[1].isdigit() and puesto[2].isdigit():
		if puesto[0].isdigit():
			arregloLineas.append(nuevaLinea)
			nuevaLinea = ""
		nuevaLinea += lineas[count]
		count += 1
	arregloLineas.append(nuevaLinea)
	return arregloLineas

def quitar_campo1_2(oferta,lineasIngles):
   
    linea = ""
    linea = oferta[1+oferta.find(','):]
 
    clase = ""
    clase = linea[:linea.find(',')]
    

    linea = linea[1+linea.find(','):]
    
    id= ""
    id = linea[:linea.find(',')]
    #print id
    
    if id in lineasIngles:
        print id
        return -1;
    linea = linea[1+linea.find(','):]

    nLinea = ""
    nLinea += clase
    nLinea +=","
    nLinea += linea
    return nLinea
#Lectura y limpieza
#Quitamos todos los caracteres de puntuacion

def strip_accents(s): 
    res = s.decode('utf-8')
    linea = ''.join(c for c in unicodedata.normalize('NFD', res) 
        if unicodedata.category(c) != 'Mn')
    nlinea = linea.encode('ascii', 'ignore')
    nlinea = str(nlinea)
    return nlinea

#fin lectura y limpieza
def imprimir_archivo(lineas, nombreArch):
    archEscritura=codecs.open(nombreArch, "w", "utf-8")
    #with codecs.open("test_output", "w", "utf-8") as archEscritura:
    #archEscritura = open(nombreArch, "w", "utf-8")
    for lin in lineas:
            archEscritura.write(lin.decode("utf-8"))
            archEscritura.write("\n")
    archEscritura.closed
        
def quitar_puntuacion(linea):
    
    exclude1 = set(string.punctuation)
    exclude = set()
    while len(exclude1) > 0:
        i = exclude1.pop()
        if not i == ',':
            if not i == '"':
                exclude.add(i)
    word = ''.join(ch for ch in linea if ch not in exclude)
    return word


#print limpiarLinea("1,1,1231,iop,\"d,e,s,c\",\"re,q,u,i\"",4)


archLectura = open("TA_Registros_etiquetados.csv")
lineas = arreglo_ofertas(archLectura)

archIngles=open("TA_JobID_English.txt")
lineasIngles=archIngles.readlines()

lineasIngles1=[]
for lin in lineasIngles:
    lineasIngles1.append(lin.translate(None,'\n'))
print lineasIngles1   
#print lineas[0]
#print quitar_campo1_2(lineas[0])
#
#print limpiarLinea(lineas[155],4)
#print quitarComillasPuestoClase
#print strip_accents("aa")

contador=0
contadorEliminados=0
arregloLineas = []
arregloLineasEliminadas = []
for linea in lineas:
    
    if (limpiarLinea(linea,4,lineasIngles1)!=-1):
        arregloLineas.append(limpiarLinea(linea,4,lineasIngles1))
        contador+=1
    else:
        
        arregloLineasEliminadas.append(linea)
        contadorEliminados+=1
        print "Linea eliminada "
        

print contador
print contadorEliminados

imprimir_archivo(arregloLineas,"limpio.csv")
imprimir_archivo(arregloLineasEliminadas,"eliminados.csv")
#Genera el nuevo archivo
archLectura= open('limpio.csv', 'r')
lineas=archLectura.readlines()
i=0
lineaTotal=""
primerCampo=True
clases=[]
for linea in lineas:
    
    claseAux= linea[:linea.find(',')]
   
    linea= linea[linea.find(',')+1:]
    if (primerCampo):
        primerCampo=False
        
    else:        
        lineaTotal+=linea
    clases.append("\" Tipo"+claseAux+"\"")
lineaTotal=lineaTotal.replace(',',' ')

print clases
blob=TextBlob(lineaTotal.decode('utf-8'))
words=blob.words
dict = dict.fromkeys(words)
dictList=sorted(dict.keys())
bag=[]
for word in dict:
    bag.append(word)
    

#seq = ('name', 'age', 'sex','name')

archLectura.seek(0)
lineas=archLectura.readlines()
N=3748
IDF=[] # hallamos IDF por cada palabra
for word in dict:
    DF=0
    for linea in lineas:
        nlinea = linea.decode('utf-8')
        if word in nlinea:
            DF+=1      
    IDF.append(math.log(N/DF))
 

archLectura.seek(0)
archVect= open('Vectores.txt', 'w')
archValues=open('valuesTodo.csv','w')
lineas=archLectura.readlines()
n=0
for word in dict:
    if (n==0):
        archValues.write(word)
    else:
        archValues.write(','+word)
    n+=1
primer =True
archValues.write(',Clase')
archValues.write("\n")    
count=0
for linea in lineas:
    nlinea = linea.decode('utf-8')
    oracion= TextBlob(nlinea)
    
    
    #print clases[count]
    for word in dict:      #tf=oracion.word_counts[word]
        dict[word]=oracion.word_counts[word]*IDF[count] # multiplica el tf*idf
        
        if (primer):
            primer=False
            archValues.write(str(dict[word]))
        else:
            archValues.write(','+str(dict[word]))
            
    #archValues.write(str(dict.values()))
    #print count
    
    primer=True
    archValues.write(','+clases[count]+"\n")
    count += 1
print n
print "FIN"
archVect.write(str(dict.keys()))
   
archVect.close()
archLectura.close()


"""
#print limpiarLinea("1,iop,\"d,e,s,c\",\"re,q,u,i\"",4)"""
