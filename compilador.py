# -*- coding: utf-8 -*-
#Elaborado por Edgar Cortés Padilla
import os
import sys
import re
import collections
#Verifica que la ruta exista
try:
    os.stat("/home/edgar/NetBeansProjects/CompiladorPy/src")
    print "¡Ruta encontrada con exito!\n"
except:
    print "Ruta no encontrada"

#Lee el archivo
archivo = open("program","r")

#Caracteres válidos
caracteres = "ABCDEFGHIJKLMNÑOPQRTSUVWXYZqwertyuiopasdfghjklñmnbvcxz,;.:áéíóú1234567890() /*{ } # < > = >= <= == + -  \n \t '"

caracteres_Letras = "ABCDEFGHIJKLMNÑOPQRTSUVWXYZqwertyuiopasdfghjklmnbvcxz"

caracteres_Numeros = "0123456789"

pal_Reservadas = ['int ','String ','if','float ', 'bolean ','elif', 'else', 'and']

#token= {"/*":"abre_comentario","*/":"Cierra_comentario","int":"int","string":"String",'if':"si","{":"}","+":"+"}
token= {"#":"Comentario","int":"int","string":"String",'if':"si","{":"{","}":"}","+":"+","if":"if"}
v=["Lexema","Token","Valor","Coorrelativo","Tipo","Tamano"]

#global bloque
bloque = 0
tabla_Simbolos = {}
tabla_String = {}
tabla_Int = {}
tabla_bolean = {}


def ifbloque():
    ifbloque = {}
    return ifbloque

class Pila:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

def infixAPostfix(infixexpr):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Pila()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)



def interrumpir():
    sys.exit()
    return None
def compara_en(lexema):    
    if (lexema in token):
        #print "Lexma",lexema
        #return True
        return lexema
    else:
        return False
    
def es_token(lexema):
    if(lexema in token):
        print lexema in token
        return token
    else:
        return null

def es_reservada(palabra):
    if palabra in pal_Reservadas:
        return True
    else:
        False
def es_entero(valor):
    #caracteres_Numeros = "0123456789"
    val = True
    caracteres_Numeros = tuple("0123456789")
    for i in range(len(valor)):
        if(valor[i] not in caracteres_Numeros):                        
            return False
            val=False
            break
    return val
                                            
    
def es_var(variable):
    val = True
    caracteres_letra = tuple("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWYZ ")
    for i in range(len(variable)):
        if(variable[i] not in caracteres_letra):                        
            return False
            val=False
            break
    return val

def es_string(esString):
    val = True
    caracteres_letra = tuple("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWYZ")
    for i in range(len(esString)):
        if(esString[i] not in caracteres_letra):                        
            return False
            val=False
            break
    return val
    
def compara(lexema):
    if(es_reservada(lexema)==True):
        #print "reservada",lexema
        return "Palabra reservada"            
    elif(es_entero(lexema)==True):
        #print "es entero"
        return True
    else: return None

def bloques():
    """"""
    bloqueObj = {}        
    return bloqueObj

#Token = collections.namedtuple('Token', ['tipo', 'valor', 'linea'])
Token = collections.namedtuple('Token', ['tipo', 'valor'])

def tokenIf(s):
    reservada = ['if','THEN','ENDIF','FOR','NEXT','GOSUB','RETURN']
    especifica_token = [
        ('Numerico',  r'\d+(\.\d*)?'), # Entero o decimal
        ('asignacion',  r'='),         # Operador de asignacion
        ('fin',     r';'),             # id terminador
        ('id',      r'[A-Za-z]+'),     # Identificador
        ('op',      r'[+*\/\-]'),      # Operador aritmetico
        ('nlinea', r'\n'),             # Linea final
        ('salto',    r'[ \t]'),        # saltar espacios y tabulacion
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % par for par in especifica_token)
    obtiene_token = re.compile(tok_regex).match
    linea = 1
    pos = 0
    mo = obtiene_token(s)
    while mo is not None:
        tipo = mo.lastgroup
        if tipo == 'nlinea':
            #line_start = pos
            linea += 1
        elif tipo != 'salto':
            valor = mo.group(tipo)
            if tipo == 'id' and valor in reservada:
                tipo = valor
            #yield Token(typ, val, line, mo.start()-line_start)
            yield Token(tipo, valor)
        pos = mo.end()
        mo = obtiene_token(s, pos)
    if pos != len(s):
        raise RuntimeError('Caracter inesperado %r en la linea %d' %(s[pos], linea))

vec_caract=[]
Valido = True

