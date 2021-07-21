import sqlite3
from employee import Employee

#conn = sqlite3.connect('employee.db')
conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE employees (
            first text, 
            last text, 
            pay INTEGER
            )""")


def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES(?, ?, ?)", (emp.first, emp.last, emp.pay))

def get_emps_by_name(lastname):
        c.execute("SELECT * FROM employees WHERE last=:last", {'last' : lastname})
        return c.fetchall()

def update_pay(emp, pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay 
                    WHERE first=:first AND last=:last""",
                    {"first" : emp.first, 'last' : emp.last, 'pay' : pay})

def remove_emp(emp):
    with conn:
        c.execute("DELETE from employees WHERE first=:first AND last=:last",
                    {'first' : emp.first, 'last' : emp.last})

emp1 = Employee('Jack', "Little", 80000)
emp2 = Employee('Michele', 'Little', 100000)

insert_emp(emp1)
insert_emp(emp2)
update_pay(emp1, 300000)

print(get_emps_by_name('Little'))

conn.close()