# M00 · Ejercicios

Cinco ejercicios cortos. No hay solución escrita: tráeme lo que escribas y lo revisamos.

Trabaja en un notebook nuevo en esta misma carpeta (`00_scratch.ipynb`, ya está en el
`.gitignore` por si quieres dejarlo fuera del repo) o en celdas añadidas al final de
`00_practica.ipynb`.

---

## Ejercicio 1 · Inventario del repositorio del libro

Escribe una celda que, usando solo `pathlib`, liste todos los archivos `.ipynb` que hay
en `referencia/scikit-learn-book/` y muestre para cada uno su nombre y su tamaño en KB,
ordenados de mayor a menor.

**Pistas:** `.glob("*.ipynb")`, `.stat().st_size`, `sorted(..., key=..., reverse=True)`.

**Para pensar:** el más grande pesa más de 2 MB. ¿Por qué un notebook de 39 celdas ocupa
tanto? Ábrelo con un editor de texto y mira qué hay dentro. (La respuesta tiene que ver
con las imágenes de los rostros de Olivetti.)

---

## Ejercicio 2 · Cazar deprecaciones

Escribe una celda que abra los diez notebooks de contenido del repositorio como JSON
(`json.load`), recorra sus celdas de código y cuente en cuántos aparece cada uno de
estos patrones:

- `sklearn.cross_validation`
- `sklearn.grid_search`
- `sklearn.externals`
- `load_boston`
- `print ` seguido de algo que no sea `(`

Imprime una tabla con el resultado.

**Pistas:** las celdas de un notebook están en `nb["cells"]`; cada una tiene
`cell_type` y `source` (que puede ser una lista de líneas). Para el último patrón,
una expresión regular como `r"^\s*print\s+[^(]"` con `re.MULTILINE` funciona.

**Para pensar:** ¿cuántos de los diez notebooks corren sin tocar nada? Compara tu
resultado con la tabla de `docs/deprecaciones.md`.

---

## Ejercicio 3 · Los otros datasets integrados

`load_iris()` no es el único. Carga `load_digits()`, `load_wine()` y
`load_breast_cancer()`, y arma un cuadro comparativo con, para cada uno:

| dataset | n muestras | n atributos | n clases | ¿balanceado? |

Considera "balanceado" si la clase menos frecuente tiene al menos el 80 % de las
muestras de la más frecuente.

**Pistas:** `resumen_bunch()` de `src.utils` te da casi todo; `np.unique(y, return_counts=True)`
te da los conteos.

**Para pensar:** uno de los tres no está balanceado. ¿Cuál, y por qué eso hará que la
*accuracy* sea una métrica engañosa en ese caso? (Lo retomamos en M03.)

---

## Ejercicio 4 · Rompe el escalado a propósito

Copia tu celda del TODO 6 y modifícala para hacerlo **mal**: ajusta el `StandardScaler`
sobre `X_dos` completo (train + test) antes de dividir.

Luego, para ambas versiones (la correcta y la incorrecta), imprime:

- La media y la desviación de `X_train_s` y de `X_test_s`.
- La diferencia entre la media del test en un caso y en el otro.

**Para pensar:** con iris y 150 muestras la diferencia es pequeña. ¿En qué situación
sería grande? Piensa en un dataset con pocas muestras, o con un atributo de escala muy
distinta entre train y test (por ejemplo, precios de un año frente a otro).

Este ejercicio importa más de lo que parece: es el error que más veces vas a estar
tentado de cometer, porque el código resultante es más corto.

---

## Ejercicio 5 · Amplía `src/utils.py`

Añade a `src/utils.py` una función:

```python
def comparar_versiones(minimos: dict[str, str]) -> None:
    """Compara las versiones instaladas contra un diccionario de mínimos
    e imprime OK / FALTA / DESACTUALIZADA por cada librería."""
```

Debe usar `versiones()` (que ya está) y aceptar algo como
`{"sklearn": "1.5", "pandas": "2.2"}`.

**Pistas:** comparar versiones como strings falla (`"1.10" < "1.5"` es `True`). Convierte
a tupla de enteros: `tuple(int(p) for p in v.split(".")[:2])`.

**Para pensar:** ¿qué debería hacer tu función si la versión instalada es `"1.5.dev0"`?
No hay una respuesta única; decide una y documéntala en el docstring.

---

## Cuando termines

Marca `M00` en el checklist del `README.md` de la raíz y cuéntame:

1. Cuál de los seis TODO te costó más y por qué.
2. Qué encontraste en el ejercicio 2 — es el que mejor prepara para todo lo que viene.
