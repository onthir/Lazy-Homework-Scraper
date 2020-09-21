# main framework

from framework import *
from getpass import *
from textModifier import *

idealList = []
sortedDates = []
# ask the user to login

print("Logging into Moodle\n\n")


# read credentials
with open("credentials.txt", 'r') as file:
    content = file.readlines()

username = content[0].replace("\n", "")
password = content[1].replace("\n", "")

gmailEmail = content[2].replace("\n", "")
gmailPassword = content[3].replace("\n", "")



crawler = Crawler(username, password, "https://moodle.ulm.edu/login/index.php")

print("These are the Courses I found on your Moodle: ")

# list all courses

courses = crawler.list_all_courses()

idx = 1
for course in courses[0]:
    print(str(idx) + ". " + str(course))

    idx += 1
print("\n---------------------------------")

ask = input("Enter Course Number (1/2/3... or 1,2,3 for multiple courses): ")

if len(str(ask)) == 1:
    # course link
    ask = int(ask)
    courseLink = courses[1][ask-1]

    courseName = courses[0][ask-1]
    print("\nChecking Homework for " + str(courses[0][ask-1]))
    print("\n---------------------------------\n")

    homeworks = crawler.list_all_homeworks(courseLink)
    # print(homeworks)

    for homework in homeworks:
        homework = text_breaker(homework)
        idealList.append((homework, False))

    from googlekeep import *

    createNote(courseName, idealList, gmailEmail, gmailPassword)
else:
    nums = ask.split(",")
    for num in nums:
        ask = int(num)
        courseLink = courses[1][ask-1]
        courseName = courses[0][ask-1]
        print("\nChecking Homework for " + str(courses[0][ask-1]))
        print("\n---------------------------------\n")

        homeworks = crawler.list_all_homeworks(courseLink)
        # print(homeworks)

        for homework in homeworks:
            homework = text_breaker(homework)
            idealList.append((homework, False))

        from googlekeep import *

        createNote(courseName, idealList, gmailEmail, gmailPassword)
        del(idealList[:])

print("Note Generated Successfully")