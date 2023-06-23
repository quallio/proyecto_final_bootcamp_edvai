# 1) Cargamos los datos 📕

```
data = pd.read_csv("data/customer_dataset.csv", sep=',') 
```

# 3) Discretización 📈➜📊 

Por igual frecuencia y por igual rango.
---

Vamos a hacer una copia del dataframe data para luego evaluar si los puntos de corte se guardan y leen correctamente.

probando = data.copy()

- Para `orderAmount`
  
  ```
  data['orderAmount'], saved_bins_order = pd.qcut(data['orderAmount'], q=5, duplicates='drop', retbins=True)
  ```

  Guardamos los puntos de corte

  ```
  with open('data/saved_bins_order.pickle', 'wb') as handle:
    pickle.dump(saved_bins_order, handle, protocol=pickle.HIGHEST_PROTOCOL)
  ```

- Para `transactionAmount`
  
  - Hagan lo mismo que la discretización de la columna anterior
  - Consideren un `q=4`
  - Guarden los puntos de corte o bins con el nombre `saved_bins_transaction.pickle`
  
---

Vamos a evaluar que los puntos de corte / bins generado, se han guardado correctamente:

```
with open('data/saved_bins_order.pickle', 'rb') as handle:
    new_saved_bins_order = pickle.load(handle)
```

```
with open('data/saved_bins_transaction.pickle', 'rb') as handle:
    new_saved_bins_transaction = pickle.load(handle)
```

```
probando["orderAmount"] = pd.cut(
    probando['orderAmount'],
    bins=new_saved_bins_order, 
    include_lowest=True) # importante para que coincidan todos
```

```
probando.head(3)
```

# 4) Preparación de datos 🔧

## 4.1) Intepretar los valores

### - paymentMethodIssuer

Contar los elementos únicos que aparecen

```
data['paymentMethodIssuer'].value_counts()
```

**Aclaración:** Esto se puede hacer usando expresiones regulares (Regex) y funciones lambda también, pero es más práctico de seguir / entender lo que hace el programa de la siguiente manera:

```
# Reemplazar un valor a la vez
weird_payment_method = ["B", "e", "c", "r", " ", "n", "x", "o", "a", "p"]

for payment_method in weird_payment_method:
    data['paymentMethodIssuer'] = data['paymentMethodIssuer'].replace(payment_method, 'weird')
```

```
data['paymentMethodIssuer'].value_counts()
```

### -paymentMethodProvider

```
data['paymentMethodProvider'].value_counts()
```

### -paymentMethodType

```
data['paymentMethodType'].value_counts()
```

```
status(data)
```

### - fraudulent

Vamos a hacer una especie de semáforo:
- False = Green le asignaremos el valor numérico 0
- True = Red le asignaremos el valor numérico 1
- Nan = Yellow le asignaremos el valor numérico 2

```
data['fraudulent']=data['fraudulent'].fillna(value="warning")
```

```
data["fraudulent"].value_counts()
```

Nos aseguramos que no exista ningún tipo de conflicto por falta de compatibilidad entre str y bool de True/False.

```
data['fraudulent']=data['fraudulent'].astype(str)
```

```
class_map = {'False': 0, 'True': 1, 'warning': 2}
data['fraudulent'] = data['fraudulent'].map(class_map)
```

```
data.head(3)
```

## 4.2) Custom tratamiento de datos faltantes

Lo hacemos para columnas categóricas, que en nuestro caso la única categórica con datos faltantes es `orderAmount`.

```
data['orderAmount'].value_counts()
```

```
data['orderAmount']=data['orderAmount'].cat.add_categories("desconocido")
data['orderAmount']=data['orderAmount'].fillna(value="desconocido")
```

```
data['orderAmount'].value_counts()
```

# 5) One hot encoding ✂️

Asigna el One hot encoding (ohe) a un nuevo dataframe llamado `data_ohe`

Guardar One Hot Encoding

Hay que eliminar nuestra columna objetivo de nuestro archivo pickle.

```
data_ohe_without_fraudulent = data_ohe.drop(["fraudulent"], axis=1)
```

Guardar el nombre de las columnas con el nombre: `categories_ohe_without_fraudulent.pickle`

```
with open('data/categories_ohe_without_fraudulent.pickle', 'wb') as handle:
    pickle.dump(data_ohe_without_fraudulent.columns, handle, protocol=pickle.HIGHEST_PROTOCOL)
```

# 6) Guardar dataset 💾

Guardamos todo el One Hot Encoding, incluyendo nuestra variable objetivo: fraudulent

```
filename = "data/ohe_customer_dataset.csv"
data_ohe.to_csv(filename, index = False)
```