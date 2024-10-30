data = ["Hello", "Word"]


class Foo(object):
  @property
  def bar(self):
    return data[0]
  
  def __repr__(self) -> str:
    return "Hello World"

Hello = Foo()

data_1 = Hello.bar

print(data[0])
