import WebScraping_Precio_Dolar_Blue_Oficial

import parse

from PyQt5.QtWidgets import QMessageBox , QTableWidgetItem

class Pestania_DOLAR():

	def init_component_Pestania_Dolar( self ):
		
		self.generando_tabla_Dolar()

		self.actualizando_valor_Dolar_y_pesos_total()

		# ACCIONES BUTTONS -------->>>>>
		self.button_Actualizar_Datos_Dolar.clicked.connect( self.actualizando_valor_Dolar_y_pesos_total )
		self.button_Guardar_Tabla_Dolar.clicked.connect( self.guardando_datos_tabla_Dolar )
		# ------------------------->>>>>


	def actualizando_valor_Dolar_y_pesos_total( self ):
		
		self.actulizando_precio_Dolar()

		self.actualizando_total_pesos_Dolar_Venta()


	def actulizando_precio_Dolar( self ):
		( Dolar_Oficial , Dolar_Blue , Fecha ) = WebScraping_Precio_Dolar_Blue_Oficial.Obteniendo_precio_Dolar_Blue_Oficial_hoy()
		
		if Dolar_Oficial == -1:
			self.ventana_emergente_de_texto( "Error" , f"Valor DOLAR no encontrado      " )
		elif Dolar_Oficial == -2:
			self.ventana_emergente_de_texto( "Error" , f"Codigo o Pagina      " )
		else:
			self.label_Dolar_Oficial_Compra.setText( str( Dolar_Oficial['Compra'] ) )
			self.label_Dolar_Oficial_Venta.setText( str( Dolar_Oficial['Venta'] ) )

			self.label_Dolar_Blue_Compra.setText( str( Dolar_Blue['Compra'] ) )
			self.label_Dolar_Blue_Venta.setText( str( Dolar_Blue['Venta'] ) )

			self.label_Fecha_Ultima_Actualizacion.setText( str( Fecha ) )
			

	def Obtener_Filas_del_txt(self , NameFile_txt):
		list_rows_in_txt = [ ( str( linea.replace('\n',"") ).encode('cp1252') ).decode('utf-8') for linea in open( NameFile_txt) ]
		return list_rows_in_txt

	def generando_tabla_Dolar( self ):
		self.Table_Cant_Dolares.setColumnCount( 1 )
		self.Table_Cant_Dolares.setColumnWidth(0, 335)
		self.Table_Cant_Dolares.setHorizontalHeaderLabels(['DOLARES INGRESADOS'])

		DOLARES = self.Obtener_Filas_del_txt('DOLARES_ingresadas.txt')

		self.Table_Cant_Dolares.setRowCount( len(DOLARES) + 25 )

		cont = 0
		for DOLAR in DOLARES:
			self.Table_Cant_Dolares.setItem(cont ,0 , QTableWidgetItem( DOLAR ) )
			cont += 1

	def guardando_datos_tabla_Dolar( self ):
		List_Errores = []
		Lista_Correctos = []

		for num_fila in range( self.Table_Cant_Dolares.rowCount() ):
			try:
				numero = self.Table_Cant_Dolares.item( num_fila , 0).text()
				try:
					if numero != '':
						Lista_Correctos.append( float( numero ) )
				except:
					List_Errores.append( num_fila+1 ) #El numero de la fila en tabla comienza en 1
			except:
				pass

		if len( List_Errores ) == 0:
			with open( 'Dolares_ingresadas.txt' , 'w' ) as file:
				for uva in Lista_Correctos:
					file.write( str(uva) + "\n" )
			
			self.actualizando_total_pesos_Dolar_Venta() #Actualizamos el total de Dolares

			self.ventana_emergente_de_texto( "Ventana Tabla Dolar" , f"Los Datos se Guardaron Correctamente      " )
		else:	
			self.ventana_emergente_de_texto( "Ventana Tabla Dolar" , f"Error en Fila: {str(List_Errores)}      " )

	def ventana_emergente_de_texto( self , titulo_ventana , texto_ventana ):
		dlg = QMessageBox(self)
		dlg.setWindowTitle( titulo_ventana )
		dlg.setText( texto_ventana )
		dlg.show()

	def actualizando_total_pesos_Dolar_Venta( self ):
		total = 0
		for num_fila in range( self.Table_Cant_Dolares.rowCount() ):
			try:
				total += float( self.Table_Cant_Dolares.item( num_fila , 0).text() )
			except:
				pass
		Formato_Precio = parse.compile( '{Entero:d}.{Decimal}' )
		resu = Formato_Precio.parse( str( total * float( self.label_Dolar_Blue_Venta.text() ) ) )
		self.label_Total_en_Pesos_Dolar.setText( f"${ resu['Entero'] }.{ resu['Decimal'][0:2] }" )