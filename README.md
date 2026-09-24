# ScikitLearn_2026 — Laboratorio de aprendizaje

Curso práctico de **scikit-learn** en 18 módulos, construido sobre el material de
_Learning scikit-learn: Machine Learning in Python_ (Garreta, Moncecchi, Garat — Packt),
pero escrito contra la **API moderna: Python 3.11+ y scikit-learn ≥ 1.5**.

El repositorio original ([gmonce/scikit-learn-book](https://github.com/gmonce/scikit-learn-book))
es de 2013–2015 y su código en gran parte **ya no corre**. Lo usamos como esqueleto
conceptual y traducimos cada idea a la API actual. Ver `docs/deprecaciones.md`.

---

## Puesta en marcha

Desde esta carpeta, en la terminal de VSCode:

```powershell
# 1. Crear el entorno virtual
python -m venv .venv

# 2. Activarlo (Windows PowerShell)
.venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -U pip
pip install -r requirements.txt

# 4. Clonar el repositorio del libro como referencia (solo lectura)
git clone https://github.com/gmonce/scikit-learn-book.git referencia/scikit-learn-book
```

> Si PowerShell bloquea el script de activación, ejecuta una vez:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

Luego en VSCode: `Ctrl+Shift+P` → **Python: Select Interpreter** → elige `.venv`.
Al abrir un notebook, arriba a la derecha selecciona el mismo kernel `.venv`.

### Extensiones recomendadas de VSCode

| Extensión           | Para qué                                    |
| ------------------- | ------------------------------------------- |
| Python (Microsoft)  | Intérprete y depuración                     |
| Jupyter (Microsoft) | Ejecutar notebooks dentro de VSCode         |
| Pylance             | Autocompletado y tipos                      |
| Data Wrangler       | Inspeccionar DataFrames sin escribir código |
| Ruff                | Formato y linting                           |

---

## Cómo se trabaja cada módulo

1. **Leer** `NN_teoria.md` — el concepto, cuándo se usa, los parámetros que importan.
2. **Completar** `NN_practica.ipynb` — celdas con `# TODO` que dicen _qué_ y _por qué_,
   nunca _cómo_. Cada una termina en un `assert` que te avisa si acertaste.
3. **Comparar** con el notebook original del libro en `referencia/` y anotar qué cambió.
4. **Resolver** `NN_ejercicios.md`.
5. **Marcar** el módulo en el checklist de abajo.

Regla: no avanzar al módulo siguiente con celdas sin completar.

`NN_solucion.ipynb` existe para consultarlo **después** de intentarlo, no antes.

---

## Estructura

```
ScikitLearn_2026/
├─ README.md                  ← este archivo
├─ requirements.txt
├─ .gitignore
├─ data/                      ← datasets locales
├─ referencia/
│  └─ scikit-learn-book/      ← clon del repo original (solo lectura)
├─ docs/
│  ├─ deprecaciones.md        ← tabla API vieja → API nueva
│  ├─ glosario.md             ← términos de ML (español/inglés)
│  └─ cheatsheet_api.md       ← el contrato fit/transform/predict
├─ src/
│  └─ utils.py                ← helpers reutilizables
└─ modulos/
   ├─ 00_entorno/
   ├─ 01_api_sklearn/
   └─ ...
```

---

## Plan de los 18 módulos

### Bloque 0 — Fundamentos

| Módulo | Tema                                              |
| ------ | ------------------------------------------------- |
| M00    | Entorno, estructura y cómo leer el repo del libro |
| M01    | El contrato de la API de scikit-learn             |

### Bloque 1 — El flujo supervisado completo

| Módulo | Tema                                  |
| ------ | ------------------------------------- |
| M02    | Primer clasificador end-to-end (iris) |
| M03    | Métricas de clasificación             |
| M04    | Validación cruzada                    |
| M05    | Pipelines y `ColumnTransformer`       |

### Bloque 2 — Familias de algoritmos supervisados

| Módulo | Tema                                                 |
| ------ | ---------------------------------------------------- |
| M06    | Support Vector Machines (Olivetti faces)             |
| M07    | Naive Bayes y clasificación de texto (20 newsgroups) |
| M08    | Árboles de decisión e interpretabilidad (Titanic)    |
| M09    | Ensambles: bosques, boosting, voting, stacking       |
| M10    | Regresión (California housing)                       |

### Bloque 3 — Aprendizaje no supervisado

| Módulo | Tema                                         |
| ------ | -------------------------------------------- |
| M11    | Clustering (digits)                          |
| M12    | Reducción de dimensionalidad: PCA y compañía |

### Bloque 4 — Temas avanzados

| Módulo | Tema                                   |
| ------ | -------------------------------------- |
| M13    | Ingeniería y selección de atributos    |
| M14    | Selección de modelos e hiperparámetros |
| M15    | Del notebook al código reutilizable    |

### Bloque 5 — Proyectos integradores

| Módulo | Tema                       |
| ------ | -------------------------- |
| M16    | Capstone tabular           |
| M17    | Capstone de texto o imagen |

---

## Checklist de progreso

- [x] M00 · Entorno y estructura
- [ ] M01 · El contrato de la API de scikit-learn
- [ ] M02 · Primer clasificador end-to-end
- [ ] M03 · Métricas de clasificación
- [ ] M04 · Validación cruzada
- [ ] M05 · Pipelines y ColumnTransformer
- [ ] M06 · SVM
- [ ] M07 · Naive Bayes y texto
- [ ] M08 · Árboles de decisión e interpretabilidad
- [ ] M09 · Ensambles
- [ ] M10 · Regresión
- [ ] M11 · Clustering
- [ ] M12 · Reducción de dimensionalidad
- [ ] M13 · Ingeniería y selección de atributos
- [ ] M14 · Selección de modelos e hiperparámetros
- [ ] M15 · Del notebook al código reutilizable
- [ ] M16 · Capstone tabular
- [ ] M17 · Capstone texto o imagen

### Bitácora

Una línea por módulo cerrado: qué costó, qué quedó pendiente.

| Módulo | Fecha      | Nota                                                        |
| ------ | ---------- | ----------------------------------------------------------- |
| M00    | 2026-09-24 | Rutas con pathlib y la diferencia entre raise y try/except. |
|        |            |                                                             |
