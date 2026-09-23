# El contrato de la API de scikit-learn

Toda la librería es el mismo patrón repetido. Si entiendes esta página, el resto de
scikit-learn se vuelve predecible: puedes adivinar cómo se usa una clase que nunca
has visto.

---

## Los tres roles

Cada objeto de scikit-learn cumple uno o varios de estos roles.

| Rol | Método que lo define | Ejemplos |
| --- | --- | --- |
| **Estimator** | `.fit(X, y)` | todos |
| **Predictor** | `.predict(X)` | `SVC`, `LinearRegression`, `KMeans` |
| **Transformer** | `.transform(X)` | `StandardScaler`, `PCA`, `TfidfVectorizer` |

Un `StandardScaler` es estimator + transformer.
Un `SVC` es estimator + predictor.
Un `PCA` es estimator + transformer (y también tiene `inverse_transform`).

---

## El ciclo de vida de un objeto

```python
modelo = SVC(C=1.0, kernel="rbf")   # 1. construir: SOLO hiperparámetros
modelo.fit(X_train, y_train)        # 2. aprender:  guarda lo aprendido en atributos_
y_pred = modelo.predict(X_test)     # 3. usar
modelo.score(X_test, y_test)        # 4. evaluar (métrica por defecto del tipo)
```

Tres reglas que se desprenden de esto:

1. **El constructor no valida ni calcula nada.** `SVC(C=-5)` no lanza error hasta que
   llamas a `.fit()`. Los hiperparámetros se guardan tal cual, sin tocar.
2. **`fit` siempre devuelve `self`.** Por eso puedes encadenar:
   `SVC().fit(X, y).predict(X_test)`.
3. **`fit` reinicia el objeto.** Llamar a `.fit()` dos veces no acumula aprendizaje;
   el segundo olvida el primero. (Excepción: `partial_fit` en los estimadores que lo
   tienen, y `warm_start=True`.)

---

## El guion bajo final

La convención más útil de toda la librería:

```python
scaler = StandardScaler()
scaler.mean_        # AttributeError — todavía no aprendió nada
scaler.fit(X_train)
scaler.mean_        # array([5.84, 3.05, 3.76, 1.20])  ← ahora sí
```

| Sin guion bajo | Con guion bajo final |
| --- | --- |
| `C`, `kernel`, `n_estimators`, `max_depth` | `coef_`, `mean_`, `classes_`, `n_features_in_` |
| Lo que **tú** decides | Lo que el modelo **aprendió** |
| Disponible desde el constructor | Solo existe después de `.fit()` |

Si ves un `AttributeError` sobre un atributo con guion bajo, la causa es casi siempre
la misma: olvidaste llamar a `fit`.

---

## `fit_transform` no es un atajo inocente

```python
scaler.fit_transform(X)   # equivale a scaler.fit(X).transform(X)
```

Es más rápido, pero **dónde lo usas cambia el resultado del experimento**:

```python
# CORRECTO
X_train_s = scaler.fit_transform(X_train)   # aprende media y desviación del train
X_test_s  = scaler.transform(X_test)        # aplica las del train al test

# INCORRECTO — data leakage
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.fit_transform(X_test)    # el test se escala consigo mismo
```

El segundo caso te da una métrica mejor de la que obtendrás en producción. El módulo
M05 convierte esto en imposible usando `Pipeline`.

---

## Formas de los datos

| Objeto | Forma | Tipo |
| --- | --- | --- |
| `X` | `(n_muestras, n_atributos)` — siempre 2D | ndarray, DataFrame o matriz dispersa |
| `y` clasificación | `(n_muestras,)` — 1D | enteros o strings |
| `y` regresión | `(n_muestras,)` — 1D | flotantes |

Error frecuente: pasar `X` con una sola columna como 1D.
`model.predict([5.1, 3.5, 1.4, 0.2])` falla; necesita `[[5.1, 3.5, 1.4, 0.2]]`.

---

## Los `Bunch` de los datasets

`load_iris()` no devuelve una tupla: devuelve un `Bunch`, que es un diccionario cuyas
claves también son atributos.

```python
from sklearn.datasets import load_iris

iris = load_iris()
iris.keys()          # dict_keys(['data', 'target', 'frame', 'target_names', 'DESCR', ...])
iris.data.shape      # (150, 4)
iris["data"].shape   # (150, 4)  ← lo mismo
iris.target_names    # array(['setosa', 'versicolor', 'virginica'], dtype='<U10')
print(iris.DESCR)    # la documentación del dataset

X, y = load_iris(return_X_y=True)          # si solo quieres los arrays
df = load_iris(as_frame=True).frame        # si prefieres un DataFrame
```

---

## `get_params` y `set_params`

Todo estimador expone sus hiperparámetros de forma uniforme. Esto es lo que hace
posible `GridSearchCV`.

```python
svc = SVC(C=1.0)
svc.get_params()          # {'C': 1.0, 'kernel': 'rbf', 'gamma': 'scale', ...}
svc.set_params(C=10.0)    # devuelve self
```

Dentro de un `Pipeline`, los nombres se anidan con doble guion bajo:

```python
pipe = Pipeline([("scaler", StandardScaler()), ("svc", SVC())])
pipe.set_params(svc__C=10.0)

# y por eso un grid se escribe así:
grid = {"svc__C": [0.1, 1, 10], "svc__gamma": [0.001, 0.01]}
```

Regla mnemotécnica: **un guion bajo separa palabras, dos separan niveles.**

---

## Chuleta de importaciones

```python
# Datos
from sklearn.datasets import load_iris, load_digits, fetch_20newsgroups

# División y validación
from sklearn.model_selection import (
    train_test_split, KFold, StratifiedKFold, cross_val_score,
    cross_validate, cross_val_predict, GridSearchCV, RandomizedSearchCV,
)

# Preprocesamiento
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline

# Modelos
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA

# Evaluación
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    ConfusionMatrixDisplay, r2_score, root_mean_squared_error,
)
```

---

## Cuando algo falla

| Síntoma | Causa habitual |
| --- | --- |
| `NotFittedError` | Llamaste a `predict` antes de `fit` |
| `AttributeError: 'X' object has no attribute 'coef_'` | Lo mismo, con otro nombre |
| `ValueError: Expected 2D array, got 1D array instead` | `X` con una sola muestra o columna sin envolver |
| `ValueError: X has 3 features, but ... is expecting 4 features` | El preprocesamiento del test no es el mismo que el del train |
| `ValueError: Input contains NaN` | Falta un `SimpleImputer` en el pipeline |
| `ConvergenceWarning` | Pocas iteraciones (`max_iter`) o datos sin escalar |

El último es el más subestimado: casi todos los modelos lineales y `SVC` **necesitan**
datos escalados para converger bien.
