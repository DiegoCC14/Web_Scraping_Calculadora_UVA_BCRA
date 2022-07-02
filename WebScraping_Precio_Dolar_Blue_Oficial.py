from bs4 import BeautifulSoup
import requests , parse
from datetime import datetime
import parse

def Obteniendo_precio_Dolar_Blue_Oficial_hoy():
	try:

		tiempo_ahora = str( datetime.now() )[0:19]
		
		url_Dolar_LaNacion = "https://www.lanacion.com.ar/dolar-hoy/"
		page = requests.get( url_Dolar_LaNacion )
		soup = BeautifulSoup( page.content , "html.parser" )
		try:
			table_LN = soup.find_all( "ul" , class_= 'mod-dolar' )
			
			Dolar_Oficial_Compra = table_LN[0].find_all( "li" )[0].div.p.find_all( 'strong' )[0].text
			Dolar_Oficial_Venta = table_LN[0].find_all( "li" )[0].div.p.find_all( 'strong' )[1].text

			Dolar_Blue_Compra = table_LN[0].find_all( "li" )[1].div.p.find_all( 'strong' )[0].text
			Dolar_Blue_Venta = table_LN[0].find_all( "li" )[1].div.p.find_all( 'strong' )[1].text

			Formato_Dolar = parse.compile( "${Entero:d},{Decimal:d}" )
			
			Dol_Oficial_Compra_result = Formato_Dolar.parse( Dolar_Oficial_Compra )
			Dol_Oficial_Venta_result = Formato_Dolar.parse( Dolar_Oficial_Venta )

			Dol_Blue_Compra_result = Formato_Dolar.parse( Dolar_Blue_Compra )
			Dol_Blue_Venta_result = Formato_Dolar.parse( Dolar_Blue_Venta )
			
			Dolar_Oficial = { 'Compra': float( f"{ Dol_Oficial_Compra_result['Entero'] }.{ Dol_Oficial_Compra_result['Decimal'] }" ),
				'Venta': float( f"{ Dol_Oficial_Venta_result['Entero'] }.{ Dol_Oficial_Venta_result['Decimal'] }" ) }
			
			Dolar_Blue = { 'Compra': float( f"{ Dol_Blue_Compra_result['Entero'] }.{ Dol_Blue_Compra_result['Decimal'] }" ),
				'Venta': float( f"{ Dol_Blue_Venta_result['Entero'] }.{ Dol_Blue_Venta_result['Decimal'] }" ) }

			return( Dolar_Oficial , Dolar_Blue , tiempo_ahora )
		
		except:
			return(-1 , -1, tiempo_ahora )
	except:
		return(-2 , -2, tiempo_ahora)

if __name__ == "__main__":
	( valor_Dolar_Blue , valor_Dolar_Oficial , Fecha ) = Obteniendo_precio_Dolar_Blue_Oficial_hoy()
	if valor_Dolar_Blue == -1:
		print("Error al encontrar el valor!!!")
	elif valor_Dolar_Blue == -2:
		print("Error Codigo o Pagina!!!")
	else:
		print( f"Dolar Blue: { valor_Dolar_Blue['Compra'] } , { valor_Dolar_Blue['Venta'] }" )
		print( f"Dolar Oficial: {valor_Dolar_Oficial['Compra'] } , { valor_Dolar_Oficial['Venta'] }" )