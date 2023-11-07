from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session


def select_1():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_2():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    WHERE g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subjects_id == 3).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    return result


def select_3():
    """
    SELECT
        g.group_name,
        ROUND(AVG(gb.grade)) as avg_grade
    FROM grade_book as gb
    JOIN students as st on st.id = gb.students_id
    JOIN groups as g on g.id = st.group_id
    WHERE gb.subject_id = 3
    GROUP BY g.group_name;
    """
    result = session.query(Group.name, func.round(func.avg(Grade.grade)).label('avg_grade')) \
        .select_from(Grade).join(Student).join(Group).filter(Grade.subjects_id == 3).group_by(Group.name).all()
    return result


def select_4():
    """
    select ROUND(AVG(grade)) as avg_grade
    from grade_book
    """
    result = session.query(func.round(func.avg(Grade.grade)).label('avg_grade'))\
        .select_from(Grade).all()
    return result


def select_5():
    """
    SELECT subject_name
    FROM subjects
    where teacher_id = 2
    """
    result = session.query(Subject.name) \
        .select_from(Subject).filter(Subject.teacher_id==2).all()
    return result


def select_6():
    """
    SELECT students_name
    FROM students
    where group_id = 3
    """
    result = session.query(Student.fullname) \
        .select_from(Student).filter(Student.group_id == 3).all()
    return result


def select_7():
    """
    SELECT s.students_name, gd.grade
    FROM students as s
    join groups as g on g.id = s.group_id
    join grade_book as gd on gd.students_id = s.id
    join subjects as sub on sub.id = gd.subject_id
    where g.id = 1
    and sub.id = 6
    """
    result = session.query(Student.fullname, Grade.grade) \
        .select_from(Student).join(Group).join(Grade).join(Subject).filter(Group.id == 1, Subject.id == 6).all()
    return result


def select_8():
    """
    SELECT t.teacher_name, sub.subject_name, round(AVG(gd.grade)) avg_grade
    FROM teachers as t
    join subjects as sub on sub.teacher_id = t.id
    join grade_book as gd on gd.subject_id = sub.id
    where t.id = 1
    group by sub.subject_name
    """
    result = session.query(Teacher.fullname, Subject.name, func.round(func.avg(Grade.grade))) \
        .select_from(Teacher).join(Subject).join(Grade).filter(Teacher.id == 1).group_by(Subject.name, Teacher.fullname).all()
    return result


def select_9():
    """
    SELECT s.subject_name
    FROM subjects as s
    join grade_book as gd on gd.subject_id = s.id
    join students as st on st.id = gd.students_id
    where st.id = 14
    """
    result = session.query(Subject.name) \
        .select_from(Subject).join(Grade).join(Student).filter(Student.id == 1).all()
    return result


def select_10():
    """
    SELECT s.subject_name
    FROM subjects as s
    join grade_book as gd on gd.subject_id = s.id
    join students as st on st.id = gd.students_id
    join teachers as t on t.id = s.teacher_id
    where st.id = 40
    and t.id = 1
    group_by s.subject_name
    """
    result = session.query(Subject.name) \
        .select_from(Subject).join(Grade).join(Student).join(Teacher) \
        .filter(Student.id == 40, Teacher.id == 2).group_by(Subject.name).all()
    return result


def select_11():
    """
    SELECT avg(gd.grade)
    FROM subjects as s
    join grade_book as gd on gd.subject_id = s.id
    join students as st on st.id = gd.students_id
    join teachers as t on t.id = s.teacher_id
    where st.id = 6
    and t.id = 2
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Subject).join(Grade).join(Student).join(Teacher) \
        .filter(Student.id == 6, Teacher.id == 2).all()
    return result


def select_12():
    """
    select max(grade_date)
    from grades g
    join students s on s.id = g.student_id
    where g.subject_id = 2 and s.group_id  =3;

    select s.id, s.fullname, g.grade, g.grade_date
    from grades g
    join students s on g.student_id = s.id
    where g.subject_id = 2 and s.group_id = 3 and g.grade_date = (
        select max(grade_date)
        from grades g2
        join students s2 on s2.id=g2.student_id
        where g2.subject_id = 2 and s2.group_id = 3
    );
    :return:
    """

    subquery = (select(func.max(Grade.grade_date)).join(Student).filter(and_(
        Grade.subjects_id == 2, Student.group_id == 3
    ))).scalar_subquery()

    result = session.query(Student.id, Student.fullname, Grade.grade, Grade.grade_date) \
        .select_from(Grade) \
        .join(Student) \
        .filter(and_(Grade.subjects_id == 2, Student.group_id == 3, Grade.grade_date == subquery)).all()

    return result
