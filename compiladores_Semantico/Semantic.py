#Felipe Floret

#Compiladores

from Sintatic import tree
import copy


list_Types = [('Object', None, [('abort', [], 'Object'), ('type_name', [], 'String'), ('copy', [], 'SELF_TYPE')],
               [('self', 'Object')]),
              ('SELF_TYPE', None, [], []),
              ('IO', 'Object',
               [('out_string', [('x', 'String')], 'SELF_TYPE'), ('out_int', [('x', 'Int')], 'SELF_TYPE'),
                ('in_string', [], 'String'), ('in_int', [], 'Int')], []),
              ('Int', 'IO', [], []),
              ('String', 'IO', [('length', [], 'Int'), ('concat', [('s', 'String')], 'String'),
                                ('substr', [('i', 'Int'), ('l', 'Int')], 'String')], []),
              ('Bool', 'IO', [], [])
              ]
list_metod = []
list_Ids = []

scope = 'program'

for tipo in list_Types:
    for metodo in tipo[2]:
        list_metod.append(metodo)

for tipo in list_Types:
    for id in tipo[3]:
        list_Ids.append(id)


def percorreArvore(t):
    if type(t) == list or type(t) == tuple:
        for filho in t:
            percorreArvore(filho)
        print(t[0])

def chamaFuncao(t, list_Ids, list_metod, list_Types):
    if t == None:
        return

    newlist_Types = []
    newlist_Ids = []
    newlist_metod = []
    newlist_Types = list_Types
    if isNewscopeClasse(t[0]):
        global scope
        scope = t[1]
        newlist_metod = copy.deepcopy(list_metod)
        newlist_Ids = list_Ids
    elif isNewscopeMetodo(t[0]) or isNewscopeLet(t[0]):
        newlist_Ids = copy.deepcopy(list_Ids)
        newlist_metod = list_metod

    else:
        newlist_Types = list_Types
        newlist_Ids = list_Ids
        newlist_metod = list_metod

    if t[0] == 'idType':
        manipulaIdType(t, newlist_Ids, newlist_Types)
    elif t[0] == 'exprCase':  # To do
        manipulaExprCase(t)
    elif t[0] == 'exprID':
        manipulaExprId(t, newlist_Ids)
    elif t[0] == 'exprType':
        manipulaExprType(t)  # To do
    elif t[0] == 'exprLetSeta':
        manipulaExprLetSeta(t, newlist_Ids, newlist_Types)
        chamaFuncao(t[5], newlist_Ids, newlist_metod, newlist_Types)
    elif t[0] == 'exprLet':
        manipulaExprLet(t, newlist_Ids, newlist_Types)
        chamaFuncao(t[4], newlist_Ids, newlist_metod, newlist_Types)
    elif t[0] == 'exprEntreChaves':
        chamaFuncao(t[1], newlist_Ids, newlist_metod, newlist_Types)
    elif t[0] == 'exprWhile':
        manipulaExprWhile(t, newlist_Ids)
        chamaFuncao(t[3], newlist_Ids, newlist_metod, newlist_Types)
    elif t[0] == 'exprIf':
        manipulaExprIf(t, newlist_Ids)
        chamaFuncao(t[2], newlist_Ids, newlist_metod, newlist_Types)
        chamaFuncao(t[3], newlist_Ids, newlist_metod, newlist_Types)
    elif t[0] == 'exprCallMetodo':
        manipulaExprCallMetodo(t, newlist_metod, newlist_Ids)
    elif t[0] == 'exprArroba':
        nome = None
        nomeMetodo = None
        if t[1][0] == 'exprCallMetodo':
            nome = getMetodo(t[1][1], newlist_metod)[2]
            nomeMetodo = t[1][1]
        else:
            aux = getId(t[1][1], newlist_Ids)
            nomeMetodo = t[2][1]
            if aux != None:
                nome = aux[1]
        if nome != None:
            tipo = getType(nome, newlist_Types)
            if nome == 'SELF_TYPE':
                configSelfType(newlist_Ids, newlist_metod, newlist_Types)
            if not isInListMetodo(t[2][1], tipo[2]):
                raise SyntaxError("erro de chamada: metodo %s não pertence ao tipo %s" % nomeMetodo, nome)
        chamaFuncao(t[1], newlist_Ids, newlist_metod, newlist_Types)
    elif t[0] == 'exprSemArroba':
        nome = None
        nomeMetodo = None
        if t[1][0] == 'exprCallMetodo':
            nome = getMetodo(t[1][1], newlist_metod)[2]
            nomeMetodo = t[1][1]
        else:
            aux = getId(t[1][1], newlist_Ids)
            nomeMetodo = t[2][1]
            if aux != None:
                nome = aux[1]
        if nome != None:
            tipo = getType(nome, newlist_Types)
            if nome == 'SELF_TYPE':
                configSelfType(newlist_Ids, newlist_metod, newlist_Types)
            if not isInListMetodo(nomeMetodo, tipo[2]):
                raise SyntaxError("erro de chamada: metodo %s não pertence ao tipo %s" % nomeMetodo, nome)
        chamaFuncao(t[1], newlist_Ids, newlist_metod, newlist_Types)
    elif t[0] == 'exprEntreParenteses':
        chamaFuncao(t[1], newlist_Ids, newlist_metod, newlist_Types)
    elif t[0] == 'exprSeta':
        manipulaExprSeta(t, newlist_Ids)
    elif t[0] == 'op':
        manipulaOp(t, newlist_Ids)
    elif t[0] == 'comp':
        manipulaComp(t, newlist_Ids)
    elif t[0] == 'exprNew':
        manipulaExprNew(t, newlist_Types)
    elif t[0] == 'exprVoid':
        manipulaExprVoid(t, newlist_Ids)
    elif t[0] == 'exprNot':
        manipulaExprNot(t, newlist_Ids)
    elif t[0] == 'formal':
        manipulaFormal(t, newlist_Ids, newlist_Types)
    elif t[0] == 'featureRetornoParametro':
        manipulaFeatureRetornoParametro(t, newlist_Ids, newlist_metod, newlist_Types)
        for formal in t[4]:
            chamaFuncao(formal, newlist_Ids, newlist_metod, newlist_Types)
    elif t[0] == 'featureRetorno':
        manipulaFeatureRetorno(t, newlist_metod, newlist_Types)
        chamaFuncao(t[3], newlist_Ids, newlist_metod, newlist_Types)
    elif t[0] == 'featureAnonima':
        manipulafeatureAnonima(t, newlist_Ids, newlist_Types)
        for formal in t[2]:
            chamaFuncao(formal, newlist_Ids, newlist_metod, newlist_Types)
    elif t[0] == 'featureDeclaration':
        manipulaFeatureDeclaration(t, newlist_Ids, newlist_Types)
    elif t[0] == 'class':
        for formal in t[2]:
            chamaFuncao(formal, newlist_Ids, newlist_metod, newlist_Types)
    elif t[0] == 'classInh':
        manipulaClasseInh(t, newlist_Types)
        for formal in t[3]:
            if type(formal) == list:
                for i in formal:
                    chamaFuncao(i, newlist_Ids, newlist_metod, newlist_Types)
            else:
                chamaFuncao(formal, newlist_Ids, newlist_metod, newlist_Types)
    else:
        if type(t) == list:
            for i in t:
                chamaFuncao(i, newlist_Ids, newlist_metod, newlist_Types)


