print "Este programa analiza la equivalencia entre dos formulas logicas."
print "Las cadenas a ingresar deben ser las formulas en notacion polaca inversa."
print "Las unicas letras proposicionales permitidas son: p, q, r\n \
Claves de escritura para los conectivos:\n \
La negacion se escribe: -\n \
La Or se escribe: O\n \
El AND se escribe: Y\n \
La implicacion se escribe: >\n"
#############################################################
#Creador de arboles
# Definimos la clase de objetos Tree para las formulas
class Tree(object):
    def __init__(self,l,iz,der):
        self.left = iz
        self.right = der
        self.label = l
# Define la funcion de imprimir rotulos Inorder(f)
def Inorder(f):
    # Determina si F es una hoja
    if f.right == None:
#       print "Es una hoja!"
       print f.label,
    elif f.label == '-':
        print f.label,
        Inorder(f.right)
    else:
        print "(",
        Inorder(f.left)
        print f.label,
        Inorder(f.right)
        print ")",

def poltotree():
	# Solicitamos una cadena
	f = raw_input('Ingrese una cadena: ') or 'rqpO>' # Cadena por defecto

	print "Cadena ingresada " + f

	cadena = list(f)

	print cadena


	letrasProposicionales = ['p', 'q', 'r', 's', 't', 'v']
	conectivos = ['O', 'Y', '>']

	pila = [] # inicializamos la pila

	for c in cadena:
	    if c in letrasProposicionales:
	        pila.append(Tree(c, None, None))
	    elif c == '-':
	        aux = Tree(c, None, pila[-1])
	        del pila[-1]
	        pila.append(aux)
	    elif c in conectivos:
	        aux = Tree(c, pila[-1], pila[-2])
	        del pila[-1]
	        del pila[-1]
	        pila.append(aux)

	formula = pila[-1]

	print "La formula ",
	Inorder(formula)
	print " fue creada como un objeto!\n"
	return formula

############################################################
#Posibles interpretaciones
PropoLethers = ['p', 'q','r']
interps = []
aux ={}

for a in PropoLethers:
    aux[a] = 1

interps.append(aux)

for a in PropoLethers:
    interps_aux =  [i for i in interps]

    for i in interps_aux:
        aux1 = {}

        for b in PropoLethers:
            if a == b:
                aux1[b] = 1 - i[b]
            else:
                aux1[b] = i[b]

        interps.append(aux1)

#print 'Interpretations: '
#for i in interps:
    #print i

###########################################################

def VI(f):
    if f.right == None:
        return i[f.label]
    elif f.label == '-':
        if VI(f.right) == 1:
            return 0
        else:
            return 1
    elif f.label == 'Y':
        if (VI(f.left) == 1 and VI(f.right) == 1):
            return 1
        else:
            return 0

    elif f.label == 'O':
        if (VI(f.left) == 1 or VI(f.right) == 1):
            return 1
        else:
            return 0
    elif f.label == '>':
        if (VI(f.left) == 0 or VI(f.right) == 1):
            return 1
        else:
            return 0
    elif f.label == '<->':
        if(VI(f.left) == VI(f.right)):
            return 1
        else:
            return 0

###########################################################

#Analisis de equivalencia

interpsI = []
interpsII = []
formula1 = poltotree()
formula2 = poltotree()

print "Interpretaciones posibles de las formulas: \n"
for i in interps:
	interpsI.append(VI(formula1))
print interpsI

for i in interps:
	interpsII.append(VI(formula2))
print interpsII

for i in range(0,len(interps)):
	if interpsI[i] == interpsII[i]:
		i = i + 1
		condi = True
	else:
		print "Las formulas no son equivalentes"
		condi = False
		break
if(condi == True):
	print "La formulas son equivalentes!"