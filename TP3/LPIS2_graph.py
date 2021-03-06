from ctypes import sizeof
from distutils.command.build import build
from re import S, X
from tkinter import FALSE
from lark import Discard
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter
from html import beginHtml, finalData
from sys import argv
import copy
import graphviz
from graph import *
from sdg import *


#Testar:
#: > result.html | python LPIS2_graph.py exemplo.txt >> result.html 

class MyInterpreter (Interpreter):

  def __init__(self):
      self.varsDecl = dict()
      self.varsNDecl = dict ()
      self.varsRDecl = dict()
      self.conds = dict()
      self.notInic = dict()
      self.tipoInstrucoes = {'declaracoes': 0, 'atribuicoes': 0, 'io': 0, 'ciclos': 0, 'cond': 0, 'funcoes': 0}
      self.totalInst = 0
      self.inInst = {'atual': 0, 'maior': 0, 'total': 0}
      self.aninhavel  = False 
      self.graphControl = {'aninh': 0 , 'total': 0, 'inFor': False}
      self.html = beginHtml()
      self.nodeAnt = "beginCode"
      self.sdgControl = {'instMae': [], 'inFor' : False}
      self.dicVarNode = dict()
      self.mccabe = {'nodes': 0 , 'edges': 0 }
  
  def dadosfinais(self):
    return finalData(self.varsDecl, self.varsNDecl, self.varsRDecl, self.tipoInstrucoes, self.inInst, self.totalInst, argv[1], self.conds, self.notInic, self.mccabe)


  def start(self, tree):
    sdg.node("ENTRY", shape='box')
    self.visit(tree.children[0])
    g.edge(self.nodeAnt, "endCode")
    #sdgDD(self.dicVarNode, sdg)
    return self.html + self.dadosfinais()
    
  def code(self, tree):
    for child in tree.children[0:]:
      self.visit(child)
        
  def variaveis(self, tree):
    return self.visit(tree.children[0])

  def declaracoes(self, tree):
    #declaracoes: decint | decstring | decdict | declist | decconj | dectuplos | decfloat | decinput 
    self.maior()
    self.totalInst +=1
    self.tipoInstrucoes['declaracoes'] += 1
    dec = self.visit(tree.children[0])
    #Verificar que a var ainda não foi declarada ou se o nome da var existe mas são tipos diferentes
    if (dec[1] not in self.varsDecl or (dec[1] in self.varsDecl and self.varsDecl[dec[1]]['tipo']!= dec[0] )):
      if(len(dec) > 3):
        if(dec[2] == "["):
          self.varsDecl[dec[1]] = {"tipo" : dec[0] + "[]", "inic" : 1, "utilizada": 0}
        else:
          self.varsDecl[dec[1]] = {"tipo" : dec[0], "inic" : 1, "utilizada": 0}
      else:
        self.varsDecl[dec[1]] = {"tipo" : dec[0], "inic" : 0, "utilizada": 0}
    #Se já foi declarada é anunciada com uma classe própria para tal 
    else: #Guardar as posições em que ocorreu o erro 
      self.varsRDecl[dec[1]] = {"tipo" : dec[0], "pos": (dec[0].line, dec[0].column)}
    tokensList = []
    for elem in dec[2:]:
      if not isinstance(elem, Token):
        for i in elem:
            if not isinstance(i, Token):
              for ii in i:
                 tokensList.append(ii)
            else:
              tokensList.append(i)
      elif isinstance(elem, Token):
        tokensList.append(elem)
    #decl tuples e ints com operacoes && Casos como: int x = y + 1
    node = buildNodeDec(self, dec, tokensList, g)
    #if dec[1] not in self.dicVarNode:
      #self.dicVarNode[dec[1]] = {'nodes': [], 'lines': []}
      #self.dicVarNode[dec[1]]['nodes'].append(node)
      #self.dicVarNode[dec[1]]['lines'].append(dec[1].line)
    for tt in tokensList:
      if tt.type == 'WORD' and tt not in self.varsDecl:
        self.varsNDecl[tt] = {"pos": (dec[0].line, dec[0].column)}
        #self.dicVarNode[dec[1]]['nodes'].append(node)
        #self.dicVarNode[dec[1]]['lines'].append(dec[1].line)
      elif tt.type == 'WORD':
        self.varsDecl[tt]["utilizada"] += 1
        #self.dicVarNode[dec[1]]['nodes'].append(node)
        #self.dicVarNode[dec[1]]['lines'].append(dec[1].line)
    sdgDec(self, node, sdg)
    
    return node
 

  def atribuicoes(self, tree):
    # atribuicoes: WORD IGUAL (var | operacao | input |lista | dicionario) 
    self.totalInst += 1
    self.maior()
    self.tipoInstrucoes['atribuicoes'] += 1
    var = self.visit_children(tree)
    if (var[0] not in self.varsDecl):
      if var[0] not in self.varsNDecl:
        self.varsNDecl[var[0]] = {"pos": (var[0].line, var[0].column)}
    else:
      self.varsDecl[var[0]]["utilizada"] += 1 
      self.varsDecl[var[0]]["inic"] = 1 
    node = buildNodeAtr(self, var, g, self.graphControl['inFor'])
    #if var[0] not in self.dicVarNode:
    #  self.dicVarNode[var[0]] = dict()
    #self.dicVarNode[var[0]][node] = []
    for elem in var[1:]:
        if not isinstance(elem, Token):
          if elem[0].type == 'input':
            self.visit(elem)
            break
          for i in elem:
            #Utilização de variaveis nao declaradas à direita da operação =
            if i.type == 'WORD':
              #self.dicVarNode[var[0]][node].append(i)
              if i not in self.varsDecl:
                self.varsNDecl[i] = {"pos": (i.line, i.column)}
              else:
                self.varsDecl[i]["utilizada"] += 1
    

    sdgAtr(self, node, sdg)
    return node
  

  def input(self, tree):
    self.maior()
    self.totalInst += 1
    self.tipoInstrucoes['io'] += 1
    r = self.visit_children(tree)
    #buildNodeIO(self, r, g)
    #sdgIO(self, r, sdg)
    return r

  def output(self, tree):
    #output: OUTPUTW PE ESCAPED_STRING PD PV
    self.maior()
    r = self.visit_children(tree)
    buildNodeIO(self, r, g)
    sdgIO(self, r, sdg)
    self.totalInst += 1
    self.tipoInstrucoes['io'] += 1
    return tree
 

  def ciclos(self, tree):
    #(whilee | forr | dowhile) PV
    self.maior()
    self.totalInst += 1
    self.tipoInstrucoes['ciclos'] += 1
    result = self.visit(tree.children[0])
    return result 

  def whilee(self, tree):
    self.maior()
    #WHILEW PE condicao PD CE code? CD 
    cndt = self.visit(tree.children[2])
    nodeWhile = buildNodeWhile(self, cndt, g)
    sdgWhile(self, nodeWhile, sdg)
    self.inInst['atual'] += 1
    #Significa que tem código no meio 
    self.aninhavel = False
    for elem in tree.children[5:]:
      if not isinstance(elem, Token):
        self.visit(tree.children[5])    
    self.inInst['atual'] -= 1
    self.sdgControl['instMae'].pop()
    if self.inInst['atual'] == 1:
      self.inInst['total'] += 1
    g.edge(self.nodeAnt, nodeWhile)
    self.mccabe['edges'] +=1  


    self.nodeAnt = nodeWhile
    return tree

  def cond(self, tree):
    #cond: IFW PE condicao PD CE code? CD else? PV
    self.totalInst += 1
    self.inInst['atual'] +=1
    self.graphControl['aninh'] += 1
    self.graphControl['total'] += 1
    self.tipoInstrucoes['cond'] += 1
    nodeCond = self.visit(tree.children[2])
    beginIf = buildNodeCond(self, nodeCond, g)
    vv = self.tipoInstrucoes['cond']
    sdgIfs(self, beginIf, sdg,vv)
    if not isinstance(tree.children[5], Token):#Tem codigo
      size = len(tree.children[5].children)
      sizehere = len(tree.children)
      sizeeee = len(tree.children[5].children[size-2].children)-2
      if tree.children[5].children[0].data == 'cond' and isinstance(tree.children[5].children[size-2].children[sizeeee], Token) and isinstance(tree.children[sizehere-2], Token): #o 1 elem do codigo é um if
        self.aninhavel = True 
      else:
        self.aninhavel = False 
    else:
      self.aninhavel = False
    for rule in tree.children:
      if not isinstance(rule, Token):
        if rule.data == 'elsee':
          sdgElse(self,beginIf, 'else', sdg, vv)
          endIf = buildNodeCondEnd(self, g, self.graphControl['aninh'])
          self.nodeAnt = beginIf
        edge = self.visit(rule)
    self.aninhavel = False 
    endIf = buildNodeCondEnd(self, g, self.graphControl['aninh'])
    self.inInst['atual'] -=1
    self.sdgControl['instMae'].pop()
    self.graphControl['aninh'] -= 1

    if self.graphControl['aninh'] == 1:
      self.graphControl['aninh'] = self.graphControl['total']
    if self.inInst['atual'] == 1:
      self.inInst['total'] += 1
    #se não houver else, ligar o if ao endif diretamente 
    sizehere = len(tree.children)
    if isinstance(tree.children[sizehere-2], Token):#Se não tiver um else
      g.edge(beginIf, endIf)
      self.mccabe['edges'] +=1


    return endIf
  
  def condicao(self, tree):
    #condicao: var ((II|MAIOR|MENOR|DIF|E|OU) var)?
    self.maior()
    cndt = "("
    tokens = list()
    for i in range(len(tree.children)):
      if(not isinstance(tree.children[i], Token)):
        if (tree.children[i].children[0].type == 'WORD'):
          tokens.append(tree.children[i].children[0])
        cndt = cndt + tree.children[i].children[0]
      else:
        cndt = cndt + tree.children[i]
    cndt = cndt+ ")" 
    if cndt not in self.conds:
      self.conds[cndt] = {"pos": (tree.children[0].children[0].line, tree.children[0].children[0].column), "aninh": self.aninhavel}
    #tokens.append(tree.children[0][0])
    if len(tree.children) ==2:
      tokens.append(tree.children[2][0])
    for var in tokens:
        if var not in self.varsDecl:
          self.varsNDecl[var] = {"pos": (var.line, var.column)}
        else:
          self.varsDecl[var]["utilizada"] += 1 
          if self.varsDecl[var]["inic"] == 0:
            if var not in self.notInic:
              self.notInic[var]={"pos": (var.line, var.column), "qt": 1}
            else:
              self.notInic[var]['qt'] += 1
    return cndt

  def forr(self, tree):
    self.maior()
    #forr: FORW PE variaveis condicao PV atribuicoes PD CE code? CD  
    self.inInst['atual']+= 1
    self.sdgControl['inFor'] = True
    dec = self.visit(tree.children[2])
    self.sdgControl['inFor'] = False
    self.nodeAnt = dec
    cndt = self.visit(tree.children[3])
    self.graphControl['inFor'] = True
    edgefor = buildNodeCondFor(self, g, cndt )
    sdgFor(self, edgefor, sdg)
    atr = self.visit(tree.children[5])
    sdgForAtr(edgefor, atr, sdg)
    self.graphControl['inFor'] = False 
    g.edge(atr, edgefor)  
    self.mccabe['edges'] +=1
  
    self.nodeAnt = edgefor
    if (len(tree.children) == 10 ):
        self.visit(tree.children[8])
    self.inInst['atual'] -= 1
    self.sdgControl['instMae'].pop()
    if self.inInst['atual'] == 1:
      self.inInst['total'] += 1
    g.edge(self.nodeAnt, atr)
    self.mccabe['edges'] +=1  

    self.nodeAnt = edgefor
    return dec 
  
  def dowhile (self, tree):
    self.maior()
    #dowhile: DOW CE code? CD WHILEW PE condicao PD PV
    self.inInst['atual'] +=1
    node = buildNodeWhileDo(self, 'DO', g)
    cndt  = self.visit(tree.children[len(tree.children)-2]) ##condição 
    sdgWhileDo(self, node + ' while'+ cndt, sdg )
    for elem in tree.children:
      if not isinstance(elem, Token) and  elem.data== 'code':
        self.visit(elem) 
    whiledo = buildNodeWhileDo(self, 'while' + cndt, g)
    g.edge(whiledo, node)
    self.mccabe['edges'] +=1  
    self.sdgControl['instMae'].pop()
    self.nodeAnt = node
    self.inInst['atual'] -=1


  def elsee(self,tree):
    #elsee: ELSEW CE code CD
    for elem in tree.children:
      if not isinstance(elem, Token):
        self.visit(elem)
      
 
  def funcao(self, tree):
    #DEFW WORD PE args PD CE code? return? CD 
    self.totalInst += 1
    self.tipoInstrucoes['funcoes'] += 1
    for elem in tree.children[:6]:
      if not isinstance(elem, Token):
        self.visit(elem)
    if not isinstance(tree.children[6], Token):
      if tree.children[6].data == 'code':
        self.visit(tree.children[6])
    d = copy.deepcopy(self.varsDecl)
    for key in d:
      if (self.varsDecl[key]['tipo'] == None):
        del self.varsDecl[key]
        
    
  def args(self, tree):
    for elem in tree.children:
      if isinstance(elem, Token):
        if(elem.type == 'WORD'):
          self.varsDecl[elem] = {"tipo": None, "inic": 1, "utilizada": 0}

  def maior(self):
    if self.inInst['atual'] > self.inInst['maior']:
      self.inInst['maior'] = self.inInst['atual']


