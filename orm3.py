from peewee import *

# اتصال به پایگاه داده SQLite
db = SqliteDatabase('company.db')

# مدل پایه
class BaseModel(Model):
    class Meta:
        database = db

# مدل دپارتمان
class Department(BaseModel):
    name = CharField()

# مدل کارمند
class Employee(BaseModel):
    name = CharField()
    department = ForeignKeyField(Department, backref='employees')

# تابع اصلی
def main():
    # اتصال به پایگاه داده و ایجاد جداول
    db.connect()
    db.create_tables([Department, Employee])

    # افزودن داده‌های نمونه به جدول دپارتمان‌ها
    departments = [
        {"id": 1, "name": "Sales"},
        {"id": 2, "name": "HR"},
        {"id": 3, "name": "Engineering"},
    ]
    Department.insert_many(departments).execute()

    # افزودن داده‌های نمونه به جدول کارکنان
    employees = [
        {"name": "Alice", "department": 3},  # Engineering
        {"name": "Bob", "department": 1},    # Sales
        {"name": "Charlie", "department": 3},# Engineering
        {"name": "Diana", "department": 2},  # HR
    ]
    Employee.insert_many(employees).execute()

    # انجام عملیات INNER JOIN و بازیابی داده‌ها
    query = (Employee
             .select(Employee.name, Department.name.alias('department_name'))
             .join(Department)
             .order_by(Employee.name))

    # نمایش نتایج
    print("لیست کارکنان و دپارتمان‌هایشان:")
    for employee in query:
        print(f"کارمند: {employee.name}, دپارتمان: {employee.department_name}")

    # بستن اتصال به پایگاه داده
    db.close()

if __name__ == "__main__":
    main()
