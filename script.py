from os import error
import random
from types import MethodDescriptorType
from flask import *
from werkzeug.utils import redirect 
import os.path
import os
from os import path

app = Flask(__name__)
data = []

@app.route('/')
def loginPage():
    return render_template('login.html')

@app.route('/signup')
def signupPage():
    return render_template('signup.html')

@app.route('/landingPage')
def landingPage():
    return render_template('landingPage.html')

# Login Operation
@app.route('/landingPage', methods = ['GET','POST'])
def enterDetails():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        fWrite = open('./files/signupDetails.txt','a')
        fRead = open('./files/signupDetails.txt','r')
        for line in fRead:
            line = line.rstrip()
            signupDetails = line.split('|')
            if signupDetails[0] == 'Username':
                continue
            if signupDetails[0] == username or signupDetails[1] == email:
                error = 'Username or Email exists'
                return render_template('signup.html',error=error)
        fWrite.write('\n' + username + '|' + email + '|' + password)
        fRead.close()
        fWrite.close()
        return render_template('landingPage.html')

# Signup Operation
@app.route('/homePage', methods = ['GET','POST'])
def checkDetails():
    if request.method == 'POST':
        error = None
        username = request.form.get('username')
        password = request.form.get('password')
        fRead = open('./files/signupDetails.txt','r')
        for line in fRead:
            line = line.rstrip()
            loginDetails = line.split('|')
            print(loginDetails[0])
            if loginDetails[0] == 'Username':
                continue
            if loginDetails[0] == username:
                if loginDetails[-1] == password:
                    return render_template('landingPage.html')
                else:
                    error = 'Password Incorrect'
                    continue
            else:
                error = 'Username does not Exist'
                continue
        if error == 'Password Incorrect':
            return render_template('login.html',error = error)
        elif error == 'Username does not exist':
            return render_template('login.html',error = error)
        fRead.close()

# Bird Record operations
@app.route('/birdRecord')
def showBirdRecord():
    heading = []                                 #Displaying animal record 
    data.clear()
    fRead = open('./files/birdRecord.txt','r')
    for line in fRead:
        line = line.rstrip()                            #Removing \n from each line
        birdRecordHeader = line.split('|')            #Converting into a list
        heading += birdRecordHeader                   #Adding Data into heading list
        if birdRecordHeader[-1] == 'Staff':           
            break
    while data == []:
        for line in fRead:
            line = line.rstrip()
            birdRecordData = line.split('|')
            data.append(birdRecordData)                   #Appending data into data list
        if data != []:
            break
    fRead.close()
    return render_template('bird.html',heading = heading, data = data)

@app.route('/addBirdRecord',methods = ['GET','POST'])
def addBirdRecord():
    if request.method == 'POST':
        birdID = request.form.get('birdID')
        name = request.form.get('name')
        species = request.form.get('species')
        diet = request.form.get('diet')
        health = ' , '.join(request.form.getlist('health'))
        staff = request.form.get('staff')
        fRead = open('./files/birdRecord.txt','r')
        fWrite = open('./files/birdRecord.txt','a')
        for line in fRead:
            line = line.rstrip()
            birdData = line.split('|')
            if birdData[0] == 'Bird ID':
                continue
            elif birdData[0] == birdID:
                error = 'Bird ID already exists'
                return redirect('/birdRecord')
            else:
                continue
        fRead.close()
        fWrite.write('\n' + birdID + '|' + name + '|' + species + '|' + diet + '|' + health + '|' + staff)
        fWrite.close()
        return redirect('/birdRecord')

@app.route('/updateBirdRecord', methods = ['GET','POST'])
def updateBirdRecord():
    if request.method == 'POST':
        fRead = open('./files/birdRecord.txt','r')
        fWrite = open('./files/tempBirdRecord.txt','w')
        birdID = request.form.get('birdID')
        line = ' '
        while(line):
            line = fRead.readline()
            updateBirdData = line.split('|')
            if updateBirdData[0] == 'Bird ID':
                fWrite.write(line)
                continue
            if updateBirdData[0] == birdID:
                health = updateBirdData[4]
                staff = updateBirdData[-1]
                name = updateBirdData[1]
                species = updateBirdData[2]
                diet = updateBirdData[3]
                replaceHealth = ','.join(request.form.getlist('health'))
                replaceStaff = request.form.get('staff')
                replaceHealth = health.replace(health,replaceHealth)
                replaceStaff = staff.replace(staff,replaceStaff)
                fWrite.write(birdID + '|' + name + '|' + species + '|' + diet + '|' + replaceHealth + '|' + replaceStaff + '\n')
            else:
                fWrite.write(line)
    fWrite.close()
    fRead.close()
    os.remove('./files/birdRecord.txt')
    os.rename('./files/tempBirdRecord.txt','./files/birdRecord.txt')
    return redirect('/birdRecord')

