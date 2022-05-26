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


def buildNodeDec(dec, tokensList, g):
    edge = dec[0] + " " + dec[1] + " "
    for tok in tokensList:
        edge = edge + tok+ " "
    g.node(edge, fontcolor='blue', color='blue')
    return edge


def buildNodeAtr(var, g):
    edge =  " "
    for tok in var:
        if not isinstance(tok, Token):
            for i in tok:
                edge = edge + i
        else:
            edge = edge + tok+ " "
    g.node(edge, fontcolor='green', color='green')
    return edge
