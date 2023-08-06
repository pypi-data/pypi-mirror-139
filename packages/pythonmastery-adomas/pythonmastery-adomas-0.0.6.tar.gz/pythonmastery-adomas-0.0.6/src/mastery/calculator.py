import math

class Calculator:
    """
    This is a class for computing math operations.
    
    Properties:
        memory (float): Value inside calculator's memory. Default 0.
    """
    
    def __init__(self, memory: float=0):
        """
        The constructor for Calculator class.
        
        Args:
            memory (float, optional): calculator's memory. Defaults to 0.
        """
        self._memory = memory
    
    
    
    @property
    def memory(self):
        return self._memory
    
    @memory.setter
    def memory(self, value: float):
        self._memory = value
    
    @memory.deleter
    def memory(self):
        del self._memory
    
    def add(self, value: float):
        """
        The function to add a value to memory.
        
        Args:
            value (float): number
        """
        self.memory += value
    
    def substract(self, value: float):
        """
        The function to substract a value from memory.
        
        Args:
            value (float): number
        """
        self.memory -= value
        
    def multiply(self, value: float):
        """
        The function to multiply memory by a value.
        
        Args:
            value (float): number
        """
        self.memory *= value
        
    def divide(self, value: float):
        """
        The function to divide memory by a value.
        
        Args:
            value (float): number
        """
        self.memory /= value
            
    def root(self, n: int=2, value: float=-1):
        """
        The function to take n'th root from memory value.
        
        Args:
            n (int): number
            value (float, optional): custom value to be taken a root from.
        """
        try:
            if value == -1:
                self.memory = math.pow(self.memory, 1/n)
            else:
                return math.pow(value, 1/n)
        except ValueError:
            print('Square root can only be taken from positive integers!')
            
    def reset(self, value: float=0):
        """
        The function to reset memory to desired value. Default 0.
        
        Args:
            value (float, optional): number
        """
        self.memory = value