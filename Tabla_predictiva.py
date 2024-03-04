import re

class AnalizadorPredictivo:
    def __init__(self):
        self.pila = []  # Cambio de 'stack' a 'pila'
        self.entrada = []  # Cambio de 'input' a 'entrada'
        self.tabla = {
            ('S', 'LLAVEAPERTURA'): ['I', 'M', 'A', 'F'],   
            ('A', 'PUNTOCOMA'): ['PUNTOCOMA', 'M', 'A'],
            ('A', 'LLAVECIERRE'): ['epsilon'],
            ('M', 'DISPLAYDATA'): ['D', 'PARENTESISA', 'C', 'PARENTESISC'], 
            ('D', 'DISPLAYDATA'): ['DISPLAYDATA'],
            ('C', 'COMILLA'): ['COMILLA', 'T', 'COMILLA'], 
            ('I', 'LLAVEAPERTURA'): ['LLAVEAPERTURA'],
            ('F', 'LLAVECIERRE'): ['LLAVECIERRE'],
            ('T', 'LETRAS'): ['L', 'R'],
            ('L', 'LETRAS'): ['LETRAS'],
            ('R', 'LETRAS'): ['L', 'R'],
            ('R', 'COMILLA'): ['epsilon'],
        }
        
    def analizar(self, tokens):  #  'analizar'
        self.tokens = tokens
        self.pila = ['$', 'S']  # inicio de la tabla
        self.cursor = 0
        salida = []  
        
        while self.pila:
            print(f"Pila: {self.pila}")
            salida.append("Pila: " + str(self.pila[:]))
            top = self.pila[-1]  # Mira el elemento superior de la pila sin desapilarlo
            current_token = self.tokens[self.cursor][0] if self.cursor < len(self.tokens) else '$'
            
            if top == current_token:  # Coincidencia con un terminal
                self.pila.pop()  # Desapila solo si hay una coincidencia
                self.cursor += 1
            elif (top, current_token) in self.tabla:
                self.pila.pop()  # Desapila cuando reemplaza el no terminal
                simbolos = self.tabla[(top, current_token)]
                if simbolos != ['epsilon']:  # Manejo de producción vacía
                    for simbolo in reversed(simbolos):
                        self.pila.append(simbolo)
            else:
                print(f"No se encontró entrada en la tabla para: {top}, {current_token}")
                raise Exception("Error de sintaxis")
        
        if self.cursor == len(self.tokens):
            raise Exception("Error de sintaxis - La entrada no ha sido consumida completamente")
        print("Análisis completado con éxito")
        return "\n".join(salida)

def analizador_lexico(entrada_string): 
    tokens = []
    especificaciones_tokens = [
        ('DISPLAYDATA', r'\bdisplayData\b'),  # ✅
        ('LETRAS', r'[a-zA-Z]+'),  # ✅
        ('LLAVEAPERTURA', r'\{'),  # ✅
        ('LLAVECIERRE', r'\}'),  # ✅
        ('PUNTOCOMA', r'\;'),  # ✅
        ('COMILLA', r'\"'),  # ✅
        ('PARENTESISA', r'\('),  # ✅
        ('PARENTESISC', r'\)'),  # ✅
        ('IGNORAR', r'[ \t\n]+'),    
        ('NO_CORRESPONDE', r'.'),
    ]
    patron_regex = '|'.join('(?P<%s>%s)' % par for par in especificaciones_tokens)
    for coincidencia in re.finditer(patron_regex, entrada_string):
        tipo = coincidencia.lastgroup
        if tipo == 'IGNORAR':
            continue
        elif tipo == 'NO_CORRESPONDE':
            raise RuntimeError(f'Carácter ilegal: {coincidencia.group(0)}')
        else:
            tokens.append((tipo, coincidencia.group(0)))
    return tokens

def analizar_entrada(entrada_string):
    try:
        tokens = analizador_lexico(entrada_string)
        analizador = AnalizadorPredictivo()
        estado_pila = analizador.analizar(tokens)  # Asegúrate de que analizar retorne algo útil, como el estado final de la pila.
        return f"Análisis completado con éxito.\nEstado final de la pila: {estado_pila}"
        # return estado_pila
    except Exception as e:
        return str(e)
