#imports
import sys #to be able to call 'cls' and clear cmd
import csv #to be able to use scv to store information
import number_generator #generator function being used to label students.

class Student:
    def __init__(self, fname, lname, major, pid, email, phone):
        self.fname = fname
        self.lname = lname
        self.name = fname + " " + lname
        self.major = major
        self.pid = pid
        self.email = email
        self.phone = phone

    def __str__(self):
        infoline = f'|{self.name:^27}|{self.major:^15}|{self.pid:^11}|{self.email:^22}|{self.phone:^15}|'
        return infoline

    def store(self):
        studnum = next(studnum_iter)
        student_data = {'studnum' : studnum, 'fname': self.fname, 'lname': self.lname, 'major': self.major, 'pid': self.pid, 'email': self.email, 'phone': self.phone}
        return student_data

def menu(students):
    print("\nStudent Registry\n" + "*"*30 + "\n[1] View List of Students \n" + "[2] Add Students \n" + "[3] Search Entry \n" + "[4] Edit Entry \n" + "[5] Quit \n")
    option = select_action(5)
    if option == 1:
        table(students)
        input("Press Enter to Continue ")
        menu(students)
    elif option == 2:
        try:
            students = addstudent(students)
        except:
            print("Student could not be added... Please try again")
        else:
            input("Student was added succesfully!\nPress Enter to Continue... ")
        menu(students)
    elif option == 3:
        search_student(students)
    elif option == 4:
        edit_student(students)
    elif option == 5:
        sys.exit()
    else:
        print("Invalid Input. Please select valid action.")
        input("Press <Enter> to return to Main Menu")
        menu(students)

def select_action(options):
    while True:
        try:
            action = int(input("Select from the following numbered actions: "))
            if action > options:
                raise Exception
        except Exception:
            print("Invalid Input. Please select action using the available numbered actions.")
            continue
        else:
            return action

def tableheader():
    header = f'|          Student          |     Major     |    PID    |        e-Mail        |     Phone     |'
    rowline = '-'*len(header)
    print(header + "\n" + rowline)
    return len(header)

def table(students):
    '''
    Prints out the a table with the current students on the registry formated with a head and lines.
    '''
    tableheader()
    if students == []:
        empty = ' empty '
        print(f'{empty:=^96}')
    for student in students:
        print(student)
    
def addstudent(students):
    '''
    Requests input from user to define attributes of new student.
    Appends the new student to existing list.
    '''
    fname = input("Enter student's first name: ")
    lname = input("Enter student's last name: ")
    major = input("Enter major of student: ")
    pid = input("Enter Panther ID of student: ")
    email = input("Enter email of student: ")
    phone = input("Enter cellphone of student: ")
    newstudent = Student(fname, lname, major, pid, email, phone) 
    students.append(newstudent)
    save_student(newstudent)
    return students

def save_student(student):
    '''
    Appends new student to the end of file
    '''
    student_data = student.store()
    with open(registry, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writerow(student_data)

def update_students(students):
    '''
    Re-writes the entire list CSV file to update any of the attributes changed
    '''
    update_list = []
    for student in students:
        student_data = student.store()
        update_list.append(student_data)
    with open(registry, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        writer.writerows(update_list)

def restore_students():
    '''
    Reads csv file to recreate and re-list all students created from previous sessions with their
    corresponding attributes. This shall be executed at initialization of the program. 
    '''
    with open(registry, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        existing_student_count = 0
        existing_students = []
        for row in reader:
            existing_student = Student(row['fname'], row['lname'],row['major'], row['pid'], row['email'], row['phone'])
            existing_students.append(existing_student)
            existing_student_count +=1
    return existing_students, existing_student_count  

def search_student(students):
    '''
    Searches a student from the existing list by using their last name.
    This is done by iterating through all entries and comparing to a target.
    '''
    print("\nSearch\n*********\n" + "[1] By Last Name \n" + "[2] By Panther ID \n")
    mode = select_action(2)
    if mode == 1:
        target = input("Enter Student's Last Name: ")
        tableheader()
        try:
            nlist = []
            for student in students:
                if student.lname == target:
                    nlist.append(student)
            for student in nlist:
                print(student)
        except:
            print('No Students Match')
        finally:
            input('Press Enter to Continue')
            menu(students)
    elif mode == 2:
        target = input("Enter Student's Panther ID: ")
        pidlist = []
        for student in students:
            pidlist.append(student.pid)
        try:
            i = pidlist.index(target)
            tableheader()
            print(students[i])
        except:
            print('Student not found')
        finally:
            input('Press Enter to Continue')
            menu(students)
    else:
        print("Invalid Input. Please select action with either 1 or 2")
        input('Press Enter to Continue')
        search_student(students)

def edit_student(students):
    '''
    Changes one of the student parameters by targeting it via its PID 
    and then re-declaring its specified attribute. Executes update_students().
    '''
    target = input("Enter Student's Panther ID: ")
    pidlist = []
    for student in students:
        pidlist.append(student.pid)
    try:
        i = pidlist.index(target)
    except:
        print('No such student found')
        menu(students)
    print('[1] Name\n[2] Major \n[3] Panther ID\n[4] e-Mail\n[5] Cell Phone\n[6] Back to Main Menu')
    attribute = select_action(6)
    if attribute == 1:
        students[i].fname = input(f'Change first name from {students[i].fname} to: ')
        students[i].lname = input(f'Change last name from {students[i].lname} to: ')
        students[i].name = students[i].fname + " " + students[i].lname
        update_students(students)
        input("Changes were applied to student\nPress Enter to Continue...")
        menu(students)
    elif attribute == 2:
        students[i].major = input(f'Change major from {students[i].major} to: ')
        update_students(students)
        input("Changes were applied to student\nPress Enter to Continue...")
        menu(students)
    elif attribute == 3:
        students[i].pid = input(f'Change Panther ID from {students[i].pid} to: ')
        update_students(students)
        input("Changes were applied to student\nPress Enter to Continue...")
        menu(students)
    elif attribute == 4:
        students[i].email = input(f'Change e-Mail from {students[i].email} to: ')
        update_students(students)
        input("Changes were applied to student\nPress Enter to Continue...")
        menu(students)
    elif attribute == 5:
        students[i].phone = input(f'Change Cell Phone from {students[i].phone} to: ')
        update_students(students)
        input("Changes were applied to student\nPress Enter to Continue...")
        menu(students)
    elif attribute == 6:
        menu(students)
    else:
        print("Invalid Input. Please select action with a number from 1 to 6")
        input("Press Enter to return to Main Menu")
        menu(students)

#set up
registry = "mycsvfile.csv" #csv file to be used
fields = ['studnum', 'fname', 'lname', 'major', 'pid', 'email', 'phone']

try: #tries to restore all data from storage (csv file)
    students, existing_studnum = restore_students() #students and current student number are restored
    studnum_iter = number_generator.studnum_gen(num = existing_studnum) #iterator from the generator
    with open(registry, 'r') as csvfile: #MOVE HEADER DETECTION TO INITIALIZATION!!!!
        sniffer = csv.Sniffer() 
        header = sniffer.has_header(csvfile.read(32))
except (FileNotFoundError, Exception) as error: #when no file is found (e.i. first time using the program), 
    students = [] #program will start with empty list of students 
    studnum_iter = number_generator.studnum_gen() #program will start fresh from student #1 
    header = False
finally:
    if header == False:
        with open(registry, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fields)
            writer.writeheader()
    menu(students)
