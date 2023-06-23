# AED 1 🤓

## 1) Cargamos los datos 📕

```
import pandas as pd
data=pd.read_csv("data/customer_dataset.csv", sep = ",")
```

## 4) Variables categóricas

- Analicen `paymentMethodType`
- Para la creación de la query consideren evaluar: `"frequency<=30"` 

# AED 2 😧

## 1) Análisis de variables categóricas

- Analicen `fraudulent`

## 2) Análisis bivariado

### 2.A) Análisis de categórica vs. categórica

- Analicen `fraudulent` y `transactionFailed`

### 2.B) Análisis de numérica vs. categórica

- Analicen `fraudulent` y `transactionAmount`

### 2.C) Análisis de numérica vs

- Analicen `orderAmount` y `transactionAmount`

- Promedio de todas las variables, por nuestra variable a predecir `transactionAmount`

## 3) Gráficos en AED

### 3.A) Análisis de numérica vs. categórica

- Analicen `transactionAmount` y `transactionFailed`. **¿Existen outliers o valores anomalos?**

### 3.B) Análisis de categórica vs. categórica

- Consideren `x="paymentMethodType"` y `col="orderState"`

### 3.C) Análisis de numérica vs. numérica

Al parecer toma los booleanos `fraudulent` y `paymentMethodRegistrationFailure` como un número entero.

Para nuestro caso vamos a evaluar un sub dataset en este item:
```
data_aux = data[["orderAmount", "transactionAmount"]].copy()
```

# CORRELACIÓN 🤯

## 1) Samples

Como tenemos pocas columnas / filas no es necesario tomar una muestra / sample del dataset completo.

## 5) Volvemos al análisis de correlación: Gráficos 📊

**Obtengan 5 insights que les llamo la atención del gráfico de correlación**

## 6) Análisis de correlaciones no lineales basadas en teoría de la información

Para MINE consideren:

```
# 2do calculo de los estadísticos
mine.compute_score(data3['transactionAmount'], data3['transactionFailed'])
```