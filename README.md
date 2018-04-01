# Clasificación de cigarrillos.

Este algoritmo es capaz de clasificar entre 5 tipos de cigarrillos: Habano, purito, porro, pipa y cigarrillo común utilizando la libreria de OpenCV. La imagen que se utilizó para las pruebas fué la siguiente:

<p align="center">
  <img src="https://github.com/gnoya/Cigarette-Classification-OpenCV/blob/master/images/cigarsOriginal.png" width="396" height="396">
</p>

<p align="center">
  Imagen a clasificar.
</p>

# Procedimiento

Se separó el fondo de los objetos utilizando un threshold binario invertido y se procedió a encontrar los contornos de cada uno de ellos. Luego, se aplicó un algoritmo de clasificación basado en los siguientes features de cada objeto: alto, ancho y color promedio.

### Clasificación

Se tomó el cociente entre el largo y el ancho del objeto. Este cociente representa, en un objeto, cuántas veces es más largo que ancho y, teniendo unas referencias reales de los cigarrillos, pudimos clasificarlos en 3 tipos: cigarrillos/puritos, porros/habanos y pipas. Estos cocientes son valores aproximados, y aunque son distintos, su variedad no es tan amplia como para clasificarlos directamente.

  | Objeto     |  Cociente  |
  | ---------- | ----------:|
  | Cigarrillo |     9.5    |
  | Purito     |      9     |
  | Porro      |      7     |
  | Habano     |     6.5    |
  | Pipa       |     2.5    |

Para diferenciar entre cigarrillos/puritos y porros/habanos se utilizó el feature del color promedio del objeto. Este color promedio se calculó tomando el contorno obtenido para el objeto y haciendo un recorte de la imagen RGB original. Luego de calcular el valor promedio del color de cada canal, este se transformó a HSV. 

Previamente se habían calculado los colores HSV promedio de los siguientes tipos de cigarrillo, con cada valor entre 0 y 255:

| Objeto     |  H  |  S  |  V  |
| ---------- |:---:|:---:| ---:|
| Cigarrillo | 101 |  50 | 215 |
| Purito     | 109 | 131 | 158 |
| Porro      | 100 |  22 | 187 |
| Habano     | 107 | 116 | 145 |


Se puede apreciar que el valor de saturación es muy diferente entre el cigarrillo y el purito y entre el porro y el habano. Esto se debe a que en el cigarrillo y en el porro el color predominante es el blanco, cuyo valor de saturación es 0.

# Resultados
<p align="center">
  <img src="https://github.com/gnoya/Cigarette-Classification-OpenCV/blob/master/images/results.png" width="411" height="482">
</p>
<p align="center">
  Imagen clasificada en colores.
</p>
