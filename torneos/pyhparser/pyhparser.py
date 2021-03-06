#this is the main class
import re, sys
sys.path.append('../')
from .cleaner import *
from .utils import *
from .classParser import *

#regex constants:
regexConfigurationVariables = r"{(.*),(.*),(.*)}"
regexParseLenVariable = r"^{(.+)}"                      #format {varName}
regexSingleVar = r"^\(([^\(\),\s]+),([^\(\),\s]+)\)"    #format (varName,type)
class pyhparser:
    configs = {"delimiter": ' ', "tempVar": "parserTemp"}#configuration variables
    pythonTypes = {'int': int, 'float': float, 'complex':complex, 'bool': bool, 'str': str, 'dict':dict, 'tuple':tuple, 'list':list, 'set':set}
    def __init__(self, inputText, parserText, classes):#creates a new instance
        self.variables = dict()          #dict of variables to return to the user
        self.inputData = cleanInput(inputText)  #remove whitespaces
        self.parserData = cleanText(parserText) #remove comments and whitespaces
        self.head, self.body = separateHeadBody(self.parserData)
        self.parserData = parseTextToList(self.body) #conver the inpute into a list
        self.inputData = inputTextToList(self.inputData, self.configs["delimiter"])  #split the input file by the delimiter into a list
        self.classes = classParser(classes)     #list of classes required for this input (classParser instance)
        self.parseConfigs()
    def clear(self):#removes the variables created thus far
        self.variables = dict()
    def parseConfigs(self):#parses the head variable for configuration variables
        matches = re.finditer(regexConfigurationVariables, self.head, re.MULTILINE)
        for matchNum, match in enumerate(matches):
            tempConfig = [] #0 -> name 1 -> value, 2 -> type    
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                tempConfig.append(match.group(groupNum))
            tempConfig[1] = removeQuotes(tempConfig[1])
            if not tempConfig[2] in self.pythonTypes.keys():
                print("ERROR - Failed to apply configuration variable (INVALID TYPE): number %d, name: %s, type: %s" % (matchNum+1, tempConfig[0], tempConfig[2]))
            else:
                self.configs[tempConfig[0]] = self.pythonTypes[tempConfig[2]](tempConfig[1]) #cast to type
    def getVariables(self):#returns the variables created after parsing the file
        return self.variables
    def countVariables(self):#return the number of variables in self.variables
        return len(self.variables)
    def appendVariables(self, appendTo):#appends out variables to the dict passed
        if type(appendTo)!= dict:
            print("Error - appendVariables should receive a dict, passed argument is of type %s" % type(appendTo))
            return
        appendTo.update(self.variables)
    def setVariable(self, name, value, t, initializeOnly = False, saveVar = True):#creates a variable and returns it, global or temporary
        try:
            if validTypeSingle(t):
                locals()[name] = self.pythonTypes[t](value) #cast to type
            elif validTypeContainer(t):
                if initializeOnly:
                    locals()[name] = self.pythonTypes[t]()
                else:
                    locals()[name] = value
            if saveVar and name != self.configs["tempVar"]:#if the name of the var is not the protected name in the configuration variables
                self.variables[name] = locals()[name]
            return locals()[name]
        except ValueError:
            print("ERROR - the variable value in the input {%s} does not match its type {%s}" % (value, t))
            exit()
    def parseLenValue(self, text):#receives a text to parse, checks if the text is a value or a variable name containing the size in the format {varName}, ex: 10, {n}
        text.strip(self.configs["delimiter"])
        if text[0] == "{" and ";" in text:
            parserTemp = parseDictGetBothParts(text, ";")
            if parserTemp and parserTemp[0] in self.variables and parserTemp[1] in self.variables:
                return self.variables[parserTemp[0]][len(self.variables[parserTemp[1]])]  #var0[len(var1)], this is like increasing the index, but len is used because it increases by one on each call
        elif text[0] == "{":
            text = re.sub(regexParseLenVariable, "\\1", text, 0, re.MULTILINE)
            if text in self.variables:
                return self.variables[text]
        try: 
            return int(text)
        except ValueError:
            print("ERROR - the variable name you specified for the length {%s} does not exist at this point or is not valid" % text)
            exit()
    def isThereEnoughDataToParse(self, length):#returns False if the values left to parse are less than the required ones
        return length <= len(self.inputData)

    def parseSingleVarType(self, text):#parses (type)
        regexSingleVarAnonymous = r"^\(([^\(\),\s]+)\)" #format (type)
        match = re.search(regexSingleVarAnonymous,text)  #match the format (type)
        if match and validTypeSingle(match.group(1)):
            parserVar = self.setVariable(self.configs["tempVar"], self.inputData[0], match.group(1), saveVar = False)#never global
            del self.inputData[0]
            return parserVar
        return None
    def parseSingleVarNameType(self, text):#parses (name,type)
        match = re.search(regexSingleVar,text)  #match the format (varName, type)
        if match and validTypeSingle(match.group(2)):
            parserVar = self.setVariable(match.group(1), self.inputData[0], match.group(2))#default sets it as global
            del self.inputData[0]
            return parserVar
        regexSingleVarDict = r"^\(([^\(\),\s]+),({.+,.+})\)" #format (int,{sth,sth})
        match = re.search(regexSingleVarDict, text)
        if match:
            dictParts = parseDictGetBothParts(match.group(2))
            if dictParts:                        #instantiate the local variable
                parserTempKey = self.parseVariable(dictParts[0])
                parserTempValue = self.parseVariable(dictParts[1])
                parserVar = {parserTempKey: parserTempValue}
                return self.setVariable(match.group(1),parserVar, "dict")
        return None
    def parseSingleVarNameTypeLen(self, text):#parses (name,type,len)
        regexSingleVarLen = r"^\(([^\(\),\s]+),(str),([^\(\),\s]+)\)"       #format (varName,str,len)
        match = re.search(regexSingleVarLen,text)  #match the format (varName,str,len)
        if match: 
            length = self.parseLenValue(match.group(3))
            if not self.isThereEnoughDataToParse(length):  #exits if this len is not parsable
                print("\n\nERROR - Not enough data to parse in:\n%s" % text)
                exit()
            if length > 0:
                #if not match.group(1) in locals():# TODO: I believe this is an unnecessary, and probably buggy condition check
                parserVar = self.setVariable(match.group(1), self.inputData[0], "str") #instantiate the string, it is set as global as long as the name is not self.configs["tempVar"]
                del self.inputData[0]
                for valIndex in range(length-1):
                    parserVar+= self.configs["delimiter"] + self.inputData[0]
                    del self.inputData[0]
            else: #only create an empty string
                parserVar = self.setVariable(match.group(1), "", "str")
            if match.group(1) != self.configs["tempVar"]:
                self.variables[match.group(1)] = parserVar
            return parserVar
        return None
    def parseSingleVar(self, text):#receives something like (type), (name,type) or (name,type,len) and returns a new variable
        parserVar = self.parseSingleVarType(text)#attempt to parse as (type)
        if parserVar == None:
            match = re.search(regexSingleVar,text)  #match the format (type, len), called before
            if match and match.group(1) == "str":#the names cannot be protected words so this is type, len
                text = "(%s,%s,%s)" % (self.configs["tempVar"], match.group(1), match.group(2))
            parserVar = self.parseSingleVarNameType(text)
            if parserVar == None:
                parserVar = self.parseSingleVarNameTypeLen(text)
                if parserVar == None:
                    print("\n\nERROR - Unable to parse single variable in:\n%s" % text)
                    exit()
        return parserVar
    def parseClassVar(self, text):#format [name,class,className,{param1:paramType1,param2:paramType2,...}]
        regexClassVar = r"^\[([^\[\],\s]+),(class),([^\(\),\s]+),(.+)\]$" #format [varName,class,className,n*{param:paramType}], >=1 params
        match = re.search(regexClassVar, text)
        if match:   #this is a class container #format [varName,class,className,n*{param:paramType}]
            if not self.classes.hasClass(match.group(3)):
                print("\nERROR - the specified class (%s) was not supplied in the constructor of this pyhparser instance, in:\n   %s" % (match.group(3), text))
                exit()
            classParamsText = match.group(4)
            classParams = dict()    #this will contain a dict of {paramName : value}
            while len(classParamsText)>0:
                splitted = parseDictGetBothParts(classParamsText, ":")
                if not splitted:
                    print("\nERROR - unable to create instance of (%s) failed to read param (%s), in:\n   %s" % (match.group(3), classParamsText, text))
                    exit()
                classParams[splitted[0]] = self.parseVariable(splitted[1])
                classParamsText = splitted[2]
            parserVar = self.variables[match.group(1)] = self.classes.initClass(match.group(3),classParams)
            return parserVar
        return None
    def parseContainerVar(self, text):#format [name,type,length,unitType]
        regexContainerVariable = r"^\[([^\s]+?),([^\s]+?),([^\s]+?),([^\s]+?)\]$"   #format [varName,typeContainer,len,unitType]
        match = re.search(regexContainerVariable,text)  #format [varName, typeContainer, length, unitType]
        if match and validTypeContainer(match.group(2)):
            parserIndexList = 0
            length = self.parseLenValue(match.group(3))
            if not self.isThereEnoughDataToParse(length):  #exits if this len is not parsable
                print("\n\nERROR - Not enough data to parse in:\n%s" % match.group(1))
                exit()
            parserVar = self.setVariable(match.group(1), "", match.group(2), initializeOnly = True, saveVar = False) #instantiate the local variable
            if length > 0: #something inside the container
                self.setVariable(match.group(1), parserVar, match.group(2), True)
                parserTemp = self.parseVariable(match.group(4))
                parserVar = addElementToContainer(parserVar, parserTemp)
                for parserIndexList in range(1,length):
                    self.setVariable(match.group(1), parserVar, match.group(2))
                    parserTemp = self.parseVariable(match.group(4))
                    parserVar = addElementToContainer(parserVar, parserTemp)
            return self.setVariable(match.group(1), parserVar, match.group(2))
        return None
    def parseContainerOrClassVar(self, text):#format [name,type,length,unitType]  or [varName,class,className,n*{param:paramType}]
        parserVar = self.parseClassVar(text)#attempt to parse as a class instance
        if parserVar == None:
            parserVar = self.parseContainerVar(text)
            if parserVar == None:
                print("\n\nERROR - Unable to parse container variable in:\n%s" % text)
                exit()
        return parserVar
    def parseDictVar(self, text):#format {type1,type2}
        match = parseDictGetBothParts(text)
        #match = re.search(regexParseDictionary,text)  #match the format {type1,type2}
        if match:                        #instantiate the local variable
            parserTempKey = self.parseVariable(match[0])
            parserTempValue = self.parseVariable(match[1])
            parserVar = {parserTempKey: parserTempValue}
            return parserVar
        return None
    def parseVariable(self, text, saveVar = False):#saveVar == True means this is a variable the user wants, not a temp
        text = text.strip(self.configs["delimiter"])     #remove side delimeters
        if text[0] == "(":      #single var
            return self.parseSingleVar(text)
        elif text[0] == "[":    #container var, can be class instance
            return self.parseContainerOrClassVar(text)
        elif text[0] == "{":    #dict
            return self.parseDictVar(text)
        else:
            print("\n\nERROR - Unable to detect if single or container variable in:\n%s" % text)
            exit()
    def parse(self):#executes the parsing functions and creates the varialbes from the Parser and inputData
        #linePrint = "Parsing line %2d  - %"+str(len(max(self.body, key=len)))+"s...   \n"
        for lineIndex, line in enumerate(self.parserData):              #iterate body line by line
            #print(linePrint % (lineIndex, line), end='')
            line = line.strip(self.configs["delimiter"])
            parts = line.split(self.configs["delimiter"])
            for part in parts:                      #iterate line part by part, separated by the defaultDelimiter
                if len(self.inputData) == 0:
                    print("\nERROR - The input file has less variables than the parser file indicated, stopped at instruction:\n       %s" % part)
                    exit()
                if len(part)>0:
                    self.parseVariable(part)