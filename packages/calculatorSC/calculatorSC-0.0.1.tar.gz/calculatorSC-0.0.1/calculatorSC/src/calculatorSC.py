def convert_to_int(x):
  try:
    return int(x)
  except:
    return None

def convert_to_float(x):
  try:
    return float(x)
  except:
    return None

def convert_to_number(string):
  x = convert_to_int(string)
  if x is None:
    x = convert_to_float(string)
  return x

def prepare(value):
  x = None
  if type(value) is str:
      # try to convert string to number
      x = convert_to_number(value)
  else:
    x = value
  if type(x) is not int and type(x) is not float:
    raise
  return x

class Calculator:
  def __init__(self, initial_value = 0):
    x = prepare(initial_value)
    self.value_now = x


  def screen(self):
    print(self.value_now)
    return self.value_now

 
  def multiply(self, value_to_be_multiplied):
    x = prepare(value_to_be_multiplied)
    self.value_now *= x
    return  self.value_now
    
    # string multiplication: (just for fun)


  def add(self, value_to_be_added):
    x = prepare(value_to_be_added)
    self.value_now += x
    self._stdout = None
    self._stderr = None
    return  self.value_now
    
    # string addition: (just for fun)


  def n_root(self, order_of_root):
    x = prepare(order_of_root)
    self.value_now **= 1 / x
    return  self.value_now
    
    # string rooting: (just for fun)


  def raise_to_power(self, exponent):
    x = prepare(exponent)
    self.value_now **= x
    return  self.value_now

    #string exponentiation: (just for fun)


  def divide_by(self, divisor):
    x = prepare(divisor)
    self.value_now **= x
    return  self.value_now

    #string division: (just for fun)