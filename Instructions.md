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

---

## Notas técnicas y recomendaciones adicionales

- **Script Python de generación**
  - El script debería:
    - Leer el fichero de muestra (JSON).
    - Extraer la fecha de la muestra y las claves/valores de ejemplo.
    - Para cada día desde la fecha de la muestra hasta la fecha actual:
      - Generar un nuevo JSON con la misma estructura, variando numéricamente los valores en un rango de ±10 unidades (utilizar ruido aleatorio).
      - Guardar cada JSON en la carpeta correspondiente al tipo de datos, nombrando los ficheros con la fecha (ej. `tipoA_YYYY-MM-DD.json`).
  - Sugerencia: usar `datetime`, `random`/`numpy` y `json` para implementar la generación.

- **Estrategia de carga en Power BI**
  - Importar cada carpeta (por tipo de datos) como fuente JSON (o como carpeta de archivos).
  - En Power Query:
    - Expandir objetos JSON y normalizar la estructura.
    - Convertir la columna de fecha al tipo `Date`.
    - Agrupar por fecha si fuera necesario y usar agregaciones (sum, average, min, max) para obtener una única fila por fecha.
    - Eliminar duplicados y asegurarse de que la columna índice/clave sea la fecha.

- **Cálculo de YoY y MoM**
  - Añadir columnas calculadas en Power BI (DAX) para:
    - **MoM%** = `(ThisMonth - PreviousMonth) / PreviousMonth`.
    - **YoY%** = `(ThisYear - PreviousYear) / PreviousYear`.
  - Manejar divisiones por cero y fechas sin periodo anterior con `IF` o funciones condicionales.

- **Visuales recomendados**
  - Series temporales (line charts) para progresión diaria.
  - Tarjetas métricas para mostrar Media, Máximo y Mínimo.
  - Gráficos de barras para comparaciones mensuales/anuales.
  - Tabla o matriz con detalle diario (posibilidad de exportar a Excel).
  - Slicers para rango de fechas y filtros adicionales.

- **Estética (ejemplo para petrolera)**
  - Paleta sugerida: tonos azul oscuro, gris petróleo y acentos en naranja o amarillo.
  - Cabecera con logo a la izquierda, título del reporte y selector de rango de fechas visible en la parte superior.
  - Uso de iconos (bombas, tanques, combustibles) de forma sutil y profesional.
  - Espaciado claro, tipografía legible y contraste suficiente para pantallas y proyección.

---

## Entregables propuestos

1. Script Python `generar_ficheros_diarios.py` que:
   - Toma como entrada: ruta del fichero de muestra y carpeta destino.
   - Crea la estructura de carpetas por tipo de datos.
   - Genera un JSON por día con variación aleatoria.

2. Carpeta zip con los ficheros JSON generados (o ruta a carpeta local).

3. Documento/Guía en Markdown (este archivo) con:
   - Instrucciones paso a paso para la carga y transformación en Power BI.
   - Ejemplos de fórmulas DAX para YoY y MoM.
   - Recomendaciones de visualización y estilo.

4. Archivo Power BI (opcional) con un reporte de ejemplo usando los datos generados.

---

Si quieres, puedo además:
- Generar el script Python de ejemplo aquí mismo.
- Ejecutarlo (si me facilitas la fecha de muestra y/o el fichero de muestra).
- Crear los JSON y empaquetarlos para descarga.

