# M00 · Entorno, estructura y cómo leer el repositorio del libro

> **Antes de empezar:** el entorno virtual creado y activado, y `pip install -r requirements.txt`
> ejecutado. Si eso no está, vuelve al `README.md` de la raíz.

---

## 1. Qué problema resuelve este módulo

Ningún módulo posterior funciona si el entorno no está en orden, y la mayor parte de la
frustración de quien empieza con scikit-learn no viene de los algoritmos: viene de un
kernel apuntando al Python equivocado, de una ruta que se rompe al mover la carpeta, o
de copiar un fragmento del libro que fue escrito para una versión de hace diez años.

Este módulo deja resueltas esas tres cosas de una vez. Al terminar tendrás un entorno
verificado, un patrón de rutas que no se rompe, y el criterio para leer los notebooks
del libro sabiendo qué traducir.

No hay machine learning aquí todavía. Hay fontanería. Pero es la fontanería que te va a
ahorrar horas en los diecisiete módulos siguientes.

---

## 2. La intuición

### El problema del kernel

Cuando abres un notebook en VSCode, hay **dos** cosas que eligen un Python, y no tienen
por qué coincidir:

```
VSCode  ──(Python: Select Interpreter)──►  Python A   ← para archivos .py
Notebook ──(selector de kernel, arriba a la derecha)──►  Python B   ← para celdas
```

Si instalaste las librerías en `.venv` pero el kernel del notebook apunta al Python del
sistema, obtienes `ModuleNotFoundError: No module named 'sklearn'` con las librerías
perfectamente instaladas. Es el error número uno de quien empieza.

La comprobación definitiva no es `pip list`, es ejecutar dentro del notebook:

```python
import sys
print(sys.executable)
```

Si esa ruta no contiene `.venv`, el kernel está mal. Nada más importa hasta arreglarlo.

### El problema de las rutas

Este código funciona hoy en tu máquina y en ninguna otra, nunca más:

```python
df = pd.read_csv(r"C:\Users\herna\OneDrive\Documentos\CARRERA INGENIERIA INFORMATICA DUOC\ScikitLearn_2026\data\titanic.csv")
```

Se rompe si mueves la carpeta, si sincronizas en otro equipo, si lo subes a GitHub, o si
un profesor lo abre. Y con OneDrive de por medio, la ruta puede cambiar sola.

La alternativa es **resolver la raíz del proyecto en tiempo de ejecución** y construir
todo a partir de ahí. Eso hace `raiz_proyecto()` en `src/utils.py`: sube carpeta por
carpeta hasta encontrar `requirements.txt`, que solo existe en la raíz.

```python
from src.utils import raiz_proyecto
ruta_csv = raiz_proyecto() / "data" / "titanic.csv"
```

Esto funciona en Windows, macOS y Linux sin cambiar nada, porque `pathlib` se encarga de
las barras.

### El problema del libro

El repositorio del libro es material excelente y código muerto al mismo tiempo. Está
escrito para **Python 2.7 y scikit-learn 0.15** (2013–2015). Si copias una celda tal
cual, en el mejor de los casos falla; en el peor, corre y te da un resultado distinto en
silencio.

La forma correcta de usarlo: **leer la explicación, ignorar la sintaxis**. La intuición
sobre por qué un SVM necesita datos escalados no ha caducado. La línea
`from sklearn.cross_validation import train_test_split` sí.

---

## 3. La matemática mínima

Ninguna. Este módulo es entorno.

Lo único cuantitativo que aparece es la comparación de versiones: el notebook comprueba
que `scikit-learn >= 1.5`, porque varias cosas del plan (`root_mean_squared_error`,
`set_config(transform_output="pandas")`) no existen antes.

---

## 4. La API

### Verificar el entorno

```python
import sklearn
sklearn.__version__        # '1.5.2'
sklearn.show_versions()    # informe completo: Python, dependencias, BLAS
```

`show_versions()` es lo que te van a pedir si alguna vez abres un issue en GitHub.

### Las rutas con `pathlib`

