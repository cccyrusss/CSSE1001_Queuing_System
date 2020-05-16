import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox
import time
import socket
from threading import Thread

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 5004
clientsocket.connect((host, port))


class Mainwin:
    """
    A class that manages the main window.
    """

    def __init__(self, master):
        """
        Construct a main window.

        Parameters:

            master(tk): Main window.
        """
        self._master = master
        self._master.title("CSSE1001 Queue")

        self._qwaitlist = []
        self._lwaitlist = []
        self._shortstudentlabel = {}
        self._longstudentlabel = {}
        self._qrownum = 0
        self._lrownum = 0
        self._students = {}
        self._role = input("Are you a student or a tutor?\n").upper()
        self._name = input("Please enter your name: ")
        clientsocket.send(bytes(self._name, "utf-8"))

        """
        Create a frame for the notice.
        """
        noticeframe = tk.Frame(master, bg="#FEFBED")
        noticeframe.pack(fill=tk.X, expand=1)

        self._header = tk.Label(noticeframe, text="Important:", bg="#FEFBED", fg="#BF9852")
        headerfont = Font(family="Arial", size=14, weight="bold")
        self._header.pack(side=tk.TOP, padx=20, pady=5, expand=1, anchor=tk.W)
        self._header.config(font=headerfont)

        msgtext = "Individual assessment items must be solely your own work." + \
                  " While students are encouraged to have high-level conversations" + \
                  " about the programs they are\ntrying to solve, you must not look at" + \
                  " another student's code or copy from it. The University uses sophisticated" + \
                  " anti-collusion measures to automatically\ndetect similarity between assignment " + \
                  "submissions."

        self._msg = tk.Label(noticeframe, text=msgtext, bg="#FEFBED")
        self._msg.pack(side=tk.TOP, pady=5, padx=20, expand=1, anchor=tk.W)
        msgfont = Font(family="Arial", size=11)
        self._msg.config(font=msgfont, justify=tk.LEFT)

        """
        Create a frame which manages the left side.
        """
        leftframe = tk.Frame(master)
        leftframe.pack(side=tk.LEFT, fill=tk.X, padx=20, expand=tk.FALSE, pady=10)

        lefttopframe = tk.Frame(leftframe)
        lefttopframe.pack(fill=tk.X, expand=1, anchor=tk.N)

        greenframe = tk.Frame(lefttopframe, bg="#DFF0D8")
        greenframe.pack(fill=tk.X, expand=1, ipady=20)

        queuefont = Font(family="Arial", size=23, weight="bold")
        tutorfont = Font(family="Arial", size=12, slant="italic")

        self._quickq = tk.Label(greenframe, text="Quick Questions", bg="#DFF0D8", fg="#3D763D")
        self._quickq.pack(side=tk.TOP, expand=1, pady=10)
        self._quickq.config(font=queuefont)

        self._qtutor = tk.Label(greenframe, text="< 2 mins with a tutor", bg="#DFF0D8", fg="#666666")
        self._qtutor.pack(side=tk.TOP, expand=1, pady=5)
        self._qtutor.config(font=tutorfont)

        """
        Create a frame which manages the right side.
        """
        rightframe = tk.Frame(master)
        rightframe.pack(side=tk.LEFT, fill=tk.X, padx=20, expand=tk.FALSE, pady=10)

        righttopframe = tk.Frame(rightframe)
        righttopframe.pack(fill=tk.X, expand=1)

        blueframe = tk.Frame(righttopframe, bg="#D8EDF7")
        blueframe.pack(fill=tk.X, expand=1, ipady=20)

        self._longq = tk.Label(blueframe, text="Long Questions", bg="#D8EDF7", fg="#31708F")
        self._longq.pack(expand=1, pady=10)
        self._longq.config(font=queuefont)

        self._ltutor = tk.Label(blueframe, text="> 2 mins with a tutor", bg="#D8EDF7", fg="#666666")
        self._ltutor.pack(expand=1, pady=5)
        self._ltutor.config(font=tutorfont)

        textfont = Font(family="Arial", size=11)
        qtextframe = tk.Frame(lefttopframe)
        qtextframe.pack(fill=tk.X, expand=1, pady=5)

        self._qex = tk.Label(qtextframe, text="Some examples of quick questions:")
        self._qex.pack(expand=1, anchor=tk.W)
        self._qex.config(font=textfont, justify=tk.LEFT)

        self._qtext = tk.Label(qtextframe,
                               text="  \u2022  Syntax errors\n  \u2022  Interpreting error output\n  \u2022  Assignment/MyPyTutor interpretation\n  \u2022  MyPyTutor submission issues\n")
        self._qtext.pack(expand=1, anchor=tk.W)
        self._qtext.config(font=textfont, justify=tk.LEFT)

        if self._role == "STUDENT":
            self._qreq = tk.Button(qtextframe, text="Request Quick Help", bg="#5CB85B", fg="white",
                                   command=lambda: self.checkname(self._qstudentframe))
            self._qreq.pack(ipady=5, ipadx=5)
            self._qreq.config(font=textfont)

        ltextframe = tk.Frame(righttopframe)
        ltextframe.pack(fill=tk.X, expand=1, pady=5)

        self._lex = tk.Label(ltextframe, text="Some examples of long questions:")
        self._lex.pack(expand=1, anchor=tk.W)
        self._lex.config(font=textfont, justify=tk.LEFT)

        self._ltext = tk.Label(ltextframe,
                               text="  \u2022  Open ended questions\n  \u2022  How to start a problem\n  \u2022  How to improve code\n  \u2022  Debugging\n  \u2022  Assignment help")
        self._ltext.pack(expand=1, anchor=tk.W)
        self._ltext.config(font=textfont, justify=tk.LEFT)

        if self._role == "STUDENT":
            self._lreq = tk.Button(ltextframe, text="Request Long Help", bg="#5CC0DE", fg="white",
                                   command=lambda: self.checkname(self._lstudentframe))
            self._lreq.pack(ipady=5, ipadx=5)
            self._lreq.config(font=textfont)

        qgreyframe = tk.Frame(lefttopframe, bg="#EEEEEE")
        qgreyframe.pack(ipady=1, fill=tk.X, expand=1)

        """
        Create a frame which manages the status of student's wait time in quick queue.
        """
        qstatusframe = tk.Frame(qgreyframe)
        qstatusframe.pack(fill=tk.X, expand=1)
        statusfont = Font(family="Arial", size=11, slant="italic")

        self._qavgwait = tk.Label(qstatusframe, text="No students in queue")
        self._qavgwait.pack(expand=1, anchor=tk.W, ipady=5)
        self._qavgwait.config(font=statusfont, justify=tk.LEFT)

        lgreyframe = tk.Frame(righttopframe, bg="#EEEEEE")
        lgreyframe.pack(ipady=1, fill=tk.X, expand=1)

        """
        Create a frame which manages the status of student's wait time in long queue.
        """
        lstatusframe = tk.Frame(lgreyframe)
        lstatusframe.pack(fill=tk.X, expand=1)

        self._lavgwait = tk.Label(lstatusframe, text="No students in queue")
        self._lavgwait.pack(expand=1, anchor=tk.W, ipady=5)
        self._lavgwait.config(font=statusfont, justify=tk.LEFT)

        leftbottomframe = tk.Frame(leftframe)
        leftbottomframe.pack(expand=1, fill=tk.X)

        rightbottomframe = tk.Frame(rightframe)
        rightbottomframe.pack(expand=1, fill=tk.X)

        """
        Create frames that manage students.
        """
        self._qstudentframe = tk.Frame(leftbottomframe)
        self._qstudentframe.pack(expand=1, fill=tk.X)
        self._lstudentframe = tk.Frame(rightbottomframe)
        self._lstudentframe.pack(expand=1, fill=tk.X)

        """
        Create headers.
        """
        headersfont = Font(family="Arial", size=11, weight="bold")

        self._qnum = tk.Label(self._qstudentframe, text="#")
        self._qnum.grid(row=0, column=0)
        self._qnum.config(font=headersfont)

        self._qname = tk.Label(self._qstudentframe, text="Name                       ")
        self._qname.grid(row=0, column=1)
        self._qname.config(font=headersfont)

        self._qqasked = tk.Label(self._qstudentframe, text="Question Asked  ")
        self._qqasked.grid(row=0, column=2)
        self._qqasked.config(font=headersfont)

        self._qtime = tk.Label(self._qstudentframe, text="Time                 ")
        self._qtime.grid(row=0, column=3)
        self._qtime.config(font=headersfont)

        tk.Label(self._qstudentframe, width=3).grid(row=0, column=4)
        tk.Label(self._qstudentframe, width=3).grid(row=0, column=5)

        self._lnum = tk.Label(self._lstudentframe, text="#")
        self._lnum.grid(row=0, column=0)
        self._lnum.config(font=headersfont)

        self._lname = tk.Label(self._lstudentframe, text="Name                       ")
        self._lname.grid(row=0, column=1)
        self._lname.config(font=headersfont)

        self._lqasked = tk.Label(self._lstudentframe, text="Question Asked  ")
        self._lqasked.grid(row=0, column=2)
        self._lqasked.config(font=headersfont)

        self._ltime = tk.Label(self._lstudentframe, text="Time                 ")
        self._ltime.grid(row=0, column=3)
        self._ltime.config(font=headersfont)

        tk.Label(self._lstudentframe, width=3).grid(row=0, column=4)
        tk.Label(self._lstudentframe, width=3).grid(row=0, column=5)

        self.update_loop(self._qstudentframe)
        self.update_loop(self._lstudentframe)

    def get_waitlist(self, frame):
        """
        Return waitlist of the queue.

        Parameter:
            frame(tk.Frame): the frame that the waitlist belongs to.
        """
        if frame == self._qstudentframe:
            return self._qwaitlist
        else:
            return self._lwaitlist

    def get_studentlabel(self, frame):
        """
        Return the labels of the student.

        Parameter:
            frame(tk.Frame): the frame that the student belongs to.
        """
        if frame == self._qstudentframe:
            return self._shortstudentlabel
        return self._longstudentlabel

    def get_waitnum(self, frame, student):
        """
        Return the number of the position of the student in the queue.

        Parameters:
            frame(tk.Frame): the frame that the student belongs to.
            student(Students): the student who is waiting.
        """
        waitlist = self.get_waitlist(frame)
        return waitlist.index(student) + 1

    def checkname(self, frame):
        """
        Check if the student is in any queue already. If no, add the student into the queue.

        Parameters:
            frame(tk.Frame): the frame that the student belongs to.
        """
        name = self._name
        if name not in self._students:
            student = Students(name)
            self._students[name] = student
        else:
            student = self._students[name]
        waitlist = self.get_waitlist(frame)
        if frame == self._qstudentframe:
            self._qrownum += 1
            rownum = self._qrownum
        else:
            self._lrownum += 1
            rownum = self._lrownum
        if student in self._qwaitlist or student in self._lwaitlist:
            messagebox.showerror("Error", "Please be patient!")
        else:
            waitlist.append(student)
            studentlabel = self.get_studentlabel(frame)
            qasked = self.get_questionasked(frame, student)
            student._rownum = rownum
            waitnum = self.get_waitnum(frame, student)
            waitnumlabel = self.add_label(frame, waitnum, 0, rownum)
            namelabel = self.add_label(frame, name, 1, rownum)
            qaskedlabel = self.add_label(frame, qasked, 2, rownum)
            timelabel = self.add_label(frame, "a few seconds ago", 3, rownum)
            student._qaskedtime = time.time()
            askedtime = student._qaskedtime
            if frame == self._qstudentframe:
                clientsocket.send(bytes(f"student: {name} , short question asked: {qasked} , askedtime: {askedtime}", "utf-8"))
            else:
                clientsocket.send(bytes(f"student: {name} , long question asked: {qasked} , askedtime: {askedtime}", "utf-8"))
            studentlabel[student] = [waitnumlabel, namelabel, qaskedlabel, timelabel]
            self.updateframe(frame)
            self._master.after(10000, lambda: self.updatetime(frame, student))
            self.updateavg(frame)

    def updateframe(self, frame):
        """
        Sort the students in the queue based on their number of questions asked.

        Parameter:
            frame(tk.Frame): the frame that the queue belongs to.
        """
        studentlabel = self.get_studentlabel(frame)
        waitlist = self.get_waitlist(frame)
        qasked = {}
        for ppl in waitlist:
            qasked[ppl] = self.get_questionasked(frame, ppl)
        sortedstudent = sorted(qasked.items(), key=lambda kv: kv[1])
        for rownum, student in enumerate(sortedstudent, start=1):
            for num, label in enumerate(studentlabel[student[0]]):
                label.grid_forget()
                label.grid(column=num, row=rownum, sticky=tk.W)
                studentlabel[student[0]][0].config(text=rownum)

    def add_label(self, frame, text, column, row):
        """
        Add label for the student.

        Parameters:
            frame(tk.Frame): the frame that the student belongs to.
            text(str): text of the label.
            column(int): column number of the label.
            row(int): row number of the label.
        """
        font = Font(family="Arial", size=11)
        newlabel = tk.Label(frame, text=text)
        newlabel.grid(row=row, column=column, sticky=tk.W)
        newlabel.config(font=font)
        return newlabel

    def accept(self, frame, student):
        """
        Accept the student.

        Parameters:
            frame(tk.Frame): the frame that the student belongs to.
            student(Students): the student who is about to be accepted.
        """
        if frame == self._qstudentframe:
            student._shortquestionasked += 1
            clientsocket.send(bytes(f"short {student.get_name()} accepted", "utf-8"))
        else:
            student._longquestionasked += 1
            clientsocket.send(bytes(f"long {student.get_name()} accepted", "utf-8"))
        self.decline(frame, student)

    def decline(self, frame, student):
        """
        Decline the students.

        Parameters:
            frame(tk.Frame): the frame that the student belongs to.
            student(Students): the student who is about to be declined.
        """
        waitlist = self.get_waitlist(frame)
        waitlist.remove(student)
        studentlabel = self.get_studentlabel(frame)
        self.updateavg(frame)
        for label in studentlabel[student]:
            label.grid_forget()
        del studentlabel[student]
        self.updateframe(frame)
        if frame == self._qstudentframe:
            clientsocket.send(bytes(f"short {student.get_name()} deleted", "utf-8"))
        else:
            clientsocket.send(bytes(f"long {student.get_name()} deleted", "utf-8"))

    def get_questionasked(self, frame, student):
        """
        Return how many short/long questions the student has asked.

        Parameters:
            frame(tk.Frame): the frame that the student belongs to.
            student(Students): the student who has asked questions.
        """
        if frame == self._qstudentframe:
            questionasked = student.get_shortquestionasked()
        else:
            questionasked = student.get_longquestionasked()
        return questionasked

    def update_loop(self, frame):
        """
        Constantly update the average wait time of the queue.

        Parameter:
            frame(tk.Frame): the frame that the queue belongs to.
        """
        self.updateavg(frame)
        self._master.after(10000, self.update_loop, frame)

    def updateavg(self, frame):
        """
        Update the average wait time of the queue.

        Parameter:
            frame(tk.Frame): the frame that the queue belongs to.
        """
        waitlist = self.get_waitlist(frame)
        if frame == self._qstudentframe:
            waitlabel = self._qavgwait
        else:
            waitlabel = self._lavgwait
        try:
            totalwait = 0
            for ppl in waitlist:
                waittime = ppl.get_waittime()
                totalwait += waittime
            avgwait = int(totalwait/len(waitlist))
            studentunit = "student" if len(waitlist) == 1 else "students"
            if avgwait < 60:
                avgwait = "a few"
                unit = "seconds"
                about = ""
            elif avgwait < 120:
                avgwait = 1
                unit = "minute"
                about = "about"
            elif avgwait < 3600:
                avgwait = int(avgwait / 60)
                unit = "minutes"
                about = "about"
            elif avgwait < 7200:
                avgwait = "an"
                unit = "hour"
                about = "about"
            else:
                avgwait = int(avgwait / 3600)
                unit = "hours"
                about = "about"
            waitlabel.config(text=f"An average wait of {about} {avgwait} {unit} for {len(waitlist)} {studentunit}.")
        except ZeroDivisionError:
            waitlabel.config(text="No students in queue")

    def updatetime(self, frame, student):
        """
        Update the time label of the student.

        Parameters:
            frame(tk.Frame): the frame that the student belongs to.
            student(Students): the student to be updated.
        """
        studentlabel = self.get_studentlabel(frame)
        if student in studentlabel:
            timelabel = studentlabel[student][3]
            waittime = student.get_waittime()
            waitlist = self.get_waitlist(frame)
            if student in waitlist:
                if waittime < 60:
                    timelabel.config(text="a few seconds ago")
                elif waittime < 120:
                    timelabel.config(text="a minute ago")
                elif waittime < 3600:
                    timelabel.config(text=f"{int(waittime/60)} minutes ago")
                elif waittime < 7200:
                    timelabel.config(text="an hour ago")
                else:
                    timelabel.config(text=f"{int(waittime/3600)} hours ago")
                self._master.after(10000, lambda: self.updatetime(frame, student))

    def receive(self):
        """
        Receive commands from the server.
        """
        while True:
            try:
                msg = clientsocket.recv(1024).decode("utf-8")
                if "student: "in msg:
                    name = msg.split()[1]
                    if name not in self._students:
                        student = Students(name)
                        self._students[name] = student
                    else:
                        student = self._students[name]
                    if "short" in msg:
                        self._qwaitlist.append(student)
                        student._shortquestionasked = int(msg.split()[-4])
                        qasked = student._shortquestionasked
                        self._qrownum += 1
                        rownum = self._qrownum
                        frame = self._qstudentframe
                        studentlabel = self._shortstudentlabel
                    else:
                        self._lwaitlist.append(student)
                        student._longquestionasked = int(msg.split()[-4])
                        qasked = student._longquestionasked
                        self._lrownum += 1
                        rownum = self._lrownum
                        frame = self._lstudentframe
                        studentlabel = self._longstudentlabel
                    student._qaskedtime = float(msg.split()[-1])
                    waitnum = self.get_waitnum(frame, student)
                    waitnumlabel = self.add_label(frame, waitnum, 0, rownum)
                    namelabel = self.add_label(frame, name, 1, rownum)
                    qaskedlabel = self.add_label(frame, qasked, 2, rownum)
                    timelabel = self.add_label(frame, "a few seconds ago", 3, rownum)
                    studentlabel[student] = [waitnumlabel, namelabel, qaskedlabel, timelabel]
                    if self._role == "TUTOR":
                        decline = tk.Button(frame, bg="#F6A5A3", command=lambda f=frame, s=student: self.decline(f, s))
                        decline.grid(column=4, row=rownum)
                        accept = tk.Button(frame,bg="#5CB85B", command=lambda f=frame, s=student: self.accept(f, s))
                        accept.grid(column=5, row=rownum)
                        studentlabel[student] = [waitnumlabel, namelabel, qaskedlabel, timelabel, decline, accept]
                    self.updateframe(frame)
                    self._master.after(10000, lambda: self.updatetime(frame, student))
                    self.updateavg(frame)
                elif "deleted" in msg:
                    if "short" in msg:
                        frame = self._qstudentframe
                    else:
                        frame = self._lstudentframe
                    name = msg.split()[1]
                    student = self._students[name]
                    waitlist = self.get_waitlist(frame)
                    waitlist.remove(student)
                    studentlabel = self.get_studentlabel(frame)
                    self.updateavg(frame)
                    for label in studentlabel[student]:
                        label.grid_forget()
                    del studentlabel[student]
                    self.updateframe(frame)
                elif "accepted" in msg:
                    student = self._students[msg.split()[1]]
                    if "short" in msg:
                        frame = self._qstudentframe
                        student._shortquestionasked += 1
                    else:
                        frame = self._lstudentframe
                        student._longquestionasked += 1
            except OSError:
                break

    def on_closing(self):
        """
        Tell the server that the client has disconnected.
        """
        clientsocket.send(bytes("quit", "utf-8"))
        self._master.destroy()
        clientsocket.close()