@app.route('/deleteBirdRecord',methods = ['GET','POST'])
def deleteBirdRecord():
    if request.method == 'POST':
        fRead = open('./files/birdRecord.txt','r')
        fWrite = open('./files/tempBirdRecord.txt','w')
        deleteRecord = request.form.get('deleteRecord')
        line = ' '
        while(line):
            line = fRead.readline()
            deleteBirdData = line.split('|')
            if deleteBirdData[0] == 'Bird ID':
                fWrite.write(line)
                continue
            if len(line) > 0:
                if deleteBirdData[0] == deleteRecord:
                    continue
                else:
                    fWrite.write(line)
    fWrite.close()
    fRead.close()
    os.remove('./files/birdRecord.txt')
    os.rename('./files/tempBirdRecord.txt','./files/birdRecord.txt')
    return redirect('/birdRecord')


# Animal Record Operations
@app.route('/animalRecord')
def showAnimalRecord():  
    heading = []                                 #Displaying animal record 
    data.clear()
    fRead = open('./files/animalRecord.txt','r')
    for line in fRead:
        line = line.rstrip()                            #Removing \n from each line
        animalRecordHeader = line.split('|')            #Converting into a list
        heading += animalRecordHeader                   #Adding Data into heading list
        if animalRecordHeader[-1] == 'Staff':           
            break
    while data == []:
        for line in fRead:
            line = line.rstrip()
            animalRecordData = line.split('|')
            data.append(animalRecordData)                   #Appending data into data list
        if data != []:
            break
    fRead.close()
    return render_template('animal.html',heading=heading, data = data)

@app.route('/addAnimalRecord',methods = ['GET','POST'])
def addAnimalRecord():
    if request.method == 'POST':
        error =  None
        animalID = request.form.get('animalID')
        name = request.form.get('name')
        species = request.form.get('species')
        diet = request.form.get('diet')
        health = ','.join(request.form.getlist('health'))
        staff = request.form.get('staff')
        fRead = open('./files/animalRecord.txt','r')
        fWrite = open('./files/animalRecord.txt','a')
        for line in fRead:
            line = line.rstrip()
            animalData = line.split('|')
            if animalData[0] == 'Animal ID':
                continue
            elif animalData[0] == animalID:
                error = 'Animal ID already exists'
                return render_template('animal.html',error = error)
            else:
                continue
        fRead.close()
        fWrite.write(animalID + '|' + name + '|' + species + '|' + diet + '|' + health + '|' + staff + '\n')
        fWrite.close()
        return redirect('/animalRecord')

@app.route('/updateAnimalRecord', methods = ['GET','POST'])
def updateAnimalRecord():
    if request.method == 'POST':
        fRead = open('./files/animalRecord.txt','r')
        fWrite = open('./files/tempAnimalRecord.txt','w')
        animalID = request.form.get('animalID')
        line = ' '
        while(line):
            line = fRead.readline()
            updateAnimalData = line.split('|')
            if updateAnimalData[0] == 'Animal ID':
                fWrite.write(line)
                continue
            if updateAnimalData[0] == animalID:
                name = updateAnimalData[1]
                species = updateAnimalData[2]
                diet = updateAnimalData[3]
                # health = updateAnimalData[4]
                # staff = updateAnimalData[-1]
                replaceHealth = ','.join(request.form.getlist('health'))
                replaceStaff = request.form.get('staff')
                # replaceHealth = health.replace(health,replaceHealth)
                # replaceStaff = staff.replace(staff,replaceStaff)
                fWrite.write(animalID + '|' + name + '|' + species + '|' + diet + '|' + replaceHealth + '|' + replaceStaff + '\n')
            else:
                fWrite.write(line)
    fWrite.close()
    fRead.close()
    os.remove('./files/animalRecord.txt')
    os.rename('./files/tempAnimalRecord.txt','./files/animalRecord.txt')
    return redirect('/animalRecord')

