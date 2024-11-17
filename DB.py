
from PyQt5 import QtCore, QtGui, QtWidgets
import pymssql
from functools import partial

from PyQt5.QtWidgets import QMessageBox


def get_db_connection():
    """创建并返回数据库连接的函数。"""
    try:
        connection = pymssql.connect(
            server='LAPTOP-2UJ543GH\\NEWEST',
            database='学生成绩管理'
        )
        print("数据库连接成功")
        return connection
    except pymssql.DatabaseError as e:
        print(f"数据库连接错误: {e}")
        return None
class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("LoginWindow")
        self.resize(800, 500)
        self.setWindowTitle("登录界面")
        self.setStyleSheet("background: #f0f0f0;")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(20)

        self.titleLabel = QtWidgets.QLabel("欢迎登录", self)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont("Helvetica", 24, QtGui.QFont.Bold)
        self.titleLabel.setFont(font)
        self.layout.addWidget(self.titleLabel)

        self.roleLabel = QtWidgets.QLabel("请选择身份:", self)
        self.layout.addWidget(self.roleLabel)

        self.roleComboBox = QtWidgets.QComboBox(self)
        self.roleComboBox.addItems(["学生", "教师", "管理员"])
        self.layout.addWidget(self.roleComboBox)

        self.usernameLabel = QtWidgets.QLabel("用户名:", self)
        self.layout.addWidget(self.usernameLabel)

        self.usernameLineEdit = QtWidgets.QLineEdit(self)
        self.usernameLineEdit.setPlaceholderText("请输入用户名")
        self.layout.addWidget(self.usernameLineEdit)

        self.passwordLabel = QtWidgets.QLabel("密码:", self)
        self.layout.addWidget(self.passwordLabel)

        self.passwordLineEdit = QtWidgets.QLineEdit(self)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit.setPlaceholderText("请输入密码")
        self.layout.addWidget(self.passwordLineEdit)

        self.loginButton = QtWidgets.QPushButton("登录", self)
        self.loginButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                border-radius: 5px;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.layout.addWidget(self.loginButton)

        self.setLayout(self.layout)

        self.loginButton.clicked.connect(self.login)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        role = self.roleComboBox.currentText()
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        connection = get_db_connection()
        if not connection:
            QtWidgets.QMessageBox.warning(self, "连接失败", "无法连接到数据库。")
            return

        if role == "学生":
            query = "SELECT StudentID, StudentName, ClassID FROM Students WHERE username = %s AND password = %s"
        elif role == "教师":
            query = "SELECT TeacherID, TeacherName, Title FROM Teachers WHERE username = %s AND password = %s"
        elif role == "管理员":
            query = "SELECT AdminID, AdminName FROM Admins WHERE username = %s AND password = %s"
        else:
            QtWidgets.QMessageBox.warning(self, "身份错误", "当前身份不支持。")
            return

        cursor = connection.cursor()

        try:
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            print(f"查询结果: {result}")

            if result:
                if role == "学生":
                    self.show_student_info(result)
                elif role == "教师":
                    self.show_teacher_info(result)
                elif role == "管理员":
                    self.show_admin_management(result)
            else:
                QtWidgets.QMessageBox.warning(self, "登录失败", "用户名或密码错误。")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "SQL错误", str(e))
            print(f"SQL执行错误: {e}")
        finally:
            cursor.close()
            connection.close()  # 确保在任何情况下都关闭连接

    def show_student_info(self, result):
        self.student_info_window = StudentInfoWindow(result)
        self.student_info_window.show()
        self.close()  # 关闭登录窗口

    def show_teacher_info(self, result):
        self.teacher_info_window = TeacherInfoWindow(result)
        self.teacher_info_window.show()
        self.close()  # 关闭登录窗口

    def show_admin_management(self, result):
        self.admin_window = AdminManagementWindow(result)
        self.admin_window.show()
        self.close()  # 关闭登录窗口