class Students:
    """
    A class that manages students.
    """
    def __init__(self, name):
        """
        Construct a new student object.

        Parameters:

            name(str): name of the student.
        """
        self._name = name
        self._iswaiting = False
        self._shortquestionasked = 0
        self._longquestionasked = 0
        self._qaskedtime = 0
        self._labellist = []
        self._rownum = 0

    def get_name(self):
        """
        Return the name of the student.
        """
        return self._name

    def get_longquestionasked(self):
        """
        Return how many long questions the student has asked.
        """
        return self._longquestionasked

    def get_shortquestionasked(self):
        """
        Return how many short questions the student has asked.
        """
        return self._shortquestionasked

    def get_qaskedtime(self):
        """
        Return the time that the student asked question.
        """
        return self._qaskedtime

    def get_waittime(self):
        """
        Return how long the student has been waiting.
        """
        currenttime = time.time()
        asktime = self.get_qaskedtime()
        waittime = currenttime - asktime
        return waittime

    def __repr__(self):
        return self._name


if __name__ == "__main__":
    root = tk.Tk()
    mainwin = Mainwin(root)
    Thread(target=mainwin.receive).start()
    root.resizable(0, 0)
    root.protocol("WM_DELETE_WINDOW", mainwin.on_closing)
    root.mainloop()