def manipulaIdType(t, list_Ids, list_Types):
    if len(t) == 4:
        aux = ('featureAnonima', t[1], t[2], t[3])
        manipulafeatureAnonima(aux, list_Ids, list_Types)
    elif len(t) == 3:
        aux = ('featureDeclaration', t[1], t[2])
        manipulaFeatureDeclaration(aux, list_Ids, list_Types)
    pass


def manipulaExprCase(t):
    pass


def manipulaExprType(t):
    pass


def manipulaExprId(t, list_Ids):
    if not isInListId(t[1], list_Ids):
        raise SyntaxError("erro de declaração: %s não foi declarado" % t[1])


def manipulaExprLetSeta(t, list_Ids, list_Types):
    aux = ('featureAnonima', t[1], t[2], t[3])
    manipulafeatureAnonima(aux, list_Ids, list_Types)
    for fanonima in t[4]:
        if fanonima != None:
            manipulaIdType(fanonima, list_Ids, list_Types)


def manipulaExprLet(t, list_Ids, list_Types):
    aux = ('featureDeclaration', t[1], t[2])
    manipulaFeatureDeclaration(aux, list_Ids, list_Types)
    for fanonima in t[3]:
        if fanonima != None:
            manipulaIdType(fanonima, list_Ids, list_Types)


def manipulaExprWhile(t, list_Ids):
    if t[1][0] == 'comp':
        manipulaComp(t[1], list_Ids)
        return
    if t[1][0] == 'exprNot':
        manipulaExprNot(t[1], list_Ids)
        return
    raise SyntaxError("erro de declaração: expressão %s não é booleano" % t[1])


def manipulaExprIf(t, list_Ids):
    if t[1][0] == 'comp':
        manipulaComp(t[1], list_Ids)
        return
    if t[1][0] == 'exprNot':
        manipulaExprNot(t[1], list_Ids)
        return
    raise SyntaxError("erro de declaração: expressão %s não é booleano" % t[1])


