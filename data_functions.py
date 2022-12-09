from accessConnection import Employee, Courses, CourseAssignments, ConversionRequester, get_session


def add_employee(session ,employee_id, first_name, last_name, email):

    check = session.query(Employee).filter_by(employee_id=employee_id).first()
    if check:
        return

    new_employee = Employee(
        employee_id=employee_id,
        first_name=first_name,
        last_name=last_name,
        email=email

    )
    session.add(new_employee)
    session.commit()


def add_course(session, course_name, course_gen_id, semester, canvas_id):

    check = session.query(Courses).filter_by(course_gen_id=course_gen_id).first()
    if check:
        return check.id

    new_course = Courses(
        course_name=course_name,
        course_gen_id=course_gen_id,
        semester=semester,
        canvas_id=canvas_id

    )
    session.add(new_course)
    course_id = session.flush()
    session.commit()
    return course_id


def assign_employee_to_course(session, employee_id, course_id):

    check = session.query(CourseAssignments).filter_by(employee_id=employee_id, course_id=course_id).first()
    if check:
        return check.id

    new_course_assignment = CourseAssignments(
        employee_id=employee_id,
        course_id=course_id,

    )
    session.add(new_course_assignment)
    course_assignment_id = session.flush()
    print(course_assignment_id)
    session.commit()
    return course_assignment_id


def create_course_requester(session, course_assignment_id):

    requester_check = session.query(ConversionRequester).filter_by(course_assignment_id=course_assignment_id).first()
    if requester_check:
        return

    new_course_requester = ConversionRequester(
        course_assignment_id=course_assignment_id
    )
    session.add(new_course_requester)
    session.commit()
    return


def add_course_requester(employee_id, first_name, last_name, email, course_name, course_gen_id, canvas_id, semester):
    session = get_session()

    add_employee(session, employee_id, first_name, last_name, email)

    course_id = add_course(session, course_name, canvas_id, course_gen_id, semester)

    course_assignment_id = assign_employee_to_course(session, employee_id, course_id)

    create_course_requester(session, course_assignment_id)

    session.close()






# add_course_requester("918848923", "Amy", "Ranger", "aranger@sfsu.edu", "Phil 431-01", "fa22PHIL43101", "11001", "Fa22")









