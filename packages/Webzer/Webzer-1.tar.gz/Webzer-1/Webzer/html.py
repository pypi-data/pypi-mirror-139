file = ''
f = open(file)
end = open(file.split('.')[0]+'.html','w')
end.write('<html>\n  <head>\n    <body>')
dent = '\n      '
class App():
	def __init__(self,name):
		global file
		file = name
class Section():
    def __init__(self,_class):
        end.write(dent+'<div class="'+_class+'">')
        self.dent = dent+'  '
    def addButton(self,text,link,_class):
        end.write(self.dent+'<button href="'+link+'" class="'+_class+'">'+text+'</button>')
    def addLink(self,text,link,_class):
        end.write(self.dent+'<a href="'+link+'" class="'+_class+'">'+text+'</a>')
    def addText(self,text,_class):
        end.write(self.dent+'<p class="'+_class+'">'+text+'</p>')
    def pack(self):
        end.write(dent+'</div>')
def style(_file):
    end.write(dent+'<link rel="stylesheet" href="'+_file+'" type="text/css">')
def finnish():
    end.write('\n    </body>\n  </head>\n</html>')