@app.route('/deleteAnimalRecord',methods = ['GET','POST'])
def deleteAnimalRecord():
    if request.method == 'POST':
        fRead = open('./files/animalRecord.txt','r')
        fWrite = open('./files/tempAnimalRecord.txt','w')
        deleteRecord = request.form.get('deleteRecord')
        line = ' '
        while(line):
            line = fRead.readline()
            deleteAnimalData = line.split('|')
            if deleteAnimalData[0] == 'Animal ID':
                fWrite.write(line)
                continue
            if len(line) > 0:
                if deleteAnimalData[0] == deleteRecord:
                    continue
                else:
                    fWrite.write(line)
    fWrite.close()
    fRead.close()
    os.remove('./files/animalRecord.txt')   
    os.rename('./files/tempAnimalRecord.txt','./files/animalRecord.txt')
    return redirect('/animalRecord')

@app.route('/searchAnimalRecord', methods = ['GET','POST'])
def searchAnimalRecord():
    heading = []
    data.clear()
    if request.method == 'POST':
        searchID = request.form.get('searchID')
        with open('./files/animalRecord.txt','r') as fRead:
            for line in fRead:
                line = line.rstrip()
                search_animal = line.split('|')
                if search_animal[0] == 'Animal ID':
                    stringSearchAnimal = '|'.join(search_animal)


#Visitor Record operations
@app.route('/visitorRecord')
def showVisitorRecord():  
    heading = []                                 #Displaying visitor record 
    data.clear()
    fRead = open('./files/visitorRecord.txt','r')
    for line in fRead:
        line = line.rstrip()                            #Removing \n from each line
        visitorRecordHeader = line.split('|')            #Converting into a list
        heading += visitorRecordHeader                   #Adding Data into heading list
        if visitorRecordHeader[-1] == 'Visit Date':           
            break
    while data == []:
        for line in fRead:
            line = line.rstrip()
            visitorRecordData = line.split('|')
            data.append(visitorRecordData)                   #Appending data into data list
        if data != []:
            break
    fRead.close()
    return render_template('visitor.html',heading=heading, data = data)

@app.route('/addVisitorRecord',methods = ['GET','POST'])
def addVisitorRecord():
    if request.method == 'POST':
        error =  None
        visitorID = request.form.get('visitorID')
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        entryTime = request.form.get('entryTime')
        exitTime = request.form.get('exitTime')
        visitedDate = request.form.get('visitedDate')

        fRead = open('./files/visitorRecord.txt','r')
        fWrite = open('./files/visitorRecord.txt','a')
        for line in fRead:
            line = line.rstrip()
            visitorData = line.split('|')
            if visitorData[0] == 'Visitor ID':
                continue
            elif visitorData[0] == visitorID:
                error = 'Visitor ID already exists'
                return render_template('visitor.html',error = error)
            else:
                continue
        fRead.close()
        fWrite.write('\n' + visitorID + '|' + name + '|' + mobile + '|' + entryTime + '|' + exitTime + '|' + visitedDate)
        fWrite.close()
        return redirect('/visitorRecord')

@app.route('/editVisitorRecord', methods = ['GET','POST'])
def updateVisitorRecord():
    if request.method == 'POST':
        fRead = open('./files/visitorRecord.txt','r')
        fWrite = open('./files/tempVisitorRecord.txt','w')
        visitorID = request.form.get('visitorID')
        line = ' '
        while(line):
            line = fRead.readline()
            updateVisitorData = line.split('|')
            if updateVisitorData[0] == 'Visitor ID':
                fWrite.write(line)
                continue
            if updateVisitorData[0] == visitorID:
                name = updateVisitorData[1]
                mobile = updateVisitorData[2]
                entryTime = request.form.get('entryTime')
                exitTime = request.form.get('exitTime')
                visitedDate = request.form.get('visitedDate')
                fWrite.write(visitorID + '|' + name + '|' + mobile + '|' + entryTime + '|' + exitTime + '|' + visitedDate + '\n')
            else:
                fWrite.write(line)
    fWrite.close()
    fRead.close()
    os.remove('./files/visitorRecord.txt')
    os.rename('./files/tempVisitorRecord.txt','./files/visitorRecord.txt')
    return redirect('/visitorRecord')

