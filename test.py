class Person:
    def a(self):
        for name, action in self.behaviors():
            if name is 'a':
                return action

    def behaviors(self):
        return [
            ('a', self.addOne),
            ('b', self.addTwo)
        ]

    def addOne(self, a):
        return a + 1

    def addTwo(self, b):
        return b + 2


def test(data, *args):
    return data['a']


if __name__ == '__main__':
    p = Person()
    print(p.a()(1))
    pass
