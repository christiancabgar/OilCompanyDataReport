# Instrucciones para generación de ficheros, carga en Power BI y diseño de reporte

A partir de las muestras de ficheros adjuntos:

1. **Generación de ficheros diarios**
   - Puesto que solo hay un fichero de muestra para cada tipo de datos, generar con un **script Python** un fichero para cada día, desde el día de la muestra proporcionada hasta el día actual.
   - Se tratará de que los valores de los parámetros simulen cierta variación aleatoria (sobre **±10 unidades**), para que los datos resultantes no sean absolutamente iguales.

2. **Organización en carpetas**
   - Los ficheros de cada tipo de datos se agregarán en una **carpeta distinta**, para facilitar la carga agregada de cada tipo de datos en Power BI.

3. **Transformaciones en Power BI**
   - Una vez cargados los datos de todos los JSON en Power BI, se realizarán las transformaciones adecuadas para que la tabla correspondiente a cada tipo de datos contenga **exclusivamente una fila por cada fecha**.
   - Cada fila deberá contener los valores correspondientes a cada día en las columnas adecuadas.
   - **Pista:** cuidado con la forma de rellenar, la columna índice y la eliminación de duplicados.

4. **Reporte y visualizaciones**
   - Generar un reporte con representaciones gráficas de los datos, donde se pueda ver:
     - **Progresión temporal**.
     - **Estadísticos**: Media, Máximo, Mínimo, etc.
     - **YoY** (variación porcentual Year over Year).
     - **MoM** (variación porcentual Month over Month).
     - **Tabla con detalle de datos**.

5. **Filtros**
   - El reporte debe permitir filtrar por:
     - **Intervalo de fechas**.

6. **Aspecto visual**
   - Trabajad no solo el contenido, sino el **aspecto visual** del propio reporte, considerando que el cliente en este caso es una **petrolera**.
   - Posible cabecera con **logo** o **colores corporativos**.
   - Dejad volar la creatividad para adaptar el diseño a la identidad corporativa (paleta de colores, tipografías, iconografía relacionada con energía/petróleo, layout sobrio y profesional).
