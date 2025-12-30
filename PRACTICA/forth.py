import sys
from antlr4 import *
from forthLexer import forthLexer
from forthParser import forthParser
from forthVisitor import forthVisitor

global_defs= {}

class ForthError(Exception):
    """Excepció personalitzada per als errors del nostre intèrpret."""
    pass

class TreeVisitor(forthVisitor):
    def __init__(self):
        # La Pila de dades (inicialment buida)
        self.stack = []
        # Diccionari per guardar definicions de funcions (nom -> node de l'arbre)
        self.defs = global_defs
        # Pila per saber quina funció s'està executant (per al 'recurse')
        self.current_func_name = []

    def visitRoot(self, ctx):
        # Visita tots els fills (instruccions o definicions) en ordre
        for child in ctx.getChildren():
            self.visit(child)

    def visitPushNumber(self, ctx):
        # Quan trobem un número, el convertim a int i el posem a la pila
        num = int(ctx.getText())
        self.stack.append(num)

    def visitPrintTop(self, ctx):
        # Implementació del '.' (treure tope i imprimir)
        if not self.stack:
            raise ForthError("Stack underflow")
        print(self.stack.pop(), end='') # Forth sol imprimir sense salt de línia extra, o amb espai

    def visitPrintStack(self, ctx):
        # Implementació del '.s' (mostrar pila sense tocar-la)
        # El format de sortida sol ser <count> [elem1, elem2, ...] o directament la llista
        # Segons l'enunciat sembla que printar la llista directament és acceptable:
        print(f"<{len(self.stack)}> {str(self.stack).replace(',', '')}") 

    # --- Aquí anirem afegint la resta de mètodes (Suma, Resta, Dup, If...) ---
    # --- Operacions Aritmètiques ---

    def visitAdd(self, ctx):
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a + b)

    def visitSub(self, ctx):
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a - b)

    def visitMul(self, ctx):
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a * b)

    def visitDiv(self, ctx):
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        if b == 0: raise ForthError("Division by zero")
        # Forth treballa amb enters, fem servir divisió entera //
        self.stack.append(a // b)

    def visitMod(self, ctx):
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        if b == 0: raise ForthError("Division by zero")
        self.stack.append(a % b)

    # --- Operacions de Pila Simples ---

    def visitStackDup(self, ctx):
        # ( a -- a a )
        if not self.stack: raise ForthError("Stack underflow")
        self.stack.append(self.stack[-1])

    def visitStackDrop(self, ctx):
        # ( a -- )
        if not self.stack: raise ForthError("Stack underflow")
        self.stack.pop()

    def visitStackSwap(self, ctx):
        # ( a b -- b a )
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(b)
        self.stack.append(a)

    def visitStackOver(self, ctx):
        # ( a b -- a b a )
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        self.stack.append(self.stack[-2])

    def visitStackRot(self, ctx):
        # ( a b c -- b c a )
        if len(self.stack) < 3: raise ForthError("Stack underflow")
        c = self.stack.pop()
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.extend([b, c, a])

    # --- Operacions de Pila Dobles (prefix 2) ---
    # Tracten parelles de números com si fossin un sol element

    def visitStack2Dup(self, ctx):
        # ( a b -- a b a b )
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        self.stack.extend(self.stack[-2:])

    def visitStack2Drop(self, ctx):
        # ( a b -- )
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        self.stack.pop()
        self.stack.pop()

    def visitStack2Swap(self, ctx):
        # ( a b c d -- c d a b )
        if len(self.stack) < 4: raise ForthError("Stack underflow")
        d = self.stack.pop()
        c = self.stack.pop()
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.extend([c, d, a, b])

    def visitStack2Over(self, ctx):
        # ( a b c d -- a b c d a b )
        if len(self.stack) < 4: raise ForthError("Stack underflow")
        self.stack.extend(self.stack[-4:-2])


    # --- Operacions Relacionals i Booleanes ---

    def visitEqual(self, ctx):
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(-1 if a == b else 0)

    def visitNotEqual(self, ctx):
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(-1 if a != b else 0)

    def visitLess(self, ctx):
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(-1 if a < b else 0)

    def visitGreater(self, ctx):
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(-1 if a > b else 0)

    def visitLogicAnd(self, ctx):
        # Bitwise AND (funciona per a -1 i 0)
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a & b)

    def visitLogicOr(self, ctx):
        # Bitwise OR
        if len(self.stack) < 2: raise ForthError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a | b)

    def visitLogicNot(self, ctx):
        # Bitwise NOT (Invertir bits)
        if not self.stack: raise ForthError("Stack underflow")
        a = self.stack.pop()
        self.stack.append(~a)

    # --- Estructures de Control ---

    def visitIfStatement(self, ctx):
        if not self.stack: raise ForthError("Stack underflow")
        condition = self.stack.pop()
        
        # En Forth, qualsevol cosa diferent de 0 és True
        if condition != 0:
            self.visit(ctx.block(0)) # Executa el bloc del IF
        elif ctx.ELSE(): 
            # Si la condició és falsa i tenim token ELSE, executem el 2n bloc
            self.visit(ctx.block(1))

    def visitDefFunction(self, ctx):
        # Guardem la definició. NO visitem el block ara.
        name = ctx.ID().getText()
        self.defs[name] = ctx.block()

    def visitCallFunction(self, ctx):
        name = ctx.ID().getText()
        if name in self.defs:
            # Entrem a la funció: apilem el nom per si hi ha 'recurse'
            self.current_func_name.append(name)
            try:
                self.visit(self.defs[name])
            finally:
                # Sortim de la funció: desapilem el nom
                self.current_func_name.pop()
        else:
            raise ForthError(f"Unknown word: {name}")

    def visitRecursiveCall(self, ctx):
        if not self.current_func_name:
            raise ForthError("recurse used outside of a function definition")
        
        # Cridem la funció que tenim al tope de la pila de noms
        func_name = self.current_func_name[-1]
        self.visit(self.defs[func_name])

def interpret(input_stream):
    # Setup del pipeline d'ANTLR
    lexer = forthLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = forthParser(token_stream)
    
    parser.removeErrorListeners()
    # L'entrada comença per la regla 'root'
    tree = parser.root()
    
    # Si hi ha errors sintàctics, el parser ja s'haurà queixat per stderr.
    if parser.getNumberOfSyntaxErrors() > 0:
        # Podem decidir parar o continuar, l'enunciat demana gestionar errors.
        print("Syntax Error")
        return

    # Creem el nostre visitador i recorrem l'arbre
    visitor = TreeVisitor()
    try:
        visitor.visit(tree)
    except ForthError as e:
        print(f"Runtime Error: {e}")
    except Exception as e:
        # Captura genèrica per si de cas
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    
    # Si hi ha arguments o estem passant un fitxer per "pipe" (<), executem normal
    if len(sys.argv) > 1 or not sys.stdin.isatty():
        input_stream = InputStream(sys.stdin.read())
        interpret(input_stream)
    
    # Si no, obrim mode interactiu
    else:
        print("Mini Forth Interpreter (escriu 'exit' per sortir)")
        while True:
            try:
                # Mostrem un prompt personalitzat
                text = input("? ")
                if text.strip() == "exit": break
                
                # Executem la línia
                interpret(InputStream(text))
                print() # Salt de línia extra per estètica
                
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")