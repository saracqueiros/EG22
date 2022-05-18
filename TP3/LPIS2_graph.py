from re import S, X
from lark import Discard
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter
from html import beginHtml, finalData
import copy

#Testar:
#: > result.html | python LPIS2_graph.py >> result.html 

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
      self.html = beginHtml()
  
  def start(self, tree):
    self.visit(tree.children[0])
    self.html = self.html + self.dadosfinais() 
    return self.html

  def dadosfinais(self):
    return finalData(self.varsDecl, self.varsNDecl, self.varsRDecl, self.tipoInstrucoes, self.inInst, self.totalInst)

  """
  def declaracoes(self, tree):
    #self.maior()
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
    self.html = self.html + "</p>"   
    if (self.forC == 0):
      self.html = self.html + '</p>'
""""""
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
    if self.inInst['atual'] == 1:
      self.inInst['total'] += 1
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
    if self.inInst['atual'] == 1:
      self.inInst['total'] += 1
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
    self.html = self.html + "</p>"
    self.aninhavel = False
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
    #DEFW WORD PE args PD CE code? return? CD 
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
    d = copy.deepcopy(self.varsDecl)
    for key in d:
      if (self.varsDecl[key]['tipo'] == None):
        del self.varsDecl[key]
        
    
  def args(self, tree):
    for elem in tree.children:
      if isinstance(elem, Token):
        self.html = self.html + elem + " "
        if(elem.type == 'WORD'):
          self.varsDecl[elem] = {"tipo": None, "inic": 1, "utilizada": 0}
      else:
        self.html = self.html + elem.children[0] + " "


  
  def maior(self):
    if self.inInst['atual'] > self.inInst['maior']:
      self.inInst['maior'] = self.inInst['atual']
"""

## Primeiro precisamos da GIC
grammar = '''
start: code
code: (variaveis | funcao | cond | output | ciclos)+

variaveis: (declaracoes | atribuicoes ) PV
declaracoes: decint | decstring | decdict | declist | decconj | dectuplos | decfloat | decinput 
decint : INTW WORD (IGUAL (INT | operacao))? 
  operacao : (NUMBER|WORD) (opsign (NUMBER|WORD))+
  opsign : SUM | SUB | MUL | DIV | MOD
decstring : STRINGW WORD (IGUAL ESCAPED_STRING)?
decdict : DICTW WORD (IGUAL DICTW PE PD)?
declist : INTW WORD (PRE NUMBER? PRD)+ (IGUAL (content | ultracontent))?
  content : CE (val)* CD
  val : INT (VIR INT)*
  ultracontent: CE (content (VIR content)*)* CD
decconj: CONJW  WORD (IGUAL CE (ESCAPED_STRING (VIR ESCAPED_STRING)*)? CD )* 
dectuplos: TUPLEW WORD (IGUAL PE var (VIR var)+ PD)* 
  var: INT | WORD | ESCAPED_STRING | FLOAT 
decfloat: FLOATW WORD (IGUAL FLOAT)* 
decinput: STRINGW IGUAL input

atribuicoes: WORD IGUAL (var | operacao | input |lista | dicionario) 
  input: INPUTW PE PD 
  lista: WORD (PRE INT PRD)+
  dicionario: CE ESCAPED_STRING DP (INT | WORD)(VIR ESCAPED_STRING DP (INT | WORD))* CD 

funcao: DEFW WORD PE args PD CE code? return? CD 
  args: (types WORD VIR)* types WORD 
  types: (STRINGW |DICTW |INTW | TUPLEW| FLOATW| CONJW)
  return: RETURNW (WORD VIR)* WORD
  DEFW: "def"
  RETURNW: "return" 

cond: IFW PE condicao PD CE code? CD elsee? PV
  condicao: var ((II|MAIOR|MENOR|DIF|E|OU) var)?
  elsee: ELSEW CE code CD
  ELSEW: "else"

output: OUTPUTW PE ESCAPED_STRING PD PV

ciclos: (whilee | forr | dowhile) PV
whilee: WHILEW PE condicao PD CE code? CD 
forr: FORW PE variaveis condicao PV atribuicoes PD CE code? CD 
dowhile: DOW CE code? CD WHILEW PE condicao PD 

DP: ":"
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
WORD: "a".."z"("a".."z"|"0".."9")*


%import common.WS
%import common.NEWLINE 
%import common.INT
%import common.FLOAT
%import common.ESCAPED_STRING
%import common.NUMBER
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





