from re import S, X
from lark import Discard
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

class MyInterpreter (Interpreter):

  def __init__(self):
      self.varsDecl = dict()
      self.varsNDecl = dict ()
      self.html = str(''' <!DOCTYPE html>
<html>
<style>
    .error {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
        color: red;
    }
    
    .code {
        position: relative;
       
    }
    
    .error .errortext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -40px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .error .errortext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 20%;
        margin-left: -5px;
        border-width: 5px;
        1 border-style: solid;
        border-color: #555 transparent transparent transparent;
    }
    
    .error:hover .errortext {
        visibility: visible;
        opacity: 1;
    }
</style>

<body>
  ''')
  
  def start(self, tree):
    self.visit(tree.children[0])
    self.html = self.html + str('''</body></html>''')
    return self.html
  
  def declaracoes(self, tree):
    var = self.visit_children(tree.children[0])
    if(var[2] != ";"):
      self.varsDecl[var[1]] = {"tipo" : var[0], "inic" : 1}
    else:
      self.varsDecl[var[1]] = {"tipo" : var[0], "inic" : 0}
    self.html = self.html + "<p class='code'>\n" 
    for elem in var:
      #decl tuples e ints com operacoes
      if isinstance(elem, Token):
        self.html = self.html + elem + " "
      else:
        for i in elem:
          self.html = self.html + i + " "
    self.html = self.html + "\n</p>\n"

    

  def atribuicoes(self, tree):
    var = self.visit_children(tree)
    if (var[0] not in self.varsDecl):
      self.html = self.html + "<p class='code'><div class='error'>"+ var[0]+ "<span class='errortext'>Variável não declarada</span></div>"
      for elem in var[1:]:
        if isinstance(elem, Token):
          self.html = self.html + elem + " "
        else:
          for i in elem:
            self.html = self.html + i + " "
      
      self.html = self.html +  "</p>\n"



## Primeiro precisamos da GIC
grammar = '''
start: code
code: (variaveis | cond | input | output | ciclos)+

variaveis: declaracoes | atribuicoes 
atribuicoes: WORD IGUAL var operacao? PV
declaracoes: decint | decstring | declista | decdict | decconj | dectuplos | decfloat
decint : INTW WORD (IGUAL INT (operacao)?)? PV
declista : INTW WORD PRE PRD IGUAL CE (INT ( VIR INT)*)? CD PV
decstring: STRINGW WORD (IGUAL ESCAPED_STRING)? PV
decdict: DICTW WORD (IGUAL DICTW PE PD )? PV
decconj: CONJW WORD (IGUAL CE (ESCAPED_STRING (VIR ESCAPED_STRING)*)? CD )* PV
dectuplos: TUPLEW WORD (IGUAL PE var (VIR var)+ PD)* PV 
decfloat: FLOATW WORD (IGUAL FLOAT)* PV

operacao: ((SUM|SUB|MUL|DIV|MOD) INT)+

cond: IFW PE condicao PD CE code? CD PV
condicao: var (("=="|">"|"<"|"!=") var)?

input: WORD IGUAL INPUTW PE PD PV
output: OUTPUTW PE ESCAPED_STRING PD PV

ciclos: while | for | dowhile
while: WHILEW PE condicao PD CE code? CD PV 
for: FORW PE variaveis condicao PV WORD IGUAL tipo PD CE code? CD PV 
dowhile: DOW CE code? CD WHILEW PE condicao PD PV

var: INT | WORD | ESCAPED_STRING | WORD | ESCAPED_STRING
tipo: var operacao?

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
SUM: "+"
SUB: "-"
MUL: "*"
DIV: "/"
MOD: "%"


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
#print(parse_tree.pretty())
data = MyInterpreter().visit(parse_tree)
print(data)






