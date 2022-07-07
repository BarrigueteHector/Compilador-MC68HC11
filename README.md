# Compilador MC68HC11

Proyecto
--------------------------------------------------------------------------------------------------------------------------------------------------------
Programar un compilador básico del MC68HC11 en cualquier lenguaje de programación de alto nivel.

Consideraciones
--------------------------------------------------------------------------------------------------------------------------------------------------------
- Debe reconocer todos los mnemónicos del set de instrucciones del MC68HC11, tanto en mayúsculas como minúsculas, así como la sintaxis de cada uno de los seis modos de direccionamiento.
- Debe soportar archivos documentados (con comentarios, los cuales debe ignorar).
- Deberá reconocer las directivas `ORG`, `EQU`, `FCB` y `END`.
- Debe de abrir un archivo de texto con extensión `.asc`, que tendrá el código en lenguaje ensamblador (código que se va a compilar).
- Se debe generar un archivo de texto con extensión `.LST` que tenga el código fuente y objeto empleando el siguiente formato (***en una sola línea***):

`Número de linea`: `Código objeto`: `código fuente`
- Se generará un archivo de texto con exttensión `.S19` que contenga el código objeto correspondiente empleando el siguiente formato (***en una sola línea***):

`<Dirección> XX0 XX1 XX2 XX3 XX4 XX5 XX6 XX7 XX8 XX9 XXA XXB XXC XXD XXE XXF`
- Debe detectar errores (***posteriormente se explica cada uno***).

Errores
--------------------------------------------------------------------------------------------------------------------------------------------------------
| # de error | Tipo de error |
| :----------: | ------------- |
| 1          | Constante inexistente              |
| 2          | Variable inexistente              |
| 3          | Etiqueta inexistente              |
| 4          | Mnemónico inexistente              |
| 5          | Instrucción carece de operandos              |
| 6          | Instrucción no lleva operandos              |
| 7          | Magnitud de operando erronea              |
| 8          | Salto relativo muy lejano              |
| 9          | Instrucción carece de almenos un espacio relativo al margen              |
| 10         | No se encuentra ***END***              |

Extra
--------------------------------------------------------------------------------------------------------------------------------------------------------
En el archivo [Ejemplo](https://github.com/BarrigueteHector/Compilador-MC68HC11/blob/main/ejemplo.asc) se presenta un programa en el que se pretendío implementar todas las instrucciones **MC68HC11**.

Para la ejecución del código es necesario descargar los archivos [instrucciones](https://github.com/BarrigueteHector/Compilador-MC68HC11/blob/main/instrucciones.csv) y [Lista instrucciones](https://github.com/BarrigueteHector/Compilador-MC68HC11/blob/main/lista_instrucciones.csv).

Ejemplo
--------------------------------------------------------------------------------------------------------------------------------------------------------
Si se ejecuta el archivo [Ejemplo](https://github.com/BarrigueteHector/Compilador-MC68HC11/blob/main/ejemplo.asc) se generarán los archivos de la carpeta [Archivos generados](https://github.com/BarrigueteHector/Compilador-MC68HC11/tree/main/Archivos%20generados).

El ejemplo tiene algunos errores para comprobar que el funcionamiento, en dicha apartado, sea correcto. Los errores son los siguientes:
- **ERROR 004**: Mnemonico inexistente: XGDY
- **ERROR 004**: Mnemonico inexistente: XGDY
- **ERROR 004**: Mnemonico inexistente: XGDY
- **ERROR 004**: Mnemonico inexistente: XGDY
- **ERROR 009**: Se esperaba un espacio antes de: COMA
