# Instrucciones para ejecutar  el proyecto:
Descargar y compilar glucose. Luego, pegar el archivo "glucose" dentro de la carpeta "Solver".

El proyecto ha sido desarrollado en Python. Se debe tener el interpretador de [Python](https://www.python.org/downloads/) instalado. Luego, instalar las dependencias ejecutando el siguiente comando dentro de la carpeta ./Solver:

`pip install -r requirements.txt `

Para correr el proyecto, debe estar en el directorio ./Solver. Para ello, se mueve hacia él desde la raíz del proyecto usando:

`cd Solver`

Dentro de la carpeta ./Problemas hay una variedad de problemas de ejemplos. Puede ejecutar alguno de estos problemas con el comado:


`python3 main.py <ruta al problema>`

La imagen con la solución del problema se genera dentro de la carpeta donde está el problema. El nombre de la imagen es el mismo que el del archivo del problema pero con extensión .png

### Ejemplo de ejecución
A continuación, se muestra un ejemplo para ejecutar el proyecto.

El archivo de prueba se encuentra en 

`../Problemas/kakuro-collection/3x3.txt`

Para ejecutarlo, se posiciona dentro de la carpeta ./Solver y ejecuta:

`python3 main.py ../Problemas/kakuro-collection/3x3.txt`

Esto le generara la imagen 3x3.png dentro de la carpeta `../Problemas/kakuro-collection`
