from re import S, X
from lark import Discard
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

class MyInterpreter (Interpreter):

  def __init__(self):
      self.algo = dict()
      


  

## Primeiro precisamos da GIC
grammar = '''
start: code
code: (variaveis | cond | input | output | ciclos)+

variaveis: declaracoes | atribuicoes 
atribuicoes: WORD IGUAL tipo PV
declaracoes: decint | decstring | declista | decdict | decconj | dectuplos | decfloat
decint : INTW WORD (IGUAL INT (operacao)?)? PV
declista : INTW WORD PRE PRD IGUAL CE (INT ( VIR INT)*)? CD PV
decstring: STRINGW WORD (IGUAL ESCAPED_STRING)? PV
decdict: DICTW WORD (IGUAL DICTW PE PD )? PV
decconj: CONJW WORD (IGUAL CE (ESCAPED_STRING (VIR ESCAPED_STRING)*)? CD )* PV

operacao: (("+"|"-"|"*"|"/"|"%") INT)+

cond: IFW PE condicao PD CE code? CD PV
condicao: var (("=="|">"|"<"|"!=") var)?

input: WORD IGUAL INPUTW PE PD PV
output: OUTPUTW PE ESCAPED_STRING PD PV

ciclos: while | for | dowhile
while: WHILEW PE condicao PD CE code? CD PV 
for: FORW PE variaveis condicao PV WORD IGUAL tipo PD CE code? CD PV 
dowhile: DOW CE code? CD WHILEW PE condicao PD PV

tipo: (INT | WORD | ESCAPED_STRING | FLOAT ) operacao?
dectuplos: TUPLEW WORD (IGUAL PE var (VIR var)+ PD)* PV 
decfloat: FLOATW WORD (IGUAL FLOAT)* PV
var: INT | WORD | ESCAPED_STRING | WORD | ESCAPED_STRING

INT:("0".."9")+
INTW: "int"
INPUTW: "input"
OUTPUTW: "print"
STRINGW: "string"
DICTW: "dict"
CONJW: "conj"
TUPLEW: "tuple"
FLOATW: "float"
WHILEW: "while"
DOW: "do"
IFW: "if"
FORW: "for"
WORD: "a".."z"("a".."z"|"0".."9")*
FLOAT: "0".."9"+".""0".."9"+

PE:"("
PRE:"["
PRD: "]"
PD:")"
CE:"{"
CD:"}"
IGUAL:"="
PV:";"
VIR:","


%import common.WS
%import common.NEWLINE 
%import common.ESCAPED_STRING
%ignore NEWLINE
%ignore WS
'''

f = open("exemplo.txt", "r")

linhas = f.read()
p = Lark(grammar) 
parse_tree = p.parse(linhas)
print(parse_tree.pretty())
data = MyInterpreter().visit(parse_tree)
#print(data)






