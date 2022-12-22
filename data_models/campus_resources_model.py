
from sqlalchemy import Integer, Column, String,  ForeignKey
from base import Base

class CanvasIds(Base):

    __tablename__ = 'canvas_ids'

    id = Column(Integer(), primary_key=True)
    course_id = Column(Integer(),  ForeignKey("courses.id"))
    canvas_id = Column(Integer())


class Courses(Base):

    __tablename__ = 'courses'
    id = Column(Integer(), primary_key=True)
    semester = Column(String(50))
    term_code = Column(String(4))
    course_registration_number = Column(String(4))
    subject_code = Column(String(5))
    course_number = Column(Integer())
    section_number = Column(Integer())
    class_title = Column(String())


class Students(Base):

    __tablename__ = 'students'
    student_id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    email = Column(String())


class Employee(Base):

    __tablename__ = 'employee'
    employee_id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    email = Column(String())


class CourseAssignments(Base):

    __tablename__ = 'course_assignments'
    id = Column(Integer(), primary_key=True)
    student_id = Column(Integer(),  ForeignKey("students.student_id"))
    employee_id = Column(Integer(),  ForeignKey("employee.employee_id"))
    course_id = Column(Integer(), ForeignKey("courses.id"))


class AccommodationRequesterType(Base):

    __tablename__ = 'accommodation_requester_type'
    id = Column(Integer(), primary_key=True)
    student_id = Column(Integer(),  ForeignKey("students.student_id"))
    course_assignment_id = Column(Integer(), ForeignKey("course_assignments.id"))



class Orgs(Base):

    __tablename__ = 'orgs'
    id = Column(Integer(), primary_key=True)
    org_name = Column(String())
    org_contact = Column(String())
    org_email = Column(String())


class CampusAssociation(Base):

    __tablename__ = 'campus_association'
    id = Column(Integer(), primary_key=True)
    campus_org_id = Column(Integer(), ForeignKey("orgs.id"))
    employee_id = Column(Integer(), ForeignKey("employee.employee_id"))


class Requester(Base):

    __tablename__ = 'requester'
    id = Column(Integer(), primary_key=True)
    accommodation_assignment_id = Column(Integer(), ForeignKey("accommodation_requester_type.id"))
    campus_association_id = Column(Integer(), ForeignKey("campus_association.id"))