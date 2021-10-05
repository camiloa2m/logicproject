#-*-coding: utf-8-*-
# Programado en Python3
# Programado por Camilo Martinez y Samuel Perez
# Noviembre, 2018

# Algoritmo DPLL


def unitPropagate(S, I): #Unit Propagation 
	# Hace Unit Propagation a una conjunto de clausulas
	# Input: -S, conjunto (lista de listas) de clausulas
	#		 -I, interpretacion parcial (diccionario)

	# Output: -Sx, conjunto (lista de listas) de clausulas
	#	 	  -I, interpretacion parcial (diccionario)

	Sx = S
	print(u"Unit Propagate:", Sx, I)
	unit = False # Para definir si el conjunto tiene clausula unitaria
	novoid = True # Para definir si el conjunto NO tiene clausula vacia
	ind = 0
	for i in range(len(S)): # Analisis de S
		if len(S[i]) == 0:
			novoid = False
			break
		if len(S[i]) == 1: 
			unit = True
			ind = i

	if(unit and novoid): # Si tiene clausula unitaria, y NO tiene clausula vacia...
		current = S[ind][0] # Clausula unitaria
		if '-' in current: # Si es de la forma '-p'...
			dictmp={current[1:]:False}
			I.update(dictmp)
			Sx = [x for x in S if current not in x]
			for i in range(len(Sx)):
				Sx[i] = [x for x in Sx[i] if current[1:] != x]
		else: # Si es la forma 'p'...
			dictmp={current:True}
			I.update(dictmp)
			Sx = [x for x in S if current not in x]
			for i in range(len(Sx)):
				Sx[i] = [x for x in Sx[i] if '-' + current != x]
		return unitPropagate(Sx, I)

	else: # Si alguna de las condiciones no se cumple...
		print(u"FIN UP:", Sx, I)
		return Sx, I

def assign(Sx, Ix, lit):
	# Elimina las clausulas que contienen a lit y elimina -lit de las clausulas restantes
	# Input: -Sx, conjunto (lista de listas) de clausulas
	#		 -Ix, interpretacion parcial (diccionario)
	#		 -lit, literal a evaluar

	# Output: -Sxx, conjunto (lista de listas) de clausulas
	#	 	  -Ix, interpretacion parcial (diccionario)	

	print("Assigning:", Sx, Ix, lit)
	x = lit
	if '-' in x:
		dictmp={x[1:]:False}
		Ix.update(dictmp)
		Sxx = [Cl for Cl in Sx if x not in Cl]
		for Ci in range(len(Sxx)):
			Sxx[Ci] = [l for l in Sxx[Ci] if x[1:] != l]
	else:
		dictmp={x:True}
		Ix.update(dictmp)
		Sxx = [Cl for Cl in Sx if x not in Cl]
		for Ci in range(len(Sxx)):
			Sxx[Ci] = [l for l in Sxx[Ci] if '-' + x != l]			

	return Sxx, Ix

def DPLL(S, I):
	# Funcion principal del algoritmo DPLL, depende de las dos anteriores funciones definidas
	# Input: -S, conjunto (lista de listas) de clausulas
	#		 -I, interpretacion parcial (diccionario)

	# Output: -True/False, que corresponden a 'Satisfacible' e 'Insatisfacible' respectivamente.
	#	 	  -Ix, interpretacion parcial (diccionario)	

	print("\nDPLL:", S, I)
	Sx, Ix = unitPropagate(S, I)
	if [] in Sx:
		return False, {}
	elif len(Sx) == 0:
		return True, Ix
	else:
		#print(Ix, Sx)
		lit = Sx[0][0]
		Sxx, Ixx = assign(Sx, Ix, lit)
		OK, Ir = DPLL(Sxx, Ixx)
		if OK == True:
			return True, Ir
		elif len(lit) > 0:
			#print("\nBACK!")
			if '-' in lit:
				litback = lit[1:]
				Sxx, Ixx = assign(Sx, Ix, litback)
				return DPLL(Sxx,Ixx)
			else:
				litback = '-' + lit
				Sxx, Ixx = assign(Sx, Ix, litback)
				return DPLL(Sxx,Ixx)
		else:
			return False, {}


