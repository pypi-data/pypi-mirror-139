def f():
    try:
        print("main")
        # raise Exception("In try")
    except:
        print("except")
        raise Exception("In except")
    else:
        print("Else block")
        raise Exception("In else")
    finally:
        print("finally")
        raise Exception("In finally")

class A:
    def __init__(self,a):
        self.a=a

    def __bool__(self):
        return self.a == 10

a=A(8)
def f():
    try:
        a=A(3)
        return a
    finally:
        a.a=5

        
