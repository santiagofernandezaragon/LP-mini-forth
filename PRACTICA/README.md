# Pràctica LP: Mini Forth Interpreter

**Autor:** Santiago Fernandez Aragon
**Assignatura:** Llenguatges de Programació (2025-2026 Q1)

## Descripció
Aquest projecte consisteix en la implementació d'un intèrpret per a un subconjunt del llenguatge **Forth** (Mini Forth), utilitzant **Python 3** i **ANTLR4**.

L'intèrpret permet realitzar operacions aritmètiques, manipulació de la pila, lògica booleana, definició de funcions i estructures de control (condicionals i recursivitat).

## Estructura del Projecte
* **`forth.g4`**: Gramàtica d'ANTLR4 que defineix el lèxic i la sintaxi del llenguatge.
* **`forth.py`**: Codi principal en Python. Conté la lògica de l'intèrpret i la implementació del `Visitor`.
* **`test.txt`**: Joc de proves complet en format `doctest`.
* **`Makefile`**: Automatització per generar els fitxers d'ANTLR i executar els tests.
* **`README.md`**: Aquest document.

## Instruccions d'Ús

### Requisits
* Python 3
* ANTLR4 (i el runtime de Python: `antlr4-python3-runtime`)

### Compilació i Execució
El projecte inclou un `Makefile` per facilitar les tasques:

1.  **Generar l'analitzador (Parser/Lexer):**
    ```bash
    make antlr
    ```
2.  **Executar els tests:**
    ```bash
    make test      # Execució estàndard
    make test-v    # Execució detallada (verbose)
    ```
3.  **Executar l'intèrpret interactiu:**
    Inicia la consola REPL per provar codi manualment:
    ```bash
    make run
    ```
    S'obrirà l'entorn interactiu. Aquí tens un **exemple d'ús**:

    ```text
    Mini Forth Interpreter (escriu 'exit' per sortir)
    ? 10 20 + .
    30
    ? : quadrat dup * ;
    ? 5 quadrat .
    25
    ? exit
    ```


4.  **Netejar fitxers generats:**
    ```bash
    make clean
    ```

 5. **Joc de Proves (Tests)**

El projecte inclou un conjunt exhaustiu de proves automatitzades al fitxer `test.txt`, implementat utilitzant el mòdul **`doctest`** de Python. Aquest format permet que els tests serveixin simultàniament com a documentació d'ús i com a verificació funcional.

Les proves estan organitzades temàticament i cobreixen la totalitat dels requisits de la pràctica:

* **Aritmètica:** Operacions bàsiques (`+`, `-`, `*`, `/`, `mod`) i gestió de nombres negatius.
* **Manipulació de la Pila:** Comprovació del funcionament correcte de `dup`, `swap`, `drop`, `over`, `rot` i les seves variants dobles (`2dup`, `2swap`, etc.).
* **Lògica i Comparadors:** Avaluació d'expressions booleanes (`=`, `<`, `>`) i operadors lògics (`and`, `or`, `not`).
* **Estructures de Control:** Testeig de condicionals `if ... else ... endif` niats i simples dins de definicions.
* **Funcions i Recursivitat:** Definició de noves paraules i verificació d'algorismes recursius (ex: càlcul del factorial).
* **Robustesa i Errors:** Es verifica que l'intèrpret gestiona correctament situacions anòmales (divisió per zero, *stack underflow*, paraules desconegudes) llançant les excepcions controlades corresponents sense tancar el programa inesperadament.

## Decisions de Disseny

### 1. Ús del patró Visitor
S'ha optat per utilitzar el patró **Visitor** (en lloc de Listener) perquè permet un control més natural del flux d'execució.
* Ens permet avaluar les expressions aritmètiques i empilar els resultats immediatament.
* Facilita la gestió de les estructures de control (`if/else`): podem decidir visitar o no certs blocs de codi (`ctx.block()`) depenent del valor al cim de la pila.

### 2. Gestió de la Memòria (Funcions)
Les definicions de funcions (`: nom ... ;`) s'emmagatzemen en un diccionari global (`global_defs`).
* **Decisió:** S'ha utilitzat una variable global en lloc d'una instància local dins del `Visitor` per garantir la persistència de les funcions entre diferents crides a `interpret()`. Això permet definir una funció en una línia i utilitzar-la en la següent durant una sessió interactiva o en els tests.

### 3. Gestió d'Errors
S'ha creat una excepció personalitzada `ForthError` per capturar errors d'execució específics com:
* *Stack underflow* (intentar desempilar de pila buida).
* *Division by zero*.
* *Unknown word* (funció no definida).
* *Recurse error* (ús fora de funció).

Els errors sintàctics són detectats automàticament pel parser d'ANTLR, mentre que els errors lògics es capturen al `try-except` principal del programa per evitar que l'intèrpret es tanqui inesperadament, mostrant sempre un missatge clar a l'usuari.

### 4. Estructures de Dades
* **Pila de Dades:** S'ha utilitzat una llista de Python (`[]`) actuant com a LIFO (`append`/`pop`).
* **Booleans:** Seguint l'estàndard Forth, `True` es representa com `-1` i `False` com `0`.

## Implementació
S'han implementat totes les funcionalitats requerides a l'enunciat:
* [x] Aritmètica: `+`, `-`, `*`, `/`, `mod`.
* [x] Pila: `dup`, `swap`, `drop`, `over`, `rot` (i variants `2-`).
* [x] E/S: `.`, `.s`.
* [x] Lògica: `=`, `<`, `>`, `and`, `or`, `not`.
* [x] Control: `if ... else ... endif
