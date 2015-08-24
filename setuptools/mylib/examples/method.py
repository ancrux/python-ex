class zzz():
    zoo = "zoo"

    @classmethod
    def foo(cls, name):
        print("hi! %s, it's classmethod." % name)
        print("zoo =", cls.zoo)

    @staticmethod
    def bar(name):
        print("hi! %s, it's staticmethod ." % name)
        print("zoo =", zzz.zoo)

    def normal_method(self):
        print("It's normal_method.")
        print("zoo =", self.zoo) 

zzz.foo("mission")
print("="*20)
zzz.bar("mission")
print("="*20)
zzz().normal_method()
print("="*20)
zzz.normal_method(zzz) 
