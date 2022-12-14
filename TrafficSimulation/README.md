
# Traffic Simulation

### Agentes involucrados en el proyecto:
-	Auto
    - El auto navega las calles del mapa, respetando los semáforos y la dirección de circulación, hasta llegar a su destino por el camino elegido.
-	Semáforo
    - Alternando entre verde y rojo, señaliza el siga y el alto a los autos.
-	Destino
    - Punto final que alcanza el auto para salir de la circulación del mapa.
-   Calle
    - Marca y delimita el mapa, indicando la dirección de circulación a los autos.
-   Obstáculos
    - Conforman las manzanas de edificios en el mapa adicionalmente a los Destinos.


        <br><br>![alt-text](https://github.com/G3RZZZ/TC2008B/blob/main/Documentation/TrafficGif.gif)<br><br>


## Pasos de Ejecución

### Pasos para ejecutar simulación en Mesa

1. Tener acceso a una herramienta Git.

2. Clonar el repositorio localmente.

        git clone https://github.com/G3RZZZ/TC2008B

3. Abrir un ambiente que contenga python 3.8, Flask, y Mesa
    
    Usando Anaconda:

    - ```conda create <nombre>```
    - ```conda install python=3.8```
    - ```pip install mesa```
    - ```pip instal flask```

4. Ejecutar el servidor en la dirección '...\TC2008B\TrafficSimulation\MesaVisualization\TrafficSimulation' con el comando 'python server.py'

5. Inicializar la simulación con el botón 'Start'

### Pasos para ejecutar simulación en Unity

1.	Tener acceso a una herramienta Git.

2.  Clonar el repositorio localmente.

        git clone https://github.com/G3RZZZ/TC2008B

3. Abrir un ambiente que contenga python 3.8 y Flask

    Usando Anaconda:

    -  ```conda create <nombre>```
    -  ```conda install python=3.8```
    - ```pip install mesa```
    - ```pip instal flask```

4. Ejecutar el servidor en la dirección '...\TC2008B\TrafficSimulation\Server' con el comando ```python server.py```

5. Abrir el proyecto 'UnityVisualization' en Unity ('...\TC2008B\TrafficSimulation\UnityVisualization')

6. Con el proyecto abierto, abrir la escena ```BuildCity```

7. Inicializar simulación con el botón ```Play```.
