#-*-coding: utf-8-*-
# Programado en Python3

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label

def Inorder(f):
	# Imprime una formula como cadena dada una formula como arbol
	# Input: tree, que es una formula de logica proposicional
	# Output: string de la formula

	if f.right == None:
		return f.label
	elif f.label == '-':
		return f.label + Inorder(f.right)
	else:
		return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def StringtoTree(A, letrasProposicionales):
	# Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
	# Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
			 # letrasProposicionales, lista de letras proposicionales
	# Output: formula como tree
	conectivos = ['O', 'Y', '>']
	baslet = ['p', 'q', 'r', 's']
	listring = []
	for x in range(len(A)):
		if A[x] in conectivos or A[x] == '-':
			listring.append(A[x])
		elif A[x] in baslet:
			if x + 2 < len(A):
				if (A[x+1] + A[x+2]).isdigit():
					listring.append(A[x: x+3])
				else:
					listring.append(A[x: x+2])
			else:
				listring.append(A[x: x+2])

	pila = []
	for c in listring:
		if c in letrasProposicionales:
			pila.append(Tree(c, None, None))
		elif c == '-':
			formulaAux = Tree(c, None, pila[-1])
			del pila[-1]
			pila.append(formulaAux)
		elif c in conectivos:
			formulaAux = Tree(c, pila[-1], pila[-2])
			del pila[-1]
			del pila[-1]
			pila.append(formulaAux)
	return pila[-1]

def quitarDobleNegacion(f):
	# Elimina las dobles negaciones en una formula como arbol
	# Input: tree, que es una formula de logica proposicional
	# Output: tree sin dobles negaciones

	if f.right == None:
		return f
	elif f.label == '-':
		if f.right.label == '-':
			return quitarDobleNegacion(f.right.right)
		else:
			return Tree('-', \
						None, \
						quitarDobleNegacion(f.right)\
						)
	else:
		return Tree(f.label, \
					quitarDobleNegacion(f.left), \
					quitarDobleNegacion(f.right)\
					)

def reemplazarImplicacion(f):
    # Regresa la formula reemplazando p>q por -pOq
    # Input: tree, que es una formula de logica proposicional
    # Output: tree

    if f.right == None:
        return f
    elif f.label == '-':
        return Tree('-', None, reemplazarImplicacion(f.right))
    elif f.label == '>':
        noP = Tree('-', None, reemplazarImplicacion(f.left))
        Q = reemplazarImplicacion(f.right)
        return Tree('O', noP, Q)
    else:
        return Tree(f.label, reemplazarImplicacion(f.left), reemplazarImplicacion(f.right))

def deMorgan(f):
    # Regresa la formula aplicando deMorgan -(pYq) por -pO-q
    # Input: tree, que es una formula de logica proposicional
    # Output: tree

	if f.right == None:
		return f
	elif f.label == '-':
		if f.right.label == 'Y':
			print(u"La fórmula coincide negación Y")
			return Tree('O', \
						Tree('-', None, deMorgan(f.right.left)),\
						Tree('-', None, deMorgan(f.right.right))\
						)
		elif f.right.label == 'O':
			print(u"La fórmula coincide negación O")
			return Tree('Y', \
						Tree('-', None, deMorgan(f.right.left)),\
						Tree('-', None, deMorgan(f.right.right))\
						)
		else:
			return Tree('-', \
						None, \
						deMorgan(f.right) \
						)
	else:
		return Tree(f.label, \
					deMorgan(f.left),\
					deMorgan(f.right)\
					)

def distributiva(f):
    # Distribuye O sobre Ys: convierte rO(pYq) en (rOp)Y(rOq)
    # Input: tree, que es una formula de logica proposicional
    # Output: tree

	if f.right == None:
		# print("Llegamos a una rama")
		return f
	elif f.label == 'O':
		# print("Encontramos O...")
		if f.left.label == 'Y':
			# print("... encontramos Y a la izquierda")
			P = f.left.left
			Q = f.left.right
			R = f.right
			return Tree('Y', \
						Tree('O', P, R), \
						Tree('O', Q, R)
						)
		if f.right.label == 'Y':
			# print("... encontramos Y a la derecha")
			R = f.left
			P = f.right.left
			Q = f.right.right
			return Tree('Y', \
						Tree('O', R, P), \
						Tree('O', R, Q)
						)
		else:
			# print("... pero no hay Y")
			# print("Pasamos a hijos de O")
			return Tree(f.label, \
						distributiva(f.left), \
						distributiva(f.right)
						)
	elif f.label == '-':
		# print("Pasamos a hijo de negacion")
		return Tree('-', \
					None, \
					distributiva(f.right)
					)
	else:
		# print("Pasamos a hijos de ", f.label)
		return Tree(f.label, \
					distributiva(f.left), \
					distributiva(f.right)
					)

