class Employee:
    
    raise_amount = 1.04
    num_of_emps = 0
    
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        # self.email = first + last + "@email .com"    
        Employee.num_of_emps += 1
    
    @property    
    def email(self):
        return f"{self.first}.{self.last}@gmail.com"
    
    
    def fullname(self):
        return f"{self.first} {self.last}"
    
    @fullname.setter
    def fullname(self, name):
        first, last = name.split(' ')
        self.first = first
        self.last = last
        
    @fullname.deleter
    def fullname(self):
        print("Delete Name")
        self.first = None
        self.last = None
    
    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)
        
    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amount = amount
    
    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split('-')
        return cls(first, last, pay)
    
    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True
    
    #dunder
    def __repr__(self): 
        return f"Employee({self.first}, {self.last}, {self.pay})"
    
    def __str__(self):
        return f"{self.fullname(), self.email}"
    
    def __add__(self, other):
        return self.pay + other.pay
    
    def __len__(self):
        return len(self.fullname())
        
class Developer(Employee):
    raise_amount = 1.10
    
    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay)
        self.prog_lang = prog_lang
        
class Manager(Employee):
    def __init__(self, first, last, pay, prog_lang, employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees
    
    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
            
    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)
            
    def print_emps(self):
        for emp in self.employees:
            print('--->', emp.fullnam())
        
  
    
   
emp_1 = Employee("Dav", "Ish", 4000)
emp_2 = Employee("Dav", "Ish", 4000)

print(emp_1)
print(emp_1 + emp_2)

# print(help(Developer)) 

# Employee.set_raise_amt(1.05)

# print(emp_1.fullname())
# emp_1.apply_raise()
# print(emp_1.pay)

# print(emp_1.__dict__)
# print("-"*30)
# print(Employee.__dict__)
 
# print(Employee.fullname(emp_1))