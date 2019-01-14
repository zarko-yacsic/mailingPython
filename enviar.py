from pymongo import MongoClient
import mandrill
import time
import json
import sys
import re
import hashlib
import base64

# ......... F U N C T I O N S ................

# Validar correos
def isValidEmail(correo):
	if len(correo) > 7:
		if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", correo) != None:
			return True
		else:
			return False
	else:
		return False


# Cambiar primera letra de un texto a mayuscula...
# (tipo: 'default'=Solo primera palabra; 'default'=Todas las palabras)
def capitalText(texto, tipo = 'default'):
	if tipo == 'default':
		texto = texto.lower()
		texto = texto.capitalize()
	if tipo == 'all':
		texto = texto.title()
	return texto


# Reemplazar todas las apariciones de una subcadena dentro de un string...
# (Valores de busqueda y de reemplazo deben ser pasados como array)
def replaceMultipleStrings(my_string, my_search, my_replace):
	my_list = list(zip(my_search, my_replace))
	for my_item in my_list:
	    my_string = my_string.replace(my_item[0], my_item[1])
	return my_string


# Codificar un string a base64 (El texto pasado DEBE ser de tipo 'string')...
def base64Encode(my_string, enc = 'utf-8'):
	my_string = base64.b64encode(bytes(my_string, enc))
	my_string = my_string.decode(enc)
	return my_string


# Codificar un string a md5 (El texto pasado DEBE ser de tipo 'string')...
def md5Encode(my_string):
	result = hashlib.md5(my_string.encode())
	return result.hexdigest()

# .................................................................
# 
# 
# 
# 

host = '13.52.107.12';
database = 'db_zyacsic'
username = 'zyacsic'
password = 'S7&KkB4m'
client = MongoClient('mongodb://' + username + ':' + password + '@' + host + '/' + database)
db = client[database]
url_tga = 'http://www.empresastga.com'


