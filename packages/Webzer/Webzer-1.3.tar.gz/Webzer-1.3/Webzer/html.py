dent = '\n      '
end = open('index.html','w')
end.write('<html>\n  <head>\n    <body>')
end.write('<link rel="stylesheet" href="style.css" type="text/css">')
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
def finnish():
    end.write('\n    </body>\n  </head>\n</html>')