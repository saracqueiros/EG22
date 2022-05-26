from ctypes import sizeof
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter
from sys import argv
import graphviz


class MyInterpreter (Interpreter):

  def __init__(self):
      self.newlines = 1
  
  def start(self, tree):
    self.visit(tree.children[0])
    return tree

  def code(self, tree):
    node1 = self.visit((tree.children[0]))    
    for child in tree.children[1:]:
      node2 = self.visit(child)
      g.edge(node1, node2)
      node1 = node2
  
  def variaveis(self, tree):
    return self.visit(tree.children[0])
    
  def declaracoes(self, tree):
    r = self.visit(tree.children[0])
    f = ''
    for l in r :
      f = f + ' '+ l
    return f
    

    
  

grammar = '''
start: code
code: (variaveis)+ 

variaveis: declaracoes PV
declaracoes: decint 
decint : INTW WORD (IGUAL INT)? 

INTW: "int"
IGUAL:"="
PV:";"
WORD: "a".."z"("a".."z"|"0".."9")*

%import common.WS
%import common.INT
%import common.FLOAT
%import common.ESCAPED_STRING
%import common.NUMBER


%ignore WS
'''
f = open(argv[1], "r")
g = graphviz.Digraph('G', filename='process.gv', engine='sfdp')
g.graph_attr['rankdir'] = 'TB'




linhas = f.read()
p = Lark(grammar, propagate_positions = True) 
parse_tree = p.parse(linhas)

#print(parse_tree.pretty())
data = MyInterpreter().visit(parse_tree)
#print(data)
print(g)
g.render(directory='doctest-output', view=True)  