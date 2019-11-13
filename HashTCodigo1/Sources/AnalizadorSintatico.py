""" Authores: Braslyn Rodriguez Ramirez
              Andres Zuñiga Calderon
              Enrique Mendez Cabezas  
    Descripcion:  Encargado de verificar cada linea individualmente
"""
import os
import sys
import re
import Tabla_Simbolos
file_dir = os.path.dirname(__file__)
sys.path.append("Files")



class AnalizadorSintatico:
    def __init__(self):
        self.Tabla = Tabla_Simbolos.Tabla_Simbolos()
        linea=1
        self.Alcance = "Global"
        with open("../HashTCodigo1/Files/Archivo de pruebas.txt", "r") as file:
            lines = file.read()
            cases = lines.split("\n")
            
        for data in cases:
            self.scan(data,linea)
            linea=linea+1
        """Por medio de una expresicion regular verifica si un if esta construida de forma correcta"""
        """Por medio de una expresicion regular verifica si una variable int esta construida de forma correcta"""    
        """Por medio de una expresicion regular verifica si una variable string esta construida de forma correcta"""      
        """Por medio de una expresicion regular verifica si una variable float esta construida de forma correcta"""      
        """Por medio de una expresicion regular verifica si un while esta construida de forma correctamente"""
        """Por medio de una expresicion regular verifica si una funcion esta construida de forma correctamente"""
        """^\s*([//]{2}[\s\S]*)*$"""
    def scan(self,linea,numero_linea):
        if re.match("^\s*if\s*[(]",linea):
            self.Linea_if(linea,numero_linea)
        else:
            if re.match("^\s*int\s+[a-zA-z]+\w*\s*([=]|[,]|[;])",linea): 
                self.Linea_int(linea,numero_linea)
            else:
                if re.match("^\s*string\s+[a-zA-z]+\w*\s*([=]|[,]|[;])",linea):
                    
                    self.Linea_string(linea,numero_linea)
                else:
                    if re.match("^\s*float\s+[a-zA-z]+\w*\s*([=]|[,]|[;])",linea):
                        self.Linea_float(linea,numero_linea)
                        
                    else:
                        if re.match("^\s*while\s+",linea):
                            self.Linea_while(linea,numero_linea)   
                        else:
                            if re.match("^\s*(int|void|string|float)\s+[a-zA-z]\w*\s*[(]",linea):
                                self.Linea_funcion(linea,numero_linea)
                            else:
                                if re.match("^\s*return\s+",linea):
                                    if re.match("^\s*return\s+([a-zA-Z]\w*|[0-9]+|[\"][\S\s]*[\"]|[0-9]+[.]{1}[0-9]+)\s*[;]\s*[}]{0,1}\s*([/]{2}[\s\S]*)*\s*$",linea):
                                        print("Linea correcta:"+str(numero_linea))
                                    else:
                                         print("Error de sintaxis de declaracion en return, linea "+str(numero_linea)+":"+linea)
                                else:
                                    if re.match("^\s*[a-zA-z]+\w*\s*[=]",linea):
                                        self.Linea_variable(linea,numero_linea)
    
    
    def Linea_string(self,linea,numero_linea):
                bandera = True
                element = ' '
                if re.match("(^\s*string\s+[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[\"][\S\s]*[\"])\s*[;]\s*(string\s+[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[\"][\S\s]*[\"])\s*[;]\s*|string\s+[a-zA-z]+\w*\s*[;]\s*)*([/][/][\s\S]*)*$|^\s*string\s+[a-zA-z]+\w*\s*[;]\s*(string\s+[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[\"][\S\s]*[\"])\s*[;]\s*|string\s+[a-zA-z]+\w*\s*[;]\s*)*([/][/][\s\S]*)*$|^\s*string\s+[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[\"][\S\s]*[\"])\s*(\s*[,]\s*[a-zA-z]+\w*|[,]\s*[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[\"][\S\s]*[\"])\s*)+\s*[;]\s*([/][/][\s\S]*)*$|^\s*string\s+[a-zA-z]+\w*\s*(\s*[,]\s*[a-zA-z]+\w*|\s*[,]\s*[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[\"][\S\s]*[\"])\s*)+\s*[;]\s*([/][/][\s\S]*)*$)",linea):
                    x = re.findall("([a-zA-z]+\w*|[\"][\S\s]*[\"]|([=]|[+])|[,]|[;])",linea)
                    for elemento in x:
                        if bandera == False:
                            
                            if re.match("[a-zA-z]+\w*",elemento[0]) and re.match("[\"][\s\S]*[\"]",elemento[0])==None:
                                
                                if self.Tabla.isInsideme(elemento[0]):
                                    Token = self.Tabla[elemento[0]]
                                    if Token.type != 'string' and Token.type != 'type':
                                        print('Linea '+str(numero_linea)+' variable '+elemento[0]+' no es tipo string   ,'+linea)
                                    else:
                                        if Token.isReservado():
                                            print('Linea '+str(numero_linea)+' variable '+elemento[0]+' es una palabra reservada    ,'+linea)
                                else:
                                    print('Linea '+str(numero_linea)+' variable '+elemento[0]+' no existe    ,'+linea)
                        if elemento[0] != ',' and elemento[0] != '=' and elemento[0] != ';':
                            element=elemento[0]
                        if elemento[0] == ',' or elemento[0] == '=' or elemento[0] == ';':
                            if bandera == True:
                                if self.Tabla.isInsideme(element):
                                    Token = self.Tabla[element]
                                    if Token.tipo_estructura=='variable':
                                        print('Linea '+str(numero_linea)+' variable '+element+' ya ha sido asignada anteriormente    ,'+linea)
                                    else:
                                        if Token.isReservado():
                                            print('Linea '+str(numero_linea)+' variable '+element+' es una palabra reservada    ,'+linea)
                                else:
                                    self.Tabla.añadir(element,Tabla_Simbolos.Token(element,'string',False,self.Alcance,'variable'))
                                       
                                    
                                bandera = False    
                            else:
                                bandera = True
              
                    
                else:
                    print("Error de sintaxis en declaracion de variable tipo string, linea "+str(numero_linea)+":"+linea)    
    def Linea_int(self,linea,numero_linea):
                bandera = True
                element = ' '
                if re.match("(^\s*int\s+[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)\s*)*\s*[;]\s*(int\s+[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)\s*)*\s*[;]\s*|float\s+[a-zA-z]+\w*\s*[;]\s*)*([/][/][\s\S]*)*$|^\s*int\s+[a-zA-z]+\w*\s*[;]\s*(int\s+[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)\s*)*\s*[;]\s*|int\s+[a-zA-z]+\w*\s*[;]\s*)*([/][/][\s\S]*)*$|^\s*int\s+[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)\s*)*\s*([,]\s*[a-zA-z]+\w*|[,]\s*[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)\s*)*\s*)+\s*[;]\s*([/][/][\s\S]*)*$|^\s*int\s+[a-zA-z]+\w*\s*([,]\s*[a-zA-z]+\w*|[,]\s*[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)\s*)*\s*)+\s*[;]\s*([/][/][\s\S]*)*$)",linea):
                    x = re.findall("([a-zA-z]+\w*|([=]|[+]|[-]|[/]|[*])|[0-9]+[.]{1}[0-9]+|[0-9]+|[,]|[;])",linea)
                    for elemento in x:
                        if elemento[0] != ',' and elemento[0] != '=' and elemento[0] != ';':
                            element=elemento[0]
                        if bandera == False:
                            if re.match("[a-zA-z]+\w*",elemento[0]):
                                print(elemento[0])
                                if self.Tabla.isInsideme(elemento[0]):
                                    Token = self.Tabla[elemento[0]]
                                    if Token.tipo_estructura=='variable':
                                        print('Linea '+str(numero_linea)+' variable '+elemento[0]+' no es tipo int    ,'+linea)
                                    else:
                                        if Token.tipo_estructura=='funcion':
                                            print('Linea '+str(numero_linea)+' variable '+elemento[0]+' se le esta asignando una funcion    ,'+linea)
                                        else:
                                            if Token.isReservado():
                                                print('Linea '+str(numero_linea)+' variable '+elemento[0]+' es una palabra reservada    ,'+linea)
                                else:
                                    print('Linea '+str(numero_linea)+' variable '+elemento[0]+' no existe    ,'+linea)
                        
                        if elemento[0] == ',' or elemento[0] == '=' or elemento[0] == ';':
                            if bandera == True:
                                if self.Tabla.isInsideme(element):
                                    Token = self.Tabla[element]
                                    if Token.tipo_estructura=='variable':
                                        print('Linea '+str(numero_linea)+' variable '+element+' ya ha sido asignada anteriormente    ,'+linea)
                                    else:
                                        if Token.isReservado():
                                            print('Linea '+str(numero_linea)+' variable '+element+' es una palabra reservada    ,'+linea)
                                else:
                                    self.Tabla.añadir(element,Tabla_Simbolos.Token(element,'int',False,self.Alcance,'variable'))
                                       
                                    
                                bandera = False    
                            else:
                                bandera = True
              
                    
                else:
                    print("Error de sintaxis en declaracion de variable tipo int, linea "+str(numero_linea)+":"+linea)    
        
    def Linea_float(self,linea,numero_linea):
                bandera = True
                element = ' '
                if re.match("(^\s*float\s+[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)\s*)*\s*[;]\s*(float\s+[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)\s*)*\s*[;]\s*|float\s+[a-zA-z]+\w*\s*[;]\s*)*([/][/][\s\S]*)*$|^\s*float\s+[a-zA-z]+\w*\s*[;]\s*(float\s+[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)\s*)*\s*[;]\s*|float\s+[a-zA-z]+\w*\s*[;]\s*)*([/][/][\s\S]*)*$|^\s*float\s+[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)\s*)*\s*([,]\s*[a-zA-z]+\w*|[,]\s*[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)\s*)*\s*)+\s*[;]\s*([/][/][\s\S]*)*$|^\s*float\s+[a-zA-z]+\w*\s*([,]\s*[a-zA-z]+\w*|[,]\s*[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)\s*)*\s*)+\s*[;]\s*([/][/][\s\S]*)*$)",linea):
                    x = re.findall("([a-zA-z]+\w*|([=]|[+]|[-]|[/]|[*])|[0-9]+[.]{1}[0-9]+|[0-9]+|[,]|[;])",linea)
                    for elemento in x:
                        if bandera == False:
                            if re.match("[a-zA-z]+\w*",elemento[0]):
                                if self.Tabla.isInsideme(elemento[0]):
                                    Token = self.Tabla[elemento[0]]
                                    if Token.tipo_estructura=='variable':
                                        print('Linea '+str(numero_linea)+' variable '+elemento[0]+' no es tipo float    ,'+linea)
                                    else:
                                        if Token.isReservado():
                                            print('Linea '+str(numero_linea)+' variable '+elemento[0]+' es una palabra reservada    ,'+linea)
                                else:
                                    print('Linea '+str(numero_linea)+' variable '+elemento[0]+' no existe    ,'+linea)
                        if elemento[0] != ',' and elemento[0] != '=' and elemento[0] != ';':
                            element=elemento[0]
                        if elemento[0] == ',' or elemento[0] == '=' or elemento[0] == ';':
                            if bandera == True:
                                if self.Tabla.isInsideme(element):
                                    Token = self.Tabla[element]
                                    if Token.tipo_estructura=='variable':
                                        print('Linea '+str(numero_linea)+' variable '+element+' ya ha sido asignada anteriormente    ,'+linea)
                                    else:
                                        if Token.isReservado():
                                            print('Linea '+str(numero_linea)+' variable '+element+' es una palabra reservada    ,'+linea)
                                else:
                                    self.Tabla.añadir(element,Tabla_Simbolos.Token(element,'float',False,self.Alcance,'variable'))
                                       
                                    
                                bandera = False    
                            else:
                                bandera = True
              
                    
                else:
                    print("Error de sintaxis en declaracion de variable tipo float, linea "+str(numero_linea)+":"+linea)  

    def Linea_funcion(self,linea,numero_linea):
                IsFuncion = True
                tipo = ' '
                if re.match("^\s*(int|void|string|float)\s+[a-zA-z]\w*\s*[(]\s*(int|string|float)\s+[a-zA-z]\w*(\s*[,]{1}\s*(int|string|float)\s+[a-zA-z]\w*)*\s*[)]\s*[{]{0,1}\s*([/]{2}[\s\S]*)*$",linea):
                    x = re.findall("[a-zA-z]+\w*",linea)
                    
                    for elemento in x:
                     
                        if elemento=='int' or elemento=='string' or elemento=='float' or elemento=='void':
                            tipo = elemento
                        else:
                            if IsFuncion == True:
                                if self.Tabla.isInsideme(elemento):
                                    Token = self.Tabla[elemento]
                                    if Token.tipo_estructura=='variable':
                                        print('Linea '+str(numero_linea)+' funcion '+elemento+' nombre ya ha sido asignado anteriormente para una variable   ,'+linea)
                                    else:
                                        if Token.isReservado():
                                            print('Linea '+str(numero_linea)+' funcion '+elemento+' es una palabra reservada    ,'+linea)
                                else:
                                    self.Tabla.añadir(elemento,Tabla_Simbolos.Token(elemento,tipo,False,self.Alcance,'funcion'))
                                    self.Alcance = "local"
                                IsFuncion=False
                            else:
                                if self.Tabla.isInsideme(elemento):
                                    Token = self.Tabla[elemento]
                                    if Token.tipo_estructura=='variable':
                                        print('Linea '+str(numero_linea)+' variable '+elemento+' nombre ya ha sido asignado anteriormente para una variable   ,'+linea)
                                    else:
                                        if Token.isReservado():
                                            print('Linea '+str(numero_linea)+' variable '+elemento+' es una palabra reservada    ,'+linea)
                                else:
                                    self.Tabla.añadir(elemento,Tabla_Simbolos.Token(elemento,tipo,False,self.Alcance,'variable'))
                                    
                                
                            
                    
                                
              
                    
                else:
                    print("Error de sintaxis en declaracion de funcion, linea "+str(numero_linea)+":"+linea)  
                  
    def Linea_while(self,linea,numero_linea):
                i = 1
                IsFuncion = True
                element = ' '
                if re.match("^\s*while\s*[(]\s*(([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)|[\"][\S\s]*[\"])\s+(==|<=*|>=*|!=)\s+(([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)|[\"][\S\s]*[\"])\s*([&]{2}\s*(([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)|[\"][\S\s]*[\"])\s+(==|<=*|>=*|!=)\s+(([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)|[\"][\S\s]*[\"])\s*|[|]{2}\s*(([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)|[\"][\S\s]*[\"])\s+(==|<=*|>=*|!=)\s+(([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)|[\"][\S\s]*[\"])\s*)*\s*[)]\s*[{]{0,1}\s*([/][/][\s\S]*)*$",linea):
                    x = re.findall("([a-zA-z]+\w*|[0-9]+[.]{1}[0-9]+|[0-9]+|[\"][\s\S]*[\"])",linea)
                    x.pop(0)
                    for elemento in x:
                        if i % 2 != 0:  
                            element = elemento
                            i = i + 1 
                        else:
                            if re.match("[\"][\s\S]*[\"]",element) and re.match("([0-9]+[.]{1}[0-9]+|[0-9]+)",elemento) or re.match("([0-9]+[.]{1}[0-9]+|[0-9]+)",element) and re.match("[\"][\s\S]*[\"]",elemento):
                                print("Error de tipo de variables, linea "+str(numero_linea)+":"+linea)
                            else:
                                if re.match("[a-zA-z]+\w*",element) and re.match("[a-zA-z]+\w*",elemento):
                                    if self.Tabla.isInsideme(element):
                                        if self.Tabla.isInsideme(elemento):
                                            Token1=self.Tabla[element]
                                            Token2=self.Tabla[elemento]
                                            if Token1.type != Token2.type:
                                                print("Error de tipo de variables, linea "+str(numero_linea)+":"+linea)
                                    
                                        else:
                                            print('Linea '+str(numero_linea)+' variable '+elemento+' no existe    ,'+linea) 
                                    
                                    else:
                                        print('Linea '+str(numero_linea)+' variable '+element+' no existe    ,'+linea)
                                
                            i = i + 1 

                else:
                    print("Error de sintaxis en declaracion de while, linea "+str(numero_linea)+":"+linea)
                    
    def Linea_if(self,linea,numero_linea):
                i = 1
                IsFuncion = True
                element = ' '
                if re.match("^\s*if\s*[(]\s*(([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)|[\"][\S\s]*[\"])\s+(==|<=*|>=*|!=)\s+(([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)|[\"][\S\s]*[\"])\s*([&]{2}\s*(([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)|[\"][\S\s]*[\"])\s+(==|<=*|>=*|!=)\s+(([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)|[\"][\S\s]*[\"])\s*|[|]{2}\s*(([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)|[\"][\S\s]*[\"])\s+(==|<=*|>=*|!=)\s+(([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+)|[\"][\S\s]*[\"])\s*)*\s*[)]\s*[{]{0,1}\s*([/][/][\s\S]*)*$",linea):
                    x = re.findall("([a-zA-z]+\w*|[0-9]+[.]{1}[0-9]+|[0-9]+|[\"][\s\S]*[\"])",linea)
                    x.pop(0)
                    for elemento in x:
                        if i % 2 != 0:  
                            element = elemento
                            i = i + 1 
                        else:
                            if re.match("[\"][\s\S]*[\"]",element) and re.match("([0-9]+[.]{1}[0-9]+|[0-9]+)",elemento) or re.match("([0-9]+[.]{1}[0-9]+|[0-9]+)",element) and re.match("[\"][\s\S]*[\"]",elemento):
                                print("Error de tipo de variables, linea "+str(numero_linea)+":"+linea)
                            else:
                                if re.match("[a-zA-z]+\w*",element) and re.match("[a-zA-z]+\w*",elemento):
                                    if self.Tabla.isInsideme(element):
                                        if self.Tabla.isInsideme(elemento):
                                            Token1=self.Tabla[element]
                                            Token2=self.Tabla[elemento]
                                            if Token1.type != Token2.type:
                                                print("Error de tipo de variables, linea "+str(numero_linea)+":"+linea)
                                    
                                        else:
                                            print('Linea '+str(numero_linea)+' variable '+elemento+' no existe    ,'+linea) 
                                    
                                    else:
                                        print('Linea '+str(numero_linea)+' variable '+element+' no existe    ,'+linea)
                                
                            i = i + 1 

                else:
                    print("Error de sintaxis en declaracion de if, linea "+str(numero_linea)+":"+linea)
                    
    def Linea_variable(self,linea, numero_linea):
        token = ' '
        if re.match("^\s*[a-zA-z]+\w*\s*[=]\s*([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+|[\"][\s\S]*[\"])(\s+([+]|[-]|[*]|[/]){1}\s+([a-zA-z]+\w*|[0-9]+|[0-9]+[.]{1}[0-9]+|[\"][\s\S]*[\"])\s*)*\s*[;]\s*$",linea):
            x = re.findall("([a-zA-z]+\w*|[0-9]+[.]{1}[0-9]+|[0-9]+|[\"][\s\S]*[\"])",linea)
            token = x.pop(0)
            if self.Tabla.isInsideme(token):
                    token = self.Tabla[token]
                    if token.isReservado():
                        print("Error, variable "+token.token+" ya esta declarada como una palabra reservada en linea"+str(numero_linea)+":"+linea)
                    else:
                        for elemento in x:
                            if re.match("[\"][\s\S][\"]",elemento):
                                if token.type == 'int' or token.type == 'float':
                                    print("Error de tipo de variables se le asigna un string a un int, linea "+str(numero_linea)+":"+linea)
                            else:
                                if re.match("([0-9]+|[0-9]+[.]{1}[0-9]+)",elemento):
                                    if token.type=='string':
                                        print("Error de tipo de variables se le asigna un (int o double) a un string, linea "+str(numero_linea)+":"+linea)
                                else:                                
                                    if self.Tabla.isInsideme(elemento):
                                        Token = self.Tabla[elemento]
                                        if Token.type != token.type:
                                            print("Error de tipo de variables, linea "+str(numero_linea)+":"+linea)
                                    else:
                                        print('Linea '+str(numero_linea)+' variable '+elemento+' no existe    ,'+linea)     
                    
                    
            else:
                print('Linea '+str(numero_linea)+' variable '+ token+' no existe    ,'+linea) 
        else:
            print("Error de sintaxis en asignacion a variable, linea "+str(numero_linea)+":"+linea)
                        
        