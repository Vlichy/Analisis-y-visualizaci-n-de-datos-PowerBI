# Análisis estadístico — Online Retail II

## Descripción

Este proyecto constituye la continuación estadística del análisis realizado previamente sobre el dataset **Online Retail II**.

En la fase anterior del proyecto se realizó mediante Python la limpieza, transformación y análisis exploratorio de los datos. En esta fase se utiliza el dataset procesado para estudiar, mediante técnicas estadísticas y econométricas, qué características de los pedidos están asociadas con un mayor importe de compra.

## Pregunta de investigación

**¿Qué características de un pedido están asociadas con un mayor importe de compra?**

## Dataset

El dataset Online Retail II contiene transacciones de un comercio minorista online del Reino Unido.

Para el análisis estadístico, las líneas de producto se agregan a nivel de pedido (`Invoice`), utilizando cada pedido como unidad de observación.

Tras el tratamiento de ventas y cancelaciones, la muestra estadística final contiene **19.879 pedidos**.

## Metodología

El análisis incluye:

- estadística descriptiva;
- análisis de distribuciones y valores atípicos;
- tratamiento de cancelaciones;
- transformaciones logarítmicas;
- análisis de correlaciones;
- análisis temporal y geográfico;
- regresión lineal múltiple mediante OLS;
- diagnóstico de multicolinealidad mediante VIF;
- análisis de residuos;
- contraste de heterocedasticidad de Breusch-Pagan;
- errores estándar robustos HC3.

## Modelo final

La variable dependiente es el logaritmo del importe del pedido (`LogOrderAmount`).

Las principales variables explicativas son:

- `LogTotalUnits`: logaritmo del número total de unidades.
- `LogUniqueProducts`: logaritmo del número de productos diferentes.
- `International`: variable dummy que diferencia pedidos del Reino Unido y pedidos internacionales.

El modelo final incorpora además controles categóricos por mes y día de la semana.

## Principales resultados

El modelo final alcanza un **R² ajustado de 0,7565**.

Los principales resultados indican que:

- un aumento del 1 % en el número de unidades está asociado aproximadamente con un aumento del **0,674 %** en el importe del pedido;
- un aumento del 1 % en el número de productos diferentes está asociado aproximadamente con un aumento del **0,139 %** en el importe;
- los pedidos internacionales presentan un importe estimado aproximadamente **25,5 % superior** al de los pedidos del Reino Unido, manteniendo constantes las restantes variables incluidas.

Las tres asociaciones permanecen estadísticamente significativas utilizando errores estándar robustos HC3.

Los resultados representan asociaciones estadísticas y no deben interpretarse como relaciones causales.

Dependencias

El proyecto utiliza principalmente:

pandas
numpy
matplotlib
statsmodels

Las versiones utilizadas se encuentran especificadas en requirements.txt.

## Estructura del proyecto

```text
proyecto_estadistica/
│
├── data/
│   └── onlineRetail_clean.csv
│
├── notebooks/
│   └── analisis_estadistico.ipynb
│
├── src/
│
├── README.md
└── requirements.txt