## Primeiro precisamos da GIC
grammar = '''
start: code
code: (variaveis | funcao | cond | output | ciclos)+ 

variaveis: (declaracoes | atribuicoes) PV 
declaracoes: decint | decstring | decdict | declist | decconj | dectuplos | decfloat | decinput
decint : INTW WORD (IGUAL (INT | operacao))? 
  operacao : (NUMBER|WORD) ((SUM | SUB | MUL | DIV | MOD) (NUMBER|WORD))+
decstring : STRINGW WORD (IGUAL (ESCAPED_STRING|input))? 
decdict : DICTW WORD (IGUAL DICTW PE PD)? 
declist : INTW WORD (PRE NUMBER? PRD)+ (IGUAL (content | ultracontent))?
  content : CE (INT (VIR INT)*)* CD
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
  elsee: ELSEW CE code? CD
  ELSEW: "else"

output: OUTPUTW PE (ESCAPED_STRING|WORD) PD PV

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
%import common.INT
%import common.FLOAT
%import common.ESCAPED_STRING
%import common.NUMBER

%ignore WS
'''

f = open(argv[1], "r")
g = graphviz.Digraph('grammar', format='png')
g.graph_attr['rankdir'] = 'TB'
g.graph_attr['bgcolor'] ="aliceblue"


sdg = graphviz.Digraph('sdg', format='png')
sdg.graph_attr['rankdir'] = 'TB'
#sdg.graph_attr['bgcolor'] ="mistyrose1"

linhas = f.read()
p = Lark(grammar, propagate_positions = True) 
parse_tree = p.parse(linhas)
#print(parse_tree.pretty())
data = MyInterpreter().visit(parse_tree)
g.render(directory='doctest-output', view=False)  
sdg.render(directory='doctest-output', view=False)  
print(data)







