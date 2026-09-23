"""
Utilidades compartidas por todos los módulos del laboratorio.

Se importa desde los notebooks así:

    import sys
    from pathlib import Path
    sys.path.append(str(Path.cwd().parents[1]))   # llegar a la raíz del proyecto

    from src.utils import raiz_proyecto, estilo_graficos, resumen_bunch

El objetivo es que los notebooks contengan aprendizaje, no cuarenta líneas de
matplotlib repetidas.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

__all__ = [
    "raiz_proyecto",
    "ruta_datos",
    "ruta_referencia",
    "estilo_graficos",
    "versiones",
    "resumen_bunch",
    "dispersion_2d",
    "mostrar_imagenes",
]


# ---------------------------------------------------------------------------
# Rutas del proyecto
# ---------------------------------------------------------------------------


def raiz_proyecto(inicio: Path | str | None = None) -> Path:
    """Devuelve la raíz del proyecto subiendo hasta encontrar requirements.txt.

    Funciona igual en Windows, macOS y Linux, y no depende de desde qué carpeta
    se abrió VSCode. Nunca escribas rutas absolutas en un notebook: se rompen en
    cuanto mueves el proyecto o lo abre otra persona.

    Parameters
    ----------
    inicio : Path | str | None
        Carpeta desde donde empezar a buscar. Por defecto, el directorio actual.

    Returns
    -------
    Path
        La carpeta que contiene requirements.txt.

    Raises
    ------
    FileNotFoundError
        Si no encuentra la raíz (estás fuera del proyecto).
    """
    actual = Path(inicio) if inicio is not None else Path.cwd()
    actual = actual.resolve()

    for carpeta in (actual, *actual.parents):
        if (carpeta / "requirements.txt").exists():
            return carpeta

    raise FileNotFoundError(
        "No se encontró la raíz del proyecto (ninguna carpeta padre tiene "
        f"requirements.txt). Se buscó desde: {actual}"
    )


def ruta_datos() -> Path:
    """Carpeta data/ del proyecto."""
    return raiz_proyecto() / "data"


def ruta_referencia() -> Path:
    """Carpeta con el clon del repositorio del libro."""
    return raiz_proyecto() / "referencia" / "scikit-learn-book"


# ---------------------------------------------------------------------------
# Entorno
# ---------------------------------------------------------------------------


def versiones() -> dict[str, str]:
    """Devuelve las versiones instaladas de las librerías del curso.

    Returns
    -------
    dict[str, str]
        Nombre de la librería -> versión. Las no instaladas aparecen como
        "NO INSTALADA".
    """
    import importlib
    import platform

    resultado = {"python": platform.python_version()}

    for nombre in ("sklearn", "numpy", "pandas", "matplotlib", "scipy", "joblib"):
        try:
            modulo = importlib.import_module(nombre)
            resultado[nombre] = getattr(modulo, "__version__", "desconocida")
        except ImportError:
            resultado[nombre] = "NO INSTALADA"

    return resultado


def estilo_graficos() -> None:
    """Aplica un estilo legible y consistente a todos los gráficos.

    Llámala una vez al principio de cada notebook, después de importar
    matplotlib. Evita el gris apagado por defecto y sube el tamaño de fuente,
    que en un notebook siempre queda corto.
    """
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "figure.figsize": (8, 5),
            "figure.dpi": 100,
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "axes.grid": True,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.alpha": 0.25,
            "grid.linestyle": "--",
            "legend.frameon": False,
            "image.cmap": "viridis",
        }
    )


# ---------------------------------------------------------------------------
# Exploración de datasets
# ---------------------------------------------------------------------------


def resumen_bunch(bunch, nombre: str = "dataset") -> None:
    """Imprime un resumen legible de un Bunch de sklearn.datasets.

    Parameters
    ----------
    bunch : sklearn.utils.Bunch
        Lo que devuelve load_iris(), load_digits(), fetch_20newsgroups()...
    nombre : str
        Etiqueta para el encabezado.
    """
    print(f"=== {nombre} ===")
    print(f"claves disponibles : {list(bunch.keys())}")

    if hasattr(bunch, "data"):
        datos = bunch.data
        forma = getattr(datos, "shape", f"{len(datos)} elementos")
        print(f"X (data)           : {forma}   tipo={type(datos).__name__}")

    if hasattr(bunch, "target"):
        objetivo = np.asarray(bunch.target)
        print(f"y (target)         : {objetivo.shape}   dtype={objetivo.dtype}")

        valores, conteos = np.unique(objetivo, return_counts=True)
        if len(valores) <= 30:
            print(f"clases             : {len(valores)}")
            for valor, conteo in zip(valores, conteos):
                etiqueta = ""
                if hasattr(bunch, "target_names"):
                    try:
                        etiqueta = f" ({bunch.target_names[int(valor)]})"
                    except (IndexError, ValueError, TypeError):
                        etiqueta = ""
                print(f"  {valor}{etiqueta}: {conteo}")
        else:
            print(f"objetivo continuo  : min={objetivo.min():.3f} max={objetivo.max():.3f}")

    if hasattr(bunch, "feature_names") and bunch.feature_names is not None:
        nombres = list(bunch.feature_names)
        if len(nombres) <= 12:
            print(f"atributos          : {nombres}")
        else:
            print(f"atributos          : {len(nombres)} (primeros 5: {nombres[:5]})")


# ---------------------------------------------------------------------------
# Gráficos
# ---------------------------------------------------------------------------


def dispersion_2d(
    X,
    y,
    col_x: int = 0,
    col_y: int = 1,
    nombres_atributos=None,
    nombres_clases=None,
    titulo: str = "",
    ax=None,
):
    """Dibuja dos atributos de X coloreados por la clase de y.

    Parameters
    ----------
    X : array de forma (n_muestras, n_atributos)
    y : array de forma (n_muestras,)
    col_x, col_y : int
        Índices de las columnas de X que van en cada eje.
    nombres_atributos : lista de str, opcional
        Para etiquetar los ejes.
    nombres_clases : lista de str, opcional
        Para la leyenda.
    titulo : str
    ax : matplotlib Axes, opcional
        Si no se pasa, crea una figura nueva.

    Returns
    -------
    matplotlib.axes.Axes
    """
    import matplotlib.pyplot as plt

    X = np.asarray(X)
    y = np.asarray(y)

    if ax is None:
        _, ax = plt.subplots()

    for valor in np.unique(y):
        mascara = y == valor
        etiqueta = str(valor)
        if nombres_clases is not None:
            try:
                etiqueta = str(nombres_clases[int(valor)])
            except (IndexError, ValueError, TypeError):
                pass
        ax.scatter(
            X[mascara, col_x],
            X[mascara, col_y],
            label=etiqueta,
            alpha=0.75,
            edgecolors="white",
            linewidths=0.5,
            s=45,
        )

    etiqueta_x = nombres_atributos[col_x] if nombres_atributos is not None else f"atributo {col_x}"
    etiqueta_y = nombres_atributos[col_y] if nombres_atributos is not None else f"atributo {col_y}"
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    if titulo:
        ax.set_title(titulo)
    ax.legend(title="clase")

    return ax


def mostrar_imagenes(imagenes, etiquetas=None, filas: int = 2, columnas: int = 5, titulo: str = ""):
    """Dibuja una rejilla de imágenes (para digits, Olivetti faces, MNIST).

    Parameters
    ----------
    imagenes : array de forma (n, alto, ancho) o (n, alto*ancho)
        Si viene aplanado, se intenta inferir un lado cuadrado.
    etiquetas : array, opcional
        Se muestra sobre cada imagen.
    filas, columnas : int
    titulo : str

    Returns
    -------
    matplotlib.figure.Figure
    """
    import matplotlib.pyplot as plt

    imagenes = np.asarray(imagenes)

    if imagenes.ndim == 2:
        lado = int(np.sqrt(imagenes.shape[1]))
        if lado * lado != imagenes.shape[1]:
            raise ValueError(
                f"No se puede inferir una imagen cuadrada de {imagenes.shape[1]} valores. "
                "Pasa las imágenes ya con forma (n, alto, ancho)."
            )
        imagenes = imagenes.reshape(-1, lado, lado)

    fig, ejes = plt.subplots(filas, columnas, figsize=(columnas * 1.6, filas * 1.8))
    ejes = np.atleast_1d(ejes).ravel()

    for i, eje in enumerate(ejes):
        eje.set_axis_off()
        if i < len(imagenes):
            eje.imshow(imagenes[i], cmap="gray_r", interpolation="nearest")
            if etiquetas is not None:
                eje.set_title(str(etiquetas[i]), fontsize=10)

    if titulo:
        fig.suptitle(titulo, fontweight="bold")

    fig.tight_layout()
    return fig
