from ctypes import sizeof
from re import S, X
from types import BuiltinFunctionType
from xml.dom.minicompat import NodeList
from lark import Discard
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter
from html import beginHtml, finalData
from sys import argv
import copy
import graphviz

def sdgDec(self, node, sdg):
    sdg.node(node, fontcolor='blue', color='blue')
    if self.inInst['atual'] == 0:
        sdg.edge('ENTRY', node)
    else:
        sdg.edge(self.sdgControl['instMae'], node)


def sdgAtr(self, node, sdg):
    sdg.node(node, fontcolor='green', color='green')
    if self.inInst['atual'] == 0:
        sdg.edge('ENTRY', node)
    else:
        print("atr " , self.sdgControl['instMae'])
        sdg.edge(self.sdgControl['instMae'], node)


def sdgIO(self, tokens, sdg):
    edge = ''
    for tok in tokens:
        if tok != ";":
            edge = edge + tok
    sdg.node(edge, fontcolor='brown', color='brown')
    if self.inInst['atual'] == 0:
        sdg.edge('ENTRY', edge)
    else:
        sdg.edge(self.sdgControl['instMae'], edge)

def sdgIfs(self, node, sdg, counter):
    sdg.node(node, fontcolor='red', color='red', shape='diamond')
    if self.inInst['atual'] == 1:
        sdg.edge('ENTRY', node)
        then = 'then' + str(counter)
        sdg.edge(node, then)
        self.sdgControl['instMae'] = then 
    else:
        sdg.edge(self.sdgControl['instMae'], node)
        sdg.edge(node, 'then'+str(counter))
        self.sdgControl['instMae'] = 'then' +str(counter)
        

def sdgElse(self,beginIf, nodeElse, sdg, counter):
    sdg.node(nodeElse+str(counter))
    sdg.edge(beginIf, nodeElse+str(counter))
    self.sdgControl['instMae'] = nodeElse+str(counter)
    print("else " , self.sdgControl['instMae'])


def sdgWhile(self, node ,sdg ):
    sdg.node(node, fontcolor='purple', color='purple')
    sdg.edge(node, node)
    if self.inInst['atual'] == 0:
        sdg.edge('ENTRY', node)
        self.sdgControl['instMae'] = node 
    else:
        sdg.edge(self.sdgControl['instMae'], node)
        self.sdgControl['instMae'] = node
    