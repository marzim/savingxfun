import re

class URLify:
    pattern = "([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)[-A-Za-z0-9]*\.)[-A-Za-z0-9\.]+):[0-9]*)?/[-A-Za-z0-9_\$\.\+\!\*\(\),;:@&=\?/~\#\%]*[^]'\.}>\),\"]"
    urlfinder = re.compile(re.escape(pattern))
    
    def urlify2(self, value):
        return self.urlfinder.sub(r'<a href="\1">\1</a>', value)
        
    def formatstring(self, value):
        pat1 = re.compile(r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)

        pat2 = re.compile(r"(^|[\n ])(((www|ftp)\.[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)
        value = pat1.sub(r'\1<a href="\2" target="_blank">\3</a>', value)
        value = pat2.sub(r'\1<a href="http://\2" target="_blank">\3</a>', value)
        
        return value
