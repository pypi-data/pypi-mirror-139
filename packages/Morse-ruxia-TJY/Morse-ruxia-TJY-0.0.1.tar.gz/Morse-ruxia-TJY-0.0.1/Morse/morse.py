class Morse():
    def __init__(self):
        self.encodeDict = {
            'A': '01','B': '1000', 'C': '1010', 'D': '100', 'E': '0',
            'F': '0010', 'G': '110', 'H': '0000', 'I': '00', 'J': '0111',
            'K': '101', 'L': '0100', 'M': '11', 'N': '10', 'O': '111',
            'P': '0110', 'Q': '1101', 'R': '010', 'S': '000', 'T': '1',
            'U': '001', 'V': '0001', 'W': '011', 'X': '1001', 'Y': '1011',
            'Z': '1100', '1': '01111', '2': '00111', '3': '00011', '4': '00001',
            '5': '00000', '6': '10000', '7': '11000', '8': '11100', '9': '11110',
            '0': '11111'
        }
        self.decodeDict = dict([val,key] for key,val in self.encodeDict.items())
        self.Separator = '/'
        self.dot = '.'
        self.dash = '——'
        self.isLower = False

    def encode(self,Char:str):
        code = [self.encodeDict[c.upper()] for c in Char]
        codef = f'{self.Separator}'.join(code)
        codef = codef.replace('0',self.dot).replace('1',self.dash)
        return codef

    def decode(self,Code:str):
        Code = Code.replace(self.dot,'0').replace(self.dash,'1')

        if self.Separator in Code:
            Code = [self.decodeDict[i] for i in Code.split(self.Separator)]
            Code = ''.join(Code)
        else:
            Code = self.decodeDict[Code]
        if self.isLower:
            return Code.lower()
        else:
            return Code
