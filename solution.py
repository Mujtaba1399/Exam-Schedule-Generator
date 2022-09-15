import csv
import math
import random
import copy
numberOfSlots = 10


#IMPORTING DATA ================================================================================================================

#Importing Student Names information : 1-200
StudentNamesA = []
with open('studentNames.csv','rt')as f:
    StudentNames = csv.reader(f)
    for row in StudentNames:
        StudentNamesA.append(row)

#Importing Student Course information : 0-819
StudentCourseA = []
with open('studentCourse.csv','rt')as g:
    StudentCourse = csv.reader(g)
    for row in StudentCourse:
        StudentCourseA.append(row)

#Importing teachers information : 0-63 *REMOVE EMPTY ROWS*
teachersA = []
with open('teachers.csv','rt')as h:
    teachers = csv.reader(h)
    for row in teachers:
        if row == []:
            break
        if row != [] :
            teachersA.append(row)

#Importing courses information : 0-26
coursesA = []
with open('courses.csv','rt')as i:
    courses = csv.reader(i)
    for row in courses:
        if row != []:
            coursesA.append(row)




#REMOVING DUPLICATES ================================================================================================================

#Remove Duplicates from teachers
current = 0
for i in teachersA:
    currentCheck = current + 1
    while currentCheck < len(teachersA):   
        if( i == teachersA[currentCheck]):
            teachersA.pop(currentCheck)
        else:
            currentCheck = currentCheck + 1
    current = current + 1   

#Remove Duplicates from courses
current = 0
for i in coursesA:
    currentCheck = current + 1
    while currentCheck < len(coursesA):
        if( i[0] == coursesA[currentCheck][0]):
            coursesA.pop(currentCheck)
        else:
            currentCheck = currentCheck + 1
    current = current + 1     

#Remove Duplicates from students
current = 0
for i in StudentNamesA:
    currentCheck = current + 1
    while currentCheck < len(StudentNamesA):  
        if( i[0] == StudentNamesA[currentCheck]):
            StudentNamesA.pop(currentCheck)
        else:
            currentCheck = currentCheck + 1
    current = current + 1 

#Remove Duplicates from students course information
current = 0
for i in StudentCourseA:
    currentCheck = current + 1
    while currentCheck < len(StudentCourseA):
        if( i[1] == StudentCourseA[currentCheck][1] and i[2] == StudentCourseA[currentCheck][2]):
            StudentCourseA.pop(currentCheck)
        else:
            currentCheck = currentCheck + 1
    current = current + 1 
            


#Check how many students in each course
courseIndexInFile = [0] * 29
counter = 0
for name in coursesA:
    for courseName in StudentCourseA:   
        if name[0] == courseName[2]:
            courseIndexInFile[counter] = courseIndexInFile[counter] + 1
    counter = counter + 1





#EXAM SLOT CLASS================================================================================================================

#One Exam Slot ( ie : One gene ) 
class ExamSlot:

    def __init__(self):
        self.teachersInslot = []
        self.examsInslot = []
        self.studentsInslot = []
        self.studentClashes = 0
        self.studentsPerExam = []

    def studentPopulation(self):
        #Instantiate student population (without duplicates)
        for name in self.examsInslot:
            for studentName in StudentCourseA:
                #Check if student is registered for exam
                if studentName[2] == name[0]:
                    #Check if student is already present in list
                    found = False
                    for n in self.studentsInslot:
                        if n == studentName[1]:
                            found = True
                    #If student is not already present in list , add
                    if found == False:
                        self.studentsInslot.append(studentName[1]) 
                              
    def roomsRequired(self):
        rooms = 0
        del self.studentsPerExam[:]
        #Check how many rooms per exam to add teachers according to necessity
        #Check how many students per exam
        courseIndexInFile = [0] * len(self.examsInslot)
        counter = 0
        for name in self.examsInslot:
            for courseName in StudentCourseA:    
                if name[0] == courseName[2]:
                    courseIndexInFile[counter] = courseIndexInFile[counter] + 1
            counter = counter + 1
        for a in courseIndexInFile:
            self.studentsPerExam.append(a)  
        #Per subject , add total number of teachers required
        for j in courseIndexInFile:
            rooms = rooms + math.ceil(j/28)
        c = 0
        for i in self.studentsPerExam:
            self.studentsPerExam[c] = math.ceil(i/28)
            c = c+1
        #Rooms is now number of rooms that are required
        return rooms





