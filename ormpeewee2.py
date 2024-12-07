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
    employee_count = IntegerField()

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
        {"name": "Sales", "employee_count": 10},
        {"name": "HR", "employee_count": 5},
        {"name": "Engineering", "employee_count": 20},
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

    # ساخت Subquery برای یافتن ID بزرگترین دپارتمان
    largest_department_query = (Department
                                .select(Department.id)
                                .where(Department.employee_count ==
                                       Department.select(fn.MAX(Department.employee_count)).scalar()))

    # یافتن کارکنانی که در بزرگترین دپارتمان کار می‌کنند
    query = Employee.select().where(Employee.department.in_(largest_department_query))

    # نمایش نتایج
    print("کارکنانی که در بزرگترین دپارتمان کار می‌کنند:")
    for employee in query:
        print(f"نام: {employee.name}, دپارتمان: {employee.department.name}")

    # بستن اتصال به پایگاه داده
    db.close()

if __name__ == "__main__":
    main()