#Inicia llenado de vector
numLinea = 0
my_str=""
while True:
    linea=archivo.readline()
    for i in linea:
        if(i not in caracteres):
            print "El caracter "+ i + " ,no es valido."
            sys.exit()
            Valido = False
            False                    
        if(i!='#'and i!='\n' and (i in caracteres)):                
            vec_caract.append(i)
        
        else:
            if(i=='\n' or i=='#'):
                numLinea+=1
            break    
    if not linea:break


lexema = ""
aux = ""
vect_dos = []
ant = 0
sig = 0
nvector = len(vec_caract)

#Analisis del vector
for i in range(len(vec_caract)):   
    if(vec_caract[i]=="{"):
        my_str+='a'
    if(vec_caract[i] == "}"):                        
        my_str+='b'
    if (lexema!=" "):              
        lexema += vec_caract[i]
        
    if(vec_caract[i]=='{'):                
        lexema=lexema[:-1]
        vect_dos.append(lexema)
        compara(lexema)
        vect_dos.append('{')        
        lexema = ""
                                                                        
    if(vec_caract[i]=='}'):
        lexema=lexema[:-1]
        compara(lexema)
        vect_dos.append(lexema)
        vect_dos.append('}')
        lexema += vec_caract[i]        
        lexema = ""
    
    if(vec_caract[i]=='('):                
        lexema=lexema[:-1]
        vect_dos.append(lexema)
        compara(lexema)
        vect_dos.append('(')        
        lexema = ""
    
    if(vec_caract[i]==')'):
        lexema=lexema[:-1]
        vect_dos.append(lexema)
        compara(lexema)
        vect_dos.append(')')
        lexema = ""
        
    if(vec_caract[i]=='>'):                
        lexema=lexema[:-1]
        vect_dos.append(lexema)
        compara(lexema)
        vect_dos.append('>')        
        lexema = ""    
    
    if(vec_caract[i]=='<'):                
        lexema=lexema[:-1]
        vect_dos.append(lexema)
        compara(lexema)
        vect_dos.append('<')        
        lexema = ""    
        
    """if(vec_caract[nvector-1]!='}'):        
        print "Parentesis } perdido"        
        break"""
    
    if(vec_caract[i]==';'):
        lexema=lexema[:-1]
        compara(lexema)
        vect_dos.append(lexema)
        vect_dos.append(';')
        lexema += vec_caract[i]        
        lexema = ""
    
    if(vec_caract[i]=='='):
        lexema=lexema[:-1]
        compara(lexema)
        vect_dos.append(lexema)
        vect_dos.append('=')
        lexema += vec_caract[i]        
        lexema = ""
        
        
    if(vec_caract[i]=='+'):
        lexema=lexema[:-1]
        compara(lexema)
        vect_dos.append(lexema)
        vect_dos.append('+')
        lexema += vec_caract[i]        
        lexema = ""
    
    if(vec_caract[i]=='-'):
        lexema=lexema[:-1]
        compara(lexema)
        vect_dos.append(lexema)
        vect_dos.append('-')
        lexema += vec_caract[i]        
        lexema = ""
    
        
    
    if(vec_caract[i] == ' '):        
        compara(lexema)
        #print "lexema",i,lexema        
        #if(lexema[:-1]!= " "):
        vect_dos.append(lexema)
        lexema = ""

aux = []        
for i in range(len(vect_dos)):    
    if(vect_dos[i]!=" " and vect_dos[i]!= ""):
        aux.append(vect_dos[i])
vect_dos = aux

def parentesisPar(string):
    for i,char in enumerate(string):
        if char != string[-i-1]:
            return False
    return True

#print my_str

def ispalindrome(a):
  a1 = [x.upper() for x in a if x.isalpha()]
  for ix in xrange(len(a1)):  # or xrange((len(a1)+1)/2) to check each char once
     if a1[ix] != a1[-ix-1]:
       return False
  return True



print  vect_dos
    
#v=["Lexema","Token","Valor","Coorrelativo","Tipo","Tamano"]
##int
prlex = ""
prnum = 0
aux=""
id = ""

##String
prlexS = ""
prnumS = 0

##Bolean
prlexB = ""
prnumB = 0

##if(){}
prlexIf = ""
prnumIf = 0

#print "vect_dos >> ", vect_dos