#SCHEDULE CLASS================================================================================================================

class Schedule:

    def __init__(self):
        self.slots = []
        self.fitness=[]
        self.totalExams = 0 
        self.ExamSlotClashes = []
        self.TeacherDouble = 0
        self.StudentDouble = 0

    def copySchedule(self,sched):
        self.slots = copy.deepcopy(sched.slots)
        self.fitness=copy.deepcopy(sched.fitness)
        self.totalExams = sched.totalExams
        self.ExamSlotClashes = copy.deepcopy(sched.ExamSlotClashes)
        self.TeacherDouble = sched.TeacherDouble
        self.StudentDouble = sched.StudentDouble

    def createScheduleUpdated(self):
        global numberOfSlots
        temp = copy.deepcopy(coursesA)
        random.shuffle(temp)
        #How to create schedule initially itself, where no clashes inside slots , and all subjects assigned ?
        #Take empty schedule , and array of courses
        #For each course : from slot 1 , check A) If there is clash B) If adding makes more than 10 rooms.If A-B are False
        #Add to current slot
        #If any exams are leftover , create new slots in schedule

        #Create 10 Exam slots 
        count = 0
        while count < numberOfSlots:
            self.slots.append(ExamSlot())
            count = count + 1 

        previousIteration = 0
        nextIteration = -1
        while len(temp) != 0 :
            skip = False
            if(previousIteration == nextIteration):
                #Only way to resolve clashes is to add more slots:
                self.slots.append(ExamSlot())
                numberOfSlots = numberOfSlots + 1
                self.slots[numberOfSlots-1].studentPopulation()
                self.checkFitness()
                skip = True

            previousIteration = len(temp)
            examDone = 0
            for i in temp:
                #For each course , assign to clash free slot with available rooms
                counter = 0
                while counter < numberOfSlots:
                    if(skip == True):
                        counter = numberOfSlots - 1

                    #Check Clashes                
                    previousClashes = self.slots[counter].studentClashes
                    
                    self.slots[counter].examsInslot.append(i)
                    #Assign student population to each slot
                    initi = 0
                    while initi < numberOfSlots:
                        self.slots[initi].studentPopulation()
                        #print(self.slots[initi].studentsInslot)
                        initi = initi + 1

                    self.checkFitness()
                    newClashes = self.slots[counter].studentClashes
                
                    #Check number of rooms
                    roomsNeeded = self.slots[counter].roomsRequired()

                    #If no clashes and rooms are available , then add to current slot
                    if(newClashes == 0) and roomsNeeded <= 10:    
                        temp.pop(examDone)
                        break
                    else:
                        self.slots[counter].examsInslot.pop()

                        #Assign student population to each slot
                        initi = 0
                        while initi < numberOfSlots:
                            self.slots[initi].studentPopulation()
                            #print(self.slots[initi].studentsInslot)
                            initi = initi + 1

                        self.checkFitness()
                    counter = counter + 1
                examDone = examDone + 1
            nextIteration = len(temp)

            print("Number Of Courses Which have been added (without clashes) : " , end = " ")
            print(len(coursesA) - len(temp))
            print("Teachers Assigned :  NO")

    def createSchedule(self):
        tempTeachers = copy.deepcopy(teachersA)
        numberOfExams = len(coursesA)
        count = 0
        temp = copy.deepcopy(coursesA)
        #Create 10 Exam slots 
        while count < numberOfSlots:
            self.slots.append(ExamSlot())
            count = count + 1        

        #Assign each course to a specific slot
        singleIteration = math.floor((len(coursesA)/numberOfSlots)) * 10
        randomAssigned = len(coursesA) - singleIteration
        inn = 0
        while inn < singleIteration:
            #add exams to exam slots
            self.slots[inn%numberOfSlots].examsInslot.append(temp.pop(0))
            inn = inn + 1

        innn = 0
        #How to create schedule initially itself, where no clashes inside slots , and all subjects assigned ?
        #Take empty schedule , and array of courses
        #For each course : from slot 1 , check A) If there is clash B) If adding makes more than 10 rooms.If A-B are False
        #Add to current slot
        #If any exams are leftover , create new slots in schedule
        while innn < randomAssigned:
            self.slots[random.randint(0,9)].examsInslot.append(temp.pop(0))
            innn = innn + 1

        #Assign student population to each slot
        initi = 0
        while initi < numberOfSlots:
            self.slots[initi].studentPopulation()
            #print(self.slots[initi].studentsInslot)
            initi = initi + 1    

        #Assign teachers to each slot
        teachCount = 0
        while teachCount < numberOfSlots:
            current = 0
            while current < self.slots[teachCount].roomsRequired():
                    #LEave teachers unassigned in later slots and readjust in fitness
                    if(len(tempTeachers) == 0) :
                        break
                    self.slots[teachCount].teachersInslot.append(tempTeachers.pop(0))
                    current = current + 1
            teachCount = teachCount + 1

    def checkFitness(self):
        fitness1 = [0] * len(coursesA)
        #Check if each course has an exam scheduled
        overall = True
        counter = 0
        for exam in coursesA:
            found = False
            for sl in self.slots:
                if(exam in sl.examsInslot) == True:
                    found = True     
            if found == False:
                overall = False
            else:
                fitness1[counter] = fitness1[counter] + 1     
            counter = counter + 1

        # print("fitness1  [self.fitness]************************************************")
        # print(fitness1)
        count = 0
        for e in fitness1:
            count = count + e
        #Store result of first constraint check in fitness array value 0
        self.fitness = fitness1 
        self.totalExams = count

        #Check if students are giving more than one exam at one time
        fitness2 = [0]*numberOfSlots
        #Check first exam slots
        count = 0 
        while count < numberOfSlots:
            #For Each student , check for clashes by picking up which courses they're registered in , and then 
            #checking whether there is more than of those scheduled in the current slot
            for stu in self.slots[count].studentsInslot:
                currentCourses = []
                #Find which courses student is registered in
                for x in StudentCourseA:
                    if x[1] == stu:
                        if not (x[2] in currentCourses):
                            currentCourses.append(x[2])
                #Find how many of those courses are in current slot
                counter = 0
                for x in self.slots[count].examsInslot:
                    for y in currentCourses:
                        if x[0] == y:
                            counter = counter + 1
                if(counter > 1):
                    fitness2[count] = fitness2[count] + 1
            count = count + 1

        #Fitness 2 is number of students with clashes in current slot
        # print("fitness2   [examSlotClashes]************************************************")
        # print(fitness2)    
        self.ExamSlotClashes = fitness2
        current = 0
        for a in self.slots:
            a.studentClashes = self.ExamSlotClashes[current]
            current = current + 1
              
        #Check whether any teacher is invigilating two slots in a row
        fitness3 = [0]*9       
        teacherClash = 0
        count = 0
        while count < 9:
            for x in self.slots[count].teachersInslot:
                for y in self.slots[count+1].teachersInslot:
                    if(x == y):
                        fitness3[count] = fitness3[count] + 1
            count = count + 1

        # print("fitness3   [teacherDouble]************************************************")
        # print(fitness3)
        self.TeacherDouble = fitness3

        #Check whether any student has two exams in a row
        fitness4 = [0]*9       
        studentClash = 0
        count = 0
        while count < 9:
            for x in self.slots[count].studentsInslot:
                for y in self.slots[count+1].studentsInslot:
                    if(x == y):
                        fitness4[count] = fitness4[count] + 1
            count = count + 1

        # print("fitness4   [studentDouble]************************************************")
        # print(fitness4)
        self.StudentDouble = fitness4

    def returnFitness(self):
        slotsWithClashes = 0
        for i in self.ExamSlotClashes:
            if i > 0:
                slotsWithClashes = slotsWithClashes + 1
        onlyTest = slotsWithClashes
        for i in self.StudentDouble:
            if i > 0:
                slotsWithClashes = slotsWithClashes + 1
        for i in self.TeacherDouble:
            if i > 0:
                slotsWithClashes = slotsWithClashes + 1
        return self.totalExams - slotsWithClashes







