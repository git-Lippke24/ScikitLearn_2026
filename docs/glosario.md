# Glosario

La documentación de scikit-learn está en inglés y la mayoría de los términos no se
traducen en la práctica profesional. Aquí va el término en inglés (el que verás en el
código), su equivalente en español y qué significa realmente.

---

## Conceptos generales

| Inglés | Español | Qué es |
| --- | --- | --- |
| **feature** | atributo, característica, variable | Una columna de `X` |
| **sample** / instance | muestra, instancia, ejemplo | Una fila de `X` |
| **target** / label | objetivo, etiqueta | El vector `y`, lo que queremos predecir |
| **fit** | ajustar, entrenar | Aprender parámetros a partir de los datos |
| **estimator** | estimador | Cualquier objeto con `.fit()` |
| **hyperparameter** | hiperparámetro | Lo que tú eliges (`C`, `max_depth`); no se aprende |
| **parameter** | parámetro | Lo que el modelo aprende (`coef_`, `mean_`) |
| **supervised learning** | aprendizaje supervisado | Hay `y`: el dataset trae las respuestas |
| **unsupervised learning** | aprendizaje no supervisado | No hay `y`: buscamos estructura |

---

## Entrenamiento y evaluación

| Inglés | Español | Qué es |
| --- | --- | --- |
| **training set** | conjunto de entrenamiento | Con lo que el modelo aprende |
| **test set** | conjunto de prueba | Se toca **una sola vez**, al final |
| **validation set** | conjunto de validación | Para elegir hiperparámetros sin gastar el test |
| **cross-validation (CV)** | validación cruzada | Rotar qué parte hace de validación, k veces |
| **fold** | pliegue, partición | Cada uno de los k trozos de la validación cruzada |
| **stratified** | estratificado | Cada pliegue conserva la proporción de clases |
| **overfitting** | sobreajuste | Aprende el ruido del train; falla en datos nuevos |
| **underfitting** | subajuste | El modelo es demasiado simple para el problema |
| **data leakage** | fuga de datos | Información del test se cuela en el entrenamiento |
| **baseline** | línea base | El modelo tonto contra el que comparas (`DummyClassifier`) |

**Sobre *data leakage*.** Es el error más caro y el más difícil de detectar: no produce
ningún mensaje de error, solo una métrica sospechosamente buena que se derrumba en
producción. El caso clásico es escalar antes de dividir en train/test.

---

## Métricas de clasificación

| Inglés | Español | Qué mide |
| --- | --- | --- |
| **accuracy** | exactitud | Proporción de aciertos sobre el total |
| **precision** | precisión | De los que predije positivos, cuántos lo eran |
| **recall** / sensitivity | exhaustividad, sensibilidad | De los positivos reales, cuántos encontré |
| **F1-score** | F1 | Media armónica de precisión y exhaustividad |
| **support** | soporte | Cuántas muestras reales hay de esa clase |
| **confusion matrix** | matriz de confusión | Tabla de aciertos y errores por clase |
| **ROC curve** | curva ROC | Tasa de verdaderos positivos vs. falsos positivos |
| **AUC** | área bajo la curva | Resumen de la curva ROC en un número |

Cuidado con *precisión*: en español se usa a veces como sinónimo de *exactitud*, pero
en scikit-learn `precision` y `accuracy` son métricas distintas. En este curso
mantenemos los nombres en inglés dentro del código.

**Por qué la exactitud engaña.** Si el 99 % de los correos no son spam, un modelo que
responde siempre "no es spam" tiene 99 % de exactitud y es completamente inútil. Por
eso M03 está dedicado entero a esto.

---

## Métricas de regresión

| Inglés | Español | Qué mide |
| --- | --- | --- |
| **MAE** (mean absolute error) | error absoluto medio | Error promedio, en las unidades originales |
| **MSE** (mean squared error) | error cuadrático medio | Penaliza mucho los errores grandes |
| **RMSE** (root mean squared error) | raíz del error cuadrático medio | Como MSE pero en las unidades originales |
| **R²** (coefficient of determination) | coeficiente de determinación | Proporción de varianza explicada; 1.0 es perfecto |

---

## Preprocesamiento

| Inglés | Español | Qué hace |
| --- | --- | --- |
| **scaling** | escalado | Poner los atributos en rangos comparables |
| **standardization** | estandarización | Media 0, desviación 1 (`StandardScaler`) |
| **normalization** | normalización | Llevar a un rango fijo, típico [0,1] (`MinMaxScaler`) |
| **encoding** | codificación | Convertir categorías en números |
| **one-hot encoding** | codificación *one-hot* | Una columna binaria por categoría |
| **imputation** | imputación | Rellenar valores faltantes |
| **sparse matrix** | matriz dispersa | Matriz con casi todo ceros, guardada de forma comprimida |
| **dimensionality reduction** | reducción de dimensionalidad | Menos columnas conservando la información |

---

## Términos por algoritmo

| Inglés | Contexto | Qué es |
| --- | --- | --- |
| **kernel** | SVM | Función que mide similitud entre muestras |
| **margin** | SVM | Distancia entre la frontera y los puntos más cercanos |
| **support vector** | SVM | Las muestras que definen la frontera |
| **impurity** | árboles | Cuán mezcladas están las clases en un nodo (Gini, entropía) |
| **pruning** | árboles | Podar ramas para evitar sobreajuste |
| **ensemble** | ensambles | Combinar muchos modelos en uno |
| **bagging** | ensambles | Entrenar en paralelo sobre muestras distintas (Random Forest) |
| **boosting** | ensambles | Entrenar en secuencia, cada uno corrige al anterior |
| **centroid** | clustering | El centro de un grupo |
| **inertia** | K-means | Suma de distancias al centroide; lo que K-means minimiza |
| **silhouette** | clustering | Qué tan bien separado está cada punto de los otros grupos |
| **explained variance** | PCA | Cuánta información conserva cada componente |
| **bag of words** | texto | Representar un documento por el conteo de sus palabras |
| **TF-IDF** | texto | Conteo ponderado: penaliza palabras que salen en todos lados |
| **stop words** | texto | Palabras vacías (`el`, `de`, `the`) que se descartan |
| **n-gram** | texto | Secuencia de n palabras consecutivas tratada como una unidad |
