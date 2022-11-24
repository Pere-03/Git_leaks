# Git_leaks
Un buscador de palabras conflictivas en commits de un repositorio

Esta buscará los commits de un repo de git (indicado en el código) y verá si hay alguna palabra peligrosa en los mismos.
Si la hay, imprimirá por pantalla el commit que ha hecho saltar las alarmas, con esa palabra comprometida y el autor del commit.
Todo esto lo imprimirá por pantalla y lo guardará en un json (si lo ejecutamos con docker, habrá que asignar un volumen al contenedor
cuando lo ejecutemos)