# CALCULATE TEACHER FITNESS =============================================================================================================

def calculateTeacherFitness(chromo):

    firstHalf = 0
    secondHalf = 0
    #First half
    c = 0
    while c < (numberOfSlots):
        #Check if current slot has any duplicate teachers
        check = 0
        for i in chromo.slots[c].teachersInslot:
            if(check == (len(chromo.slots[c].teachersInslot) - 1)):
                break
            toCheck = check + 1
            while toCheck < len(chromo.slots[c].teachersInslot):
                if(i == chromo.slots[c].teachersInslot[toCheck]):
                    firstHalf = firstHalf + 1
                    break
                toCheck = toCheck + 1
            check = check + 1
        c = c + 1   
    
    #Check how many teachers are giving a consecutive exam invigilation
    c = 0
    while c < (numberOfSlots):
        if(c == (numberOfSlots-1)):
            break       
        #Check if current slot has any duplicate teachers
        check = 0
        for i in chromo.slots[c].teachersInslot:
            for a in chromo.slots[c + 1].teachersInslot:
                if(a == i):
                    secondHalf = secondHalf + 1           
            check = check + 1
        c = c + 1   
    return firstHalf + secondHalf


def crossover(parent1, parent2):
    
    #Find exam slots of parent 1 with highest clashes
    tempValues = copy.deepcopy(parent1.ExamSlotClashes)
    tempValues.sort(reverse = True)
    #print(tempValues)

    #Find exam slots of parent 2 with lowest clashes
    tempValues2 = copy.deepcopy(parent2.ExamSlotClashes)
    tempValues2.sort()
    #print(tempValues2)

    #Remove half the slots with highest clashes from parent1 and store
    count = 0
    tempHighClashes = []
    while count < ((numberOfSlots)/2):
        current = 0
        for i in parent1.slots:
            if(i.studentClashes == tempValues[count]):
                tempHighClashes.append(parent1.slots.pop(current))
                break
            current = current + 1
        count = count + 1

    #Remove half the slots with lowest clashes from parent 2 and store
    count = 0
    tempLowClashes = []
    while count < ((numberOfSlots)/2):
        current = 0
        for i in parent2.slots:
            if(i.studentClashes == tempValues2[count]):
                tempLowClashes.append(parent2.slots.pop(current))
                break
            current = current + 1
        count = count + 1

    #Append low clash slots to parent1 and high clash slots to parent2
    c=0
    while c < (numberOfSlots/2):
        parent1.slots.append(tempLowClashes[c])
        parent2.slots.append(tempHighClashes[c])
        c = c + 1

    #Print
    parent1.checkFitness()
    parent2.checkFitness()

