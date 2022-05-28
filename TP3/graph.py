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
    self.mccabe['nodes'] +=1  
    if self.nodeAnt != "":
        g.edge(self.nodeAnt, edge)
        if self.nodeAnt != 'beginCode':
            self.mccabe['edges'] +=1  
        print("incrementei", self.nodeAnt, edge) 
        self.nodeAnt = edge
    return edge

def buildNodeAtr(self, var, g, flag):
    edge =  " "
    for tok in var:
        if not isinstance(tok, Token):
            for i in tok:
                edge = edge + i
        else:
            edge = edge + tok+ " "
    g.node(edge, fontcolor='green', color='green')
    self.mccabe['nodes'] +=1  
    if self.nodeAnt != "":
        if not flag:
            g.edge(self.nodeAnt, edge)
            if self.nodeAnt != 'beginCode':
                self.mccabe['edges'] +=1  
        self.nodeAnt = edge
    return edge

def buildNodeCond(self, nodeCond, g):
    edge = 'if ' + nodeCond
    g.node(edge, fontcolor='red', color='red', shape='diamond')
    self.mccabe['nodes'] +=1  
    if self.nodeAnt != "":
        g.edge(self.nodeAnt, edge)
        if self.nodeAnt != 'beginCode':
            self.mccabe['edges'] +=1 
        print("incrementei",self.mccabe['edges']) 
        self.nodeAnt = edge
    
    return edge

def buildNodeCondEnd(self, g, counter):
    endif = 'endif'+ str(counter)
    counter += 1
    g.node(endif, fontcolor='red', color='red', shape='diamond')
    self.mccabe['nodes'] +=1  
    if self.nodeAnt != "":
        g.edge(self.nodeAnt, endif)
        if self.nodeAnt != 'beginCode':
            self.mccabe['edges'] +=1
        print("incrementei",self.mccabe['edges'])     
        self.nodeAnt = endif
    return endif


def buildNodeCondFor(self, g, cond):
    edgefor = 'for '+ cond
    g.node(edgefor, fontcolor='purple', color='purple')
    self.mccabe['nodes'] +=1  
    if self.nodeAnt != "":
        g.edge(self.nodeAnt, edgefor)
        if self.nodeAnt != 'beginCode':
            self.mccabe['edges'] +=1
        print("incrementei",self.mccabe['edges']) 
        self.nodeAnt = edgefor
    return edgefor


def buildNodeIO(self, tokens, g):
    edge = ''
    for tok in tokens:
        if tok != ";":
            edge = edge + tok
    g.node(edge, fontcolor='brown', color='brown')
    self.mccabe['nodes'] +=1  
    if self.nodeAnt != "":
        g.edge(self.nodeAnt, edge)
        if self.nodeAnt != 'beginCode':
            self.mccabe['edges'] +=1  
        print("incrementei",self.mccabe['edges']) 
        self.nodeAnt = edge
    return edge



def buildNodeWhile(self, cond, g):
    edgewhile = 'while '+ cond
    g.node(edgewhile, fontcolor='purple', color='purple')
    self.mccabe['nodes'] +=1  
    if self.nodeAnt != "":
        g.edge(self.nodeAnt, edgewhile)
        if self.nodeAnt != 'beginCode':
            self.mccabe['edges'] +=1
        print("incrementei",self.mccabe['edges']) 
        self.nodeAnt = edgewhile
    return edgewhile


def buildNodeWhileDo(self, text, g):
    g.node(text,fontcolor='purple', color='purple')
    self.mccabe['nodes'] +=1  
    g.edge(self.nodeAnt, text)
    self.mccabe['edges'] +=1  
    print("incrementei",self.mccabe['edges']) 
    self.nodeAnt = text
    return text