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

<body> <p><b> Código anotado:</b></p>
  ''')


def finalData(varsDecl, varsNDecl, varsRDecl, tipoInstrucoes, inInst, totalInst):
    r = "<p><p class='code'>-------------------------Análise Geral-------------------------\n<p>Variáveis declaradas: </p><ul>"
    for e in varsDecl:
        r = r + "<li><b>" + e + "</b>: " + varsDecl[e]['tipo'] + "</li>"
    r = r + "</ul></p></p><p><p class='code'>Variáveis não declaradas: <ul>"
    for e in varsNDecl:
        r = r + "<li><b>" + e + "</b></li> "
    r = r + "</ul></p></p><p><p class='code'>Variaveis redeclaradas: <ul>"
    for e in varsRDecl:
        r = r + "<li><b>" + e + "</b></li> "
    r = r + "</ul></p></p><p><p class='code'>Variaveis declaradas e nunca mencionadas: <ul>"
    for e in varsDecl:
        if varsDecl[e]['utilizada'] == 0:
            r = r + "<li><b>" + e + "</b> </li>"
    r = r + "</ul></p></p>\n<p><p class='code'>-------------------------------Análise Instruções-------------------------------\n<p>"
    r = r + " <table>\n <tr> <th> Nº Declarações </th><th>" + str(tipoInstrucoes['declaracoes']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Atribuições </th><th>" + str(tipoInstrucoes['atribuicoes']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Input/Output </th><th>" + str(tipoInstrucoes['io']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Ciclos </th><th>" + str(tipoInstrucoes['ciclos']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Inst. Condicionais </th><th>" + str(tipoInstrucoes['cond']) + "</th></tr>"
    r = r + " \n <tr> <th> Nº Funções </th><th>" + str(tipoInstrucoes['funcoes']) + "</th></tr>"
    r = r + " \n <tr> <th> Total Instruções </th><th>" + str(totalInst) + "</th></tr></table>"
    if (inInst['total']!=0):
        r = r + " \n<p><p class='code'> NOTA: Existem <b>"+ str(inInst['total']) + "</b> situações de aninhamento e o nível máximo de instruções condicionais aninhadas é <b>" + str(inInst['maior']) + "</b>. Sugestões de simplificação são mencionadas no código acima.</p></p> "
    else:
        r = r + " \n<p><p class='code'> NOTA: Existem <b>"+ str(inInst['total']) + "</b> situações de aninhamento."
    return r + str('''</body></html>''')