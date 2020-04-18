from tkinter import *
import csv
import smtplib
import pandas as pd
root = Tk()
def sendmail(name,blood):
    with open('maillist.csv', 'r', encoding="utf8") as f:
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames
        server=smtplib.SMTP("smtp.cc.iitk.ac.in",25)
        #server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("email","password")
        msg= "your friend "+name+" is in need of blood .please help him by donating.Thanks!!"
        subject ="Urgent need of Blood Group "+blood
        body = "Subject: {}\n\n{}".format(subject,msg)
        for line in d_reader:
            server.sendmail("mriduldu@iitk.ac.in","mriduldubey2001@gmail.com",body)
    print("SUCCESSFULLY SENDED")
    server.quit()
def getvals():
    print("Submitting")

    print(f"{namevalue.get(), rollnovalue.get(), gendervalue.get(), bloodgroupvalue.get(), rhfactor.get()} ")
    with open('stuffToPlot.csv', 'r', encoding="utf8") as f:
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames
        mailid=[]
        for line in d_reader:
            if(line['blood_group']==bloodgroupvalue.get()):
                mailid.append(line['username']+"@iitk.ac.in")
    print(mailid)
    df = pd.DataFrame(mailid, columns=['username'])
    df.to_csv('maillist.csv', index=False, encoding='utf-8')

    with open("records.txt", "a") as f:
        f.write(f"{namevalue.get(), rollnovalue.get(), gendervalue.get(), bloodgroupvalue.get(), rhfactor.get()}\n ")
    #sendmail(namevalue.get(),bloodgroupvalue.get())


root.geometry("500x250")
#Heading
Label(root, text="ENTER REQUIRED FIELD FOR RECIEVER", font="comicsansms 13 bold", pady=15).grid(row=0, column=3)

#Text for our form
name = Label(root, text="Name")
rollno = Label(root, text="Rollno")
gender = Label(root, text="Gender")
Bloodgroup = Label(root, text="Blood Group")
rhfactor = Label(root, text="RH FACTOR")

#Pack text for our form
name.grid(row=1, column=2)
rollno.grid(row=2, column=2)
gender.grid(row=3, column=2)
Bloodgroup.grid(row=4, column=2)
rhfactor.grid(row=5, column=2)

# Tkinter variable for storing entries
namevalue = StringVar()
rollnovalue = StringVar()
gendervalue = StringVar()
bloodgroupvalue = StringVar()
rhfactor = StringVar()


#Entries for our form
nameentry = Entry(root, textvariable=namevalue)
phoneentry = Entry(root, textvariable=rollnovalue)
genderentry = Entry(root, textvariable=gendervalue)
emergencyentry = Entry(root, textvariable=bloodgroupvalue)
paymentmodeentry = Entry(root, textvariable=rhfactor)

# Packing the Entries
nameentry.grid(row=1, column=3)
phoneentry.grid(row=2, column=3)
genderentry.grid(row=3, column=3)
emergencyentry.grid(row=4, column=3)
paymentmodeentry.grid(row=5, column=3)

#Button & packing it and assigning it a command
Button(text="Send email", command=getvals).grid(row=7, column=3)



root.mainloop()
