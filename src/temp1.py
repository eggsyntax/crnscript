'''
Demonstrates an apparent jython bug. If the __cmp__ method and the __eq__ method use different criteria
for equality (generally a bad idea, admittedly), the sorted results follow neither criterion, but
appear to be a mix of the two.

Under python 2.5 these sort as intended, like:
    [1-00, 1-00, 1-02, 1-02, 1-03, 1-04, 1-05, 1-05, 1-09, 1-10, 2-02, 2-04, 2-05, 2-07, 2-08, 3-00, 3-00, 3-02, 3-04, 3-04, 3-04, 3-06, 3-07, 3-07, 3-09]

Under jython they sort in an apparently nonsensical way:
    [1-03, 1-05, 1-05, 1-08, 2-01, 2-01, 2-02, 2-02, 2-03, 2-05, 3-00, 3-01, 1-01, 1-05, 3-02, 2-02, 2-02, 2-07, 1-07, 3-00, 3-02, 3-04, 3-08, 3-10, 3-10]

'''
from random import randint

class tricky_object:
        
    def __init__(self):
        self.keyfield1 = "%1d" % (randint(1,3))
        self.keyfield2 = "%02d" % (randint(0,10))
        
    def __cmp__(self,other):
        return (cmp(self.keyfield1,other.keyfield1) or
                cmp(self.keyfield2,other.keyfield2))
        
    def __eq__(self,other):
        return (self.keyfield2 == other.keyfield2)

    def __repr__(self):
        return "%s-%s" %(self.keyfield1,self.keyfield2)

tos = [tricky_object() for i in range(25)]
tos.sort()
print tos
