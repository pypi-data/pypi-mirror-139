end = open('style.css','w')
class Class:
    def __init__(self,name):
        self.name = name
    def addColor(self, color):
        end.write('\n.'+self.name+'{ color: '+color+'; }')
    def addAlign(self, align):
        end.write('\n.'+self.name+'{ text-align: '+align+'; }')
    def addBox(self,value):
        end.write('\n.'+self.name+'{ border: '+value+'; }')
    def addBg(self,color):
        end.write('\n.'+self.name+'{ background-color: '+color+'; }')
class Tag:
    def __init__(self,name):
        self.name = name
    def addColor(self,color):
        end.write('\n'+self.name+'{ color: '+color+'; }')
    def addAlign(self, align):
        end.write('\n'+self.name+'{ text-align: '+align+'; }')
    def addBox(self,value):
        end.write('\n'+self.name+'{ border: '+value+'; }')
    def addBg(self,color):
        end.write('\n'+self.name+'{ background-color: '+color+'; }')