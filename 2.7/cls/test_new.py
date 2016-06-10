class A(object):
    def __new__(cls, *args, **kwargs):
        print cls
        print args
        print kwargs
        obj = super(A, cls).__new__(cls, args)
        return obj

    def __init__(self, *args, **kwargs):
        print args
        print "here"


inst = A(1)