if db.authenticate(username, password):
	
	# Obtener coleccion...
	my_collection = db['gclient_envios']
	num_items = 0
	
	if my_collection.count() > 0:
		for item in my_collection.find():

			# Validar direccion de correo...
			if isValidEmail(item['correo'].lower().strip()) == True and item['enviado'] == 0:
				id_document = item['_id']

				# Si tiene vendedor asignado...
				template_vendedor = ''
				if item['id_vendedor'] > 0 or item['id_vendedor'] != '':
					template_vendedor = '<img src="' + item['img_vendedor'] + '" width="100%"" height="auto" alt="">'

				# Si esta personalizado (Tiene nombre)...
				con_nombre = ''
				if item['con_nombre'] > 0 or item['con_nombre'] != '':
					con_nombre = '<span style="font-size: 12pt; font-weight: 400; color: #425973;">Estimado(a) ' + item['nombre'] + ' ' + item['apellido'] + ',</span>'

				# Tipo de diseno (1=imagen; 2=html)...
				if item['tipo_diseno'] == 1:
					bases_legales = 0;
					bases_legales_texto = '';
					
					if bases_legales != '' or bases_legales != None:
						bases_legales_texto = """
							<tr>
								<td>
									<p style="color: #848484;font-family: Helvetica,Arial,sans-serif;font-weight: normal;
									text-align:center;line-height: 19px;font-size: 10px;margin: 0 0 10px; padding: 0;
									background-color: #fcfcfc" align="center">""" + bases_legales + """</p>
								</td>
							</tr>"""

						contenido = """<table width="100%" bgcolor="#FFF" border="0" cellpadding="0" cellspacing="0">
									<tr>
										<td>
											<table class="content" align="center" cellpadding="0" cellspacing="0" border="0">
												<tr>
													<td>
														<p>""" + con_nombre + """</p>
														<center>
															<p><a href='""" + item['url_link'] + """' target="_blank">
															<img src='""" + item['template_html'] + """' width="100%" height="auto" alt=""></a></p>
															<p>""" + template_vendedor + """</p>
														</center>
													</td>
												</tr>""" + bases_legales_texto + """
											</table>
										</td>
									</tr>
								</table>"""
				
				
				if item['tipo_diseno'] == 2:
					t_buscar = ['{{NOMBRE}}', '{{APELLIDO}}', '{{ANIO}}', '{{MES}}', '{{DIA}}', '{{PROYECTO}}']
					t_reemplazar = [capitalText(item['nombre'], 'all'), capitalText(item['apellido'], 'all'), time.strftime("%Y"), time.strftime("%m"), time.strftime("%d"), item['proyecto']]
					contenido = replaceMultipleStrings(item['template_html'], t_buscar, t_reemplazar)

				# Mostrar encuesta...
				encuesta = ''
				b64_string = str(item['id_campania']) + '-' + str(item['id_correo'])  + '-' + str(item['tipo']) + '-' + time.strftime("%Y%m")
				b64_string_encoded = base64Encode(b64_string)


				if item['estado_encuesta'] == 1:
					respuesta1 = base64Encode('1-' + b64_string)
					respuesta2 = base64Encode('2-' + b64_string)
					respuesta3 = base64Encode('3-' + b64_string)
					respuesta4 = base64Encode('4-' + b64_string)
					respuesta5 = base64Encode('5-' + b64_string)
					encuesta = """<table class="tblevaluacion" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#e9e9e9; text-align:center;">
                                <tr>
                                    <td>&nbsp;</td>
                                </tr>
                                <tr>
                                    <td align="center">
                                        <table width="768" border="0" cellspacing="0" cellpadding="0">
                                            <tr style="text-align: center;">
                                                <td width="588" align="center"><span class="textocarita" style="color:#176963; clear:both;">&iquest;Qu&eacute; tan relevante fue esta informaci&oacute;n para usted?</span
                                                ></td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td>&nbsp;</td>
                                </tr>
                                <tr>
                                    <td>&nbsp;</td>
                                </tr>
                                <tr>
                                    <td align="center">
                                        <table class="tblcaras" width="768" border="0" cellspacing="0" cellpadding="0">
                                            <tr style="text-align: center;">
                                                <td width="90">&nbsp;</td>
                                                <td width="50" style="width:50px; height:50px; margin:0px 5px; word-wrap:normal; display:inline-block" align="justify" valign="baseline">
                                                    <a href='""" + url_tga + """/landing/respond2.php?k=""" + respuesta1 + """-""" + md5Encode(respuesta1) + """' title="Terrible">
                                                        <img width="50" height="50" src='""" + url_tga + """/images/sitio/1-blackface.png' alt="Terrible">
                                                    </a>
                                                </td>
                                                <td width="50" style="width:50px; height:50px; margin:0px 5px; word-wrap:normal; display:inline-block" align="justify" valign="baseline">
                                                    <a href='""" + url_tga + """/landing/respond2.php?k=""" + respuesta2 + """-""" + md5Encode(respuesta2) + """' title="Malo">
                                                        <img width="50" height="50" src='""" + url_tga + """/images/sitio/2-blackface.png' alt="Malo">
                                                    </a>
                                                </td>
                                                <td width="50" style="width:50px; height:50px; margin:0px 5px; word-wrap:normal; display:inline-block" align="justify" valign="baseline">
                                                    <a href='""" + url_tga + """/landing/respond2.php?k=""" + respuesta3 + """-""" + md5Encode(respuesta3) + """' title="Regular">
                                                        <img width="50" height="50" src='""" + url_tga + """/images/sitio/3-blackface.png' alt="Regular">
                                                    </a>
                                                </td>
                                                <td width="50" style="width:50px; height:50px; margin:0px 5px; word-wrap:normal; display:inline-block" align="justify" valign="baseline">
                                                    <a href='""" + url_tga + """/landing/respond2.php?k=""" + respuesta4 + """-""" + md5Encode(respuesta4) + """' titletitle="Bueno">
                                                        <img width="50" height="50" src='""" + url_tga + """/images/sitio/4-blackface.png' alt="Bueno">
                                                    </a>
                                                </td>
                                                <td width="50" style="width:50px; height:50px; margin:0px 5px; word-wrap:normal; display:inline-block" align="justify" valign="baseline">
                                                    <a href='""" + url_tga + """/landing/respond2.php?k=""" + respuesta5 + """-""" + md5Encode(respuesta5) + """' titletitle="Excelente">
                                                        <img width="50" height="50" src='""" + url_tga + """/images/sitio/5-blackface.png' alt="Excelente">
                                                    </a>
                                                </td>
                                                <td width="90">&nbsp;</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td>&nbsp;</td>
                                </tr>
                                <tr>
                                    <td>&nbsp;</td>
                                </tr>
                            </table>"""

                
				# Insertar contenido dentro de la plantilla final...
				html_enviar = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
					<html xmlns:v="urn:schemas-microsoft-com:vml" 
					xmlns:o="urn:schemas-microsoft-com:office:office" 
					xmlns:w="urn:schemas-microsoft-com:office:word" 
					xmlns:m="http://schemas.microsoft.com/office/2004/12/omml" 
					xmlns="http://www.w3.org/TR/REC-html40">
					    <head>
					        <meta name="viewport" content="width=device-width, user-scalable=no">
					        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
					        <style type="text/css">
					        body { margin: 0; padding: 0; min-width: 100%!important;}
					        .content { width: 100%; max-width: 600px;}
						    .textocarita { font-family: Helvetica, Arial, sans-serif; font-size: 20px;}
						    @media only screen and (max-width: 599px){
					            img.pattern {
					                max-width: 100%;
					                height: auto !important;
					            }
					        }
					        @media only screen and (min-device-width : 320px) and (max-device-width : 623px), (max-width : 623px){
						        .tblevaluacion { width: 100% !important;}
						        .textocarita { font-size: 80%;}
					            .tblevaluacion td { width: 100% !important; display:block;}
					            .tblcaras td { width: 15% !important; display:block;}
					        }
					        </style>
					    </head>
					    <body yahoo style="text-align: center;">
						    """ + contenido + """
						    """ + encuesta + """
						    <div style="word-break:break-word;border-collapse:collapse!important;vertical-align:top;text-align:center;color:#505050;font-family:Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:0" valign="top" align="center">
								<p style="color:#848484;font-family:Helvetica,Arial,sans-serif;font-weight:normal;text-align:center;line-height:19px;font-size:10px;margin:0 0 10px;padding:0" align="center">
									&copy; """ + time.strftime("%Y") + """ """ + item['from_nombre'] + """ - Todos los derechos reservados
								</p>
								<p style="color:#848484;font-family:Helvetica,Arial,sans-serif;font-weight:normal;text-align:center;line-height:19px;font-size:10px;margin:0 0 10px;padding:0" align="center">
									Est&aacute;s recibiendo este correo porque eres un contacto de """ + item['from_nombre'] + """<br>
									Si deseas dejar de recibir estos correos, puedes  <a href='""" + url_tga + """/landing/unsubscribe.php?k=""" + b64_string_encoded + """' style="color:#2ba6cb;text-decoration:none" target="_blank" data-saferedirecturl=" ">darte de baja</a>.
								</p>
							</div>
					    </body>
					</html>""";

				html_enviar = str(html_enviar)

				# ...... Para desarrollo y pruebas, se puede visualizar el HTML previo a enviar, guardandolo como un archivo .html
				# f = open('prueba/correo_' + str(item['id_correo']) + '.html','w')
				# f.write(html_enviar)
				# f.close()

				
				# Definir API KEY Mandrill...
				if item['tipo'] == 1:
					api_key = 'g2InZB3UVJiLHNFOsU7fqg'
				if item['tipo'] == 2 or item['tipo'] == 3:
					api_key = 'lfrxmY6DVJZpoCuQeZJjdA'

				# Enviar correos...
				try:
					mandrill_client = mandrill.Mandrill(api_key)
					tags = str(item['id_campania']) + '_' + str(item['id_inmobiliaria']) + '_' + str(item['id_proyecto'])
					message = {
    					'from_email': item['from_correo'],
					    'from_name': item['from_nombre'],
    					'html': html_enviar,
					    'important': False,
					    'merge': True,
                        'merge_language' : 'mailchimp',
    					'subject': item['campania'],
					    'tags': [tags],
    					'to': [{
	    						'email': item['correo'].lower().strip(),
	    						'name': item['nombre'] + ' ' + item['apellido'],
	    						'type': 'to'
    						}],
					    'track_clicks': True,
					    'track_opens': True,
					    'tracking_domain': None,
					    'url_strip_qs': None,
					    'view_content_link': None
					   }
					async = False
					ip_pool = 'Main Pool'
					fecha_enviado = time.strftime("%H:%M:%S")
					result = mandrill_client.messages.send(message, async, ip_pool, fecha_enviado)

					# Cuando el envio es exitoso, actualizar 'enviado' a 1 e incrementar contador...
					if result[0]['status'] == 'sent':
						my_collection.update_one({'_id': id_document}, {'$set': { 'enviado': 1}})
						num_items = num_items + 1
						#print (str(id_document) + ': ' + item['nombre'] + ' ' + item['apellido'] + ' <' + item['correo'] + '> | ' + item['campania'])

				except mandrill.Error as e:
				    # Mandrill errors are thrown as exceptions
				    print('A mandrill error occurred: %s - %s' % (e.__class__, e))
				    # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
				    raise	
			# .................................
		
		#print ('-.Elementos enviados : ' + str(num_items))
		# .................................

	# No hay documentos en la coleccion...
	else:
		print('No se encontraron elementos en esta coleccion.')

# Error de autentificacion a la BD...
else:
	print('No se ha podido conectar a la BD solicitada.')