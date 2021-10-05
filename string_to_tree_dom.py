print "Funcion que pasa de una formula como cadena a un objeto Tree\n\
Recuerde que la formula debe estar escrita en notacion polaca invertida\n \
Las unicas letras proposicionales permitidas son pi, qi, ri, si\n \
Donde i pertenece a {1, ... , 16}\n \
Claves de escritura para los conectivos:\n \
NEGACION: -\n \
OR: O\n \
AND: Y\n \
IMPLICACION: >"

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
	# print "Es una hoja!"
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

# Solicitamos una cadena
f = raw_input('Ingrese una cadena: ') or 'r1q1p1O>' # Cadena por defecto

print "Cadena ingresada " + f

baslet = ['p', 'q', 'r', 's'] # Definimos las letras base para las letras proposicionales
letrasProposicionales = []
for i in range(1, 17):
	for o in baslet:
			letrasProposicionales.append(o + str(i))

conectivos = ['O', 'Y', '>'] # Definimos conectivos binarios

cadena = []
for x in range(len(f)):
	if f[x] in conectivos or f[x] == '-':
		cadena.append(f[x])
	elif f[x] in baslet:
		if x + 2 < len(f):
			if (f[x+1] + f[x+2]).isdigit():
				cadena.append(f[x: x+3])
			else:
				cadena.append(f[x: x+2])
		else:
			 cadena.append(f[x: x+2])

print cadena

pila = [] # Inicializamos la pila

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
print " fue creada como un objeto!"
