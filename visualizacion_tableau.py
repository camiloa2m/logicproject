#-*-coding: utf-8-*-
# Basado en el codigo de Edgar Andrade, Octubre 2018
# Camilo Martinez y Samuel Perez

# Visualizacion de tableros de sudoku 4x4 a partir de
# una lista de literales. Cada literal representa un estado de una casilla;
# el literal es positivo sii el numero que representa esta en la casilla correspondiente.
# Es decir: 'p', 'q', 'r' y 's' representan respectivamente los numeros '1', '2', '3' y '4'.
# El indice 'i' del literal representa la casilla a la que corresponde, es decir: 
#   'pi': si 'i' = 1, 'p1' representaria que el numero '1' esta en la casilla 1.
#   'si': si 'i' = 9, '~s9' representaria que el numero '4' NO esta en la casilla 9.
#   y de la misma forma con los demas...

# Formato de la entrada: - las letras proposicionales seran: 'pi','qi','ri','si', 
#                          i perteneciendo a {1, ... , 16};
#                        - solo se aceptan literales (ej. p1, ~q2, r3, ~r12, etc.)
# Requiere tambien un numero natural, para servir de indice del sudoku,
# toda vez que pueda solicitarse visualizar varios sudokus.

# Salida: archivo sudoku_%j.png, donde %j es un numero natural

#################
# importando paquetes para dibujar
print "Importando paquetes..."
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import os
print "Listo!"

def dibujar_tablero(f, n):
	# Visualiza un tablero dada una formula f
	# Input:
	#   - f, una lista de literales
	#   - n, un numero de identificacion del archivo
	# Output:
	#   - archivo de imagen sudoku_n.png

	# Inicializo el plano que contiene la figura
	fig, axes = plt.subplots()
	axes.get_xaxis().set_visible(False)
	axes.get_yaxis().set_visible(False)

	# Dibujo el tablero
	step = 1./4
	tangulos = []

	# Creo los cuadrados azules en el tablero
	tangulos.append(patches.Rectangle(*[(0, 2 * step), step, step],\
			facecolor='skyblue'))
	tangulos.append(patches.Rectangle(*[(2 * step, 0), step, step],\
			facecolor='skyblue'))
	tangulos.append(patches.Rectangle(*[(2 * step, step), step, step],\
			facecolor='skyblue'))
	tangulos.append(patches.Rectangle(*[(step, 2 * step), step, step],\
			facecolor='skyblue'))
	tangulos.append(patches.Rectangle(*[(3 * step, step), step, step],\
			facecolor='skyblue'))
	tangulos.append(patches.Rectangle(*[(step, 3 * step), step, step],\
			facecolor='skyblue'))
	tangulos.append(patches.Rectangle(*[(3 * step, 0), step, step],\
			facecolor='skyblue'))
	tangulos.append(patches.Rectangle(*[(0, 3 * step), step, step],\
			facecolor='skyblue'))

	# Creo los cuadrados claros en el tablero
	tangulos.append(patches.Rectangle(*[(0, step), step, step],\
			facecolor='mintcream'))
	tangulos.append(patches.Rectangle(*[(step, 0), step, step],\
			facecolor='mintcream'))
	tangulos.append(patches.Rectangle(*[(2 * step, 2 * step), step, step],\
			facecolor='mintcream'))
	tangulos.append(patches.Rectangle(*[(step, step), step, step],\
			facecolor='mintcream'))
	tangulos.append(patches.Rectangle(*[(0, 0), step, step],\
			facecolor='mintcream'))
	tangulos.append(patches.Rectangle(*[(3 * step, 2 * step), step, step],\
			facecolor='mintcream'))
	tangulos.append(patches.Rectangle(*[(2 * step, 3 * step), step, step],\
			facecolor='mintcream'))
	tangulos.append(patches.Rectangle(*[(3 * step, 3 * step), step, step],\
			facecolor='mintcream'))

	# Creo las lineas del tablero de sudoku
	for j in range(4):
		locacion = j * step
		# Crea linea horizontal en el rectangulo
		tangulos.append(patches.Rectangle(*[(0, step + locacion), 1, 0.005],\
				facecolor='black'))
		# Crea linea vertical en el rectangulo
		tangulos.append(patches.Rectangle(*[(step + locacion, 0), 0.005, 1],\
				facecolor='black'))

	for t in tangulos:
		axes.add_patch(t)

	# Cargando imagen de numero 1
	arr_img1 = plt.imread("./num_img/one.png", format='png')
	imgone = OffsetImage(arr_img1, zoom=0.07)
	imgone.image.axes = axes

	# Cargando imagen de numero 2
	arr_img2 = plt.imread("./num_img/two.png", format='png')
	imgtwo = OffsetImage(arr_img2, zoom=0.13)
	imgtwo.image.axes = axes

	# Cargando imagen de numero 3
	arr_img3 = plt.imread("./num_img/three.png", format='png')
	imgthree = OffsetImage(arr_img3, zoom=0.07)
	imgthree.image.axes = axes

	# Cargando imagen de numero 4
	arr_img4 = plt.imread("./num_img/four.png", format='png')
	imgfour = OffsetImage(arr_img4, zoom=0.07)
	imgfour.image.axes = axes

	# Creando las direcciones en la imagen de acuerdo al indice del literal
	direcciones = {}
	direcciones[1] = [0.125, 0.875]
	direcciones[2] = [0.375, 0.875]
	direcciones[3] = [0.625, 0.875]
	direcciones[4] = [0.875, 0.875]
	direcciones[5] = [0.125, 0.625]
	direcciones[6] = [0.375, 0.625]
	direcciones[7] = [0.625, 0.625]
	direcciones[8] = [0.875, 0.625]
	direcciones[9] = [0.125, 0.375]
	direcciones[10] = [0.375, 0.375]
	direcciones[11] = [0.625, 0.375]
	direcciones[12] = [0.875, 0.375]
	direcciones[13] = [0.125, 0.125]
	direcciones[14] = [0.375, 0.125]
	direcciones[15] = [0.625, 0.125]
	direcciones[16] = [0.875, 0.125]

	# Posicionando los numeros segun los literales
	for l in f: # Evaluando cada literal del conjunto
		if '-' not in l: # Tomando los literales verdaderos (los cuales agregan un numero)
			if l[0] == 'p':
				ab = AnnotationBbox(imgone, direcciones[int(l[1:])], frameon=False)
				axes.add_artist(ab)
			if l[0] == 'q':
				ab = AnnotationBbox(imgtwo, direcciones[int(l[1:])], frameon=False)
				axes.add_artist(ab)
			if l[0] == 'r':
				ab = AnnotationBbox(imgthree, direcciones[int(l[1:])], frameon=False)
				axes.add_artist(ab)
			if l[0] == 's':
				ab = AnnotationBbox(imgfour, direcciones[int(l[1:])], frameon=False)
				axes.add_artist(ab)

	# plt.show()
	d = 'Soluciones/'
	try:
		os.makedirs(d)
		print "Creando " + d
	except OSError:
		if not os.path.isdir(d):
			raise
	fig.savefig(d + "sudoku_" + str(n) + ".png")
	print "Imagenes creadas! Verificar la carpeta " + d
