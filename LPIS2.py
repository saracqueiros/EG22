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
      self.tipoInstrucoes = {'declaracoes': 0, 'atribuicoes': 0, 'io': 0, 'ciclos': 0, 'cond': 0, 'funcoes': 0}
      self.totalInst = 0
      self.forC = 0
      self.inInst = {'atual': 0, 'maior': 0, 'total': 0}
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
        color: orange;
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

    table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>

<body> <p><b> Código anotado:</b></p>
  ''')
  
  def start(self, tree):
    #start: code
    self.visit(tree.children[0])
    self.html = self.html + self.dadosfinais() + str('''</body></html>''')
    return self.html

  def dadosfinais(self):
    r = "<p><p class='code'>-------------------------Análise Geral-------------------------\n<p>Variáveis declaradas: </p><ul>"
    for e in self.varsDecl:
      r = r + "<li><b>" + e + "</b>: " + self.varsDecl[e]['tipo'] + "</li>"
    r = r + "</ul></p></p><p><p class='code'>Variáveis não declaradas: <ul>"
    for e in self.varsNDecl:
      r = r + "<li><b>" + e + "</b></li> "
    r = r + "</ul></p></p><p><p class='code'>Variaveis redeclaradas: <ul>"
    for e in self.varsRDecl:
      r = r + "<li><b>" + e + "</b></li> "
    r = r + "</ul></p></p><p><p class='code'>Variaveis declaradas e nunca mencionadas: <ul>"
    for e in self.varsDecl:
      if self.varsDecl[e]['utilizada'] == 0:
        r = r + "<li><b>" + e + "</b> </li>"
    r = r + "</ul></p></p>\n<p><p class='code'>-------------------------------Análise Instruções-------------------------------\n<p>"
    r = r + " <table>\n <tr> <th> Nº Declarações </th><th>" + str(self.tipoInstrucoes['declaracoes']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Atribuições </th><th>" + str(self.tipoInstrucoes['atribuicoes']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Input/Output </th><th>" + str(self.tipoInstrucoes['io']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Ciclos </th><th>" + str(self.tipoInstrucoes['ciclos']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Inst. Condicionais </th><th>" + str(self.tipoInstrucoes['cond']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Funções </th><th>" + str(self.tipoInstrucoes['funcoes']) + "</th></tr>"
    r = r + " \n <tr> <th> Total Instruções </th><th>" + str(self.totalInst) + "</th></tr></table>"
    if (self.inInst['total']!=0):
      r = r + " \n<p><p class='code'> NOTA: Existem <b>"+ str(self.inInst['total']) + "</b> situações de aninhamento e o nível máximo de instruções condicionais aninhadas é <b>" + str(self.inInst['maior']) + "</b>. Sugestões de simplificação são mencionadas no código acima.</p></p> "
    else:
     r = r + " \n<p><p class='code'> NOTA: Existem <b>"+ str(self.inInst['total']) + "</b> situações de aninhamento."
    return r

  
  def declaracoes(self, tree):
    self.maior()
    self.totalInst +=1
    self.tipoInstrucoes['declaracoes'] += 1
    var = self.visit(tree.children[0])
    if (self.forC== 0):
      self.html = self.html + '<p>'
    #Verificar que a var ainda não foi declarada
    if var[1] not in self.varsDecl:
      if(var[2] != ";"):
        if(var[2] == "["):
          self.varsDecl[var[1]] = {"tipo" : var[0] + "[]", "inic" : 1, "utilizada": 0}
        else:
          self.varsDecl[var[1]] = {"tipo" : var[0], "inic" : 1, "utilizada": 0}
      else:
        self.varsDecl[var[1]] = {"tipo" : var[0], "inic" : 0, "utilizada": 0}
      self.html = self.html + "<p class='code'>"+"\n" + var[0] + " " + var[1] + " "
    #Se já foi declarada é anunciada com uma classe própria para tal 
    else:
      self.varsRDecl[var[1]] = {"tipo" : var[0]}
      self.html = self.html + "<p class='code'><div class='redeclared'>"+  var[0] + " " + var[1]+ "<span class='redeclaredtext'>Variável redeclarada</span></div> "
    for elem in var[2:]:
        #decl tuples e ints com operacoes
        if isinstance(elem, Token):
          #Casos como: int x = y + 1
          if elem.type == 'WORD' and elem not in self.varsDecl:
            self.html = self.html + "<p class='code'><div class='error'> "+ elem + " <span class='errortext'>Variável não declarada</span></div> "
          else:
            if elem.type == 'WORD':
              self.varsDecl[elem]["utilizada"] += 1
            self.html = self.html + elem + " "
        else:
          for i in elem:
            self.html = self.html + i + " "
    if (self.forC == 0):
      self.html = self.html + '</p>'
    self.html = self.html + "</p>\n"   


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
            #Utilização de variaveis nao declaradas à direita da operação 

            if i.type == 'WORD':
              if i not in self.varsDecl:
                self.varsNDecl[i] = {}
                self.html = self.html + "<p class='code'><div class='error'> "+ i + " <span class='errortext'>Variável não declarada</span></div> "
              else:
                self.varsDecl[i]["utilizada"] += 1
                self.html = self.html + i + " "
            else:
              self.html = self.html + i + " "
    if (self.forC == 0):
      self.html = self.html + '</p>'
    self.html = self.html +  "</p>\n"

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
    self.html = self.html +  "</p></p>\n"
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
    if self.inInst['atual'] == 1:
      self.inInst['total'] += 1
    self.html = self.html + "</p></p>\n"

  
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
    if self.inInst['atual'] == 1:
      self.inInst['total'] += 1
    self.html = self.html +  "</p></p>\n"


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
    self.html = self.html + "</p>\n"


  def cond(self, tree):
    #cond: IFW PE condicao PD CE code? CD else? PV
    self.totalInst += 1
    self.inInst['atual'] +=1
    self.tipoInstrucoes['cond'] += 1
    self.html = self.html + "<p><p class='code'>" 
    for elem in tree.children[:5]:
      if isinstance(elem, Token):
        self.html = self.html + elem + " "
      else:
        self.visit(elem)
    if not isinstance(tree.children[5], Token): #condições para os ifs aninhados, sinalizar se puder simplificar
      if tree.children[5].children[0].data == 'cond':
        self.aninhavel = True
      else: 
        self.aninhavel = False
      self.visit(tree.children[5])
      self.html = self.html + tree.children[6] + " " 
      if not isinstance(tree.children[7], Token): #Se houver um else
        self.visit(tree.children[7])
        self.html = self.html + tree.children[8] + " " 
      else:
        self.html = self.html + tree.children[7] + " " 
    else:
      self.html = self.html + tree.children[5] + " " 
      if not isinstance(tree.children[6], Token): #Se houver um else sem codigo no if 
        self.visit(tree.children[6])
        self.html = self.html + tree.children[7] + " " 
      else:
        self.html = self.html + tree.children[6] + " " 
    self.html = self.html + "</p>\n"
    self.inInst['atual'] -=1
    if self.inInst['atual'] == 1:
      self.inInst['total'] += 1


  def elsee(self,tree):
    #elsee: ELSEW CE code CD
    for elem in tree.children:
      if not isinstance(elem, Token):
        self.visit(elem)
      else:
        self.html = self.html + elem + " "


    
  def funcao(self, tree):
    self.totalInst += 1
    self.tipoInstrucoes['funcoes'] += 1
    self.html = self.html + "<p><p class='code'>" 
    for elem in tree.children[:6]:
      if isinstance(elem, Token):
        self.html = self.html + elem + " "
      else:
        self.visit(elem)
    if not isinstance(tree.children[6], Token):
      if tree.children[6].data == 'code':
        self.visit(tree.children[6])
        if not isinstance(tree.children[7], Token): #SE nao for um token é return
          self.html = self.html + "<p>"
          for i in tree.children[7].children:
            self.html = self.html + i + " "
          self.html = self.html + "</p>" + tree.children[8] + " "
        else:
          self.html = self.html + tree.children[7] + " "
      elif tree.children[6].data == 'return':
        self.html = self.html + "<p>"
        for i in tree.children[6].children:
            self.html = self.html + i + " "
        self.html = self.html + "</p>" +tree.children[7] + " "
    
  def args(self, tree):
    for elem in tree.children:
      if isinstance(elem, Token):
        self.html = self.html + elem + " "
      else:
        self.html = self.html + elem.children[0] + " "


  
  def maior(self):
    if self.inInst['atual'] > self.inInst['maior']:
      self.inInst['maior'] = self.inInst['atual']
## Primeiro precisamos da GIC
grammar = '''
start: code
code: (variaveis | cond | output | ciclos | funcao)+

