from ctypes import sizeof
from re import S, X
from lark import Discard
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter
from html import beginHtml, finalData
from sys import argv
import copy
import graphviz

def buildNodeDec(self, dec, tokensList, g):
    edge = dec[0] + " " + dec[1] + " "
    for tok in tokensList:
        edge = edge + tok+ " "
    g.node(edge, fontcolor='blue', color='blue')
    if self.nodeAnt != "":
        g.edge(self.nodeAnt, edge)
        self.nodeAnt = edge
    return edge


def buildNodeAtr(self, var, g):
    edge =  " "
    for tok in var:
        if not isinstance(tok, Token):
            for i in tok:
                edge = edge + i
        else:
            edge = edge + tok+ " "
    g.node(edge, fontcolor='green', color='green')
    if self.nodeAnt != "":
        g.edge(self.nodeAnt, edge)
        self.nodeAnt = edge
    return edge

def buildNodeCond(self, nodeCond, g):
    edge = 'if ' + nodeCond
    g.node(edge, fontcolor='red', color='red', shape='diamond')
    if self.nodeAnt != "":
        g.edge(self.nodeAnt, edge)
        self.nodeAnt = edge
    
    return edge

def buildNodeCondEnd(self, g, counter):
    print("entrei aqui", str(counter))
    endif = 'endif'+ str(counter)
    counter += 1
    g.node(endif, fontcolor='red', color='red', shape='diamond')
    if self.nodeAnt != "":
        g.edge(self.nodeAnt, endif)
        self.nodeAnt = endif
    return endif