for i in range(len(vect_dos)):
    if(i==0):
        tabla_Simbolos[vect_dos[i]] = 'id'
    if(i>0):
        #Entero
        if(es_reservada(vect_dos[i])==True and vect_dos[i] == 'int '):              
            i+=1
            if(es_var(vect_dos[i])==True):                
                prlex += str(prnum)
                prnum += 1
                id = str(vect_dos[i-1])+str(prnum)
                #print id
                #if(prlex in tabla_Simbolos):                       
                if(vect_dos[i] in tabla_Simbolos):
                    print "Ya existe el identificador",str(vect_dos[i])
                    sys.exit()
                else:
                    tabla_Simbolos[vect_dos[i]] = id                                                                                                                                            
            i+=1
            if(vect_dos[i]!= ';'):
                print "Excepcion!: Se esperaba el simbolo---> ;"
                sys.exit()
            
                
        #String
        if(es_reservada(vect_dos[i])==True and vect_dos[i] == 'String '):              
            i+=1             
            aux = str(vect_dos[i])
            aux = aux[:-1]
            if(vect_dos[i]in tabla_Simbolos or aux in tabla_Simbolos):
                print "Excepcion, ya existe el identificador", aux
                sys.exit()
            #print vect_dos[i]
            #auxp = vect_dos[i]
            #auxq = len(vect_dos[i])-1
            #if(auxp[0]!='\''and auxp[auxq]!='\''):
            #    print "¡Excepción!, Se esperaba un \'"
            if(es_var(vect_dos[i])==True):                                
                prlexS += str(prnumS)
                prnumS += 1
                id = str(vect_dos[i-1])+str(prnumS)
                i+=1                
                #print id,"anterior"
                
                #if(vect_dos[i] in tabla_Simbolos[id]==True):
                 #   print "nanai"
                #if(prlex in tabla_Simbolos):
                
                #
                if(vect_dos[i]=='='):                
                    i+=1
                    #print vect_dos[i]
                    auxp = vect_dos[i]                    
                    auxq = len(vect_dos[i])-1                    
                    if(auxp[0]!='\''or  auxp[auxq]!='\''):
                        print "¡Excepción!, Se esperaba un \'"
                        sys.exit()                                        
                    #Validacion comilla
                    if(type(vect_dos[i]=='str')):                        
                        tabla_Simbolos[vect_dos[i-2]] = id
                        tabla_String[vect_dos[i-2]] = vect_dos[i]
                    elif(type(vect_dos[i]!='str')):
                        sys.exit()
                elif(vect_dos[i]!='='):
                    print "Excepcion!: Se esperaba el simbolo---> ="
                    sys.exit()
                i+=1
                if(vect_dos[i]!= ';'):
                    print "Excepcion!: Se esperaba el simbolo---> ;"
                    sys.exit()
        #Bolean
        if(es_reservada(vect_dos[i])==True and vect_dos[i] == 'bolean '):
            i+=1
            aux = str(vect_dos[i])
            aux = aux[:-1]
            if(vect_dos[i]in tabla_Simbolos or aux in tabla_Simbolos):
                print "Excepcion, ya existe el identificador",vect_dos[i]
                sys.exit()
            if(es_var(vect_dos[i])==True):                                
                prlexB += str(prnumB)
                prnumB += 1
                id = str(vect_dos[i-1])+str(prnumB)
                i+=1                
                #print id,"anterior"
                
                #if(vect_dos[i] in tabla_Simbolos[id]==True):
                 #   print "nanai"
                #if(prlex in tabla_Simbolos):
                if(vect_dos[i]=='='):
                    i+=1
                    if(type(vect_dos[i]=='str')):                
                        tabla_Simbolos[vect_dos[i-2]] = id
                        tabla_bolean[vect_dos[i-2]] = vect_dos[i]
                elif(vect_dos[i]!='='):
                    print "Excepcion!: Se esperaba el simbolo---> ="
                    sys.exit()
                i+=1
                if(vect_dos[i]!= ';'):
                    print "Excepcion!: Se esperaba el simbolo---> ;"
                    sys.exit()
        
        #If
        if(es_reservada(vect_dos[i])==True and vect_dos[i] == 'if'):
            #i+=1             
            aux = str(vect_dos[i])
            aux = aux[:-1]            
            if(es_reservada(vect_dos[i])==True):
                prlexIf += str(prnumS)
                prnumIf += 1
                id = str(vect_dos[i-1])+str(prnumIf)
                i+=1                
                if(vect_dos[i]=='('):
                    i+=1
                    #print vect_dos[i]
                    if(vect_dos[i] not in tabla_Int): # or vect_dos[i] not in tabla_String):
                        print "El valor \"",vect_dos[i],"\" no está declarado"
                        sys.exit()
                    i+=1                    
                    if(vect_dos[i] not in caracteres):
                        sys.exit()
                    i+=1
                    if(vect_dos[i] not in tabla_Int): # or vect_dos[i] not in tabla_String):
                        print "El valor \"",vect_dos[i],"\" no está declarado"
                        sys.exit()
                    i+=1                                        
                i+=1                
                if(vect_dos[i]==')'):
                    i+=1
                if(vect_dos[i]!='{'):
                    print "Se esperaba un {"
                    sys.exit()                    
                if(vect_dos[i]=='{'):
                    i+=1
                    bloq ="bloque"
                    bloq+=str(bloque)
                    bloque+=1
                    bloq = ifbloque()                        
            while(vect_dos[i]!='}'):                            
                if(vect_dos[i]=="{"):
                    break
                qwert = "bloque_If"
                id = qwert+str(bloque)
                bloq[id] = vect_dos[i]
                print bloq
                i+=1
                if(vect_dos[i]=='}'):    
                    i+=1
                    break
            i+=1 
        #ELSE    
        if(es_reservada(vect_dos[i])==True and vect_dos[i] == 'else'):
            print "\nCiclo ELSE"            
            i+=1            
            if(vect_dos[i]!='{'):
                print "EXcepcion"
            i+=1
            if(es_reservada(vect_dos[i])==True and vect_dos[i] == 'if'):
                #i+=1             
                aux = str(vect_dos[i])
                aux = aux[:-1]            
                if(es_reservada(vect_dos[i])==True):
                    prlexIf += str(prnumS)
                    prnumIf += 1
                    id = str(vect_dos[i-1])+str(prnumIf)
                    i+=1                
                    if(vect_dos[i]=='('):
                        i+=1
                        #print vect_dos[i]
                        if(vect_dos[i] not in tabla_Int): # or vect_dos[i] not in tabla_String):
                            print "El valor \"",vect_dos[i],"\" no está declarado"
                            sys.exit()
                        i+=1                    
                        if(vect_dos[i] not in caracteres):
                            sys.exit()
                        i+=1
                        if(vect_dos[i] not in tabla_Int): # or vect_dos[i] not in tabla_String):
                            print "El valor \"",vect_dos[i],"\" no está declarado"
                            sys.exit()                                
                    i+=1                
                    if(vect_dos[i]==')'):
                        i+=1
                    if(vect_dos[i]!='{'):
                        print "Se esperaba un {"
                        sys.exit()                    
                    if(vect_dos[i]=='{'):
                        i+=1
                        bloq ="bloque"
                        bloq+=str(bloque)
                        bloque+=1
                        bloq = ifbloque()                        
                while(vect_dos[i]!='}'):                            
                    if(vect_dos[i]=="{"):
                        break
                    qwert = "bloque_If"
                    id = qwert+str(bloque)
                    bloq[id] = vect_dos[i]
                    print bloq
                    i+=1
                    if(vect_dos[i]=='}'):    
                        i+=1
                        break
                i+=1                                
            i+=1                
            if(vect_dos[i]=='{'):                    
                print "\nCiclo Else"
                i+=1
                tokeninf=""
                while(vect_dos[i]!='}'):                    
                #    print vect_dos[i]
                    tokeninf+=str(vect_dos[i])
                    i+=1
                print tokeninf
                #print(infixAPostfix(tokeninf))
                auxad=""
                for i in range((len(tokeninf))):                        
                    x = " "
                    auxad+=x
                    auxad+=tokeninf[i]
                    #print auxad                    
                print(infixAPostfix("( A + B ) * ( C + D ) / 2"))
                
            break
            i+=1                
                    #i+=1                    
                    #ifToken=""
                    #while(vect_dos[i]!='}'):                        
                     #   ifToken+=vect_dos[i]
                      #  i+=1
                    ##Sentencia IF
                    #print "Operaciones del ciclo  IF\n"
                    
                    
                    #for token in tokenIf(ifToken):
                     #   print(token)
                    
                    #print ifToken 
                    #auxad=""
                    #for i in range((len(ifToken))):                        
                        #auxad+=ifToken[i]
                       # print auxad
                      #  x = " "
                     #   auxad+=x
                    #print(infixAPostfix(auxad))

#                    while True:
 #                       if(vect_dos[i]!=')'):
  #                          i+=1
   #                     else: break
                        

    #ASIGNA ENTEROS
    if(vect_dos[i] in tabla_Simbolos):    
        i+=1            
        if(vect_dos[i]== '='):
            i+=1
            if(es_entero(vect_dos[i])==True):                
                auxP = tabla_Simbolos.get(vect_dos[i-2])                
                if(re.match('int .',str(auxP))):                    
                    tabla_Int[vect_dos[i-2]] = vect_dos[i]                        

    
    
print "\nTokens ", tabla_Simbolos
print "String ", tabla_String
print "Bolean ", tabla_bolean
print "Enteros", tabla_Int





#Elaborado por Edgar Cortés Padilla