def manipulaExprCallMetodo(t, list_metod, list_Ids):
    if not isInListMetodo(t[1], list_metod):
        raise SyntaxError("erro de chamada: metodo %s não declarado" % t[1])
    verificaParametroCall(t[2], getMetodo(t[1], list_metod), list_Ids)


def manipulaExprEntreParenteses(t):
    pass


def manipulaExprSeta(t, list_Ids):
    if getId(t[1], list_Ids) == None:
        raise SyntaxError("erro de atribuição: %s não foi declarada" % t[1])
    elif t[3][0] == 'op':
        manipulaOp(t[3], list_Ids)
    elif t[3][0] == 'exprID':
        id = getId(t[3][1], list_Ids)
        if id == None:
            raise SyntaxError("erro de atribuição: %s não foi declarada" % t[3][1])
    return t[1]


def manipulaOp(t, list_Ids):
    id1 = getId(t[2], list_Ids)
    id2 = getId(t[3], list_Ids)

    if id1 == None:
        tryParseInt(t[2][1], list_Ids)
    elif id1[1] != "Int":
        raise SyntaxError("erro de operação: %s deve ser do tipo Int" % id1[0])
    if id2 == None:
        tryParseInt(t[3][1], list_Ids)
    elif id2[1] != "Int":
        raise SyntaxError("erro de operação: %s deve ser do tipo Int" % id2[0])


def manipulaComp(t, list_Ids):
    if t[2][0] == 'exprNot':
        id1 = getId(t[2][2][1], list_Ids)
    elif t[2][0] == 'op':
        manipulaOp(t[2], list_Ids)
        id1 = (0, 'Int')
    else:
        id1 = getId(t[2][1], list_Ids)
    if t[3][0] == 'exprNot':
        id2 = getId(t[3][2][1], list_Ids)
    elif t[3][0] == 'op':
        manipulaOp(t[3], list_Ids)
        id2 = (0, 'Int')
    else:
        id2 = getId(t[3][1], list_Ids)

    if id1 == None:
        if type(tryConvertInt(t[2][1])) != int:
            raise SyntaxError("erro de declaração: %s não foi declarado" % t[2][1])
        id1 = (str(tryConvertInt(t[2][1])), 'Int')
    if id2 == None:
        if type(tryConvertInt(t[3][1])) != int:
            raise SyntaxError("erro de declaração: %s não foi declarado" % t[3][1])
        id2 = (str(tryConvertInt(t[3][1])), 'Int')
    if id1[1] != id2[1]:
        raise SyntaxError("erro de comparação: %s %s devem ser do mesmo tipo" % id1[0], id2[0])


def manipulaExprNew(t, list_Types):
    if not isInListType(t[2], list_Types):
        raise SyntaxError("erro de declaração: tipo %s não foi declarado" % t[2])


def manipulaExprVoid(t, list_Ids):
    if not isInListId(t[2], list_Ids):
        raise SyntaxError("erro de declaração: %s não foi declarado" % t[2])


def manipulaExprNot(t, list_Ids):
    if t[2][0] == 'comp':
        manipulaComp(t[2], list_Ids)
        return
    raise SyntaxError("erro de declaração: expressão %s não é booleano" % t[2])


def manipulaFormal(t, list_Ids, list_Types):
    if isInListId(t[1], list_Ids):
        raise SyntaxError("erro de declaração: %s já declarado" % t[1])
    if not isInListType(t[2], list_Types):
        raise SyntaxError("erro de declaração: tipo %s não foi declarado" % t[2])
    list_Ids.append((t[1], t[2]))


def manipulaFeatureRetornoParametro(t, list_Ids, list_metod, list_Types):
    if isInListMetodo(t[1], list_metod):
        raise SyntaxError("erro de declaração: metodo %s já declarado" % t[1])
    if not isInListType(t[3], list_Types):
        raise SyntaxError("erro de declaração: tipo %s não foi declarado" % t[3])
    verificaParametro(t[2], list_Types)
    metodo = (t[1], [], t[3])
    tipo = getType(scope, list_Types)
    if tipo != None:
        tipo[2].append(metodo)
    for id in t[2]:
        newId = (id[1], id[2])
        list_Ids.append(newId)
        metodo[1].append(newId)
    list_metod.append(metodo)


def manipulaFeatureRetorno(t, list_metod, list_Types):
    if isInListMetodo(t[1], list_metod):
        raise SyntaxError("erro de declaração: metodo %s já declarado" % t[1])
    if not isInListType(t[2], list_Types):
        raise SyntaxError("erro de declaração: tipo %s não foi declarado" % t[2])
    metodo = (t[1], [], t[2])
    tipo = getType(scope, list_Types)
    if tipo != None:
        tipo[2].append(metodo)
    list_metod.append(metodo)


