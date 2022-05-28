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
    if self.inInst['atual'] == 0 or self.sdgControl['inFor']:
        sdg.edge('ENTRY', node)
    else:
        sdg.edge(self.sdgControl['instMae'][-1], node)



def sdgAtr(self, node, sdg):
    sdg.node(node, fontcolor='green', color='green')
    if self.inInst['atual'] == 0:
        sdg.edge('ENTRY', node)
    else:
        sdg.edge(self.sdgControl['instMae'][-1], node)


def sdgIO(self, tokens, sdg):
    edge = ''
    for tok in tokens:
        if tok != ";":
            edge = edge + tok
    sdg.node(edge, fontcolor='brown', color='brown')
    if self.inInst['atual'] == 0:
        sdg.edge('ENTRY', edge)
    else:
        sdg.edge(self.sdgControl['instMae'][-1], edge)

def sdgIfs(self, node, sdg, counter):
    sdg.node(node, fontcolor='red', color='red', shape='diamond')
    then = 'then' + str(counter)
    if self.inInst['atual'] == 1:
        sdg.edge('ENTRY', node)
    else:
        sdg.edge(self.sdgControl['instMae'][-1], node)
    sdg.edge(node, then)
    self.sdgControl['instMae'].append(then)
        

def sdgElse(self,beginIf, nodeElse, sdg, counter):
    sdg.node(nodeElse+str(counter))
    sdg.edge(beginIf, nodeElse+str(counter))
    self.sdgControl['instMae'].append(nodeElse+str(counter))


def sdgWhile(self, node , sdg):
    sdg.node(node, fontcolor='purple', color='purple')
    sdg.edge(node, node)
    if self.inInst['atual'] == 0:
        sdg.edge('ENTRY', node)
    else:
        sdg.edge(self.sdgControl['instMae'][-1], node)
    self.sdgControl['instMae'].append(node)
    
def sdgFor(self, edgefor, sdg):
    sdg.node(edgefor, fontcolor='purple', color='purple')
    if self.inInst['atual'] == 1:
        sdg.edge('ENTRY', edgefor)
    else:
        sdg.edge(self.sdgControl['instMae'][-1], edgefor)
    self.sdgControl['instMae'].append(edgefor)

def sdgForAtr(edgefor, atr, sdg):
    sdg.node(atr, fontcolor='purple', color='purple')
    sdg.edge(atr, edgefor)
    #sdg.edge(atr, atr, style='dashed')


def sdgWhileDo(self, edge, sdg):
    sdg.node(edge, fontcolor='purple', color='purple')
    sdg.edge(edge, edge)
    if self.inInst['atual'] == 1:
        sdg.edge('ENTRY', edge)
    else:
        sdg.edge(self.sdgControl['instMae'][-1], edge)
    self.sdgControl['instMae'].append(edge)
