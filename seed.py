import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

import conf.models
from conf.db import session
from conf.models import Teacher, Student, Group, Subject, Grade

fake = Faker('uk-UA')

class_dict = {
    "Teacher": [conf.models.Teacher, conf.models.Teacher.fullname],
    "Group": [conf.models.Group, conf.models.Group.name],
    "Subject": [conf.models.Subject, conf.models.Subject.name],
    "Student": [conf.models.Student, conf.models.Student.fullname]
}


def insert_teachers(data=fake.name()):
    for _ in range(5):
        teacher = Teacher(
            fullname=data
        )
        session.add(teacher)


def insert_group(data=fake.word()):
    for _ in range(3):
        group = Group(
            name=data
        )
        session.add(group)


def insert_students(data=fake.name()):
    groups = session.query(Group).all()
    for _ in range(50):
        student = Student(
            fullname=data,
            group_id=random.choice(groups).id
        )
        session.add(student)


def insert_subjects(data=fake.word()):
    teachers = session.query(Teacher).all()
    for _ in range(8):
        student = Subject(
            name=data,
            teacher_id=random.choice(teachers).id
        )
        session.add(student)


def insert_grades():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()

    for _ in range(20):
        for student in students:
            grade = Grade(
                grade=random.randint(1, 100),
                grade_date=fake.date_between(start_date='-100d'),
                student_id=student.id,
                subjects_id=random.choice(subjects).id
            )
            session.add(grade)


def select(class_name):
    table = class_dict[class_name][0]
    result = session.query("*").select_from(table).all()
    return result


def delete(class_name, table_id=None):
    table = class_dict[class_name][0]
    result = session.query(table).filter(table.id == int(table_id)).delete()
    session.commit()
    if result == 1:
        result_text = f"В таблиці: {class_name} ID запису: {table_id} видалено"
    else:
        result_text = f"В таблиці: {class_name} ID запису: {table_id} не знайдено"
    return result_text


def update(class_name, table_id=None, new_data=None):
    if table_id is not None and new_data is not None:
        table = class_dict[class_name][0]
        if class_name in ("Teacher", "Student"):
            ex = session.query(table).filter(table.id == table_id). \
                update({'fullname': new_data})
        else:
            ex = session.query(table).filter(table.id == table_id). \
                update({'name': new_data})
        session.commit()
        if ex == 1:
            return f"В таблиці: {class_name} ID запису: {table_id} змінився на: {new_data}"
        else:
            return f"В таблиці: {class_name} ID запису: {table_id} не змінився"


if __name__ == '__main__':
    try:
        insert_teachers()
        session.commit()
        insert_group()
        session.commit()
        insert_students()
        session.commit()
        insert_subjects()
        session.commit()
        insert_grades()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
