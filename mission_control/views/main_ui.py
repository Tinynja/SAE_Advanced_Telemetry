# Built-in libraries
from math import cos, sin, radians

# Pipy libraries
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# User libraries
from lib.analog_gauge_widget import AnalogGaugeWidget



class MainUi:
	def __init__(self, main_window):
		self._main_window = main_window
		self._main_window.show()

		# Init main window
		self._main_window.setWindowTitle('Avion-Cargo Mission Control')
		# self._main_window.setWindowIcon(QIcon('resources/icons/nomad.ico'))
		self._main_window.setCentralWidget(QWidget())

		# Create all sub-layouts
		self._create_gauges()
		self._create_PFD()
		self._create_drop_history()
		self._create_MAP()

		# Merge all sub-layouts to the main layout
		self._create_main_layout()
	
	def _create_main_layout(self):
		main_layout = QVBoxLayout(self._main_window.centralWidget())

		row1_layout = QHBoxLayout()
		row2_layout = QHBoxLayout()
		main_layout.addLayout(row1_layout)
		main_layout.addLayout(row2_layout)

		row1_layout.addLayout(self._gauges_layout)
		row1_layout.setStretch(0,1)
		row1_layout.addLayout(self._PFD_layout)
		row1_layout.addLayout(self._drop_history_layout)

		# row2_layout.addLayout(self._MAP_layout)
	
	def _activer_bouton_standby(self):
		print('LOOL')

	def _create_gauges(self):
		self._gauges_layout = QVBoxLayout()
		
		# #Switch active/stand by
		activation_layout = QHBoxLayout()
		b1 = QPushButton("ACTIVE")
		b1.setGeometry(0,0,60,50)
		b1.setStyleSheet("background-color: green; color: white")

		self.b2 = QPushButton("Stand by")
		self.b2.setGeometry(0,0,60,50)
		self.b2.setStyleSheet("background-color: red; color: white")
		self.b2.move(60,0)
		self.b2.clicked.connect(lambda: print('Inactif'))

		activation_layout.addWidget(b1)
		activation_layout.addWidget(self.b2)

		# # #Batterie
		Bat = QProgressBar()
		Bat.setGeometry(30,40,200,75)
		step = 25
		Bat.setValue(step)

		activation_layout.addWidget(Bat)

		self._gauges_layout.addLayout(activation_layout)


		#Jauges
		#Module pour Jauges 

		jauges = QGridLayout()

		#Jauge de la puissance
		puissance = AnalogGaugeWidget()
		puissance.update_value(233)
		jauges.addWidget(puissance, 0, 0)

		#Jauge du voltage de l'avion mère
		volt_Avion = AnalogGaugeWidget()
		volt_Avion.update_value(200)
		jauges.addWidget(volt_Avion, 1, 0)

		#Jauge du voltage de la télémétrie
		volt_telem = AnalogGaugeWidget()
		volt_telem.update_value(350)
		jauges.addWidget(volt_telem, 2, 0)

		#Jauge de l'accéléromètre en X
		acc_x = AnalogGaugeWidget()
		acc_x.update_value(350)
		jauges.addWidget(acc_x, 0, 1)

		#Jauge de l'accéléromètre en Y
		acc_y = AnalogGaugeWidget()
		acc_y.update_value(350)
		jauges.addWidget(acc_y, 1, 1)

		self._gauges_layout.addLayout(jauges)

	def _create_PFD(self):
		self._PFD_layout = QVBoxLayout()
		
		top_layout    = QHBoxLayout()
		bottom_layout = QHBoxLayout()
		self._PFD_layout.addLayout(top_layout)
		self._PFD_layout.addLayout(bottom_layout)

		GS_display     = QVBoxLayout()
		Clock_display  = QVBoxLayout()
		VSI_display    = QVBoxLayout()

		TAS_display    = QStackedLayout()
		TAS_display.setStackingMode(QStackedLayout.StackAll)
		Attitude_display = QStackedLayout()
		ALT_display    = QStackedLayout()
		ALT_display.setStackingMode(QStackedLayout.StackAll)
		#... à continuer pour la partie du bas

		self._PFD_layout.setContentsMargins(5,5,5,5)

		#indicateur de GS
		GS_label = QLabel('Ground speed (kts)')
		GS_label.setAlignment(Qt.AlignCenter)		
		GS_display.addWidget(GS_label)
		GS_value = QLabel('19')
		GS_value.setAlignment(Qt.AlignCenter)
		GS_value.setFont(QFont('Arial',20))
		GS_value.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		GS_display.addWidget(GS_value)

		#indicateur de temps écoulé
		Clock_label = QLabel('Time since beggining of flight')
		Clock_label.setAlignment(Qt.AlignCenter)	
		Clock_display.addWidget(Clock_label)
		Clock_value = QLabel('01:22.1')
		Clock_value.setAlignment(Qt.AlignCenter)	
		Clock_value.setFont(QFont('Arial',20))
		Clock_value.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		Clock_display.addWidget(Clock_value)

		#indicateur de vertical speed
		VSI_label = QLabel('Vertical speed (fpm)')
		VSI_label.setAlignment(Qt.AlignCenter)		
		VSI_display.addWidget(VSI_label)
		VSI_value = QLabel('+ 50')
		VSI_value.setAlignment(Qt.AlignCenter)
		VSI_value.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		VSI_value.setFont(QFont('Arial',20))
		VSI_display.addWidget(VSI_value)


		#indicateur de TAS
		original_img_TAS = QPixmap('resources/TAS_Graphic.JPG')
		tas = 33
		calculated_top = 100 - 9.803921569 * (tas-57)
		top = round(calculated_top)
		height = 300
		def __update_img(adj=0):
			global top1
			top1 = max(0, min(top+adj, original_img_TAS.height()-height))
			TAS_img.setPixmap(original_img_TAS.copy(QRect(0, top, original_img_TAS.width(), height)))
		TAS_img = QLabel()
		__update_img()
		TAS_img.setFrameStyle(QFrame.Box)
		TAS_value = QLabel(str(tas))
		TAS_value.setFont(QFont('Arial',25))
		TAS_value.setAlignment(Qt.AlignCenter)	
		TAS_value.setFrameStyle(QFrame.Panel | QFrame.Raised)
		TAS_value.setStyleSheet("background-color: black; color: white")
		dummy_widget = QWidget()
		TAS_layout = QVBoxLayout(dummy_widget)
		TAS_layout.setContentsMargins(5,0,5,0)
		TAS_layout.addStretch(1)
		TAS_layout.addWidget(TAS_value)
		TAS_layout.addStretch(1)
		TAS_display.addWidget(TAS_img)
		TAS_display.addWidget(dummy_widget)

		#Attitude
		self._original_attitude_img = QPixmap('resources/Attitude_Graphic.png')
		self.pitch, self.roll = 0, 0
		self._attitude = QLabel()
		# Attitude_label = QLabel('Roll and pitch angle')
		self._attitude.setFrameStyle(QFrame.Box)
		Attitude_display.addWidget(self._attitude)
		# Attitude_value = QLabel('Pitch = -0.5 deg | Roll = 12.2 deg')
		# Attitude_display.addWidget(Attitude_value)
		self.set_attitude(pitch=20, roll=10)

		# attitude_img = QLabel()
		# update_img(bank_angle)
		# attitude_img.setFrameStyle(QFrame.Box) #TODO: je suis rendu ici - Francois
		# original_img_attitude = QPixmap('resources/Attitude_Graphic.JPG')

		# #indicateur de VS graphique
		# Altitude_display = bottom_layout.addWidget(Color('black'))
		# #indicateur d'altitude
		# VSI_graphic_display = bottom_layout.addWidget(Color('purple'))


		#indicateur de ALT
		original_img_ALT = QPixmap('resources/ALT_Graphic.PNG')
		alt = 64
		calculated_top = 100 - 5.464490874 * (alt-94)
		top = round(calculated_top)
		height = 300
		def __update_img(adj=0):
			global top1
			top1 = max(0, min(top+adj, original_img_ALT.height()-height))
			ALT_img.setPixmap(original_img_ALT.copy(QRect(0, top, original_img_ALT.width(), height)))
		ALT_img = QLabel()
		__update_img()
		ALT_value = QLabel(str(alt))
		ALT_value.setFrameStyle(QFrame.Box)
		ALT_value.setFont(QFont('Arial',25))
		ALT_value.setAlignment(Qt.AlignCenter)	
		ALT_value.setFrameStyle(QFrame.Panel | QFrame.Raised)
		ALT_value.setStyleSheet("background-color: green; color: white")
		alt_dummy_widget = QWidget()
		ALT_layout = QVBoxLayout(alt_dummy_widget)
		ALT_layout.setContentsMargins(5,0,5,0)
		ALT_layout.addStretch(1)
		ALT_layout.addWidget(ALT_value)
		ALT_layout.addStretch(1)
		ALT_display.addWidget(ALT_img)
		ALT_display.addWidget(alt_dummy_widget)

		#Assemblage de top_layout et bottom_layout
		top_layout.addLayout( GS_display )
		top_layout.addLayout( Clock_display )
		top_layout.addLayout( VSI_display )

		bottom_layout.addLayout( TAS_display )
		bottom_layout.addLayout( Attitude_display )
		bottom_layout.addLayout( ALT_display )
		# bottom_layout.addLayout( VSI_graphic_display )
	
	# Indicateur d'assiette
	def set_attitude(self, pitch=None, roll=None):
		pitch = pitch or self.pitch
		roll = roll or self.roll
		self.pitch = pitch
		self.roll = roll

		# Calibration de l'indicateur d'assiette:
		# 	pitch := 1023px/160deg
		width, height = 400, 300
		radius, angle = pitch*1023/160, roll+90
		x_center, y_center = radius*cos(radians(angle)), radius*sin(radians(angle))
		
		rotation = QTransform().rotate(roll)
		new_attitude = self._original_attitude_img.transformed(rotation, Qt.SmoothTransformation)
		crop = QRect(int(new_attitude.width()/2-x_center-width/2), int(new_attitude.height()/2-y_center-height/2), width, height)
		self._attitude.setPixmap(new_attitude.copy(crop))

	def _create_drop_history(self):
		self._drop_history_layout = QGridLayout()
	
		labels = []
		buttons = []

		def clickme(btn):
			btn.setStyleSheet("background-color: green")

		def __create_button(text):
			btn = QPushButton(text)
			buttons.append(btn)
			btn.setFont(QFont('Arial',32))
			# clickme(123)
			btn.clicked.connect(lambda btn=btn: clickme(btn))
			# btn.clicked.emit()

		def __create_label(text):
			labels.append(QLabel(text))
			labels[-1].setFont(QFont('Arial',32))
			labels[-1].setFrameStyle(QFrame.Box|QFrame.Plain)
			labels[-1].setLineWidth(2)

		__create_button("Planeur 1")
		__create_button("Planeur 2")
		__create_button("Vivres")
		__create_button("Habitats")

		__create_label("Altitude Planeur 1")
		__create_label("Altitude Planeur 2")
		__create_label("Altitude Vivres")
		__create_label("Altitude Habitats")
		
		self._drop_history_layout.addWidget(QPushButton("Enregistrement"),0,2)
		self._drop_history_layout.addWidget(QPushButton("Settings"),0,3)
		for i in range(2):
			for j in range(4):
				if i == 0:
					self._drop_history_layout.addWidget(buttons[j],j+1,0,1,2)
				elif i == 1:
					self._drop_history_layout.addWidget(labels[j],j+1,2,1,2)
		
		# if labels[0].mousePressEvent or labels[1].mousePressEvent and labels[2].mousePressEvent or labels[3].mousePressEvent: #Verification que planeur et largage ne soient pas clicker en meme temps
		# 	labels[2].setStyleSheet("background-color: red")
		# 	labels[3].setStyleSheet("background-color: red")
		# 	print("Erreur! Incompatibilité entre les composantes à larguer")

		# for i in range(4): #Double click pour modifier le text et save l'altitude de largage
		# 	if labels[i-1].mouseDoubleClickEvent is True:
		# 		labels[i+4].setText(self.__record_altitude)

		def __record_altitude(self, drop, altitude):
			pass

	def _create_MAP(self):
		pass


# Color est ajouté pour PFD, à voir si on laisse ça là
class Color(QWidget):

	def __init__(self, color, *args, **kwargs):
		super(Color, self).__init__(*args, **kwargs)
		self.setAutoFillBackground(True)

		palette = self.palette()
		palette.setColor(QPalette.Window, QColor(color))
		self.setPalette(palette)