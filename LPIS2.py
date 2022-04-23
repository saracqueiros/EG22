from re import S, X
from lark import Discard
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

class MyInterpreter (Interpreter):

  def __init__(self):
      self.varsDecl = dict()
      self.varsNDecl = dict ()
      self.varsRDecl = dict()
      self.tipoInstrucoes = {'declaracoes': 0, 'atribuicoes': 0, 'io': 0, 'ciclos': 0, 'cond': 0}
      self.totalInst = 0
      self.forC = 0
      self.inInst = {'atual': 0, 'maior': 0}
      self.aninhavel  = False 
      self.html = str(''' <!DOCTYPE html>
<html>
<style>
     p {
        line-height: 2;
        margin-top: 0;
        margin-bottom: 0;
    }
    
      .customIndent {
        padding-left: 1em;
    }
    
    .error {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
        color: red;
    }
    
    .redeclared {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
        color: blue;
    }
    
    .notinic {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
        color: grey;
    }
    .aninh {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
        color: green;
    }
    
    .code {
        position: relative;
        display: inline-block;
    }
    
    .error .errortext,
    .redeclared .redeclaredtext,
    .notinic .notinictext, .aninh .aninhtext  {
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
    
    .error .errortext::after,
    .redeclared .redeclaredtext::after,
    .notinic .notinictext::after, .aninh .aninh::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 20%;
        margin-left: -5px;
        border-width: 5px;
        1 border-style: solid;
        border-color: #555 transparent transparent transparent;
    }
    
    .error:hover .errortext,
    .redeclared:hover .redeclaredtext,
    .notinic:hover .notinictext, .aninh:hover .aninhtext {
        visibility: visible;
        opacity: 1;
    }
</style>

<body>
  ''')
  
  def start(self, tree):
    self.visit(tree.children[0])
    self.html = self.html + self.dadosfinais() + str('''</body></html>''')
    return self.html

  def dadosfinais(self):
    r = "<p><p class='code'>Variaveis declaradas: "
    for e in self.varsDecl:
      r = r + e + ": " + self.varsDecl[e]['tipo'] + " , "
    r = r + "</p></p><p><p class='code'>Variaveis não declaradas: "
    for e in self.varsNDecl:
      r = r + e + ", "
    r = r + "</p></p<p><p class='code'>Variaveis redeclaradas: "
    for e in self.varsRDecl:
      r = r + e + ", "
    r = r + "</p></p><p><p class='code'>Total Instruções: " + str(self.totalInst) + "</p></p>"
    r = r + "<p><p class='code'>Inst por tipo: " + "declaracoes: " + str(self.tipoInstrucoes['declaracoes']) + "; atribuições: " + str(self.tipoInstrucoes['atribuicoes']) + "; io: " + str(self.tipoInstrucoes['io'])+ "; ciclos: " + str(self.tipoInstrucoes['ciclos']) + "cond: " + str(self.tipoInstrucoes['cond']) + "</p></p>"
    r = r + "<p><p class='code'>Inst aninhadas: " + str(self.inInst['maior'])
    return r

  
  def declaracoes(self, tree):
    self.maior()
    self.totalInst +=1
    self.tipoInstrucoes['declaracoes'] += 1
    var = self.visit(tree.children[0])
    if (self.forC== 0):
      self.html = self.html + '<p>'
    #VErificar que a var ainda não foi declarada
    if var[1] not in self.varsDecl:
      if(var[2] != ";"):
        self.varsDecl[var[1]] = {"tipo" : var[0], "inic" : 1, "utilizada": 0}
      else:
        self.varsDecl[var[1]] = {"tipo" : var[0], "inic" : 0, "utilizada": 0}
      self.html = self.html + "<p class='code'>"+"\n" + var[0] + " " + var[1] + " "
    #Se foi declarada é anunciada com uma classe própria para tal 
    else:
      self.varsRDecl[var[1]] = {"tipo" : var[0]}
      self.html = self.html + "<p class='code'><div class='redeclared'>"+  var[0] + " " + var[1]+ "<span class='redeclaredtext'>Variável redeclarada</span></div> "
    for elem in var[2:]:
        #decl tuples e ints com operacoes
        if isinstance(elem, Token):
          self.html = self.html + elem + " "
        else:
          for i in elem:
            self.html = self.html + i + " "
    self.html = self.html + "</p>"   
    if (self.forC == 0):
      self.html = self.html + '</p>'

  def atribuicoes(self, tree):
    self.totalInst += 1
    self.maior()
    self.tipoInstrucoes['atribuicoes'] += 1
    var = self.visit_children(tree)
    if (self.forC == 0):
      self.html = self.html + '<p>'
    if (var[0] not in self.varsDecl):
      self.varsNDecl[var[0]] = {}
      self.html = self.html + "<p class='code'><div class='error'> "+ var[0]+ "<span class='errortext'>Variável não declarada</span></div>"
    else:
      self.varsDecl[var[0]]["utilizada"] += 1 
      self.varsDecl[var[0]]["inic"] = 1 
      self.html = self.html + "<p class='code'>" + var[0] + " "
    for elem in var[1:]:
        if isinstance(elem, Token):
          self.html = self.html + elem + " "
        else:
          for i in elem:
            self.html = self.html + i + " "
    self.html = self.html +  "</p>\n"
    if (self.forC == 0):
      self.html = self.html + '</p>'

  def input(self, tree):
    self.maior()
    self.totalInst += 1
    self.tipoInstrucoes['io'] += 1
    return self.visit_children(tree)

  def output(self, tree):
    self.maior()
    tokens = self.visit_children(tree)
    self.totalInst += 1
    self.tipoInstrucoes['io'] += 1
    self.html = self.html + "<p><p class='code'>"
    for t in tokens:
      self.html = self.html + t + " "
    self.html = self.html +  "</p></p>"
    return tree
 
  def ciclos(self, tree):
    self.maior()
    self.totalInst += 1
    self.tipoInstrucoes['ciclos'] += 1
    result = self.visit(tree.children[0])
    return result 

  def whilee(self, tree):
    self.maior()
    self.html = self.html + "<p><p class='code'>" 
    for i in range(2):
      self.html = self.html + tree.children[i] + " " 
    self.visit(tree.children[2])
    self.html = self.html + tree.children[3] + " " + tree.children[4] + " "
    #Significa que tem código no meio 
    self.inInst['atual'] += 1
    if len(tree.children) == 8:
      self.visit(tree.children[5])
      self.html = self.html + tree.children[6] + " " + tree.children[7]
    else:
      self.html = self.html + tree.children[5] + " " + tree.children[6]
    self.inInst['atual'] -= 1
    self.html = self.html + "</p></p>"

  def condicao(self, tree):
    self.maior()
    self.totalInst += 1
    child = self.visit_children(tree)
    flag = True #Para saber se há algum operador a escrever no meio
    first = child[0][0]
    if len(child) == 3:
      l = [first, child[2][0]]
    else:
      l = [first]
      flag = False
    if self.aninhavel == True: #Se for aninhavel colocamos a verde 
      self.html = self.html + "<div class='aninh'>"
    for var in l:
      if var.type == "WORD": #Se for uma variavel temos de ver se ela é declarada ou assim para anotar o codigo 
        if var not in self.varsDecl:
          self.varsNDecl[var] = {}
          self.html = self.html + "<div class='error'> "+ var + "<span class='errortext'>Variável não declarada</span></div>"
        else:
          self.varsDecl[var]["utilizada"] += 1 
          if self.varsDecl[var]["inic"] == 0:
            self.html = self.html + "<div class='notinic'> "+ var + "<span class='notinictext'>Variável não inicializada</span></div>"
          else:
            self.html = self.html + var 
      else:
        self.html = self.html + " " + var 
      if (flag):
          self.html = self.html + " " + child[1] + " "
          flag = False
    if self.aninhavel == True:
      self.html = self.html + "<span class='aninhtext'>Pode simplificar com a condição anterior utilizando '&&'</span></div>"
        
  def forr(self, tree):
    self.maior()
    #forr: FORW PE variaveis condicao PV WORD IGUAL tipo PD CE code? CD PV 
    self.inInst['atual']+= 1
    self.forC = 1
    self.html = self.html + "<p><p class='code'>" + tree.children[0] + " " + tree.children[1] 
    self.visit(tree.children[2])
    self.visit(tree.children[3])
    self.totalInst += 1
    self.tipoInstrucoes['atribuicoes'] += 1
    self.html = self.html + tree.children[4]
    if (tree.children[5] not in self.varsDecl):
      self.varsNDecl[tree.children[5]] = {}
      self.html = self.html + "<p class='code'><div class='error'> "+ tree.children[5]+ "<span class='errortext'>Variável não declarada</span></div>"
    else:
      self.varsDecl[tree.children[5]]["utilizada"] += 1 
      self.varsDecl[tree.children[5]]["inic"] = 1 
      self.html = self.html + tree.children[5] + " "
    self.html = self.html + tree.children[6] + " "
    self.visit(tree.children[7])
    self.html = self.html + tree.children[8] + " " + tree.children[9] + " "
    self.forC = 1
    if (isinstance(tree.children[10], Token)):
      self.html = self.html + tree.children[10] + " " + tree.children[11] + " "
    else:
      self.visit(tree.children[10])
      self.html = self.html + tree.children[11] + " " + tree.children[12] + " "
    self.inInst['atual'] -= 1
    self.html = self.html +  "</p></p>"


  def tipo(self, tree):
    #var operacao?
    #operacao: ((SUM|SUB|MUL|DIV|MOD) INT)+
    var = self.visit(tree.children[0])
    self.html = self.html + var[0]
    operacao = self.visit(tree.children[1])
    for op in operacao:
      self.html = self.html + op


  def dowhile (self, tree):
    self.maior()
    #dowhile: DOW CE code? CD WHILEW PE condicao PD PV
    self.html = self.html + "<p><p class='code'>" 
    for elem in tree.children:
      if isinstance(elem, Token):
        self.html = self.html + elem + " "
      else:
        self.visit(elem)
    self.html = self.html + "</p>"


  def cond(self, tree):
    #cond: IFW PE condicao PD CE code? CD PV
    self.totalInst += 1
    self.inInst['atual'] +=1
    self.tipoInstrucoes['cond'] += 1
    self.html = self.html + "<p><p class='code'>" 
    for elem in tree.children[:5]:
      if isinstance(elem, Token):
        self.html = self.html + elem + " "
      else:
        self.visit(elem)
    if len(tree.children) == 8: ##condicções para os ifs aninhados, sinalizar se puder simplificar
      if tree.children[5].children[0].data == 'cond':
        self.aninhavel = True
      else: 
        self.aninhavel = False
      self.visit(tree.children[5])
      self.html = self.html + tree.children[6] + " " + tree.children[7]
    else:
      self.html = self.html + tree.children[5] + " " + tree.children[6]
    self.html = self.html + "</p>"
    self.inInst['atual'] -=1
    
  def maior(self):
    if self.inInst['atual'] > self.inInst['maior']:
      self.inInst['maior'] = self.inInst['atual']
