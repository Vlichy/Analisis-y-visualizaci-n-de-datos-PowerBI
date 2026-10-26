# Estadística, análisis y visualización de datos — Online Retail II

Proyecto de análisis de transacciones de un comercio minorista online del Reino Unido. Estudia **qué características de un pedido están asociadas con un mayor importe de compra**, mediante estadística descriptiva, visualizaciones y regresión lineal múltiple.

**[Consultar el análisis completo y sus resultados](notebooks/analisis_estadistico.ipynb).**

> El material disponible corresponde a Python y Jupyter. Aunque el nombre del repositorio menciona Power BI, esta entrega no incluye informes `.pbix`, modelos de Power BI ni medidas DAX.

## Datos y procedencia

El proyecto identifica su fuente como **Online Retail II**, de Daqing Chen, publicado por UCI Machine Learning Repository: [ficha del dataset](https://archive.ics.uci.edu/dataset/502/online+retail+ii), [DOI 10.24432/C5CG6D](https://doi.org/10.24432/C5CG6D).

El CSV procesado incluido contiene **535.186 filas y 15 columnas**, según las salidas guardadas del notebook, y corresponde al periodo diciembre de 2010 a diciembre de 2011. No representa los dos años completos del dataset fuente. El Excel original no forma parte de esta carpeta; `src/io.py` contempla la hoja `Year 2010-2011`.

| Campos | Contenido |
| --- | --- |
| `Invoice`, `StockCode`, `Description` | Factura, código y descripción del producto |
| `Quantity`, `Price`, `TotalAmount` | Cantidad, precio e importe de la línea |
| `InvoiceDate`, `Country`, `Customer ID` | Fecha, país e identificador de cliente |
| `IsCancelled` | Identificación de facturas cuyo código comienza por C |
| `Year`, `Month`, `MonthName`, `DayOfWeek`, `Hour` | Variables temporales derivadas |

### Licencia y privacidad de los datos

UCI distribuye Online Retail II bajo [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/), que permite compartir y adaptar los datos con atribución. Cita: **Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D.**

El CSV es una versión transformada: se aplican limpieza y variables derivadas, descritas más abajo. Esta atribución corresponde al dataset y no asigna una licencia al código del proyecto.

Se conservan los identificadores de cliente y factura del conjunto público para mantener el análisis reproducible. No hay columnas de nombre, correo, teléfono o dirección postal; no deben cruzarse estos identificadores con fuentes destinadas a identificar personas. La revisión de los archivos no detectó credenciales ni correos electrónicos. No se dispone del Excel original en esta entrega para realizar una comparación íntegra de procedencia.

## Metodología

1. **Limpieza y transformación en los módulos Python.** `src/cleaning.py` elimina duplicados, descarta descripciones ausentes, normaliza textos, convierte fechas y conserva precios no negativos. Mantiene los identificadores de cliente ausentes. `src/features.py` calcula `TotalAmount = Quantity * Price`, identifica cancelaciones y crea variables temporales. El notebook parte del CSV ya procesado; no ejecuta de nuevo esta fase.
2. **Selección de ventas.** Se excluyen cancelaciones y líneas con cantidad o precio no positivos: quedan **524.879 líneas de venta** en las salidas guardadas.
3. **Agregación por pedido.** Se suman importe y unidades y se cuentan productos distintos por `Invoice`: inicialmente **19.960 pedidos**. Se comprueba la consistencia de país, cliente y fecha. Las 42 facturas con marcas temporales distintas difieren como máximo un minuto; se toma la fecha mínima.
4. **Tratamiento de cancelaciones posteriores.** Se buscan coincidencias de cliente, producto, precio y cantidad con operaciones posteriores de signo contrario. Se excluyen **81 pedidos candidatos a reversión completa dentro de 24 horas** y quedan **19.879 pedidos**. Los demás valores extremos se conservan; el emparejamiento no garantiza detectar todas las devoluciones.
5. **Exploración.** Estadísticos descriptivos, distribuciones, criterio IQR, correlaciones y comparaciones temporales y geográficas.
6. **Modelización.** Regresión OLS, controles temporales, diagnóstico VIF, residuos, gráfico Q-Q y contraste de Breusch-Pagan. La inferencia final utiliza errores estándar robustos HC3 ante la heterocedasticidad detectada.

## Modelo y resultados

La unidad de observación es el pedido. Se modela el logaritmo del importe con el logaritmo de las unidades, el logaritmo de los productos distintos, una variable que distingue pedidos internacionales y controles categóricos de mes y día de la semana:

```text
LogOrderAmount ~ LogTotalUnits + LogUniqueProducts
                 + International + C(DayOfWeek) + C(Month)
```

Los resultados siguientes proceden de las **salidas ya guardadas** en el notebook; no se han vuelto a estimar durante la preparación del repositorio.

| Variable principal | Coeficiente | Interpretación, manteniendo constantes las demás variables |
| --- | ---: | --- |
| `LogTotalUnits` | 0,6738 | Un 1 % más de unidades se asocia aproximadamente con un 0,674 % más de importe |
| `LogUniqueProducts` | 0,1388 | Un 1 % más de productos distintos se asocia aproximadamente con un 0,139 % más de importe |
| `International` | 0,2270 | Diferencia estimada de aproximadamente +25,5 % respecto al Reino Unido, mediante `exp(β) − 1` |

El **R² ajustado es 0,7565**. Las tres asociaciones principales mantienen significación estadística con HC3 (`p < 0,001`). El ajuste corresponde al logaritmo del importe en la muestra analizada; no es una medida de precisión predictiva fuera de muestra.

## Visualizaciones

El notebook contiene figuras integradas: histogramas de importe, unidades y variedad; distribuciones antes y después de la transformación logarítmica; dispersiones entre importe, unidades y variedad; residuos frente a valores ajustados y gráfico Q-Q.

`src/visualization.py` contiene además funciones para evolución mensual de facturación, rankings de productos, países y clientes, y productos cancelados. Estas funciones forman parte del código disponible; no se presenta aquí un dashboard Power BI ni se afirma que esos gráficos adicionales se hayan ejecutado en el notebook estadístico.

## Conclusiones y limitaciones

El volumen de unidades y la variedad de productos presentan asociaciones positivas con el importe. La diferencia entre pedidos internacionales y del Reino Unido persiste tras incorporar controles temporales. Estos controles apenas modifican las asociaciones principales.

Los resultados son **observacionales y no causales**. Existe una relación estructural entre cantidad e importe. El análisis también está condicionado por la concentración de pedidos en el Reino Unido, la heterogeneidad de los mercados internacionales, la cobertura temporal limitada y el tratamiento aproximado de las cancelaciones. HC3 aborda la inferencia ante heterocedasticidad, pero no resuelve por sí solo otras limitaciones del modelo.

## Herramientas y reproducción

Python, pandas, NumPy, Matplotlib y statsmodels. Las versiones declaradas se conservan en [requirements.txt](requirements.txt); los metadatos del notebook registran Python **3.14.5**.

Desde la raíz del repositorio, en PowerShell, con Python instalado:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install jupyterlab ipykernel
.\.venv\Scripts\python.exe -m jupyterlab
```

Abrir `notebooks/analisis_estadistico.ipynb`, seleccionar el kernel del entorno y ejecutar las celdas en orden, con `notebooks/` como directorio de trabajo: la ruta de entrada es `../data/onlineRetail_clean.csv`. Las celdas finales con `pip freeze` documentan el entorno y no son necesarias para el análisis.

El CSV incluido permite iniciar directamente la fase estadística. Para reutilizar `load_excel()` con el archivo fuente sería necesario descargar el Excel de UCI e instalar `openpyxl`, dependencia opcional que no figura en el archivo original de requisitos. No se ha modificado el notebook, los módulos ni las versiones declaradas, ni se ha validado aquí una ejecución completa en un entorno nuevo.

## Estructura

```text
.
├── data/
│   └── onlineRetail_clean.csv
├── notebooks/
│   └── analisis_estadistico.ipynb
├── src/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── features.py
│   ├── io.py
│   ├── utils.py
│   └── visualization.py
├── docs/
│   └── README_original.md
├── .gitignore
├── README.md
└── requirements.txt
```

El README previo se conserva sin cambios en [docs/README_original.md](docs/README_original.md). Las salidas, tablas y figuras permanecen integradas en el notebook; no se generan copias innecesarias. Los archivos de caché locales se excluyen de Git.

## Tamaño de los archivos

`data/onlineRetail_clean.csv` ocupa **68.017.363 bytes (64,87 MiB)**. Se conserva íntegro en Git: supera el umbral de aviso de 50 MiB, pero no el límite de 100 MiB por archivo. La subida desde el navegador tiene un límite de 25 MiB; para este archivo se utiliza Git. Si futuras versiones superan 100 MiB, deberá emplearse Git LFS o distribuirse el dataset mediante Releases sin eliminar el original. Véase la [documentación de GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).
