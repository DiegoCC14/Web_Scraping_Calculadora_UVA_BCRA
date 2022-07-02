from bs4 import BeautifulSoup
import requests , parse
from datetime import datetime

def Obteniendo_precio_UVA_hoy():
	try:
		
		tiempo_ahora = str( datetime.now() )[0:19]

		url_BCRA_Principales_Variables = "http://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables.asp"

		page = requests.get( url_BCRA_Principales_Variables )
		soup = BeautifulSoup( page.content , "html.parser" )
		
		table_BCRA = soup.find_all( "table" , class_="table-BCRA" )
		for tr in table_BCRA[0].tbody:
			try:
				filas_td = tr.find_all( "td" )
				text_fila = filas_td[0].a.text
				if text_fila.find("Unidad de Valor Adquisitivo (UVA)") == 0: #Si el valor es encontrado en el texto retorna 0
					formato_precio = parse.compile( '{Entero:d},{Decimal:d}' ) #Exprecion regular para encontrar parte entero y decimal
					set_resultados = formato_precio.parse( filas_td[2].text )
					return ( float( f"{set_resultados['Entero']}.{set_resultados['Decimal']}" ) , tiempo_ahora ) #Precio de la UVA hoy y fecha
			except:
				pass
		return(-1 , tiempo_ahora )
	except:
		print("Error en Pagina o Codigo")
		return(-2 , tiempo_ahora)

if __name__ == "__main__":
	valor_UVA = Obteniendo_precio_UVA_hoy()
	if valor_UVA == -1:
		print("Error al encontrar el valor!!!")
	elif valor_UVA == -2:
		print("Error Codigo o Pagina!!!")
	else:
		print( f"UVA: {valor_UVA}" )