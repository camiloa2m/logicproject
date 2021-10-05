#-*-coding: utf-8-*-

from random import choice

##############################################################################
# Definicion de objeto tree y funciones
##############################################################################

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

def imprime_tableau(tableau):
	cadena = '['
	for l in tableau:
		cadena += "{"
		primero = True
		for f in l:
			if primero == True:
				primero = False
			else:
				cadena += ", "
			cadena += Inorder(f)
		cadena += "}"
	return cadena + "]"

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"

def obtiene_literales(cadena, letrasProposicionales):
	literales = []
	contador = 0
	baslet = ['p', 'q', 'r', 's']
	while contador < len(cadena) - 1:
		if cadena[contador] == '-':
			if "".join(cadena[contador+2: contador+4]).isdigit():
				l = "".join(cadena[contador: contador+4])
			else:
				l = "".join(cadena[contador: contador+3])
			literales.append(l)
			contador += 2
		elif "".join(cadena[contador]) in baslet:
			if "".join(cadena[contador+1: contador+3]).isdigit():
				l = "".join(cadena[contador: contador+3])
			else:
				l = "".join(cadena[contador: contador+2])
			literales.append(l)
		contador += 1
	print "\nlit2:", literales
	return literales


def Tableaux(lista_hojas, letrasProposicionales):

	# Algoritmo de creacion de tableau a partir de lista_hojas

	# Imput: - lista_hojas: lista de lista de formulas
	#			(una hoja es una lista de formulas)
	#		 - letrasProposicionales: lista de letras proposicionales del lenguaje

	# Output: - String: Satisfacible/Insatisfacible
	# 		  - interpretaciones: lista de listas de literales que hacen verdadera
	#			la lista_hojas

	print "Trabajando con: ", imprime_tableau(lista_hojas)

	marcas = ['x', 'o']
	interpretaciones = [] # Lista para guardar interpretaciones que satisfacen la raiz

	while any(x not in marcas for x in lista_hojas): # Verifica si hay hojas no marcadas

		# Hay hojas sin marcar
		# Crea la lista de hojas sin marcar
		hojas_no_marcadas = [x for x in lista_hojas if x not in marcas]
		print u"Cantidad de hojas sin marcar: ", len(hojas_no_marcadas)
		# Selecciona una hoja no marcada
		hoja = choice(hojas_no_marcadas)
		print "Trabajando con hoja: ", imprime_hoja(hoja)

		# Busca formulas que no son literales
		formulas_no_literales = []
		for x in hoja:
			if x.label not in letrasProposicionales:
				if x.label != '-':
					# print Inorder(x) + " no es un literal"
					formulas_no_literales.append(x)
					break
				elif x.right.label not in letrasProposicionales:
					# print Inorder(x) + " no es un literal"
					formulas_no_literales.append(x)
					break

		# print "Formulas que no son literales: ", imprime_hoja(formulas_no_literales)

		if formulas_no_literales != []: # Verifica si hay formulas que no son literales
			# Hay formulas que no son literales
			print "Hay formulas que no son literales"
			# Selecciona una formula no literal
			f = choice(formulas_no_literales)
			if f.label == 'Y':
				# print u"Fórmula 2alfa" # Identifica la formula como A1 y A2
				hoja.remove(f) # Quita a f de la hoja
				A1 = f.left
				if  A1 not in hoja:
					hoja.append(A1) # Agrega A1
				A2 = f.right
				if  A2 not in hoja:
					hoja.append(A2) # Agrega A2
			elif f.label == 'O':
				# print u"Fórmula 2beta" # Identifica la formula como B1 o B2
				hoja.remove(f) # Quita la formula de la hoja
				lista_hojas.remove(hoja) # Quita la hoja de la lista de hojas
				B1 = f.left
				if  B1 not in hoja:
					S1 = [x for x in hoja] + [B1] # Crea nueva hoja con B1
				lista_hojas.append(S1) # Agrega nueva hoja con B1
				B2 = f.right
				if B2 not in hoja:
					S2 = [x for x in hoja] + [B2] # Crea nueva hoja con B2
				lista_hojas.append(S2) # Agrega nueva hoja con B2
			elif f.label == '>':
				# print u"Fórmula 3beta" # Identifica la formula como B1 > B2
				hoja.remove(f) # Quita la formula de la hoja
				lista_hojas.remove(hoja) # Quita la hoja de la lista de hojas
				noB1 = Tree('-', None, f.left)
				if  noB1 not in hoja:
					S1 = [x for x in hoja] + [noB1] # Crea nueva hoja con no B1
				lista_hojas.append(S1) # Agrega nueva hoja con no B1
				B2 = f.right
				if B2 not in hoja:
					S2 = [x for x in hoja] + [B2] # Crea nueva hoja con B2
				lista_hojas.append(S2) # Agrega nueva hoja con B2
			elif f.label == '-':
				if f.right.label == '-':
					# print u"Fórmula 1alfa" # Identifica la formula como no no A1
					hoja.remove(f) # Quita a f de la hoja
					A1 = f.right.right
					if A1 not in hoja:
						hoja.append(A1) # Agrega la formula sin doble negacion
				elif f.right.label == 'O':
					# print u"Fórmula 3alfa" # Identifica la formula como no(A1 o A2)
					hoja.remove(f) # Quita a f de la hoja
					noA1 = Tree('-', None, f.right.left)
					if noA1 not in hoja:
						hoja.append(noA1) # Agrega no A1
					noA2 = Tree('-', None, f.right.right)
					if noA2 not in hoja:
						hoja.append(noA2) # Agrega no A2
				elif f.right.label == '>':
					# print u"Fórmula 4alfa" # Identifica la formula como no(A1 > A2)
					hoja.remove(f) # Quita a f de la hoja
					A1 = f.right.left
					if A1 not in hoja:
						hoja.append(A1) # Agrega A1
					noA2 = Tree('-', None, f.right.right)
					if noA2 not in hoja:
						hoja.append(noA2) # Agrega no A2
				elif f.right.label == 'Y':
					# print u"Fórmula 1beta" # Identifica la formula como no(B1 y B2)
					hoja.remove(f) # Quita la formula de la hoja
					lista_hojas.remove(hoja) # Quita la hoja de la lista de hojas
					noB1 = Tree('-', None, f.right.left)
					if  noB1 not in hoja:
						S1 = [x for x in hoja] + [noB1] # Crea nueva hoja con no B1
					lista_hojas.append(S1) # Agrega nueva hoja con no B2
					noB2 = Tree('-', None, f.right.right)
					if  noB2 not in hoja:
						S2 = [x for x in hoja] + [noB2] # Crea nueva hoja con no B2
					lista_hojas.append(S2) # Agrega nueva hoja con no B2

		else: # No hay formulas que no sean literales
			# print "La hoja contiene solo literales!"
			lista = list(imprime_hoja(hoja))
			# print lista
			literales = obtiene_literales(lista, letrasProposicionales)
			# print literales
			hojaConsistente = True
			for l in literales: # Verificamos que no hayan pares complementarios en la hoja
				if '-' not in l: # Verifica si el literal es positivo
					if '-' + l in literales: # Verifica si el complementario esta en la hoja
						print "La hoja " + imprime_hoja(hoja) +  " es inconsistente!"
						lista_hojas.remove(hoja)
						# lista_hojas.append('x') # Marca la hoja como inconsistente con una 'x'
						hojaConsistente = False
						break

				elif l[1:] in literales: # Verifica si el complementario esta en la hoja
						print "La hoja " + imprime_hoja(hoja) +  " es inconsistente!"
						lista_hojas.remove(hoja)
						# lista_hojas.append('x') # Marca la hoja como inconsistente con una 'x'
						hojaConsistente = False
						break

			if hojaConsistente: # Se recorrieron todos los literales y no esta el complementario
				print "La hoja " + imprime_hoja(hoja) +  " es consistente :)"
				interpretaciones.append(hoja) # Guarda la interpretacion que satisface la raiz
				lista_hojas.remove(hoja)
				# lista_hojas.append('o') # Marca la hoja como consistente con una 'o'

	# Dice si la raiz es inconsistente
	# print "Hay " + str(len(interpretaciones)) + u" interpretaciones que satisfacen la fórmula"
	if len(interpretaciones) > 0:
		print u"La fórmula es satisfacible por las siguientes interpretaciones: "

		# Interpreta como string la lista de interpretaciones
		INTS = []
		for i in interpretaciones:
			aux = [Inorder(l) for l in i]
			INTS.append(aux)
			print aux

		# Eliminamos repeticiones dentro de cada interpretacion
		INTS = [list(set(i)) for i in INTS]
		# Eliminamos interpretaciones repetidas
		INTS_set = set(tuple(x) for x in INTS)
		INTS = [list(x) for x in INTS_set]
		print "Hay " + str(len(INTS)) + u" interpretaciones que satisfacen la fórmula"

		return "Satisfacible", INTS
	else:
		print(u"La lista de fórmulas dada es insatisfacible!")
		return "Insatisfacible", None

##############################################################################
# Fin definicion de objeto tree y funciones
##############################################################################
