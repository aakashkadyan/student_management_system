import os
import pymongo
from tkcalendar import Calendar, DateEntry  
import tkinter as tk
import tkinter.messagebox as mb  
import tkinter.ttk as ttk  


client =  pymongo.MongoClient("mongodb://localhost:27017/")
db_name = client["ems_test"]
emp_collection = db_name['user']  
# creating database_cursor to perform SQL operation  
#db_cursor = db_connection.cursor(buffered=True) # "buffered=True".makes db_cursor.row_count return actual number of records selected otherwise would return -1  
class Employee(tk.Tk):
    
    
    def __init__(self):
        
        super().__init__()  
        self.title("Employee Management System")  
        self.geometry("800x650+351+174")
        self.lblTitle = tk.Label(self, text="Employee Management System", font=("Helvetica", 16), bg="yellow", fg="green")  
        self.lblFName = tk.Label(self, text="Enter FirstName:", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.lblLName = tk.Label(self, text="Enter LastName:", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.age = tk.Label(self, text="Enter Age:", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.gender = tk.Label(self, text="Enter Gender:", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.department = tk.Label(self, text="Enter Department:", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.doj = tk.Label(self, text="Enter Date of Joining", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.lblSelect = tk.Label(self, text="Please select one record below to update or delete", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.lblSearch = tk.Label(self, text="Please Enter Roll No:",font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.entFName = tk.Entry(self)  
        self.entLName = tk.Entry(self)  
        self.entContact = tk.Entry(self)  
        self.entCity = tk.Entry(self)  
        self.entState = tk.Entry(self)  
        self.calDOB = DateEntry(self, width=12, background='darkblue',  
        foreground='white', borderwidth=2, year=1950,locale='en_US', date_pattern='y-mm-dd')  
        #self.entDOB = tk.Entry(self)  
        self.entSearch = tk.Entry(self)  
        self.btn_register = tk.Button(self, text="Register", font=("Helvetica", 11), bg="yellow", fg="blue",  
        command=self.register_student)  
        self.btn_update = tk.Button(self,text="Update",font=("Helvetica",11),bg="yellow", fg="blue",command=self.update_student_data)  
        self.btn_delete = tk.Button(self, text="Delete", font=("Helvetica", 11), bg="yellow", fg="blue",  
        command=self.delete_student_data)  
        self.btn_clear = tk.Button(self, text="Clear", font=("Helvetica", 11), bg="yellow", fg="blue",  
        command=self.clear_form)  
        self.btn_show_all = tk.Button(self, text="Show All", font=("Helvetica", 11), bg="yellow", fg="blue",  
        command=self.load_student_data)  
        self.btn_search = tk.Button(self, text="Search", font=("Helvetica", 11), bg="yellow", fg="blue",  
        command=self.show_search_record)  
        self.btn_exit = tk.Button(self, text="Exit", font=("Helvetica", 16), bg="yellow", fg="blue",command=self.exit)  
        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")  
        self.tvStudent= ttk.Treeview(self,show="headings",height="5", columns=columns)  
        self.tvStudent.heading('#1', text='RollNo', anchor='center')  
        self.tvStudent.column('#1', width=60, anchor='center', stretch=False)  
        self.tvStudent.heading('#2', text='FirstName', anchor='center')  
        self.tvStudent.column('#2', width=10, anchor='center', stretch=True)  
        self.tvStudent.heading('#3', text='LastName', anchor='center')  
        self.tvStudent.column('#3',width=10, anchor='center', stretch=True)  
        self.tvStudent.heading('#4', text='City', anchor='center')  
        self.tvStudent.column('#4',width=10, anchor='center', stretch=True)  
        self.tvStudent.heading('#5', text='State', anchor='center')  
        self.tvStudent.column('#5',width=10, anchor='center', stretch=True)  
        self.tvStudent.heading('#6', text='PhoneNumber', anchor='center')  
        self.tvStudent.column('#6', width=10, anchor='center', stretch=True)  
        self.tvStudent.heading('#7', text='Date of Birth', anchor='center')  
        self.tvStudent.column('#7', width=10, anchor='center', stretch=True)  
        #Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget  
        vsb= ttk.Scrollbar(self, orient=tk.VERTICAL,command=self.tvStudent.yview)  
        vsb.place(x=40 + 640 + 1, y=310, height=180 + 20)  
        self.tvStudent.configure(yscroll=vsb.set)  
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tvStudent.xview)  
        hsb.place(x=40 , y=310+200+1, width=620 + 20)  
        self.tvStudent.configure(xscroll=hsb.set)  
        self.tvStudent.bind("<<TreeviewSelect>>", self.show_selected_record)  
        self.lblTitle.place(x=280, y=30, height=27, width=300)  
        self.lblFName.place(x=175, y=70, height=23, width=100)  
        self.lblLName.place(x=175, y=100, height=23, width=100)  
        self.age.place(x=171, y=129, height=23, width=104)  
        self.gender.place(x=210, y=158, height=23, width=65)  
        self.department.place(x=205, y=187, height=23, width=71)  
        self.doj.place(x=148, y=217, height=23, width=128)  
        self.lblSelect.place(x=150, y=280, height=23, width=400)  
        self.lblSearch.place(x=174, y=560, height=23, width=134)  
        self.entFName.place(x=277, y=72, height=21, width=186)  
        self.entLName.place(x=277, y=100, height=21, width=186)  
        self.entContact.place(x=277, y=129, height=21, width=186)  
        self.entCity.place(x=277, y=158, height=21, width=186)  
        self.entState.place(x=278, y=188, height=21, width=186)  
        self.calDOB.place(x=278, y=218, height=21, width=186)  
        self.entSearch.place(x=310, y=560, height=21, width=186)  
        self.btn_register.place(x=290, y=245, height=25, width=76)  
        self.btn_update.place(x=370, y=245, height=25, width=76)  
        self.btn_delete.place(x=460, y=245, height=25, width=76)  
        self.btn_clear.place(x=548, y=245, height=25, width=76)  
        self.btn_show_all.place(x=630, y=245, height=25, width=76)  
        self.btn_search.place(x=498, y=558, height=26, width=60)  
        self.btn_exit.place(x=320, y=610, height=31, width=60)  
        self.tvStudent.place(x=40, y=310, height=200, width=640)  
        #self.create_table()  
        self.load_student_data()  
    def clear_form(self):  
        self.entFName.delete(0, tk.END)  
        self.entLName.delete(0, tk.END)  
        self.entContact.delete(0, tk.END)  
        self.entCity.delete(0, tk.END)  
        self.entState.delete(0, tk.END)  
        self.calDOB.delete(0, tk.END)  
    def exit(self):  
        MsgBox = mb.askquestion('Exit Application', 'Are you sure you want to exit the application', icon='warning')  
        if MsgBox == 'yes':  
            self.destroy()  
#     def delete_student_data(self):  
#         MsgBox = mb.askquestion('Delete Record', 'Are you sure! you want to delete selected student record', icon='warning')  
#         if MsgBox == 'yes':
            
#             if db_connection.is_connected() == False:  
#                 db_connection.connect()  
#                 db_cursor.execute("use Student") # Interact with Student Database  
#     # deleteing selected student record  
#                 Delete = "delete from student_master where RollNo='%s'" % (roll_no)  
#                 db_cursor.execute(Delete)  
#                 db_connection.commit()  
#                 mb.showinfo("Information", "Student Record Deleted Succssfully")  
#                 self.load_student_data()  
#                 self.entFName.delete(0, tk.END)  
#                 self.entLName.delete(0, tk.END)  
#                 self.entContact .delete(0, tk.END)  
#                 self.entCity.delete(0, tk.END)  
#                 self.entState.delete(0, tk.END)  
#                 self.calDOB.delete(0, tk.END)  
#     def create_table(self):  
#         if db_connection.is_connected() == False:
            
            
#             db_connection.connect()  
#     # executing cursor with execute method and pass SQL query  
#             db_cursor.execute("CREATE DATABASE IF NOT EXISTS Student") # Create a Database Named Student  
#             db_cursor.execute("use Student") # Interact with Student Database  
#     # creating required tables  
#             db_cursor.execute("create table if not exists Student_master(Id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,rollno INT(15),fname VARCHAR(30),lname VARCHAR(30),city VARCHAR(20),state VARCHAR(30),mobileno VARCHAR(10),dob date)AUTO_INCREMENT=1")  
#             db_connection.commit()  
    
    def add_employee(self):

        details_list = [{'first_name':self.self.lblFName, 'last_name':self.lblLName,'age':self.age,'gender':self.gender,'department':self.department,'date_of_joining':self.doj}]
        insert_data = emp_collection.insert_many(details_list)
        print(insert_data.inserted_ids)
    
    
    
#     def fetch_max_roll_no(self):  
#         if db_connection.is_connected() == False:  
#             db_connection.connect()  
#             db_cursor.execute("use Student") # Interact with Student Database  
#             rollno = 0  
#             query1 = "SELECT rollno FROM student_master order by id DESC LIMIT 1"  
#             # implement query Sentence  
#             db_cursor.execute(query1) # Retrieving maximum student id no  
#             print("No of Record Fetched:" + str(db_cursor.rowcount))  
#         if db_cursor.rowcount == 0:  
#             rollno = 1  
#         else:  
#             rows = db_cursor.fetchall()  
#         for row in rows:  
#             rollno = row[0]  
#             rollno = rollno + 1  
#             print("Max Student Id: " + str(rollno))  
#     return rollno

    @staticmethod
    def search_emp():

        print("You can search by their Names!")
        searching_1st_name = str(input("Enter first name of Employee here: ")).lower().strip()
        searching_last_name = str(input("Enter last name of Employee here: ")).lower().strip()

        search_by_name = emp_collection.find_one({ "first_name": searching_1st_name, "last_name": searching_last_name})
        if searching_1st_name and searching_last_name:

            print(search_by_name)

        else:
            print("Record Not Found!!")        
#     def show_selected_record(self, event):  
#         self.clear_form()  
#         for selection in self.tvStudent.selection():  
#             item = self.tvStudent.item(selection)  
#             global roll_no  
#             roll_no,first_name,last_name,city,state,contact_no,dob = item["values"][0:7]  
#             self.entFName.insert(0, first_name)  
#             self.entLName.insert(0, last_name)  
#             self.entCity.insert(0, city)  
#             self.entState .insert(0, state)  
#             self.entContact.insert(0, contact_no)  
#             self.calDOB.insert(0, dob)  
#         return roll_no  
    def update_details():

        print("Enter The Employee Name you want to Update!")

        searching_1st_name = str(input("Enter first name of Employee here: ")).lower().strip()
        searching_last_name = str(input("Enter last name of Employee here: ")).lower().strip()
        employee_record = emp_collection.find_one({ "first_name": searching_1st_name, "last_name": searching_last_name})
        if employee_record:

            data_id = employee_record['_id']

            print("You can only choose the options you want to update below!")

            print("1 - First Name")
            print("2 - Last Name")
            print("3 - Age")
            print("4 - Gender")
            print("5 - Department")
            print("6 - Date of Joining")


            update_details = {

                "1" : "First Name",
                "2" : "Last Name",
                "3" : "Age",
                "4" : "Gender",
                "5" : "Department",
                "6" : "Date of Joining"

            }


            try:
                input_choice = input("Enter your inputs using separated Commas:").replace(" ","").split(",")



                for data in input_choice:

                    updated_details = input(f"Enter your {update_details[data]} : ").lower().strip()    

                    if data == "1":

                        set_values = { "$set": { 'first_name':updated_details}}
                        emp_collection.update_one({'_id':data_id}, set_values)

                    elif data == "2":

                        set_values = { "$set": { 'last_name':updated_details}}
                        emp_collection.update_one({'_id':data_id}, set_values)


                    elif data == "3":

                        set_values = { "$set": { 'age':updated_details}}
                        emp_collection.update_one({'_id':data_id}, set_values)

                    elif data == "4":

                        set_values = { "$set": { 'gender':updated_details}}
                        emp_collection.update_one({'_id':data_id}, set_values)

                    elif data == "5":

                        set_values = { "$set": { 'department':updated_details}}
                        emp_collection.update_one({'_id':data_id}, set_values)

                    elif data == "6":

                        set_values = { "$set": { 'date_of_joining':updated_details}}
                        emp_collection.update_one({'_id':data_id}, set_values)


            except Exception as error:
                print("Something went Wrong,you cannot Enter This: ", error)


        else:
            print("You have entered Wrong Details, Try to Enter Correct Details!")

    @staticmethod
    def del_emp():


        print("You can search by their Names!")
        searching_1st_name = str(input("Enter first name of Employee here: ")).lower().strip()
        searching_last_name = str(input("Enter last name of Employee here: ")).lower().strip()
        emp_record = emp_collection.find_one({ "first_name": searching_1st_name, "last_name": searching_last_name})
        if emp_record:
            print(emp_record)
            print("Are you Sure you want to delete this Emplyee details?")
            
            confirmation = str(input("Please confirm here Yes/No :")).lower().strip()

            if confirmation == "yes":

                deleted_result = emp_collection.delete_one(emp_record)

                print(deleted_result.deleted_count, " documents deleted.")

        else:
            print("Record Not Found!!")        
            
            
            
    def ask_user(self):

        print("You can choose from the Below options!")
        print("1 - To add details of Employee!")
        print("2 - To update the details of Employee!")
        print("3 - To search the details of Employee!")
        print("4 - To Delete an Employee!")
        print()
        option = int(input("Enter Options Here: "))
        print()
        if option ==1:
            self.add_employee()

        elif option == 2:
            update_details()

        elif option == 3:
            search_emp()

        elif option == 4:
            del_emp()

        else:
            print("You Entered wrong option!")


        self.enter_again()   
        
        
 
    def enter_again(self):
        start_again  = str(input("Do you wanna Continue? y/n: ")).lower().strip()

        if start_again == 'y':
            print()
            self.ask_user()
        else:
            print("Thank you, Have a good day! ")        
    
    
    
    
        
    def load_student_data(self):
        
        if db_connection.is_connected() == False:  
            db_connection.connect()  
            self.calDOB.delete(0, tk.END)#clears the date entry widget  
            self.tvStudent.delete(*self.tvStudent.get_children()) # clears the treeview tvStudent  
            # Inserting record into student_master table of student database  
            db_cursor.execute("use Student") # Interact with Bank Database  
            sql = "SELECT rollno,fname,lname,city,state,mobileno,date_format(dob,'%d-%m-%Y') FROM student_master"  
            db_cursor.execute(sql)  
            total = db_cursor.rowcount  
            #if total ==0:  
            #mb.showinfo("Info", "Nothing To Display,Please add data")  
            #return  
            print("Total Data Entries:" + str(total))  
            rows = db_cursor.fetchall()  
            RollNo = ""  
            First_Name = ""  
            Last_Name = ""  
            City = ""  
            State = ""  
            Phone_Number = ""  
            DOB =""  
        for row in rows:  
            RollNo = row[0]  
            First_Name = row[1]  
            Last_Name = row[2]  
            City = row[3]  
            State = row[4]  
            Phone_Number = row[5]  
            DOB = row[6]  
            self.tvStudent.insert("", 'end', text=RollNo, values=(RollNo, First_Name, Last_Name, City, State, Phone_Number,DOB))  
    
    
if __name__ == "__main__":  
    emp_data = Employee()
    emp_data.ask_user()