def mutation(parent):
    
    #Randomly mutate by changing the exam 
    index = random.randint(0,9)
    examToRemove = parent.slots[index].examsInslot.pop(0)
    current = 0

    for a in parent.slots[index].studentsInslot:
        for b in StudentCourseA:
            if(b[1] == a) and (b[2] == examToRemove[0]):
                parent.slots[index].studentsInslot.pop(current)
        current = current + 1
    
    indexToAdd = random.randint(0,len(coursesA)-1)
    parent.slots[index].examsInslot.append(coursesA[indexToAdd])
    parent.slots[index].studentPopulation()
    parent.checkFitness()
    
    return None

def mutationPhaseOne(self):

    #Take input of one schedule and find slot with lowest number of clashes
    #Remove One Exam and check number of clashes
    #If not 0 , re-insert previously removed exam , and then remove another exam and see number of clashes
    #If this doesn't give zero in any way , remove all exams and then add same number of exams randomly , then check fitness
    #If now 0 , finish
    #If not 0 , repeat initial process , until removal of one gives zero
    # Randomly add one and then check if it now gives zero or not. 
    # If yes , check whether this exam is in any other slot.If yes, remove from that slot.If no , finish
    #If doesn't give zero , remove currently inserted exam ,and add other exam and repeat until all exams have been checked
    #If no exam can be added to slot without making its clashes more than 0 , end cycle
    return None