```python
from pathlib import Path

Path.cwd()                      # carpeta actual
Path.cwd().parent               # la de arriba
Path.cwd().parents[1]           # dos niveles arriba
carpeta / "data" / "x.csv"      # el operador / construye rutas
ruta.exists()                   # ¿existe?
ruta.resolve()                  # ruta absoluta y sin '..'
list(carpeta.glob("*.ipynb"))   # buscar por patrón
```

El operador `/` sobre un `Path` es la parte que sorprende: no divide, concatena. Y usa
el separador correcto según el sistema operativo.

### Importar código propio desde un notebook

Un notebook en `modulos/00_entorno/` no ve `src/` automáticamente. Hay que añadir la
raíz al camino de búsqueda de Python:

```python
import sys
from pathlib import Path

RAIZ = Path.cwd()
while not (RAIZ / "requirements.txt").exists():
    RAIZ = RAIZ.parent

if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.utils import raiz_proyecto, estilo_graficos
```

Ese bloque se repite al inicio de todos los notebooks del curso. Cópialo sin pensarlo.

### Los datasets integrados

```python
from sklearn.datasets import load_iris

iris = load_iris()           # devuelve un Bunch
iris.data.shape              # (150, 4)
iris.target.shape            # (150,)
iris.target_names            # array(['setosa', 'versicolor', 'virginica'], ...)
print(iris.DESCR)            # documentación del dataset

X, y = load_iris(return_X_y=True)        # solo los arrays
df = load_iris(as_frame=True).frame      # como DataFrame de pandas
```

Un `Bunch` es un diccionario al que también puedes acceder con punto: `iris["data"]` y
`iris.data` son lo mismo. Detalle completo en `docs/cheatsheet_api.md`.

---

## 5. Errores comunes

| Síntoma | Causa | Arreglo |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'sklearn'` | El kernel apunta a otro Python | Selecciona el kernel `.venv` arriba a la derecha del notebook |
| `ModuleNotFoundError: No module named 'src'` | La raíz no está en `sys.path` | El bloque de la sección 4 |
| `FileNotFoundError` con un CSV | Ruta relativa al directorio equivocado | Usa `raiz_proyecto() / "data" / ...` |
| `.venv\Scripts\Activate.ps1 no se puede cargar` | Política de ejecución de PowerShell | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| Los gráficos no aparecen | Falta el backend inline | En VSCode funciona solo; si no, `%matplotlib inline` |
| Conflictos raros de OneDrive | OneDrive sincroniza `.venv` mientras trabajas | Excluye `.venv` de la sincronización, o crea el entorno fuera de OneDrive |

**Sobre OneDrive.** Tu proyecto está dentro de una carpeta sincronizada. Funciona, pero
`.venv` tiene miles de archivos pequeños y OneDrive los subirá todos. Dos opciones: en
OneDrive → Configuración → *Elegir carpetas*, desmarca `.venv`; o crea el entorno virtual
fuera de OneDrive y apunta VSCode a él. El `.gitignore` ya excluye `.venv` de git, que es
un problema distinto.

---

## 6. Qué dice el libro y qué cambió

El repositorio tiene un notebook llamado `Library versions, readme.ipynb` con esto:

```python
import sklearn as sk
import numpy as np
import matplotlib
import IPython

print sk.__version__      # ← Python 2: sin paréntesis
print np.__version__
print matplotlib.__version__
print IPython.__version__
```

Las versiones que reporta son de la época: scikit-learn 0.15, NumPy 1.8, IPython 2.x.
Nuestro `00_practica.ipynb` hace lo mismo pero en Python 3, comprobando contra los
mínimos del plan y con `sklearn.show_versions()`.

Dos observaciones sobre el repositorio que conviene tener claras desde ya:

- De los diez notebooks de contenido, **solo uno está en Python 3**: *Chapter 1 (2nd ed.)*.
  Los otros nueve usan `print` sin paréntesis y no ejecutan ni la primera celda.
- El más útil para empezar es precisamente ese, *Chapter 1 (2nd ed.)*, porque además de
  estar en Python 3 cubre clasificación, clustering y regresión en un solo recorrido.
  Aun así usa `sklearn.cross_validation`, que ya no existe.

La tabla completa de traducciones está en `docs/deprecaciones.md`. En el TODO 6 del
notebook de práctica vas a traducir tu primer fragmento.