## Primeiro precisamos da GIC
grammar = '''
start: code
code: (variaveis | cond | output | ciclos )+

variaveis: declaracoes | atribuicoes 
atribuicoes: WORD IGUAL ((var operacao? PV)|input)
declaracoes: decint | decstring | declista | decdict | decconj | dectuplos | decfloat | decinput |decvallist
decvallist: (INTW | STRINGW | FLOAT) WORD IGUAL WORD PRE INT PRD PV
decint : INTW WORD (IGUAL INT (operacao)?)? PV
declista : INTW WORD PRE PRD IGUAL CE (INT ( VIR INT)*)? CD PV
decstring: STRINGW WORD (IGUAL ESCAPED_STRING)? PV
decdict: DICTW WORD (IGUAL DICTW PE PD )? PV
decconj: CONJW WORD (IGUAL CE (ESCAPED_STRING (VIR ESCAPED_STRING)*)? CD )* PV
dectuplos: TUPLEW WORD (IGUAL PE var (VIR var)+ PD)* PV 
decfloat: FLOATW WORD (IGUAL FLOAT)* PV
decinput: STRINGW IGUAL input

operacao: ((SUM|SUB|MUL|DIV|MOD) INT)+

condicao: var ((II|MAIOR|MENOR|DIF|E|OU) var)?
cond: IFW PE condicao PD CE code? CD PV

input: INPUTW PE PD PV
output: OUTPUTW PE ESCAPED_STRING PD PV

ciclos: whilee | forr | dowhile
whilee: WHILEW PE condicao PD CE code? CD PV 
forr: FORW PE variaveis condicao PV WORD IGUAL tipo PD CE code? CD PV 
dowhile: DOW CE code? CD WHILEW PE condicao PD PV

var: INT | WORD | ESCAPED_STRING | WORD 
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
PV:";"
VIR:","
SUM: "+"
SUB: "-"
MUL: "*"
DIV: "/"
MOD: "%"
II: "=="
MAIOR: ">"
MENOR: "<"
DIF: "!="
E: "&&"
OU: "||"
IGUAL:"="

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






