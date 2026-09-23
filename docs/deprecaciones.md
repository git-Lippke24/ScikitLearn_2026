# Mapa de deprecaciones: del libro (2013–2015) a scikit-learn moderno

El repositorio [gmonce/scikit-learn-book](https://github.com/gmonce/scikit-learn-book)
fue escrito para **Python 2.7 y scikit-learn 0.15**. Esta tabla es la traducción que
aplicamos módulo a módulo. Tenla abierta al lado cuando leas un notebook del libro.

---

## 1. Python 2 → Python 3

| En el libro | Hoy |
| --- | --- |
| `print x` | `print(x)` |
| `print "texto", x` | `print("texto", x)` |
| `import StringIO` | `from io import StringIO` |
| `xrange(n)` | `range(n)` |
| `dict.iteritems()` | `dict.items()` |
| `5 / 2` → `2` (división entera) | `5 / 2` → `2.5`; usa `5 // 2` para entera |

La división es la trampa silenciosa: código del libro que calculaba proporciones
puede dar resultados distintos sin lanzar ningún error.

---

## 2. Módulos que desaparecieron

| En el libro (0.15) | Hoy (≥ 1.5) | Eliminado en |
| --- | --- | --- |
| `from sklearn.cross_validation import train_test_split, KFold, cross_val_score, ShuffleSplit, LeaveOneOut` | `from sklearn.model_selection import ...` | 0.20 |
| `from sklearn.grid_search import GridSearchCV, ParameterGrid` | `from sklearn.model_selection import ...` | 0.20 |
| `from sklearn.externals import joblib` | `import joblib` (paquete independiente) | 0.23 |
| `from sklearn.learning_curve import learning_curve` | `from sklearn.model_selection import learning_curve` | 0.20 |

Todo lo que en el libro se reparte entre `cross_validation`, `grid_search` y
`learning_curve` vive hoy en un único módulo: **`sklearn.model_selection`**.

---

## 3. Cambios de API dentro de las clases

### `KFold` ya no recibe el número de muestras

```python
# Libro (0.15)
cv = KFold(len(y), n_folds=5, shuffle=True, random_state=33)

# Hoy
from sklearn.model_selection import KFold
cv = KFold(n_splits=5, shuffle=True, random_state=33)
```

El objeto ya no sabe cuántas muestras hay: se lo dice `split(X, y)` en el momento.
Consecuencia práctica: un mismo `cv` sirve para varios datasets.

### `StratifiedKFold` es el nuevo default en clasificación

`cross_val_score` con un clasificador ya estratifica por defecto. En el libro había
que pedirlo a mano.

### `GMM` → `GaussianMixture`

```python
# Libro
from sklearn.mixture import GMM
gmm = GMM(n_components=10, covariance_type='tied', n_iter=100)

# Hoy
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=10, covariance_type='tied', max_iter=100)
```

Además `GaussianMixture` ya no tiene `.fit_predict()` heredado del viejo `GMM` con la
misma semántica: revisa la firma antes de usarlo.

### `OneHotEncoder` se rehizo por completo

```python
# Libro: codificar solo algunas columnas dentro del propio encoder
enc = OneHotEncoder(categorical_features=[0, 2])

# Hoy: el encoder codifica todo lo que recibe;
# quién recibe qué lo decide un ColumnTransformer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

pre = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["sexo", "clase"]),
    ("num", StandardScaler(), ["edad", "tarifa"]),
])
```

Otros detalles: el parámetro `sparse` se llama ahora `sparse_output`, y
`handle_unknown="ignore"` es casi obligatorio si vas a predecir sobre datos nuevos.

### `.predict_proba` y `.decision_function`

Sin cambios de nombre, pero hoy conviene saber que no son lo mismo: `SVC` necesita
`probability=True` para tener `predict_proba`, y eso lo hace notablemente más lento.

---

## 4. Datasets

| En el libro | Hoy | Por qué |
| --- | --- | --- |
| `load_boston()` | `fetch_california_housing()` | Retirado en 1.2 |
| `fetch_mldata("MNIST original")` | `fetch_openml("mnist_784", version=1)` | mldata.org dejó de existir |
| `fetch_olivetti_faces()` | igual | Sigue disponible |
| `fetch_20newsgroups()` | igual | Sigue disponible |
| `load_iris()`, `load_digits()` | igual | Siguen disponibles |

**Sobre Boston.** scikit-learn lo eliminó en la versión 1.2. El dataset incluye un
atributo (`B`) construido a partir de la proporción de población negra en cada barrio,
bajo el supuesto explícito de que esa variable influye en el precio de la vivienda.
La documentación de scikit-learn lo señala como un problema ético del propio diseño
del dataset, no solo de su uso. Lo reemplazamos por California housing y lo discutimos
en el módulo M10 como caso de estudio sobre procedencia de datos.

---

## 5. Visualización de árboles

```python
# Libro: requiere pydot, graphviz y StringIO
import pydot, StringIO
dot_data = StringIO.StringIO()
tree.export_graphviz(clf, out_file=dot_data, feature_names=['age','sex'])
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_png('tree.png')

# Hoy: sin dependencias externas
from sklearn.tree import plot_tree, export_text
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(16, 10))
plot_tree(clf, feature_names=['age', 'sex'], class_names=['no', 'si'],
          filled=True, rounded=True, ax=ax)

print(export_text(clf, feature_names=['age', 'sex']))   # versión en texto
```

---

## 6. Paralelización

El libro usa `IPython.parallel` con un cluster de motores para repartir un grid search.
Hoy eso está resuelto dentro de la propia librería:

```python
GridSearchCV(pipe, grid, cv=5, n_jobs=-1)   # -1 = todos los núcleos
```

`n_jobs` está disponible en `GridSearchCV`, `cross_val_score`, `cross_validate`,
`RandomForestClassifier`, `permutation_importance` y muchos más.

---

## 7. Cosas que no existían y hoy son estándar

Aparecen en el plan aunque el libro no las mencione:

| Herramienta | Qué resuelve | Módulo |
| --- | --- | --- |
| `ColumnTransformer` | Aplicar transformaciones distintas a columnas distintas | M05 |
| `SimpleImputer` | Rellenar valores faltantes dentro del pipeline | M05 |
| `set_config(transform_output="pandas")` | Que los transformers devuelvan DataFrames con nombres de columna | M05 |
| `ConfusionMatrixDisplay`, `RocCurveDisplay` | Gráficos de evaluación en una línea | M03 |
| `HistGradientBoostingClassifier` | Boosting rápido, tolera nulos y categóricas | M09 |
| `permutation_importance` | Importancia de atributos sin el sesgo de `feature_importances_` | M08 |
| `RandomizedSearchCV`, `HalvingGridSearchCV` | Búsqueda de hiperparámetros más barata que el grid completo | M14 |
| `root_mean_squared_error` | RMSE directo, sin `np.sqrt(mean_squared_error(...))` | M10 |

---

## Cómo usar esta tabla

Cuando abras un notebook del libro y algo no corra:

1. ¿Es un `print` sin paréntesis? → punto 1.
2. ¿Es un `ImportError` o `ModuleNotFoundError`? → punto 2.
3. ¿Es un `TypeError` sobre argumentos? → punto 3, la firma cambió.
4. ¿Es un dataset que no se descarga? → punto 4.

Si no cae en ninguno, revisa el
[historial de versiones de scikit-learn](https://scikit-learn.org/stable/whats_new.html).