def manipulafeatureAnonima(t, list_Ids, list_Types):
    if isInListId(t[1], list_Ids):
        raise SyntaxError("erro de declaração: variavel %s já declarada" % t[1])
    if not isInListType(t[2], list_Types):
        raise SyntaxError("erro de declaração: tipo %s não foi declarado" % t[2])
    if t[2] == 'String':
        if type(t[3][1]) != str:
            raise SyntaxError("erro de declaração: valor incompativel com a variavel %s" % t[1])
    if t[2] == 'Int':
        if type(t[3][1]) != int:
            raise SyntaxError("erro de declaração: valor incompativel com a variavel %s" % t[1])

    list_Ids.append((t[1], t[2]))


def manipulaFeatureDeclaration(t, list_Ids, list_Types):
    if isInListId(t[1], list_Ids):
        raise SyntaxError("erro de declaração: variavel %s já declarada" % t[1])
    if not isInListType(t[2], list_Types):
        raise SyntaxError("erro de declaração: tipo %s não foi declarado" % t[2])
    list_Ids.append((t[1], t[2]))


def manipulaClasseInh(t, list_Types):
    inherits = getType(t[2], list_Types)
    classe = getType(t[1], list_Types)
    for metodo in inherits[2]:
        classe[2].append(metodo)
    for id in inherits[3]:
        classe[3].append(id)


def isInListType(item, lista):
    for i in lista:
        if item == i[0]:
            return True
    return False


def isInListId(item, lista):
    for i in lista:
        if item == i[0]:
            return True
    return False


def getId(nome, lista):
    for item in lista:
        if item[0] == nome:
            return item
    return None


def tryParseInt(valor, list_Ids):
    try:
        valor = int(valor)
    except:
        if isInListId(valor, list_Ids):
            tipo = getId(valor, list_Ids)[1]
            if tipo == 'Int':
                return
        raise SyntaxError("erro de conversão: %s não é do tipo inteiro" % valor)


def tryConvertInt(s):
    try:
        return int(s)
    except:
        return s


def isInListMetodo(metodo, lista):
    for i in lista:
        if metodo == i[0]:
            return True
    return False


def verificaParametro(parametros, list_Types):
    idsParametros = []
    for parametro in parametros:
        if not isInListType(parametro[2], list_Types):
            raise SyntaxError("erro de declaração: tipo %s não foi declarado" % parametro[2])
        if parametro[1] in idsParametros:
            raise SyntaxError("erro de declaração: id %s já utilizado por outro parametro" % parametro[1])
        idsParametros.append(parametro[1])


def verificaParametroCall(parametros, metodo, list_Ids):
    if parametros[0] == None:
        del (parametros[0])
    if len(parametros) != len(metodo[1]):
        raise SyntaxError("erro de chamada: metodo %s deve conter %d parametros" % metodo[0], len(metodo[1]))
    for i in range(0, len(parametros)):
        if not isInListId(parametros[i][1], list_Ids):
            if metodo[1][i][1] == 'Int':
                tryParseInt(parametros[i][1], list_Ids)
            elif metodo[1][i][1] != 'String':
                raise SyntaxError("erro de chamada: parametro %s de tipo incorreto" % parametros[i][1])
            if parametros[i][0] != 'exprValores':
                raise SyntaxError("erro de chamada: id %s não foi declarado" % parametros[i][1])
        else:
            parametro = getId(parametros[i][1], list_Ids)
            if parametro[1] != metodo[1][i][1]:
                raise SyntaxError("erro de chamada: parametro %s de tipo incorreto" % parametros[i][1])


def getMetodo(nome, list_metod):
    for metodo in list_metod:
        if nome == metodo[0]:
            return metodo
    return None


def getType(nome, list_Types):
    for tipo in list_Types:
        if nome == tipo[0]:
            return tipo
    return None


def isNewscopeClasse(s):
    return s == 'classInh' or s == 'class'


def isNewscopeMetodo(s):
    return s == 'featureRetornoParametro' or s == 'featureRetorno'


def isNewscopeLet(s):
    return s == 'exprLetSeta' or s == 'exprLet'


def configSelfType(list_Ids, list_metod, list_Types):
    selftype = getType('SELF_TYPE', list_Types)
    selftype[2].clear()
    selftype[3].clear()
    for metodo in list_metod:
        selftype[2].append(metodo)
    for id in list_Ids:
        selftype[3].append(id)


for filho in tree[0]:
    if type(filho) == tuple:
        if isInListType(filho[1], list_Types):
            raise SyntaxError("erro de declaração: tipo %s já foi declarado" % filho[1])
        if filho[0] == 'class':
            list_Types.append((filho[1], None, [], []))
        elif filho[0] == 'classInh':
            list_Types.append((filho[1], filho[2], [], []))

for filho in tree[0]:
    chamaFuncao(filho, list_Ids, list_metod, list_Types)
