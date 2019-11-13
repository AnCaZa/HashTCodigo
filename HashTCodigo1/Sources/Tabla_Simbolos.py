"""
    Autor: Braslyn Rodriguez Ramirez
    Descripcion: Implementacion de un Hash para crear una Tabla de simbolos
"""

STRING= r"\"[a-zA-Z_0-9]*\""
"""float funcional con ambos"""
FLOAT = r"-?[\d']+.?[\d']+"
INT =  r"-?[\d']+"

class Token:
    def __init__(self,token,Type,reservado,alcance,tipo_estructura):
        self.token=token
        self.reservado=reservado
        self.type=Type
        self.alcance = alcance
        self.tipo_estructura=tipo_estructura
    def __repr__(self):
        return f"{self.token} reservado: {self.reservado}"
    def isReservado(self):
        return self.reservado


class Tabla_Simbolos:
    Instance=None
    class TablaSingleton:
        """Constructor Inicia la tabla de simbolos"""
        def __init__(self):
            self.hash={}
            with open("../HashTCodigo1/Files/Lexico.txt", "r") as file:
                lines = file.read()
                cases = lines.split("\n")
            for data in cases:
                datain=data.split(" ")
                self.añadir(datain[0],Token(datain[0]," ",True,"global",datain[1]))
        """Se imprimen todos los elementos del dicionario"""
        def __repr__(self):
            return  f"{list(self.hash.values())}"
        """ Funcion encargada de añadir elementos al hash"""
        def añadir(self,key,item):
            self.hash[key]=item
        """ Devuelve el numero de elementos del diccionario"""
        def __len__(self):
            return len(self.hash)
        """ Funcion encargada de eliminar un elemento del diccionario"""
        def eliminarElemento(self,key):
            del self.hash[key]
        """Funcion encargada de elimina todos los elementos """
        def EliminarTodo(self):
            self.hash.clear()
        """ Tomar un elemento de la tabla de sibolos"""
        def __getitem__(self,key):
            return self.hash[key]
        """Obtiene todos los valores de un tipo"""
        def getAllforType(self,type):
            lista=[]
            for key in self.hash:
                if self.hash[key].type==type:
                    lista.append(self.hash[key])
            return lista
        """ Devuelve true si el elemento pertenece a la tabla"""
        def isInsideme(self,keySearch):
            return keySearch in self.hash
        def GenerarRE(self,keyword):
            line=""
            for word in self.hash.values():
                if word.type==keyword:
                    if len(line)>0:
                        line+="|"
                    line+=word.token
            return line




    """Singleton de Tabla de Simbolos"""
    def __new__(cls): # __new__ always a classmethod
        if not Tabla_Simbolos.Instance:
            Tabla_Simbolos.Instance = Tabla_Simbolos.TablaSingleton()
        return Tabla_Simbolos.Instance
    def __getattr__(self, name):
        return self.Instance
    
