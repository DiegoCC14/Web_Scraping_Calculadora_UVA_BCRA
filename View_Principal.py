
import os , sys , pathlib , parse

import WebScraping_Precio_UVAS

from PyQt5 import uic #Carga la interfaz  grafica
from PyQt5.QtWidgets import QMainWindow , QApplication , QTableWidgetItem , QMessageBox

class Inicio_App( QMainWindow ):

	def __init__(self):
		super().__init__()
		uic.loadUi( 'View_Principal.ui' , self )

		self.init_component()		

	def init_component( self ):

		self.generando_tabla_UVAS()

		self.actualizando_valor_UVA_y_pesos_total()

		# ACCIONES BUTTONS -------->>>>>
		self.button_Actualizar_UVA.clicked.connect( self.actualizando_valor_UVA_y_pesos_total )
		self.button_Guardar_Tabla_UVA.clicked.connect( self.guardando_datos_tabla_UVA )
		# ------------------------->>>>>


	def actualizando_valor_UVA_y_pesos_total( self ):
		
		self.actulizando_precio_UVA()
		self.actualizando_total_pesos()				

	def actulizando_precio_UVA( self ):
		( UVA_precio , Fecha )= WebScraping_Precio_UVAS.Obteniendo_precio_UVA_hoy()
		
		if UVA_precio == -1:
			self.ventana_emergente_de_texto( "Error" , f"Valor UVA no encontrado      " )
		elif UVA_precio == -2:
			self.ventana_emergente_de_texto( "Error" , f"Codigo o Pagina      " )
		else:
			self.label_Precio_UVA.setText( str( UVA_precio ) )
			self.label_Fecha_Actualizacion_UVA.setText( str( Fecha ) )
			

	def Obtener_Filas_del_txt(self , NameFile_txt):
		list_rows_in_txt = [ ( str( linea.replace('\n',"") ).encode('cp1252') ).decode('utf-8') for linea in open( NameFile_txt) ]
		return list_rows_in_txt

	def generando_tabla_UVAS( self ):
		self.Table_Cant_Uvas.setColumnCount( 1 )
		self.Table_Cant_Uvas.setColumnWidth(0, 335)
		self.Table_Cant_Uvas.setHorizontalHeaderLabels(['UVAS INGRESADAS'])

		UVAS = self.Obtener_Filas_del_txt('UVAS_ingresadas.txt')

		self.Table_Cant_Uvas.setRowCount( len(UVAS) + 25 )

		cont = 0
		for UVA in UVAS:
			self.Table_Cant_Uvas.setItem(cont ,0 , QTableWidgetItem( UVA ) )
			cont += 1

	def guardando_datos_tabla_UVA( self ):
		List_Errores = []
		Lista_Correctos = []

		for num_fila in range( self.Table_Cant_Uvas.rowCount() ):
			try:
				numero = self.Table_Cant_Uvas.item( num_fila , 0).text()
				try:
					if numero != '':
						Lista_Correctos.append( float( numero ) )
				except:
					List_Errores.append( num_fila+1 ) #El numero de la fila en tabla comienza en 1
			except:
				pass

		if len( List_Errores ) == 0:
			with open( 'UVAS_ingresadas.txt' , 'w' ) as file:
				for uva in Lista_Correctos:
					file.write( str(uva) + "\n" )
			self.ventana_emergente_de_texto( "Ventana Tabla UVAS" , f"Los Datos se Guardaron Correctamente      " )
		else:	
			self.ventana_emergente_de_texto( "Ventana Tabla UVAS" , f"Error en Fila: {str(List_Errores)}      " )

	def ventana_emergente_de_texto( self , titulo_ventana , texto_ventana ):
		dlg = QMessageBox(self)
		dlg.setWindowTitle( titulo_ventana )
		dlg.setText( texto_ventana )
		dlg.show()

	def actualizando_total_pesos( self ):
		total = 0
		for num_fila in range( self.Table_Cant_Uvas.rowCount() ):
			try:
				total += float( self.Table_Cant_Uvas.item( num_fila , 0).text() )
			except:
				pass
		Formato_Precio = parse.compile( '{Entero:d}.{Decimal}' )
		resu = Formato_Precio.parse( str( total * float( self.label_Precio_UVA.text() ) ) )
		self.label_Total_en_Pesos.setText( f"${ resu['Entero'] }.{ resu['Decimal'][0:2] }" )
app = QApplication( sys.argv )

Aplicacion = Inicio_App()
Aplicacion.setFixedSize( 438, 500 ) 
Aplicacion.show()

sys.exit( app.exec_() )