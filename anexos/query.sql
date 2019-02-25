
# Query de ejemplo usada en el script PHP actual
# (La estructura de los documentos JSON en MongoDBTodas incluye todas las columnas generadas)
# 
# Observación: El nombre de tabla 'envio_201812' es sólo un ejemplo, ya que este nombre se genera de manera dinámica

SELECT a.idEnvio AS campania, b.idLista AS idcorreo, a.idInmobiliaria AS inmo, 
                        a.idEnvioProy AS proyec,
                        a.nombre AS nombrecampania, a.fromCorreo, a.fromNombre, 
                        a.estadoencuesta, b.nombre, b.apellido, 
                        b.correo,c.descripcion AS templatehtml, a.idTipo AS tipo, 
                        conNombre,IFNULL(d.idListaNegra, 0) AS idListaNegra,
                        urlLink,idPais,NOW() AS fechaIng, b.horaEnvio, 
                        c.tipoDiseno, b.idVendedor,b.proyecto
                FROM gclient_envio a
                        INNER JOIN envio_201812 b ON a.idEnvio = b.idEnvio
                        LEFT JOIN gclient_template c ON a.idTemplate=c.idTemplate
                        LEFT JOIN gclient_listaNegra d ON b.correo=d.correo
                        AND a.idInmobiliaria=d.idInmobiliaria
                WHERE  a.estado =1
                        AND b.estado = 0
                        AND DATE(fechaEnvio) = DATE(NOW())
                        AND CAST(horaEnvio AS time) < CURTIME()
                GROUP BY b.correo, a.idEnvio 
                ORDER BY campania, b.correo ASC
                LIMIT 100;