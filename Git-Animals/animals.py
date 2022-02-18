from logging import exception
import sys
class Animal(object):
  def __init__(self, name, age):
    self.name = name
    self.age = age
    
  def speak(self):
    print("I am", self.name[:-3], "and I am", self.age, "years old")
    
class Dog(Animal):
  def __init__(self, name, age):
    super().__init__(name, age)
    self.type = 'dog'
    
  def speak(self):
    super().speak()
    print("Woof!")

class Cat(Animal):
  def __init__(self, name, age):
    super().__init__(name, age)
    self.type = 'cat'
    
  def speak(self):
    super().speak()
    print("Meow!")
    
if __name__ == "__main__":
    if len(sys.argv) <3:
        raise Exception("Too few arguments")
    called_animal = Dog(sys.argv[0], sys.argv[1])
    called_animal.speak()