def schedulePrinter(chrom):

    #Print Slot
    days = ["Monday" , "Monday","Tuesday","Tuesday","Wednesday" ,"Wednesday","Thursday" ,"Thursday","Friday","Friday"]
    time = ["9:00 - 12:00" , "2:00 - 5:00"]
    slot = 0

    while slot < numberOfSlots:
        room = 1
        #For Each slot , assign rooms required to each exam and print as necessary
        print("\n===========================================================================")
        print(days[slot%10])
        print(time[slot%2])
        print("")
        # print("['courseCode' , 'courseName']      ['teacherName']      ['roomNo']")
        currentExam = 0
        temp = copy.deepcopy(chrom.slots[slot].teachersInslot)
        teacherCount = 0
        for a in chrom.slots[slot].examsInslot:
            count = 0
            while count < chrom.slots[slot].studentsPerExam[currentExam]:               
                print(a , end="")
                print(chrom.slots[slot].teachersInslot[teacherCount], end="")
                print("[Room No : " + str(teacherCount) + "]")
                teacherCount = teacherCount + 1
                count = count + 1
            currentExam = currentExam + 1
        slot = slot + 1
        
def runGA():
    ## Create Initial Population
    population = []
    pop = 0
    while pop < 8:
        population.append(Schedule())
        population[pop].createSchedule()
        population[pop].checkFitness()
        pop = pop + 1
    
    #print(population)
    ## Select parent
    cu = 0
    while cu < 100:
        #Find fitness of each schedule
        populationFitness=[0]*8
        count = 0
        for i in population:
            populationFitness[count]=i.returnFitness()
            count = count + 1
        #print(populationFitness)

        #Choose two parents with highest fitness
        max1 = float('-inf')
        max1Index = 0
        current = 0

        for a in populationFitness:
            if a > max1:
                max1 = a
                max1Index = current
            current = current + 1

        max2 = float('-inf')
        max2Index = 0
        current = 0
        for a in populationFitness:
            if a > max2 and a != max1:
                max2 = a
                max2Index = current
            current = current + 1    

        if max2 == float('-inf'):
            max2 = max1
            max2Index = 1
        
        ## Apply crossover and mutation
        #crossover(population[max1Index],population[max2Index])
        ind = random.randint(0,7)
        mutation(population[ind])
        ## Calculate Fitness of population
        populationFitness=[0]*8
        count = 0
        for i in population:
            populationFitness[count]=i.returnFitness()
            count = count + 1
        print(populationFitness)
        
        ## Find fittest cadidates
        ### print Every 100th generation results
        cu = cu + 1


def runningGA():
        
    ## Create Initial Population
    population = []
    pop = 0
    while pop < 8:
        population.append(Schedule())
        if pop == 0:
            population[pop].createScheduleUpdated()
        else:
            population[pop].copySchedule(population[0])
        pop = pop + 1
        
    #Teachers 
    temp = copy.deepcopy(teachersA)
    random.shuffle(temp)
    c = 0
    while c < 8:
        n = 0
        while n < numberOfSlots:
            currentLimit = population[c].slots[n].roomsRequired()
            t = 0
            while t < currentLimit:
                if(len(temp) == 0):
                    temp = copy.deepcopy(teachersA)
                    random.shuffle(temp)
                population[c].slots[n].teachersInslot.append(temp.pop(0))
                t = t + 1
            n = n + 1
        c = c + 1  
        
    #Finding suitable Teacher distribution
    c = 0
    fittest = 0
    while c < 8:
        n = 0      
        if  (calculateTeacherFitness(population[c])) == 0:
            fittest = c
            break
        c = c + 1  

    print("\n-----------------------------------------------------------------")
    print("Number of Courses added without clashes : ALL")
    print("Teachers Assigned : YES")
    print("-----------------------------------------------------------------")
        
    #Printing Teachers and rooms in each schedule
    
    schedulePrinter(population[fittest])  

    # print(population)
    ## Select parent

    #Find fitness of each schedule
    #print(populationFitness)
    #Choose two parents with highest fitness 
    ## Apply crossover and mutation
    #crossover(population[max1Index],population[max2Index]) 
    ## Calculate Fitness of population   
    ## Find fittest cadidates   
    ### print Every 100th generation results
        
#print(test1.returnFitness())
runningGA()