def aplicaDistributiva(f):
    # Devuelve True si la distributiva de f es distinta a f
    # Input: tree, que es una formula de logica proposicional
    # Output: - True/False,
	# 		  - tree
	aux1 = Inorder(f)
	print("Se analiza: ", aux1)
	B = distributiva(f)
	aux2 = Inorder(B)
	print("Se obtuvo : ", aux2)
	if  aux1 != aux2:
		print(u"Hubo distribución")
		return True, B
	else:
		print(u"No hubo distribución")
		return False, f

def eliminaConjunciones(f):
    # Devuelve una lista de disyunciones de literales
    # Input: tree, que es una formula en CNF
    # Output: lista de cadenas
	if f.right == None:
		a = [Inorder(f)]
		print("Clausula unitaria positiva, ", a)
		return a
	elif f.label == 'O':
		return [Inorder(f)]
	elif f.label == 'Y':
		print(u"Dividiendo los lados de la conjunción")
		a = eliminaConjunciones(f.left)
		print("a, ", a)
		b = eliminaConjunciones(f.right)
		print("b, ", b)
		c = a + b
		print("c, ", c)
		return a + b
	else:
		if f.label == '-':
			if f.right.right == None:
				print("Clausula unitaria negativa")
				return [Inorder(f)]
			else:
				print("Oh, Oh, la formula no estaba en CNF!")

def complemento(l):
    # Devuelve el complemento de un literal
    # Input: l, que es una cadena con un literal (ej: p, -p)
    # Output: l complemento
	if '-' in l:
		return l[1:]
	else:
		return '-' + l

def formaClausal(f):
    # Obtiene la forma clausal de una formula en CNF
    # Input: tree, que es una formula de logica proposicional en CNF
    # Output: lista de clausulas

	# Primero elimino las conjunciones, obteniendo
	# una lista de disyunciones de literales
	print("Encontrando lista de disyunciones de literales...")
	aux = eliminaConjunciones(f)
	badChars = ['(', ')']
	conjuntoClausulas = []
	for C in aux:
		C = ''.join([x for x in C if x not in badChars])
		C = C.split('O')
		conjuntoClausulas.append(C)

	aux = []
	print(u"Eliminando cláusulas triviales...")
	for C in conjuntoClausulas:
		trivial = False
		for x in C:
			xComplemento = complemento(x)
			if xComplemento in C:
				print(u"Cláusula trivial encontrada")
				trivial = True
				break
		if not trivial:
			aux.append(C)

	print("Eliminando repeticiones...")
	# Eliminamos repeticiones dentro de cada clausula
	aux = [list(set(i)) for i in aux]
	# Eliminamos clausulas repetidas
	aux_set = set(tuple(x) for x in aux)
	aux = [list(x) for x in aux_set]

	conjuntoClausulas = aux

	return conjuntoClausulas

#################################################

#Letras proposicionales basicas
baslet = ['p', 'q', 'r', 's'] 

# Creo las letras proposicionales
letrasProposicionales = []
for i in range(1, 17):
    for o in baslet:
            letrasProposicionales.append(o + str(i))

# cadena = 'q--p->--'
# cadena = 'qpY-'
# cadena = 'rq-pO->'
# cadena = 'qpYprYO'
# cadena = 'qpYpr>O'
# cadena = 'pr>qpYO'
# cadena = 'q--qpYprYO->--'
# cadena = 'q-pYqp-YO'
# cadena = 'r-q-YpY'
# cadena = cadena + 'r-qYp-Y' + 'O'
# cadena = cadena + 'rq-Yp-Y' + 'O'
def toclaus(cadena, letrasProposicionales):
	A = StringtoTree(cadena, letrasProposicionales)

	print(u"Trabajando con la fórmula:\n ", Inorder(A))

	A = quitarDobleNegacion(A)

	print(u"La fórmula sin dobles negaciones es:\n ", Inorder(A))

	A = reemplazarImplicacion(A)

	print(u"La fórmula reemplazando implicaciones es:\n ", Inorder(A))

	A = quitarDobleNegacion(A)

	print(u"La fórmula sin dobles negaciones es:\n ", Inorder(A))

	OK = True
	while OK:
		aux1 = Inorder(A)
		print("Se analiza: ", aux1)
		B = deMorgan(A)
		B = quitarDobleNegacion(B)
		aux2 = Inorder(B)
		print("Se obtuvo : ", aux2)
		if  aux1 != aux2:
			print(u"Se aplicó deMorgan")
			OK = True
			A = B
		else:
			print(u"No se aplicó deMorgan")
			OK = False

	OK = True
	while OK:
		OK, A = aplicaDistributiva(A)

	conjuntoClausulas = formaClausal(A)

	print("Conjunto de disyunciones de literales:\n ", conjuntoClausulas)

	return conjuntoClausulas
