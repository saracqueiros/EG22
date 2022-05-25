from ctypes import sizeof
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter
from sys import argv

class MyInterpreter (Interpreter):

    def __init__(self):
        self.total = 0
        self.movsCredito = 0
        self.contasDestDeb = list()
    
    def start(self, tree):
        self.visit(tree.children[0])
        return self.total, self.movsCredito, self.contasDestDeb

    def move(self, tree):
        sinal = self.visit(tree.children[2])
        print(sinal)
        if sinal[0].type == 'CREDITO':
            self.movsCredito +=1
            self.total += int(self.visit(tree.children[3])[0])
        elif sinal[0].type == 'DEBITO':
            self.total -= int(self.visit(tree.children[3])[0])
            conta = self.visit(tree.children[1])
            self.contasDestDeb.append(str(conta[0]))

        


    

grammar = '''
start: code
code:  movimentos 
movimentos: move "." | movimentos move "."
move: data ";" cntdestino ";" sinal ";" quantia ";" cntordenante ";" descr
cntdestino: WORD
sinal: CREDITO | DEBITO
quantia: INT
cntordenante: WORD
descr: WORD
data: WORD

CREDITO:"credito"
DEBITO:"debito"
INTW: "int"
IGUAL:"="
PV:";"
WORD: "a".."z"("a".."z"|"0".."9")*

%import common.WS
%import common.INT
%import common.ESCAPED_STRING
%import common.NUMBER


%ignore WS
'''
f = open(argv[1], "r")

linhas = f.read()
p = Lark(grammar, propagate_positions = True) 
parse_tree = p.parse(linhas)
#print(parse_tree.pretty())
data = MyInterpreter().visit(parse_tree)
print(data)
