
import os , sys

from PyQt5 import uic #Carga la interfaz  grafica
from PyQt5.QtWidgets import QMainWindow , QApplication , QMessageBox

import Pestania_UVA , Pestania_DOLAR

class Inicio_App( QMainWindow ,
	Pestania_UVA.Pestania_UVA ,
	Pestania_DOLAR.Pestania_DOLAR ):
	

	def __init__(self):
		super().__init__()
		uic.loadUi( 'View_Principal.ui' , self )

		self.init_component_View_Principal()

		self.init_component_Pestania_UVA()

		self.init_component_Pestania_Dolar()


	def init_component_View_Principal( self ):
		self.button_Pestania_UVA.clicked.connect( self.VerPestana_UVA )
		self.button_Pestania_DOLAR.clicked.connect( self.VerPestana_DOLAR )


	def VerPestana_UVA( self ): 
		self.Group_UVA.move( 30 , 60 ) #Cambiamos de lugar los group box, dando la ilucion de cambiar ventanas
		self.Group_Dolar_Bl_Of.move( 980 , 60) #Cambiamos de lugar los group box, dando la ilucion de cambiar ventanas


	def VerPestana_DOLAR( self ):
		self.Group_UVA.move( 980 , 60) #Cambiamos de lugar los group box, dando la ilucion de cambiar ventanas
		self.Group_Dolar_Bl_Of.move( 30 , 50) #Cambiamos de lugar los group box, dando la ilucion de cambiar ventanas


app = QApplication( sys.argv )

Aplicacion = Inicio_App()
Aplicacion.setFixedSize( 495, 530 ) 
Aplicacion.show()

sys.exit( app.exec_() )