variaveis: declaracoes | atribuicoes 
atribuicoes: WORD IGUAL ((var operacao? PV)| input |lista | dicionario)
declaracoes: decint | decstring | declista | decdict | decconj | dectuplos | decfloat | decinput | decvallist
decvallist: (INTW | STRINGW | FLOATW) WORD IGUAL WORD (PRE INT PRD)+ PV
decint : INTW WORD (IGUAL INT (operacao)?)? PV
declista : INTW WORD PRE PRD IGUAL CE (INT ( VIR INT)*)? CD PV
decstring: STRINGW WORD (IGUAL ESCAPED_STRING)? PV
decdict: DICTW WORD (IGUAL DICTW PE PD )? PV
decconj: CONJW  WORD (IGUAL CE (ESCAPED_STRING (VIR ESCAPED_STRING)*)? CD )* PV
dectuplos: TUPLEW WORD (IGUAL PE var (VIR var)+ PD)* PV 
decfloat: FLOATW WORD (IGUAL FLOAT)* PV
decinput: STRINGW IGUAL input

operacao: ((SUM|SUB|MUL|DIV|MOD) INT)+
lista: WORD (PRE INT PRD)+ PV
dicionario: CE ESCAPED_STRING DP (INT | WORD)(VIR ESCAPED_STRING DP (INT | WORD))* CD PV

funcao: DEFW WORD PE args PD CE code? return? CD 
args: (types WORD VIR)* types WORD 
types: (STRINGW |DICTW |INTW | TUPLEW| FLOATW| CONJW)
return: RETURNW (WORD VIR)* WORD

condicao: var ((II|MAIOR|MENOR|DIF|E|OU) var)?
cond: IFW PE condicao PD CE code? CD elsee? PV
elsee: ELSEW CE code CD

input: INPUTW PE PD PV
output: OUTPUTW PE ESCAPED_STRING PD PV

ciclos: whilee | forr | dowhile
whilee: WHILEW PE condicao PD CE code? CD PV 
forr: FORW PE variaveis condicao PV WORD IGUAL tipo PD CE code? CD PV 
dowhile: DOW CE code? CD WHILEW PE condicao PD PV

var: INT | WORD | ESCAPED_STRING | FLOAT 
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
ELSEW: "else"
DEFW: "def"
RETURNW: "return"
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
DP: ":"
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