class StudentInfoWindow(QtWidgets.QWidget):
    def __init__(self, student_info):
        super().__init__()
        self.student_info = student_info
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("学生信息")
        self.resize(800, 500)
        layout = QtWidgets.QVBoxLayout()

        # 显示学生信息
        self.studentIDLabel = QtWidgets.QLabel(f"学生ID: {self.student_info[0]}")
        self.studentNameLabel = QtWidgets.QLabel(f"学生姓名: {self.student_info[1]}")
        self.classIDLabel = QtWidgets.QLabel(f"班级ID: {self.student_info[2]}")

        layout.addWidget(self.studentIDLabel)
        layout.addWidget(self.studentNameLabel)
        layout.addWidget(self.classIDLabel)

        # 查看课程成绩按钮
        self.viewGradesButton = QtWidgets.QPushButton("查看课程成绩", self)
        self.viewGradesButton.clicked.connect(self.view_grades)
        layout.addWidget(self.viewGradesButton)

        # 修改密码按钮
        self.changePasswordButton = QtWidgets.QPushButton("修改密码", self)
        self.changePasswordButton.clicked.connect(self.change_password)
        layout.addWidget(self.changePasswordButton)

        self.setLayout(layout)

    def view_grades(self):
        grades = self.get_grade(self.student_info[0])

        # 创建一个对话框
        grades_dialog = QtWidgets.QDialog(self)
        grades_dialog.setWindowTitle("课程成绩")
        grades_dialog.resize(700, 300)

        # 创建表格
        grades_table = QtWidgets.QTableWidget(grades_dialog)
        grades_table.setColumnCount(3)  # 3列: 课程ID, 课程名称, 成绩
        grades_table.setHorizontalHeaderLabels(["课程ID", "课程名称", "成绩"])

        # 填充表格数据
        grades_table.setRowCount(len(grades))
        for row_index, grade in enumerate(grades):
            grades_table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(grade['CourseID'])))
            grades_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(grade['CourseName']))
            grades_table.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(grade['Score'])))

        # 创建布局
        grades_layout = QtWidgets.QVBoxLayout(grades_dialog)
        grades_layout.addWidget(grades_table)

        # 设置对话框的布局
        grades_dialog.setLayout(grades_layout)
        grades_dialog.exec_()  # 使用 exec_() 显示对话框并暂停其他交互

    def get_grade(self, student_id):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            query = '''
                SELECT Courses.CourseID, Courses.CourseName, Grades.Score
                FROM Grades
                JOIN Courses ON Grades.CourseID = Courses.CourseID
                WHERE Grades.StudentID = %s
            '''
            cursor.execute(query, (student_id,))  # 使用元组传递参数

            # 获取查询结果
            grades = []
            for row in cursor.fetchall():
                grades.append({
                    'CourseID': row[0],
                    'CourseName': row[1],
                    'Score': row[2]
                })

        except Exception as e:
            print(f"获取成绩时出错: {e}")
            grades = []  # 如果出错，返回空列表
        finally:
            # 关闭数据库连接
            cursor.close()
            connection.close()

        return grades
    def change_password(self):
        old_password, ok = QtWidgets.QInputDialog.getText(self, '输入旧密码', '请输入旧密码:',
                                                          QtWidgets.QLineEdit.Password)
        if ok and old_password:
            if not self.verify_old_password(self.student_info[0], old_password):
                QtWidgets.QMessageBox.critical(self, "失败", "旧密码错误！")
                return

            # 输入新密码
            new_password, ok = QtWidgets.QInputDialog.getText(self, '输入新密码', '请输入新密码:',
                                                              QtWidgets.QLineEdit.Password)
            if ok and new_password:
                # 再次确认新密码
                confirm_password, ok = QtWidgets.QInputDialog.getText(self, '确认新密码', '请再次输入新密码:',
                                                                      QtWidgets.QLineEdit.Password)
                if ok and confirm_password:
                    if new_password != confirm_password:
                        QtWidgets.QMessageBox.warning(self, "失败", "两次输入的新密码不匹配！")
                        return

                    if self.update_password(self.student_info[0], new_password):
                        QtWidgets.QMessageBox.information(self, "成功", "密码修改成功。")
                    else:
                        QtWidgets.QMessageBox.critical(self, "失败", "密码修改失败。")

    def verify_old_password(self, student_id, old_password):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            query = "SELECT StudentID FROM Students WHERE StudentID = %s AND password = %s"
            cursor.execute(query, (student_id, old_password))
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"检查旧密码失败: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    def update_password(self, student_id, new_password):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            query = "UPDATE Students SET password = %s WHERE StudentID = %s"
            cursor.execute(query, (new_password, student_id))
            connection.commit()  # 提交更改
            return True
        except Exception as e:
            print(f"修改密码失败: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
def get_student_grades(course_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    grades = []

    try:
        query = """
        SELECT g.StudentID, s.StudentName, g.Score, cl.ClassID 
        FROM Grades g
        JOIN Students s ON g.StudentID = s.StudentID
        JOIN Classes cl ON g.CourseID = cl.CourseID
        WHERE g.CourseID = %s
        ORDER BY cl.ClassID ASC
        """
        cursor.execute(query, (course_id,))

        results = cursor.fetchall()
        print("查询到的结果:")
        for row in results:
            print(row)  # 打印每一行结果，检查数据

        for row in results:
            grades.append({
                'StudentID': row[0],
                'StudentName': row[1],
                'Score': row[2],
                'ClassID': row[3]  # 添加班级ID
            })
    except Exception as e:
        print(f"查询学生成绩失败: {e}")
    finally:
        cursor.close()
        connection.close()

    return grades

def get_teacher_courses(teacher_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    courses_info = []

    try:
        query = """
        SELECT DISTINCT c.CourseID, c.CourseName
        FROM Courses c
        JOIN Classes cl ON c.CourseID = cl.CourseID
        WHERE cl.TeacherID = %s
        """
        cursor.execute(query, (teacher_id,))

        results = cursor.fetchall()
        for row in results:
            courses_info.append({
                'CourseID': row[0],
                'CourseName': row[1]
            })
    except Exception as e:
        print(f"查询课程失败: {e}")
    finally:
        cursor.close()
        connection.close()

    return courses_info

def delete_student_grade(course_id, student_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "DELETE FROM Grades WHERE CourseID = %s AND StudentID = %s"
        cursor.execute(query, (course_id, student_id))
        connection.commit()
        return True
    except Exception as e:
        print(f"删除成绩失败: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def change_student_grade(course_id, student_id, new_score):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "UPDATE Grades SET Score = %s WHERE CourseID = %s AND StudentID = %s"
        cursor.execute(query, (new_score, course_id, student_id))
        connection.commit()
        return True
    except Exception as e:
        print(f"更改成绩失败: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def add_student_grade(course_id, student_id, score):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO Grades (CourseID, StudentID, Score) VALUES (%s, %s, %s)"
        cursor.execute(query, (course_id, student_id, score))
        connection.commit()
        return True
    except Exception as e:
        print(f"添加成绩失败: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def check_student_exists(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "SELECT StudentID FROM Students WHERE StudentID = %s"
        cursor.execute(query, (student_id,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"检查学生是否存在失败: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def check_student_grade_exists(course_id, student_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM Grades WHERE CourseID = %s AND StudentID = %s"
        cursor.execute(query, (course_id, student_id))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"检查学生成绩是否存在失败: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def get_class_students_grades(course_id, teacher_id):
    global class_average_scores, class_high_low_scores
    connection = get_db_connection()
    cursor = connection.cursor()

    grades = []
    class_scores = {}

    try:
        # 查询学生成绩
        query = """
        SELECT s.StudentID, s.StudentName, g.Score, s.ClassID 
        FROM Students s
        JOIN Classes cl ON s.ClassID = cl.ClassID
        JOIN Grades g ON g.StudentID = s.StudentID AND g.CourseID = cl.CourseID 
        WHERE g.CourseID = %s AND cl.TeacherID = %s
        ORDER BY s.ClassID ASC
        """
        cursor.execute(query, (course_id, teacher_id))
        results = cursor.fetchall()

        for row in results:
            grades.append({
                'StudentID': row[0],
                'StudentName': row[1],
                'Score': row[2],
                'ClassID': row[3]
            })

            # 根据班级ID计算班级的成绩数据
            class_id = row[3]
            if class_id not in class_scores:
                class_scores[class_id] = {
                    'total_score': 0,
                    'count': 0,
                    'scores': []
                }
            class_scores[class_id]['total_score'] += row[2]
            class_scores[class_id]['count'] += 1
            class_scores[class_id]['scores'].append(row[2])  # 添加成绩

        # 计算每个班级的平均分、最高分和最低分
        class_average_scores = {}
        class_high_low_scores = {}

        for class_id, score_data in class_scores.items():
            average_score = score_data['total_score'] / score_data['count'] if score_data['count'] > 0 else 0
            highest_score = max(score_data['scores']) if score_data['scores'] else 0
            lowest_score = min(score_data['scores']) if score_data['scores'] else 0

            class_average_scores[class_id] = average_score
            class_high_low_scores[class_id] = (average_score, highest_score, lowest_score)

    except Exception as e:
        print(f"查询班级学生成绩失败: {e}")
    finally:
        cursor.close()
        connection.close()

    return grades, class_average_scores, class_high_low_scores
class TeacherInfoWindow(QtWidgets.QWidget):
    def __init__(self, teacher_info):
        super().__init__()
        self.teacher_info = teacher_info
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("教师信息")
        self.resize(800, 600)
        layout = QtWidgets.QVBoxLayout()

        # 显示教师信息
        self.teacherIDLabel = QtWidgets.QLabel(f"教师ID: {self.teacher_info[0]}")
        self.teacherNameLabel = QtWidgets.QLabel(f"教师姓名: {self.teacher_info[1]}")
        self.titleLabel = QtWidgets.QLabel(f"职称: {self.teacher_info[2]}")

        layout.addWidget(self.teacherIDLabel)
        layout.addWidget(self.teacherNameLabel)
        layout.addWidget(self.titleLabel)

        # 查询所授课程按钮
        self.queryCoursesButton = QtWidgets.QPushButton("查询所授课程", self)
        self.queryCoursesButton.clicked.connect(self.query_courses)
        layout.addWidget(self.queryCoursesButton)

        # 修改密码按钮
        self.changePasswordButton = QtWidgets.QPushButton("修改密码", self)
        self.changePasswordButton.clicked.connect(self.change_password)
        layout.addWidget(self.changePasswordButton)

        self.setLayout(layout)

    def query_courses(self):
        courses = get_teacher_courses(self.teacher_info[0])
        courses_dialog = QtWidgets.QDialog(self)
        courses_dialog.setWindowTitle("所授课程")
        courses_dialog.resize(800, 500)

        courses_table = QtWidgets.QTableWidget(courses_dialog)
        courses_table.setColumnCount(3)  # 列：课程ID, 课程名称, 操作
        courses_table.setHorizontalHeaderLabels(["课程ID", "课程名称", "操作"])

        courses_table.setRowCount(len(courses))
        for row_index, course in enumerate(courses):
            courses_table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(course['CourseID'])))
            courses_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(course['CourseName']))

            # 使用 partial 绑定课程ID，解决 lambda 的问题
            view_grades_button = QtWidgets.QPushButton('查看学生成绩')
            view_grades_button.clicked.connect(partial(self.view_students_grades, course_id=course['CourseID']))
            courses_table.setCellWidget(row_index, 2, view_grades_button)

        courses_layout = QtWidgets.QVBoxLayout(courses_dialog)
        courses_layout.addWidget(courses_table)
        courses_dialog.setLayout(courses_layout)

        courses_dialog.exec_()

    def add_student_grade(self):
        try:
            student_id, ok1 = QtWidgets.QInputDialog.getText(self, '添加成绩', '请输入学生ID:')
            if ok1 and student_id:
                # 检查学生是否存在
                if not check_student_exists(student_id):
                    QtWidgets.QMessageBox.warning(self, "错误", f"学生ID {student_id} 不存在！")
                    return

                # 获取该学生的班级ID
                student_class_id = self.get_student_class_id(student_id)  # 确保只传递一个参数
                print(f"学生 {student_id} 的班级ID: {student_class_id}")

                if student_class_id is None:
                    QtWidgets.QMessageBox.warning(self, "错误", f"无法获取学生 {student_id} 的班级信息！")
                    return

                # 检查课程的班级ID是否匹配
                if not self.is_class_id_valid_for_course(self.current_course_id, student_class_id):
                    QtWidgets.QMessageBox.warning(self, "错误", f"学生ID {student_id} 不在您所教的班级下！")
                    return

                # 检查是否已有成绩记录
                if check_student_grade_exists(self.current_course_id, student_id):
                    QtWidgets.QMessageBox.warning(self, "错误", f"学生ID {student_id} 在该课程下的成绩已存在！")
                    return

                # 获取成绩
                score, ok2 = QtWidgets.QInputDialog.getInt(self, '添加成绩', f'请输入学生 {student_id} 的成绩:', 0, 0,
                                                           100)
                if ok2:
                    if add_student_grade(self.current_course_id, student_id, score):
                        QtWidgets.QMessageBox.information(self, "成功", "成绩添加成功！")
                        self.view_students_grades(self.current_course_id)
                    else:
                        QtWidgets.QMessageBox.critical(self, "错误", "成绩添加失败！")
        except Exception as e:
            print(f"发生异常: {e}")  # 输出异常信息

    def get_student_class_id(self,student_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT ClassID FROM Students WHERE StudentID = %s", (student_id,))
            class_id = cursor.fetchone()
            return class_id[0] if class_id else None
        except Exception as e:
            print(f"获取班级ID失败: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    def is_class_id_valid_for_course(self, course_id, class_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM Classes 
                WHERE CourseID = %s AND ClassID = %s AND TeacherID = %s
            """, (course_id, class_id, self.teacher_info[0]))  # 使用当前教师的ID

            return cursor.fetchone()[0] > 0
        except Exception as e:
            print(f"检查班级是否在课程下失败: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
    def view_students_grades(self, course_id):
        self.current_course_id = course_id  # 记住当前课程ID
        try:
            # 获取成绩数据和班级的平均分、最高分和最低分
            grades, class_average_scores, class_high_low_scores = get_class_students_grades(course_id,
                                                                                            self.teacher_info[0])
            print(f"获取到的成绩: {grades}")  # 调试信息

            grades_dialog = QtWidgets.QDialog(self)
            grades_dialog.setWindowTitle("学生成绩")
            grades_dialog.resize(1300, 600)

            grades_table = QtWidgets.QTableWidget(grades_dialog)
            grades_table.setColumnCount(6)  # 学生ID, 学生姓名, 成绩, 班级ID, 更改, 删除
            grades_table.setHorizontalHeaderLabels(["学生ID", "学生姓名", "成绩", "班级ID", "更改", "删除"])

            if not grades:
                QtWidgets.QMessageBox.warning(self, "信息", "没有找到该课程的学生成绩！")
                return

            grades_table.setRowCount(len(grades))

            for row_index, grade in enumerate(grades):
                grades_table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(grade['StudentID'])))
                grades_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(grade['StudentName']))
                grades_table.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(grade['Score'])))
                grades_table.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(grade['ClassID'])))

                # 添加更改按钮
                change_button = QtWidgets.QPushButton('更改')
                change_button.clicked.connect(
                    lambda _: self.show_change_student_grade_dialog(row_index,course_id,grades_table))
                grades_table.setCellWidget(row_index, 4, change_button)

                # 添加删除按钮
                delete_button = QtWidgets.QPushButton('删除')
                delete_button.clicked.connect(
                    lambda _, student_id=grade['StudentID']: self.delete_student_grade(course_id, student_id,
                                                                                       grades_table))
                grades_table.setCellWidget(row_index, 5, delete_button)

            grades_layout = QtWidgets.QVBoxLayout(grades_dialog)
            grades_layout.addWidget(grades_table)

            # 班级成绩信息显示
            class_scores_text = "班级成绩信息: \n" + ' \n'.join(
                f"班级ID {class_id}: 平均分: {average:.2f}, 最高分: {high}, 最低分: {low}"
                for class_id, (average, high, low) in class_high_low_scores.items()
            )

            class_scores_label = QtWidgets.QLabel(class_scores_text, grades_dialog)
            grades_layout.addWidget(class_scores_label)  # 添加班级成绩信息标签

            # 添加“添加成绩”按钮
            add_grade_button = QtWidgets.QPushButton("添加成绩")
            add_grade_button.clicked.connect(self.add_student_grade)
            grades_layout.addWidget(add_grade_button)

            grades_dialog.setLayout(grades_layout)

            grades_dialog.exec_()

        except Exception as e:
            print(f"发生异常: {e}")
            QtWidgets.QMessageBox.critical(self, "错误", f"发生错误: {e}")

    def show_change_student_grade_dialog(self, row,course_id,grades_table):
        try:
            student_id=grades_table.item(row,0).text()
            # 打开对话框以获取新成绩
            score, ok = QtWidgets.QInputDialog.getInt(
                self,
                "更改成绩",
                f"请输入学生 {student_id} 的新成绩:",
                value=int(grades_table.item(row,2).text()),
                min=0,
                max=100
            )

            if ok:  # 如果用户点击了确认
                if self.update_student_grade(course_id, student_id, score):  # 更新成绩的函数
                    QtWidgets.QMessageBox.information(self, "成功", "成绩修改成功！")
                    self.view_students_grades(course_id)  # 刷新显示
                else:
                    QtWidgets.QMessageBox.critical(self, "错误", "成绩修改失败！")
        except Exception as e:
            print(f'{e}')
    def update_student_grade(self,course_id, student_id, new_score):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            # 更新成绩的 SQL 语句
            update_query = """
            UPDATE Grades 
            SET Score = %s 
            WHERE StudentID = %s AND CourseID = %s
            """
            cursor.execute(update_query, (new_score, student_id, course_id))
            connection.commit()  # 提交事务
            return True  # 成功
        except Exception as e:
            print(f"更新成绩失败: {e}")
            return False  # 失败
        finally:
            cursor.close()
            connection.close()

    def delete_student_grade(self, course_id, student_id, grades_table):
        reply = QtWidgets.QMessageBox.question(self, '确认删除', f'确定要删除学生ID {student_id} 的成绩吗？',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            if delete_student_grade(course_id, student_id):
                row = grades_table.currentRow()  # 获取当前选中行
                grades_table.removeRow(row)  # 从表格中删除这一行
                QtWidgets.QMessageBox.information(self, "成功", "成绩删除成功。")
                grades_table.parent().close()  # 关闭grades_table关联的对话框
                # 刷新成绩并显示平均分
                self.view_students_grades(course_id)  # 刷新显示
            else:
                QtWidgets.QMessageBox.critical(self, "错误", "成绩删除失败。")

    def change_password(self):
        old_password, ok = QtWidgets.QInputDialog.getText(self, '输入旧密码', '请输入旧密码:',
                                                          QtWidgets.QLineEdit.Password)
        if ok and old_password:
            if not self.verify_old_password(self.teacher_info[0], old_password):
                QtWidgets.QMessageBox.critical(self, "失败", "旧密码错误！")
                return

            new_password, ok = QtWidgets.QInputDialog.getText(self, '输入新密码', '请输入新密码:',
                                                              QtWidgets.QLineEdit.Password)
            if ok and new_password:
                confirm_password, ok = QtWidgets.QInputDialog.getText(self, '确认新密码', '请再次输入新密码:',
                                                                      QtWidgets.QLineEdit.Password)
                if ok and confirm_password:
                    if new_password != confirm_password:
                        QtWidgets.QMessageBox.warning(self, "失败", "两次输入的新密码不匹配！")
                        return

                    if self.update_password(self.teacher_info[0], new_password):
                        QtWidgets.QMessageBox.information(self, "成功", "密码修改成功。")
                    else:
                        QtWidgets.QMessageBox.critical(self, "失败", "密码修改失败。")

    def verify_old_password(self, teacher_id, old_password):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            query = "SELECT TeacherID FROM Teachers WHERE TeacherID = %s AND password = %s"
            cursor.execute(query, (teacher_id, old_password))
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"检查旧密码失败: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    def update_password(self, teacher_id, new_password):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            query = "UPDATE Teachers SET password = %s WHERE TeacherID = %s"
            cursor.execute(query, (new_password, teacher_id))
            connection.commit()  # 提交更改
            return True
        except Exception as e:
            print(f"修改密码失败: {e}")
            return False
        finally:
            cursor.close()
            connection.close()


class TopStudentsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("班级课程最高分学生")
        self.setGeometry(100, 100, 800, 600)
        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)

        # 创建表格
        self.top_students_table = QtWidgets.QTableWidget(self)
        self.top_students_table.setColumnCount(4)  # 四列: 班级ID, 课程名称, 学生姓名, 分数
        self.top_students_table.setHorizontalHeaderLabels(["班级ID", "课程名称", "学生姓名", "分数"])

        layout.addWidget(self.top_students_table)

        # 获取数据并填充表格
        top_students = self.get_top_students()
        self.fill_table(top_students)

    def get_top_students(self):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            query = '''
         select
  cl.ClassID,c.CourseName,StudentName,Score
from
  Courses c,Students s,Classes cl,Grades g
where
  c.CourseID=cl.CourseID and cl.ClassID=s.ClassID and s.StudentID=g.StudentID and c.CourseID=g.CourseID and
  Score =
             (select max(Score)
			  from
			    Courses c2,Classes cl2,Grades g2,Students s2
			  where
			    c2.CourseID=cl2.CourseID and cl2.ClassID=s2.ClassID and s2.StudentID=g2.StudentID and c2.CourseID=g2.CourseID
				and s2.ClassID=s.ClassID and c2.CourseName=c.CourseName)
order by
  s.ClassID


            '''

            cursor.execute(query)

            # 获取查询结果
            top_students = cursor.fetchall()
            return top_students

        except Exception as e:
            print(f"获取最高分学生时出错: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    def fill_table(self, top_students):
        self.top_students_table.setRowCount(len(top_students))
        for row_index, student in enumerate(top_students):
            self.top_students_table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(student[0])))  # ClassID
            self.top_students_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(student[1]))  # CourseName
            self.top_students_table.setItem(row_index, 2, QtWidgets.QTableWidgetItem(student[2]))  # StudentName
            self.top_students_table.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(student[3])))  # Score


class AdminManagementWindow(QtWidgets.QWidget):
    def __init__(self, admin_info):
        super().__init__()
        self.admin_info = admin_info
        self.setupUi()

    def setupUi(self):
        self.setObjectName("AdminManagementWindow")
        self.resize(800, 600)
        self.setWindowTitle("管理员管理界面")
        self.setStyleSheet("background: #f0f0f0;")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(20)

        self.titleLabel = QtWidgets.QLabel(f"欢迎，{self.admin_info[1]}!", self)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont("Helvetica", 24, QtGui.QFont.Bold)
        self.titleLabel.setFont(font)
        self.layout.addWidget(self.titleLabel)

        self.managementButtonLayout = QtWidgets.QHBoxLayout()

        # 创建管理按钮
        self.create_management_buttons()

        self.layout.addLayout(self.managementButtonLayout)
        self.setLayout(self.layout)

    def create_management_buttons(self):
        buttons = {
            "管理学生信息": self.manage_students,
            "管理教师信息": self.manage_teachers,
            "管理课程信息": self.manage_courses,
            "管理授课信息": self.manage_classes,
            "管理成绩信息": self.manage_grades,
            "管理最高分信息": self.manage_top_students,  # 添加最高分管理的方法
            "退出系统": self.logout
        }

        for button_text, method in buttons.items():
            button = QtWidgets.QPushButton(button_text, self)
            button.setFixedSize(200, 100)  # 设置固定大小
            button.setStyleSheet("""
                QPushButton {
                    font-size: 25px;
                    background-color: #4CAF50; 
                    color: white; 
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            button.clicked.connect(method)  # 连接信号到对应方法
            self.managementButtonLayout.addWidget(button)

    def manage_students(self):
        self.student_management_window = StudentManagementWindow()
        self.student_management_window.show()

    def manage_teachers(self):
        self.teacher_management_window = TeacherManagementWindow()
        self.teacher_management_window.show()

    def manage_courses(self):
        self.course_management_window = CourseManagementWindow()
        self.course_management_window.show()

    def manage_classes(self):
        self.class_management_window = ClassesManagementWindow()
        self.class_management_window.show()

    def manage_grades(self):
        self.grade_management_window = GradesManagementWindow()
        self.grade_management_window.show()

    def manage_top_students(self):
        self.top_student_management_window = TopStudentsWindow()  # 打开最高分管理窗口
        self.top_student_management_window.show()

    def logout(self):
        self.close()  # 关闭管理员管理界面
        login_window = LoginWindow()  # 假设你有一个登录窗口
        login_window.show()


class StudentManagementWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("StudentManagementWindow")
        self.resize(1300, 600)
        self.setWindowTitle("学生信息管理")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setColumnCount(6)  # 4列学生信息 + 3列操作按钮
        self.tableWidget.setHorizontalHeaderLabels(["学生ID", "学生姓名", "班级","用户名" ,"更改", "删除"])
        self.layout.addWidget(self.tableWidget)

        self.setLayout(self.layout)

        # 添加学生按钮
        self.add_button = QtWidgets.QPushButton("添加学生", self)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                border-radius: 5px;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.show_add_student_dialog)

        self.load_student_data()

    def load_student_data(self):
        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()
        cursor.execute("SELECT StudentID, StudentName, ClassID,username FROM Students")

        rows = cursor.fetchall()  # 获取所有学生数据
        self.tableWidget.setRowCount(len(rows))  # 设置表格行数

        for row_index, row_data in enumerate(rows):
            self.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(row_data[0])))
            self.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(row_data[1])))
            self.tableWidget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(row_data[2])))
            self.tableWidget.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(row_data[3])))

            # 创建“更改”按钮
            change_button = QtWidgets.QPushButton('更改')
            change_button.clicked.connect(
                lambda _, row=row_index: self.show_change_student_dialog(row))
            self.tableWidget.setCellWidget(row_index, 4, change_button)

            # 创建“删除”按钮
            delete_button = QtWidgets.QPushButton('删除')
            delete_button.clicked.connect(lambda _, row=row_index: self.delete_student(row))
            self.tableWidget.setCellWidget(row_index, 5, delete_button)

        cursor.close()
        connection.close()

    def show_add_student_dialog(self):
        """显示添加学生的输入对话框"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("添加学生")
        dialog.setFixedSize(400, 300)

        layout = QtWidgets.QVBoxLayout(dialog)

        self.id_input = QtWidgets.QLineEdit(dialog)
        self.id_input.setPlaceholderText("学生ID")
        self.id_input.textChanged.connect(self.check_student_id_unique)  # 连接ID输入变化信号
        layout.addWidget(self.id_input)

        self.name_input = QtWidgets.QLineEdit(dialog)
        self.name_input.setPlaceholderText("学生姓名")
        layout.addWidget(self.name_input)

        self.class_input = QtWidgets.QLineEdit(dialog)
        self.class_input.setPlaceholderText("班级ID(1-9)")
        self.class_input.textChanged.connect(self.on_class_text_changed)
        layout.addWidget(self.class_input)

        self.username_input = QtWidgets.QLineEdit(dialog)
        self.username_input.setPlaceholderText("用户名")
        layout.addWidget(self.username_input)

        self.password_input = QtWidgets.QLineEdit(dialog)
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.confirm_button = QtWidgets.QPushButton("添加", dialog)
        self.confirm_button.clicked.connect(self.add_student)
        layout.addWidget(self.confirm_button)

        dialog.exec_()  # 显示对话框并等待用户输入

    def on_class_text_changed(self):
        class_id = self.class_input.text().strip()
        if class_id:
            if not class_id.isdigit() or not (1 <= int(class_id) <= 9):
                QtWidgets.QMessageBox.warning(self, "输入错误", "班级ID必须是1到9之间的数字。")
                self.class_input.clear()  # 清空无效输入
    def show_change_student_dialog(self, row):
        """显示更改学生信息的输入对话框"""
        student_id = self.tableWidget.item(row, 0).text()
        student_name = self.tableWidget.item(row, 1).text()
        class_id = self.tableWidget.item(row, 2).text()
        student_username=self.tableWidget.item(row, 3).text()

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("更改学生信息")
        dialog.setFixedSize(400, 300)

        layout = QtWidgets.QVBoxLayout(dialog)

        self.change_id_input = QtWidgets.QLineEdit(dialog)
        self.change_id_input.setPlaceholderText("学生ID")
        self.change_id_input.setText(student_id)
        self.change_id_input.setEnabled(False)  # 禁用编辑学生ID
        layout.addWidget(self.change_id_input)

        self.change_name_input = QtWidgets.QLineEdit(dialog)
        self.change_name_input.setPlaceholderText("学生姓名")
        self.change_name_input.setText(student_name)
        layout.addWidget(self.change_name_input)

        self.change_class_input = QtWidgets.QLineEdit(dialog)
        self.change_class_input.setPlaceholderText("班级ID(1-9)")
        self.change_class_input.setText(class_id)
        self.change_class_input.textChanged.connect(self.validate_class_id)  # 连接文本变化信号
        layout.addWidget(self.change_class_input)

        self.change_username_input = QtWidgets.QLineEdit(dialog)
        self.change_username_input.setPlaceholderText("用户名")
        self.change_username_input.setText(student_username)
        layout.addWidget(self.change_username_input)

        self.change_password_input = QtWidgets.QLineEdit(dialog)
        self.change_password_input.setPlaceholderText("密码（可留空）")
        self.change_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.change_password_input)

        self.confirm_button = QtWidgets.QPushButton("更改", dialog)
        self.confirm_button.clicked.connect(lambda: self.update_student(row))
        layout.addWidget(self.confirm_button)

        dialog.exec_()  # 显示对话框并等待用户输入

    def validate_class_id(self, text):
        """验证班级ID是否在1-9之间"""
        if text and not text.isdigit():
            QtWidgets.QMessageBox.warning(self, "输入错误", "班级ID必须是数字。")
            self.change_class_input.clear()  # 清空输入框
        elif text and (int(text) < 1 or int(text) > 9):
            QtWidgets.QMessageBox.warning(self, "输入错误", "班级ID必须在1-9之间。")
            self.change_class_input.clear()  # 清空输入框

    def update_student(self, row):
        """更新学生信息"""
        student_id = self.change_id_input.text().strip()  # ID不可更改
        student_name = self.change_name_input.text().strip()
        class_id = self.change_class_input.text().strip()
        username = self.change_username_input.text().strip()
        password = self.change_password_input.text().strip()  # 允许留空

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()

        try:
            # 更新学生信息
            if password:  # 如果提供了新密码，则更新密码
                cursor.execute(
                    "UPDATE Students SET StudentName = %s, ClassID = %s, username = %s, password = %s WHERE StudentID = %s",
                    (student_name, class_id, username, password, student_id))
            else:  # 如果没有提供新密码，则不更新密码
                cursor.execute(
                    "UPDATE Students SET StudentName = %s, ClassID = %s, username = %s WHERE StudentID = %s",
                    (student_name, class_id, username, student_id))
            connection.commit()  # 提交更改
            QtWidgets.QMessageBox.information(self, "更改成功", "学生信息已成功更新。")
            self.load_student_data()  # 重新加载数据以更新表格
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "数据库错误", str(e))
            print(f"数据库错误: {e}")
        finally:
            cursor.close()
            connection.close()

    def check_student_id_unique(self):
        """检查学生ID的唯一性"""
        student_id = self.id_input.text().strip()

        if not student_id:  # 输入为空则不进行检查
            self.enable_input(True)
            return

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Students WHERE StudentID = %s", (student_id,))
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if count > 0:  # 如果已存在该 ID
            QtWidgets.QMessageBox.warning(self, "唯一性检查", "学生ID已存在，请使用其他ID。")
            self.enable_input(False)  # 禁用输入框
        else:
            self.enable_input(True)  # 允许输入框

    def enable_input(self, enabled):
        """启用或禁用输入框"""
        self.name_input.setEnabled(enabled)
        self.class_input.setEnabled(enabled)
        self.username_input.setEnabled(enabled)
        self.password_input.setEnabled(enabled)

    def add_student(self):
        """添加新学生到数据库"""
        student_id = self.id_input.text().strip()  # 获取输入的学生ID

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Students WHERE StudentID = %s", (student_id,))
        count = cursor.fetchone()[0]

        if count > 0:  # 如果已存在该 ID
            QtWidgets.QMessageBox.warning(self, "唯一性检查", "学生ID已存在，请使用其他ID。")
            cursor.close()
            connection.close()
            return

        student_name = self.name_input.text().strip()  # 获取输入的学生姓名
        class_id = self.class_input.text().strip()  # 获取输入的班级
        username = self.username_input.text().strip()  # 获取输入的用户名
        password = self.password_input.text().strip()  # 获取输入的密码

        try:
            # 插入新学生信息
            cursor.execute(
                "INSERT INTO Students (StudentID, StudentName, ClassID, username, password) VALUES (%s, %s, %s, %s, %s)",
                (student_id, student_name, class_id, username, password))
            connection.commit()  # 提交更改
            QtWidgets.QMessageBox.information(self, "添加成功", "学生信息已成功添加。")
            self.load_student_data()  # 重新加载数据以更新表格
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "数据库错误", str(e))
            print(f"数据库错误: {e}")
        finally:
            cursor.close()
            connection.close()

        # 清空输入框
        self.id_input.clear()
        self.name_input.clear()
        self.class_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.enable_input(True)  # 重新启用输入框

    def delete_student(self, row):
        student_id = self.tableWidget.item(row, 0).text()

        reply = QtWidgets.QMessageBox.question(self, '确认删除', f'您确定要删除学生ID为 {student_id} 的记录吗?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            connection = get_db_connection()
            if not connection:
                return  # 连接失败则返回

            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM Students WHERE StudentID = %s", (student_id,))
                connection.commit()
                self.load_student_data()  # 重新加载数据以更新表格
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "数据库错误", str(e))
                print(f"数据库错误: {e}")
            finally:
                cursor.close()
                connection.close()

class TeacherManagementWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("TeacherManagementWindow")
        self.resize(1300, 600)
        self.setWindowTitle("教师信息管理")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setColumnCount(6)  # 4列教师信息 + 2列操作按钮
        self.tableWidget.setHorizontalHeaderLabels(["教师ID", "教师姓名", "职称", "用户名", "更改", "删除"])
        self.layout.addWidget(self.tableWidget)

        self.setLayout(self.layout)

        # 添加教师按钮
        self.add_button = QtWidgets.QPushButton("添加教师", self)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                border-radius: 5px;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.show_add_teacher_dialog)

        self.load_teacher_data()

    def load_teacher_data(self):
        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()
        cursor.execute("SELECT TeacherID, TeacherName, Title, username FROM Teachers")

        rows = cursor.fetchall()  # 获取所有教师数据
        self.tableWidget.setRowCount(len(rows))  # 设置表格行数

        for row_index, row_data in enumerate(rows):
            self.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(row_data[0])))
            self.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(row_data[1])))
            self.tableWidget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(row_data[2])))
            self.tableWidget.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(row_data[3])))

            # 创建“更改”按钮
            change_button = QtWidgets.QPushButton('更改')
            change_button.clicked.connect(
                lambda _,row=row_index: self.show_change_teacher_dialog(row))
            self.tableWidget.setCellWidget(row_index, 4, change_button)

            # 创建“删除”按钮
            delete_button = QtWidgets.QPushButton('删除')
            delete_button.clicked.connect(lambda _, row=row_index: self.delete_teacher(row))
            self.tableWidget.setCellWidget(row_index, 5, delete_button)

        cursor.close()
        connection.close()

    def show_add_teacher_dialog(self):
        """显示添加教师的输入对话框"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("添加教师")
        dialog.setFixedSize(400, 300)

        layout = QtWidgets.QVBoxLayout(dialog)

        self.id_input = QtWidgets.QLineEdit(dialog)
        self.id_input.setPlaceholderText("教师ID")
        self.id_input.textChanged.connect(self.check_teacher_id_unique)  # 连接ID输入变化信号
        layout.addWidget(self.id_input)

        self.name_input = QtWidgets.QLineEdit(dialog)
        self.name_input.setPlaceholderText("教师姓名")
        layout.addWidget(self.name_input)

        self.title_input = QtWidgets.QLineEdit(dialog)
        self.title_input.setPlaceholderText("职称")
        layout.addWidget(self.title_input)

        self.username_input = QtWidgets.QLineEdit(dialog)
        self.username_input.setPlaceholderText("用户名")
        layout.addWidget(self.username_input)

        self.password_input = QtWidgets.QLineEdit(dialog)
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.confirm_button = QtWidgets.QPushButton("添加", dialog)
        self.confirm_button.clicked.connect(self.add_teacher)
        layout.addWidget(self.confirm_button)

        dialog.exec_()  # 显示对话框并等待用户输入

    def show_change_teacher_dialog(self, row):
        """显示更改教师信息的输入对话框"""
        teacher_id = self.tableWidget.item(row, 0).text()
        teacher_name = self.tableWidget.item(row, 1).text()
        title = self.tableWidget.item(row, 2).text()
        username = self.tableWidget.item(row, 3).text()

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("更改教师信息")
        dialog.setFixedSize(400, 300)

        layout = QtWidgets.QVBoxLayout(dialog)

        self.change_id_input = QtWidgets.QLineEdit(dialog)
        self.change_id_input.setPlaceholderText("教师ID")
        self.change_id_input.setText(teacher_id)
        self.change_id_input.setEnabled(False)  # 禁用编辑教师ID
        layout.addWidget(self.change_id_input)

        self.change_name_input = QtWidgets.QLineEdit(dialog)
        self.change_name_input.setPlaceholderText("教师姓名")
        self.change_name_input.setText(teacher_name)
        layout.addWidget(self.change_name_input)

        self.change_title_input = QtWidgets.QLineEdit(dialog)
        self.change_title_input.setPlaceholderText("职称")
        self.change_title_input.setText(title)
        layout.addWidget(self.change_title_input)

        self.change_username_input = QtWidgets.QLineEdit(dialog)
        self.change_username_input.setPlaceholderText("用户名")
        self.change_username_input.setText(username)
        layout.addWidget(self.change_username_input)

        self.change_password_input = QtWidgets.QLineEdit(dialog)
        self.change_password_input.setPlaceholderText("密码（可留空）")
        self.change_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.change_password_input)

        self.confirm_button = QtWidgets.QPushButton("更改", dialog)
        self.confirm_button.clicked.connect(lambda: self.update_teacher())
        layout.addWidget(self.confirm_button)

        dialog.exec_()  # 显示对话框并等待用户输入

    def update_teacher(self):
        """更新教师信息"""
        teacher_id = self.change_id_input.text().strip()  # ID不可更改
        teacher_name = self.change_name_input.text().strip()
        title = self.change_title_input.text().strip()
        username = self.change_username_input.text().strip()
        password = self.change_password_input.text().strip()  # 允许留空

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()

        try:
            # 更新教师信息
            if password:  # 如果提供了新密码，则更新密码
                cursor.execute(
                    "UPDATE Teachers SET TeacherName = %s, Title = %s, username = %s, password = %s WHERE TeacherID = %s",
                    (teacher_name, title, username, password, teacher_id))
            else:  # 如果没有提供新密码，则不更新密码
                cursor.execute(
                    "UPDATE Teachers SET TeacherName = %s, Title = %s, username = %s WHERE TeacherID = %s",
                    (teacher_name, title, username, teacher_id))
            connection.commit()  # 提交更改
            QtWidgets.QMessageBox.information(self, "更改成功", "教师信息已成功更新。")
            self.load_teacher_data()  # 重新加载数据以更新表格
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "数据库错误", str(e))
            print(f"数据库错误: {e}")
        finally:
            cursor.close()
            connection.close()

    def check_teacher_id_unique(self):
        """检查教师ID的唯一性"""
        teacher_id = self.id_input.text().strip()

        if not teacher_id:  # 输入为空则不进行检查
            self.enable_input(True)
            return

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Teachers WHERE TeacherID = %s", (teacher_id,))
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if count > 0:  # 如果已存在该 ID
            QtWidgets.QMessageBox.warning(self, "唯一性检查", "教师ID已存在，请使用其他ID。")
            self.enable_input(False)  # 禁用输入框
        else:
            self.enable_input(True)  # 允许输入框

    def enable_input(self, enabled):
        """启用或禁用输入框"""
        self.name_input.setEnabled(enabled)
        self.title_input.setEnabled(enabled)
        self.username_input.setEnabled(enabled)
        self.password_input.setEnabled(enabled)

    def add_teacher(self):
        """添加新教师到数据库"""
        teacher_id = self.id_input.text().strip()  # 获取输入的教师ID

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Teachers WHERE TeacherID = %s", (teacher_id,))
        count = cursor.fetchone()[0]

        if count > 0:  # 如果已存在该 ID
            QtWidgets.QMessageBox.warning(self, "唯一性检查", "教师ID已存在，请使用其他ID。")
            cursor.close()
            connection.close()
            return

        teacher_name = self.name_input.text().strip()  # 获取输入的教师姓名
        title = self.title_input.text().strip()  # 获取输入的职称
        username = self.username_input.text().strip()  # 获取输入的用户名
        password = self.password_input.text().strip()  # 获取输入的密码

        try:
            # 插入新教师信息
            cursor.execute(
                "INSERT INTO Teachers (TeacherID, TeacherName, Title, username, password) VALUES (%s, %s, %s, %s, %s)",
                (teacher_id, teacher_name, title, username, password))
            connection.commit()  # 提交更改
            QtWidgets.QMessageBox.information(self, "添加成功", "教师信息已成功添加。")
            self.load_teacher_data()  # 重新加载数据以更新表格
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "数据库错误", str(e))
            print(f"数据库错误: {e}")
        finally:
            cursor.close()
            connection.close()

        # 清空输入框
        self.id_input.clear()
        self.name_input.clear()
        self.title_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.enable_input(True)  # 重新启用输入框

    def delete_teacher(self, row):
        teacher_id = self.tableWidget.item(row, 0).text()

        reply = QtWidgets.QMessageBox.question(self, '确认删除', f'您确定要删除教师ID为 {teacher_id} 的记录吗?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            connection = get_db_connection()
            if not connection:
                return  # 连接失败则返回

            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM Teachers WHERE TeacherID = %s", (teacher_id,))
                connection.commit()
                self.load_teacher_data()  # 重新加载数据以更新表格
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "数据库错误", str(e))
                print(f"数据库错误: {e}")
            finally:
                cursor.close()
                connection.close()

class CourseManagementWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("CourseManagementWindow")
        self.resize(1300, 400)
        self.setWindowTitle("课程信息管理")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setColumnCount(6)  # 课程信息 + 选课人数 + 操作按钮
        self.tableWidget.setHorizontalHeaderLabels(["课程ID", "课程名称", "学分", "选课人数", "更改", "删除"])
        self.layout.addWidget(self.tableWidget)

        self.setLayout(self.layout)

        # 添加课程按钮
        self.add_button = QtWidgets.QPushButton("添加课程", self)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                border-radius: 5px;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.show_add_course_dialog)

        self.load_course_data()

    def load_course_data(self):
        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()
        # 获取每门课程的信息以及对应的选课人数
        cursor.execute("""
            SELECT Courses.CourseID, Courses.CourseName, Courses.Credit, 
                   COUNT(Grades.StudentID) AS StudentCount
            FROM Courses
            LEFT JOIN Grades ON Courses.CourseID = Grades.CourseID
            GROUP BY Courses.CourseID, Courses.CourseName, Courses.Credit
        """)

        rows = cursor.fetchall()  # 获取所有课程数据
        self.tableWidget.setRowCount(len(rows))  # 设置表格行数

        for row_index, row_data in enumerate(rows):
            self.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(row_data[0])))
            self.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(row_data[1])))
            self.tableWidget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(row_data[2])))
            self.tableWidget.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(row_data[3])))  # 选课人数

            # 创建“更改”按钮
            change_button = QtWidgets.QPushButton('更改')
            change_button.clicked.connect(
                lambda _, row=row_index: self.show_change_course_dialog(row))
            self.tableWidget.setCellWidget(row_index, 4, change_button)

            # 创建“删除”按钮
            delete_button = QtWidgets.QPushButton('删除')
            delete_button.clicked.connect(lambda _, row=row_index: self.delete_course(row))
            self.tableWidget.setCellWidget(row_index, 5, delete_button)  # 修改列索引为5

        cursor.close()
        connection.close()
    def show_add_course_dialog(self):
        """显示添加课程的输入对话框"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("添加课程")
        dialog.setFixedSize(400, 250)

        layout = QtWidgets.QVBoxLayout(dialog)

        self.course_id_input = QtWidgets.QLineEdit(dialog)
        self.course_id_input.setPlaceholderText("课程ID")
        self.course_id_input.textChanged.connect(self.check_course_id_unique)  # 连接ID变化信号
        layout.addWidget(self.course_id_input)

        self.course_name_input = QtWidgets.QLineEdit(dialog)
        self.course_name_input.setPlaceholderText("课程名称")
        layout.addWidget(self.course_name_input)

        self.credit_input = QtWidgets.QLineEdit(dialog)
        self.credit_input.setPlaceholderText("学分")
        layout.addWidget(self.credit_input)

        self.confirm_button = QtWidgets.QPushButton("添加", dialog)
        self.confirm_button.clicked.connect(self.add_course)
        layout.addWidget(self.confirm_button)

        dialog.exec_()  # 显示对话框并等待用户输入

    def check_course_id_unique(self):
        """检查课程ID的唯一性"""
        course_id = self.course_id_input.text().strip()

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Courses WHERE CourseID = %s", (course_id,))
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if count > 0:  # 如果已存在该 ID
            QtWidgets.QMessageBox.warning(self, "唯一性检查", "课程ID已存在，请使用其他ID。")
            self.enable_input(False)  # 禁用输入框
        else:
            self.enable_input(True)  # 允许输入框

    def enable_input(self, enabled):
        """启用或禁用输入框"""
        self.course_name_input.setEnabled(enabled)
        self.credit_input.setEnabled(enabled)

    def show_change_course_dialog(self, row):
        """显示更改课程信息的输入对话框"""
        course_id = self.tableWidget.item(row, 0).text()
        course_name = self.tableWidget.item(row, 1).text()
        credit = self.tableWidget.item(row, 2).text()

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("更改课程信息")
        dialog.setFixedSize(400, 250)

        layout = QtWidgets.QVBoxLayout(dialog)

        self.change_course_id_input = QtWidgets.QLineEdit(dialog)
        self.change_course_id_input.setPlaceholderText("课程ID")
        self.change_course_id_input.setText(course_id)
        self.change_course_id_input.setEnabled(False)  # 禁用编辑课程ID
        layout.addWidget(self.change_course_id_input)

        self.change_course_name_input = QtWidgets.QLineEdit(dialog)
        self.change_course_name_input.setPlaceholderText("课程名称")
        self.change_course_name_input.setText(course_name)
        layout.addWidget(self.change_course_name_input)

        self.change_credit_input = QtWidgets.QLineEdit(dialog)
        self.change_credit_input.setPlaceholderText("学分")
        self.change_credit_input.setText(credit)
        layout.addWidget(self.change_credit_input)

        self.confirm_change_button = QtWidgets.QPushButton("更改", dialog)
        self.confirm_change_button.clicked.connect(lambda: self.update_course(row))
        layout.addWidget(self.confirm_change_button)

        dialog.exec_()  # 显示对话框并等待用户输入

    def update_course(self, row):
        """更新课程信息"""
        course_id = self.change_course_id_input.text().strip()  # ID不可更改
        course_name = self.change_course_name_input.text().strip()
        credit = self.change_credit_input.text().strip()

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()

        try:
            # 更新课程信息
            cursor.execute(
                "UPDATE Courses SET CourseName = %s, Credit = %s WHERE CourseID = %s",
                (course_name, credit, course_id))
            connection.commit()  # 提交更改
            QtWidgets.QMessageBox.information(self, "更改成功", "课程信息已成功更新。")
            self.load_course_data()  # 重新加载数据以更新表格
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "数据库错误", str(e))
            print(f"数据库错误: {e}")
        finally:
            cursor.close()
            connection.close()

    def add_course(self):
        """添加新课程到数据库"""
        course_id = self.course_id_input.text().strip()  # 获取输入的课程ID

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Courses WHERE CourseID = %s", (course_id,))
        count = cursor.fetchone()[0]

        if count > 0:  # 如果已存在该 ID
            QtWidgets.QMessageBox.warning(self, "唯一性检查", "课程ID已存在，请使用其他ID。")
            cursor.close()
            connection.close()
            return

        course_name = self.course_name_input.text().strip()  # 获取输入的课程名称
        credit = self.credit_input.text().strip()  # 获取输入的学分

        try:
            # 插入新课程信息
            cursor.execute(
                "INSERT INTO Courses (CourseID, CourseName, Credit) VALUES (%s, %s, %s)",
                (course_id, course_name, credit))
            connection.commit()  # 提交更改
            QtWidgets.QMessageBox.information(self, "添加成功", "课程信息已成功添加。")
            self.load_course_data()  # 重新加载数据以更新表格
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "数据库错误", str(e))
            print(f"数据库错误: {e}")
        finally:
            cursor.close()
            connection.close()

        # 清空输入框
        self.course_id_input.clear()
        self.course_name_input.clear()
        self.credit_input.clear()

    def delete_course(self, row):
        course_id = self.tableWidget.item(row, 0).text()

        reply = QtWidgets.QMessageBox.question(self, '确认删除',
                                               f'您确定要删除课程ID为 {course_id} 的记录吗？\n'
                                               '这将删除与该课程相关的所有成绩和班级信息！',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            connection = get_db_connection()
            if not connection:
                return  # 连接失败则返回

            cursor = connection.cursor()
            try:
                # 删除相关信息
                cursor.execute("DELETE FROM Grades WHERE CourseID = %s", (course_id,))
                cursor.execute("DELETE FROM Classes WHERE CourseID = %s", (course_id,))
                # 删除课程
                cursor.execute("DELETE FROM Courses WHERE CourseID = %s", (course_id,))
                connection.commit()
                self.load_course_data()  # 重新加载数据以更新表格
                QtWidgets.QMessageBox.information(self, "删除成功", "课程及其相关信息已成功删除。")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "数据库错误", str(e))
                print(f"数据库错误: {e}")
            finally:
                cursor.close()
                connection.close()

class GradesManagementWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("GradesManagementWindow")
        self.resize(1100, 800)
        self.setWindowTitle("成绩信息管理")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setColumnCount(5)  # 3列成绩信息 + 2列操作按钮
        self.tableWidget.setHorizontalHeaderLabels(["学生ID", "课程ID", "分数", "更改", "删除"])
        self.layout.addWidget(self.tableWidget)

        # 新增显示平均分的部分
        self.average_score_label = QtWidgets.QLabel(self)
        self.average_score_label.setText("各课程平均分: ")
        self.layout.addWidget(self.average_score_label)

        self.setLayout(self.layout)
        # 添加成绩按钮
        self.add_button = QtWidgets.QPushButton("添加成绩", self)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                border-radius: 5px;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.show_add_grade_dialog)

        self.load_grades_data()

    def load_grades_data(self):
        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()

        # 计算每个课程的平均分、最高分和最低分
        cursor.execute("""
            SELECT CourseID, AVG(Score) AS AverageScore, MAX(Score) AS HighestScore, MIN(Score) AS LowestScore
            FROM Grades
            GROUP BY CourseID
        """)

        average_scores = cursor.fetchall()

        # 构建字符串显示平均分、最高分和最低分
        average_score_str = "\n".join(
            [f"课程ID: {row[0]}, 平均分: {row[1]:.2f}, 最高分: {row[2]}, 最低分: {row[3]}" for row in average_scores]
        )

        self.average_score_label.setText(f"各课程成绩信息: \n{average_score_str}")

        # 获取所有成绩数据
        cursor.execute("""
            SELECT StudentID, CourseID, Score 
            FROM Grades
            ORDER BY CourseID ASC, StudentID ASC
        """)

        rows = cursor.fetchall()  # 获取所有成绩数据
        self.tableWidget.setRowCount(len(rows))  # 设置表格行数

        # 填充成绩数据
        for row_index, row_data in enumerate(rows):
            self.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(row_data[0])))  # 学生ID
            self.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(row_data[1])))  # 课程ID
            self.tableWidget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(row_data[2])))  # 分数

            # 创建“更改”按钮
            change_button = QtWidgets.QPushButton('更改')
            change_button.clicked.connect(
                lambda _, row=row_index: self.show_change_grade_dialog(row))
            self.tableWidget.setCellWidget(row_index, 3, change_button)

            # 创建“删除”按钮
            delete_button = QtWidgets.QPushButton('删除')
            delete_button.clicked.connect(lambda _, row=row_index: self.delete_grade(row))
            self.tableWidget.setCellWidget(row_index, 4, delete_button)

        cursor.close()
        connection.close()

    def show_add_grade_dialog(self):
        """显示添加成绩的输入对话框"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("添加成绩")
        dialog.setFixedSize(400, 250)

        layout = QtWidgets.QVBoxLayout(dialog)

        self.student_id_input = QtWidgets.QLineEdit(dialog)
        self.student_id_input.setPlaceholderText("学生ID")
        self.student_id_input.textChanged.connect(self.check_student_id)  # 检查学生ID存在性
        layout.addWidget(self.student_id_input)

        self.course_id_input = QtWidgets.QLineEdit(dialog)
        self.course_id_input.setPlaceholderText("课程ID")
        self.course_id_input.setEnabled(False)  # 初始禁用课程ID输入
        self.course_id_input.textChanged.connect(self.check_course_id)  # 检查课程ID存在性
        layout.addWidget(self.course_id_input)

        self.score_input = QtWidgets.QLineEdit(dialog)
        self.score_input.setPlaceholderText("分数")
        self.score_input.setEnabled(False)  # 初始禁用分数输入
        layout.addWidget(self.score_input)

        self.confirm_button = QtWidgets.QPushButton("添加", dialog)
        self.confirm_button.clicked.connect(self.add_grade)
        layout.addWidget(self.confirm_button)

        dialog.exec_()  # 显示对话框并等待用户输入

    def check_student_id(self):
        """检查学生ID的存在性"""
        student_id = self.student_id_input.text().strip()

        # 检查学生ID
        if student_id:
            connection = get_db_connection()
            if not connection:
                return  # 连接失败则返回

            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Students WHERE StudentID = %s", (student_id,))
            student_exists = cursor.fetchone()[0] > 0
            if not student_exists:
                self.course_id_input.clear()
                self.score_input.clear()  # 停止输入分数
                QtWidgets.QMessageBox.warning(self, "检查学生ID", "该学生ID不存在，无法继续输入课程ID。")
            else:
                self.course_id_input.setEnabled(True)  # 启用课程ID输入框
            cursor.close()
            connection.close()


    def check_course_id(self):
        """检查课程ID的存在性"""
        course_id = self.course_id_input.text().strip()
        student_id = self.student_id_input.text().strip()

        # 检查课程ID
        course_exists = False
        if course_id:
            connection = get_db_connection()
            if not connection:
                return  # 连接失败则返回

            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Courses WHERE CourseID = %s", (course_id,))
            course_exists = cursor.fetchone()[0] > 0
            cursor.close()
            connection.close()

        if not course_exists and course_id:
            self.score_input.setEnabled(False)  # 停止输入分数
            QtWidgets.QMessageBox.warning(self, "检查课程ID", "该课程ID不存在，请确认输入。")
        else:
            self.score_input.setEnabled(True)  # 启用分数输入框

        # 检查StudentID和CourseID组合的唯一性
        if student_id and course_id:
            connection = get_db_connection()
            if not connection:
                return  # 连接失败则返回

            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Grades WHERE StudentID = %s AND CourseID = %s",
                           (student_id, course_id))
            score_exists = cursor.fetchone()[0] > 0
            cursor.close()
            connection.close()

            if score_exists:
                self.score_input.setEnabled(False)  # 停止输入分数
                QtWidgets.QMessageBox.warning(self, "成绩已存在", "该学生在该课程已存在成绩，无法继续输入。")
            else:
                self.score_input.setEnabled(True)  # 可以输入分数

    def show_change_grade_dialog(self, row):
        """显示更改成绩信息的输入对话框"""
        student_id = self.tableWidget.item(row, 0).text()
        course_id = self.tableWidget.item(row, 1).text()
        score = self.tableWidget.item(row, 2).text()

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("更改成绩信息")
        dialog.setFixedSize(400, 250)

        layout = QtWidgets.QVBoxLayout(dialog)

        self.change_student_id_input = QtWidgets.QLineEdit(dialog)
        self.change_student_id_input.setPlaceholderText("学生ID")
        self.change_student_id_input.setText(student_id)
        self.change_student_id_input.setEnabled(False)  # 禁用编辑学生ID
        layout.addWidget(self.change_student_id_input)

        self.change_course_id_input = QtWidgets.QLineEdit(dialog)
        self.change_course_id_input.setPlaceholderText("课程ID")
        self.change_course_id_input.setText(course_id)
        self.change_course_id_input.setEnabled(False)  # 禁用编辑课程ID
        layout.addWidget(self.change_course_id_input)

        self.change_score_input = QtWidgets.QLineEdit(dialog)
        self.change_score_input.setPlaceholderText("分数")
        self.change_score_input.setText(score)
        layout.addWidget(self.change_score_input)

        self.confirm_change_button = QtWidgets.QPushButton("更改", dialog)
        self.confirm_change_button.clicked.connect(lambda: self.update_grade(row))
        layout.addWidget(self.confirm_change_button)

        dialog.exec_()  # 显示对话框并等待用户输入

    def update_grade(self, row):
        """更新成绩信息"""
        student_id = self.change_student_id_input.text().strip()  # ID不可更改
        course_id = self.change_course_id_input.text().strip()  # ID不可更改
        score = self.change_score_input.text().strip()

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()

        try:
            # 更新成绩信息
            cursor.execute(
                "UPDATE Grades SET Score = %s WHERE StudentID = %s AND CourseID = %s",
                (score, student_id, course_id))
            connection.commit()  # 提交更改
            QtWidgets.QMessageBox.information(self, "更改成功", "成绩信息已成功更新。")
            self.load_grades_data()  # 重新加载数据以更新表格
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "数据库错误", str(e))
            print(f"数据库错误: {e}")
        finally:
            cursor.close()
            connection.close()

    def add_grade(self):
        """添加新成绩到数据库"""
        student_id = self.student_id_input.text().strip()  # 获取输入的学生ID
        course_id = self.course_id_input.text().strip()  # 获取输入的课程ID
        score = self.score_input.text().strip()  # 获取输入的分数

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()
        try:
            # 插入新成绩信息
            cursor.execute(
                "INSERT INTO Grades (StudentID, CourseID, Score) VALUES (%s, %s, %s)",
                (student_id, course_id, score))
            connection.commit()  # 提交更改
            QtWidgets.QMessageBox.information(self, "添加成功", "成绩信息已成功添加。")
            self.load_grades_data()  # 重新加载数据以更新表格
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "数据库错误", str(e))
            print(f"数据库错误: {e}")
        finally:
            cursor.close()
            connection.close()

        # 清空输入框
        self.student_id_input.clear()
        self.course_id_input.clear()
        self.score_input.clear()

    def delete_grade(self, row):
        student_id = self.tableWidget.item(row, 0).text()
        course_id = self.tableWidget.item(row, 1).text()

        reply = QtWidgets.QMessageBox.question(self, '确认删除', f'您确定要删除学生ID为 {student_id} 在课程ID为 {course_id} 的记录吗?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            connection = get_db_connection()
            if not connection:
                return  # 连接失败则返回

            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM Grades WHERE StudentID = %s AND CourseID = %s", (student_id, course_id))
                connection.commit()
                self.load_grades_data()  # 重新加载数据以更新表格
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "数据库错误", str(e))
                print(f"数据库错误: {e}")
            finally:
                cursor.close()
                connection.close()

class ClassesManagementWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("ClassesManagementWindow")
        self.resize(1100, 800)
        self.setWindowTitle("班级信息管理")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setColumnCount(5)  # 3列班级信息 + 2列操作按钮
        self.tableWidget.setHorizontalHeaderLabels(["班级ID", "课程ID", "教师ID", "更改", "删除"])
        self.layout.addWidget(self.tableWidget)

        # 添加班级按钮
        self.add_button = QtWidgets.QPushButton("添加班级", self)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                border-radius: 5px;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.show_add_class_dialog)

        self.load_classes_data()

    def load_classes_data(self):
        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()
        cursor.execute("SELECT ClassID, CourseID, TeacherID FROM Classes")
        rows = cursor.fetchall()  # 获取所有班级数据
        self.tableWidget.setRowCount(len(rows))  # 设置表格行数

        for row_index, row_data in enumerate(rows):
            self.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(row_data[0])))
            self.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(row_data[1])))
            self.tableWidget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(row_data[2])))

            # 创建按钮
            self.create_buttons(row_index)

        cursor.close()
        connection.close()

    def create_buttons(self, row_index):
        """创建更改和删除按钮"""
        change_button = QtWidgets.QPushButton('更改')
        change_button.clicked.connect(lambda _, row=row_index: self.show_change_class_dialog(row))
        self.tableWidget.setCellWidget(row_index, 3, change_button)

        delete_button = QtWidgets.QPushButton('删除')
        delete_button.clicked.connect(lambda _, row=row_index: self.delete_class(row))
        self.tableWidget.setCellWidget(row_index, 4, delete_button)

    def show_add_class_dialog(self):
        """显示添加班级的输入对话框"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("添加班级")
        dialog.setFixedSize(400, 250)

        layout = QtWidgets.QVBoxLayout(dialog)

        self.class_id_input = QtWidgets.QLineEdit(dialog)
        self.class_id_input.setPlaceholderText("班级ID (1-9)")
        self.class_id_input.textChanged.connect(self.on_class_id_text_changed)  # 连接信号
        layout.addWidget(self.class_id_input)

        self.course_id_input = QtWidgets.QLineEdit(dialog)
        self.course_id_input.setPlaceholderText("课程ID")
        self.course_id_input.textChanged.connect(self.on_course_id_text_changed)  # 连接信号
        layout.addWidget(self.course_id_input)

        self.teacher_id_input = QtWidgets.QLineEdit(dialog)
        self.teacher_id_input.setPlaceholderText("教师ID")
        self.teacher_id_input.textChanged.connect(self.on_teacher_id_text_changed)  # 连接信号
        layout.addWidget(self.teacher_id_input)

        self.confirm_button = QtWidgets.QPushButton("添加", dialog)
        self.confirm_button.clicked.connect(lambda: self.validate_and_add_class(dialog))
        layout.addWidget(self.confirm_button)

        dialog.exec_()  # 显示对话框并等待用户输入

    def on_class_id_text_changed(self):
        """实时检查班级ID的输入"""
        class_id = self.class_id_input.text().strip()
        if class_id:
            # 检查班级ID是否在1-9之间
            if not class_id.isdigit() or not (1 <= int(class_id) <= 9):
                QMessageBox.warning(self, "输入错误", "班级ID必须是1到9之间的数字。")
                self.class_id_input.clear()  # 清空无效输入
                return

            # 检查班级ID与课程ID组合
            if self.course_id_input.text().strip() and self.check_class_course_combination(class_id, self.course_id_input.text().strip()):
                QMessageBox.warning(self, "输入错误", "该班级ID与课程ID的组合已存在，请更改班级ID。")
                self.class_id_input.clear()  # 清空无效输入
                self.course_id_input.clear()  # 清空无效输入
    def on_course_id_text_changed(self):
        """实时检查课程ID的输入"""
        course_id = self.course_id_input.text().strip()
        if course_id and not self.check_course_id_exists(course_id):
            QMessageBox.warning(self, "输入错误", "该课程ID不存在，请输入有效的课程ID。")
            self.course_id_input.clear()  # 清空无效输入
        # 组合验证
        if self.class_id_input.text().strip() and self.check_class_course_combination(self.class_id_input.text().strip(), course_id):
            QMessageBox.warning(self, "输入错误", "该班级ID与课程ID的组合已存在，请更改课程ID。")
            self.class_id_input.clear()  # 清空无效输入
            self.course_id_input.clear()  # 清空无效输入
    def on_teacher_id_text_changed(self):
        """实时检查教师ID的输入"""
        teacher_id = self.teacher_id_input.text().strip()
        if teacher_id and not self.check_teacher_id_exists(teacher_id):
            QMessageBox.warning(self, "输入错误", "该教师ID不存在，请输入有效的教师ID。")
            self.teacher_id_input.clear()
    def validate_and_add_class(self, dialog):
        """验证输入并添加班级"""
        class_id = self.class_id_input.text().strip()
        if not class_id or not (1 <= int(class_id) <= 9):
            QMessageBox.warning(self, "班级ID检查", "班级ID必须在1到9之间。")
            return

        course_id = self.course_id_input.text().strip()
        if not course_id:
            QMessageBox.warning(self, "课程ID检查", "课程ID不能为空。")
            return

        if not self.check_course_id_exists(course_id):
            return  # 如果不存在则直接返回，警告已在检查方法中处理

        teacher_id = self.teacher_id_input.text().strip()
        if not teacher_id:
            QMessageBox.warning(self, "教师ID检查", "教师ID不能为空。")
            return

        if not self.check_teacher_id_exists(teacher_id):
            return  # 如果不存在则直接返回，警告已在检查方法中处理

        if self.check_class_course_combination(class_id, course_id):
            return  # 如果已存在组合则直接返回，警告已在检查方法中处理

        self.add_class()  # 在这里调用添加班级的逻辑
        dialog.accept()  # 关闭对话框

    def check_course_id_exists(self, course_id):
        """检查课程ID是否存在"""
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Courses WHERE CourseID = %s", (course_id,))
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"课程ID检查失败: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    def check_class_course_combination(self, class_id, course_id):
        """检查班级ID和课程ID组合是否已经存在"""
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Classes WHERE ClassID = %s AND CourseID = %s", (class_id, course_id))
            combination_exists = cursor.fetchone()[0] > 0
            return combination_exists
        except Exception as e:
            print(f"班级与课程组合检查失败: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    def check_teacher_id_exists(self, teacher_id):
        """检查教师ID是否存在"""
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Teachers WHERE TeacherID = %s", (teacher_id,))
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"教师ID检查失败: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    def show_change_class_dialog(self, row):
        """显示更改班级信息的输入对话框"""
        class_id = self.tableWidget.item(row, 0).text()
        course_id = self.tableWidget.item(row, 1).text()
        teacher_id = self.tableWidget.item(row, 2).text()

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("更改班级信息")
        dialog.setFixedSize(400, 250)

        layout = QtWidgets.QVBoxLayout(dialog)

        self.change_class_id_input = QtWidgets.QLineEdit(dialog)
        self.change_class_id_input.setPlaceholderText("班级ID")
        self.change_class_id_input.setText(class_id)
        self.change_class_id_input.setEnabled(False)  # 禁用编辑班级ID
        layout.addWidget(self.change_class_id_input)

        self.change_course_id_input = QtWidgets.QLineEdit(dialog)
        self.change_course_id_input.setPlaceholderText("课程ID")
        self.change_course_id_input.setText(course_id)
        self.change_course_id_input.setEnabled(False)  # 禁用编辑课程ID
        layout.addWidget(self.change_course_id_input)

        self.change_teacher_id_input = QtWidgets.QLineEdit(dialog)
        self.change_teacher_id_input.setPlaceholderText("教师ID")
        self.change_teacher_id_input.setText(teacher_id)
        layout.addWidget(self.change_teacher_id_input)

        self.confirm_change_button = QtWidgets.QPushButton("更改", dialog)
        self.confirm_change_button.clicked.connect(lambda: self.update_class(row))
        layout.addWidget(self.confirm_change_button)

        dialog.exec_()  # 显示对话框并等待用户输入

    def update_class(self, row):
        """更新班级信息"""
        class_id = self.change_class_id_input.text().strip()  # ID不可更改
        course_id = self.change_course_id_input.text().strip()  # 课程ID
        teacher_id = self.change_teacher_id_input.text().strip()  # 教师ID

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()

        try:
            # 更新班级信息
            cursor.execute(
                "UPDATE Classes SET CourseID = %s, TeacherID = %s WHERE ClassID = %s",
                (course_id, teacher_id, class_id))
            connection.commit()  # 提交更改
            QMessageBox.information(self, "更改成功", "班级信息已成功更新。")
            self.load_classes_data()  # 重新加载数据以更新表格
        except Exception as e:
            QMessageBox.critical(self, "更改失败", str(e))
            print(f"数据库错误: {e}")
        finally:
            cursor.close()
            connection.close()

    def add_class(self):
        """添加新班级到数据库"""
        class_id = self.class_id_input.text().strip()  # 获取输入的班级ID
        course_id = self.course_id_input.text().strip()  # 获取输入的课程ID
        teacher_id = self.teacher_id_input.text().strip()  # 获取输入的教师ID

        connection = get_db_connection()
        if not connection:
            return  # 连接失败则返回

        cursor = connection.cursor()
        try:
            # 插入新班级信息
            cursor.execute(
                "INSERT INTO Classes (ClassID, CourseID, TeacherID) VALUES (%s, %s, %s)",
                (class_id, course_id, teacher_id))
            connection.commit()  # 提交更改
            QMessageBox.information(self, "添加成功", "班级信息已成功添加。")
            self.load_classes_data()  # 重新加载数据以更新表格
        except Exception as e:
            QMessageBox.critical(self, "数据库错误", str(e))
            print(f"数据库错误: {e}")
        finally:
            cursor.close()
            connection.close()

        # 清空输入框
        self.reset_inputs()

    def delete_class(self, row):
        class_id = self.tableWidget.item(row, 0).text()

        reply = QMessageBox.question(self, '确认删除', f'您确定要删除班级ID为 {class_id} 的记录吗?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            connection = get_db_connection()
            if not connection:
                return  # 连接失败则返回

            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM Classes WHERE ClassID = %s", (class_id,))
                connection.commit()
                self.load_classes_data()  # 重新加载数据以更新表格
            except Exception as e:
                QMessageBox.critical(self, "数据库错误", str(e))
                print(f"数据库错误: {e}")
            finally:
                cursor.close()
                connection.close()

    def reset_inputs(self):
        """重置输入框"""
        self.class_id_input.clear()
        self.course_id_input.clear()
        self.teacher_id_input.clear()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

