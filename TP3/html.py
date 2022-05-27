from itertools import count


def beginHtml():
    return str(''' <!DOCTYPE html>
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
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<body >

  ''')

def organizarTipo (varsDecl):
    return {key: value for key, value in sorted(varsDecl.items(), key=lambda item: item[1]['tipo'])}
     
def organizarLinha (vars):
    return {key: value for key, value in sorted(vars.items(), key=lambda item: item[1]['pos'][0])}
   

def varsDecl( varsDecl):

    varsDecl = organizarTipo(varsDecl)
    tipos = {"conj": 1,"dict": 2, "float":3, "int" : 4,  "list": 5, "string":6, "tuple":7 }
    r = ''' <div class="w3-round w3-teal">
            <div class="w3-container">
            <h2> → Variáveis Declaradas</h2>
            <div class="w3-responsive">
            <table class="w3-table-all", style="color:black">
            <tr>
                <th>Variável</th>
                <th>conj</th>
                <th>dict</th>
                <th>float</th>
                <th>int</th>
                <th>list</th>
                <th>string</th>
                <th>tuple</th>
            </tr> '''
    for var in varsDecl: 
        elem = varsDecl[var]['tipo']
        r = r + '<tr><td><b>' + var + '<b></td>'
        if elem in tipos:
            val = tipos[elem]
        else:
            val = 5 
        i = 1
        while i < val:
            r = r + '<td> </td>'
            i += 1
        if i == val:
            r = r + "<td> X </td>"
        while val < 7:
            r = r + '<td> </td>'
            val += 1
        r = r + '''</tr>'''
    r = r + '''   
    </table>
    <h2></h2></div></div></div>
    '''
    return r

def varsRedND(varsRDecl, varsNDecl, varsDec):
    x = 0
    r = '<div class="w3-panel w3-pale-blue w3-bottombar w3-border-teal w3-border"> <h2><b> → Warnings sobre variáveis</b></h2>'
    r = r + '''<table class="w3-table-all">
    <tr>
        <th><b>Variáveis Redeclaradas</b> <span class="w3-badge w3-blue">''' + str(len(varsRDecl))+ '''</span></th>
        <th><b>Variáveis Não Declaradas</b> <span class="w3-badge w3-red">''' + str(len(varsNDecl))+ '''</span></th>
        <th><b>Variáveis Não Inicializadas</b> <span class="w3-badge w3-yellow">''' + str(sum(1 for e in varsDec if varsDec[e]['inic'] == 0 ))+ '''</span></th>
        <th><b>Variáveis Nunca Utilizadas</b> <span class="w3-badge w3-purple">''' + str(sum(1 for e in varsDec if varsDec[e]['utilizada'] == 0 ))+ '''</span></th>
    </tr><tr><td>'''
    r = r + '''<ul class="w3-ul w3-center">'''
    for var in varsRDecl:
        r = r + '<li>' + var +'</li>'
    r = r + '</ul></td><td><ul class="w3-ul w3-center">'
    for var in varsNDecl:
        r = r + '<li>' + var +'</li>'
    r = r + '</ul></td><td><ul class="w3-ul w3-center">'
    for var in varsDec:
        if varsDec[var]['inic'] == 0:
            r = r + '<li>' + var +'</li>'
    r = r + '</ul></td><td><ul class="w3-ul w3-center">'
    for var in varsDec:
        if varsDec[var]['utilizada'] == 0:
            r = r + '<li>' + var +'</li>'
    r = r + '</ul></td>'
    r = r + '</tr></table></div>'
    return r


def warnings(varsNDecl, varsRDecl, conds, notInic):
    vs = varsNDecl | varsRDecl | conds | notInic
    vars = organizarLinha(vs)
    r='''<div class="w3-panel w3-light-grey w3-topbar w3-bottombar w3-border-teal">
    <h2 style="color: teal"><b> → Warnings</b></h2>'''
    for v in vars:
        if 'tipo' in vars[v]:
            r = r + '<p> (<u>line ' + str(vars[v]['pos'][0]) +', column ' + str(vars[v]['pos'][1])+'</u>)' + ': Variável <b>' + v + '</b> redeclarada.</p>'
        elif 'aninh' in vars[v] and vars[v]['aninh']:
                r = r + '<p> (<u>line ' + str(vars[v]['pos'][0]) +', column ' + str(vars[v]['pos'][1])+'</u>)<b> ' + v +'</b>: Possibilidade de aninhamento com a condição anterior.</p>'
        elif 'qt' in vars[v]:
            r = r + '<p> (<u>line ' + str(vars[v]['pos'][0]) +', column ' + str(vars[v]['pos'][1])+'</u>)' + ': Variável <b>' + v + '</b> não inicializada e utilizada ' + str(vars[v]['qt']) + 'x ao longo do programa.</p>'
        elif 'aninh' not in vars[v] :             
            r = r + '<p> (<u>line ' + str(vars[v]['pos'][0]) +', column ' + str(vars[v]['pos'][1])+'</u>)' + ': Variável <b>' + v + '</b> não declarada.</p>'
    return r +  '''
</div>'''

def finalData( varsDec, varsNDecl, varsRDecl, tipoInstrucoes, inInst, totalInst, nomeFich, conds, notInic):
    r = '<h2 class="w3-light-grey w3-center w3-border-top w3-border-bottom" style="text-shadow:1px 1px 0 #444">Analisador de código fonte do ficheiro "'+ nomeFich+ '"</h2>'
    r = r + varsDecl(varsDec)

    r = r + varsRedND(varsRDecl, varsNDecl, varsDec)
    r = r + '<div class="w3-panel w3-teal"><h2> → Análise tipo Instruções </h2></div>'
    r = r + " <table>\n <tr> <th> Nº Declarações </th><th>" + str(tipoInstrucoes['declaracoes']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Atribuições </th><th>" + str(tipoInstrucoes['atribuicoes']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Input/Output </th><th>" + str(tipoInstrucoes['io']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Ciclos </th><th>" + str(tipoInstrucoes['ciclos']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Inst. Condicionais </th><th>" + str(tipoInstrucoes['cond']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Funções </th><th>" + str(tipoInstrucoes['funcoes']) + "</th></tr>"
    r = r + " \n <tr> <th> Total Instruções </th><th>" + str(totalInst) + "</th></tr></table>"
    if (inInst['total']!=0):
        r = r + " \n<p><p class='code'> NOTA: Existem <b>"+ str(inInst['total']) + "</b> situações de aninhamento e o nível máximo de instruções condicionais aninhadas é <b>" + str(inInst['maior']) + ".</b></p></p> "
    else:
       r = r + " \n<p><p class='code'> NOTA: Existem <b>"+ str(inInst['total']) + "</b> situações de aninhamento."
    r = r + warnings(varsNDecl, varsRDecl, conds, notInic)


    r = r + '<h1 class="w3-center"> <div class ="w3-teal">Control Flow Graphs</div><img src="doctest-output/grammar.gv.png" ></h1>'

    return r + str('''</body></html>''')


    