@app.route('/deleteVisitorRecord',methods = ['GET','POST'])
def deleteVisitorRecord():
    if request.method == 'POST':
        fRead = open('./files/visitorRecord.txt','r')
        fWrite = open('./files/tempVisitorRecord.txt','w')
        deleteVisitorRecord = request.form.get('visitorID')
        line = ' '
        while(line):
            line = fRead.readline()
            deleteVisitorData = line.split('|')
            if deleteVisitorData[0] == 'Visitor ID':
                fWrite.write(line)
                continue
            if len(line) > 0:
                if deleteVisitorData[0] == deleteVisitorRecord:
                    continue
                else:
                    fWrite.write(line)
    fWrite.close()
    fRead.close()
    os.remove('./files/visitorRecord.txt')
    os.rename('./files/tempVisitorRecord.txt','./files/visitorRecord.txt')
    return redirect('/visitorRecord')


#Staff Record operations
@app.route('/staffRecord')
def showstaffRecord():  
    heading = []                                #Displaying animal record 
    data.clear()
    fRead = open('./files/staffRecord.txt','r')
    for line in fRead:
        line = line.rstrip()                          #Removing \n from each line
        staffRecordHeader = line.split('|')           #Converting into a list
        heading += staffRecordHeader                  #Adding Data into heading list
        if staffRecordHeader[-1] == 'Position':   
            break
    while data == []:
        for line in fRead:
            line = line.rstrip()
            staffRecordData = line.split('|')
            data.append(staffRecordData)                #Appending data into data list`  
        if data != []:
            break
    fRead.close()
    return render_template('staff.html',heading=heading, data = data)

@app.route('/addStaffRecord',methods = ['GET','POST'])
def addStaffRecord():
    if request.method == 'POST':
        error =  None
        staffID = request.form.get('staffID')
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        position = request.form.get('position')

        fRead = open('./files/staffRecord.txt','r')
        fWrite = open('./files/staffRecord.txt','a')
        for line in fRead:
            line = line.rstrip()
            staffData = line.split('|')
            if staffData[0] == 'Staff ID':
                continue
            elif staffData[0] == staffID:
                error = 'Staff ID already exists'
                return render_template('staff.html',error = error)
            else:
                continue
        fRead.close()
        fWrite.write('\n' + staffID + '|' + name + '|' + mobile + '|' + position)
        fWrite.close()
        return redirect('/staffRecord')

@app.route('/editStaffRecord', methods = ['GET','POST'])
def updatestaffRecord():
    if request.method == 'POST':
        fRead = open('./files/staffRecord.txt','r')
        fWrite = open('./files/tempstaffRecord.txt','w')
        staffID = request.form.get('staffID')
        line = ' '
        while(line):
            line = fRead.readline()
            updateStaffData = line.split('|')
            if updateStaffData[0] == 'Staff ID':
                fWrite.write(line)
                continue
            if updateStaffData[0] == staffID:
                name = request.form.get('name')
                mobile = request.form.get('mobile')
                position = request.form.get('position')
                fWrite.write(staffID + '|' + name + '|' + mobile + '|' + position + '\n')
            else:
                fWrite.write(line)
    fWrite.close()
    fRead.close()
    os.remove('./files/staffRecord.txt')
    os.rename('./files/tempstaffRecord.txt','./files/staffRecord.txt')
    return redirect('/staffRecord')

@app.route('/deleteStaffRecord',methods = ['GET','POST'])
def deleteStaffRecord():
    if request.method == 'POST':
        fRead = open('./files/staffRecord.txt','r')
        fWrite = open('./files/tempStaffRecord.txt','w')
        deleteStaffRecord = request.form.get('deleteStaffRecord')
        line = ' '
        while(line):
            line = fRead.readline()
            deleteStaffData = line.split('|')
            if deleteStaffData[0] == 'Staff ID':
                fWrite.write(line)
                continue
            if len(line) > 0:
                if deleteStaffData[0] == deleteStaffRecord or deleteStaffData[1] == deleteStaffRecord:
                    continue
                else:
                    fWrite.write(line)
    fWrite.close()
    fRead.close()
    os.remove('./files/staffRecord.txt')
    os.rename('./files/tempStaffRecord.txt','./files/staffRecord.txt')
    return redirect('/staffRecord')

if __name__ == '__main__':
    app.run(debug=True)