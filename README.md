# Exam Schedule Generator using Genetic Algorithm

The exam scheduling problem is solved using a Genetic Algorithm.
### Requirements:
Given inputs would be datasets that include:
* student names 
* teacher names 
* course names 
* student registration information. 

Using given information , we were supposed to find a solution that fulfilled certain hard constraints and certain soft constraints. 
The idea was to generate a population of schedules , each of which was assigned a calculated fitness value , and then use the crossover function on the schedules with the highest fitness , along with random mutation ,to incrementally generate solutions with better fitness , until we finally achieved a desired solution.

### Implementation:
The implementation was done to maximize chances of fulfilling hard constraints. 
The schedule was setup to instantiate an order in which all the exams in the given dataset are included in the schedule . 
Also , there are no clashes in the exams ie : No student who is registered for a subject , will have an exam for another course they are registered in, in the same slot. 
The next step was to insert teachers into the schedule without letting a teacher invigilate more than one exam in a single slot , and also without letting a teacher invigilate in twoconcurrent slots.

#### Implemented hard constraints:
* An exam will be scheduled for each course.
* A student is enrolled in at least 3 courses. A student cannot give more than 1 exam at a time.
* Exam will not be held on weekends.
* Each exam must be held between 9 am and 5 pm
* Each exam must be invigilated by a teacher. 
* A teacher cannot invigilate two exams at the same time.
* A teacher cannot invigilate two exams in a row.
* 28 students per room

#### Implemented soft constraints:
* All students and teachers shall be given a break on Friday from 1-2.
* Input data for each exam are teachers’ names, students’, exam duration, courses (course codes), and list of allowed classrooms.