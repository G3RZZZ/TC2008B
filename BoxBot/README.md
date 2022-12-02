## Evidencia 1. Actividad Integradora

### Descripción de Evidencia
Este apartado contiene la simulación del ordenamiento de cajas en un almacén. 
Se desarrolla un modelo de comportamiento de un agente robot que busque colocar una caja a la vez en una bahía correspondiente en un espacio determinado. 
En su tarea el agente debe evitar obstáculos y realizar las tareas de recoger cajas y moverse de manera eficiente. 
Se modelaron representaciones 3D de los agentes, Robot, Caja, Torre/Bahía, y obstáculo. 
Empleando texturas e iluminación en la representación de Unity

## Pasos de Ejecución

### Pasos para ejecutar simulación en Mesa

1. Tener acceso a una herramienta Git.

2. Clonar el repositorio localmente.

        git clone https://github.com/G3RZZZ/TC2008B

3. Abrir un ambiente que contenga python 3.8 y Flask
    
    Usando Anaconda:

    - ```conda create <nombre>```
    - ```conda install python=3.8```
    - ```pip install mesa```
    - ```pip instal flask```

4. Ejecutar el servidor en la dirección '...\TC2008B\BoxBot\WebServerVizualization' con el comando ```python server.py```

5. Inicializar la simulación con el botón ```Start```

### Pasos para ejecutar simulación en Unity

1.	Tener acceso a una herramienta Git (Git cli o Github Desktop).

2. Copiar repositorio de manera local.

        git clone https://github.com/G3RZZZ/TC2008B

3. Abrir un ambiente que contenga python 3.8, Flask

    Usando Anaconda:

    - ```conda create <nombre>```
    - ```conda install python=3.8```
    - ```pip instal flask```

4. Inicializar servidor de la dirección '.../TC2008B/BoxBot/UnityVizualization/Server/' con el comando ```python server.py```

5. Abrir proyecto del folder '.../TC2008B/BoxBot/UnityVizualization/BotUnity/' en Unity

6. Ejecutar simulación con botón ```Play``` de Unity.



