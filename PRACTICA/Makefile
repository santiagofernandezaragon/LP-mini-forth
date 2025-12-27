# Makefile per a la pràctica de Mini Forth

# Variables
ANTLR = antlr4
PYTHON = python3
GRAMMAR = forth.g4
TEST_FILE = test.txt
MAIN_SCRIPT = forth.py

# Objectiu per defecte: genera els fitxers d'ANTLR
all: antlr

# Genera el Lexer, Parser i Visitor en Python3
antlr: $(GRAMMAR)
	$(ANTLR) -Dlanguage=Python3 -no-listener -visitor $(GRAMMAR)

# Executa els tests definits al fitxer de doctest
test: antlr
	$(PYTHON) -m doctest $(TEST_FILE)

# Executa els tests en mode 'verbose' (útil per depurar)
test-v: antlr
	$(PYTHON) -m doctest -v $(TEST_FILE)

# Executa l'intèrpret en mode interactiu
run: antlr
	$(PYTHON) -i $(MAIN_SCRIPT)

# Neteja els fitxers generats per ANTLR i la cache de Python
clean:
	rm -f forthLexer.py forthParser.py forthVisitor.py *.tokens *.interp
	rm -rf __pycache__