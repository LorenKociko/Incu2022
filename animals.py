import sys
class Animal(object):
  def __init__(self, name, age):
    self.name = name
    self.age = age
    
  def speak(self):
    print("I am", self.name, "and I am", self.age, "years old")
    
class Dog(Animal):
  def __init__(self, name, age):
    super().__init_(name, age)
    self.type = 'dog'
    
  def speak(self):
    super().speak()
    print("Woof!")
    
if __name__ == "__main__":
  called_animal = Dog(sys.args[1], sys.args[2])
  called_animal.speak()