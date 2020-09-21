# this is the model for the program

import requests
from bs4 import BeautifulSoup as bs
import lxml
import os

class Crawler:

    def __init__(self, username, password, link):

        # instance variables
        session = requests.Session()
        self.session = session

        self.username = username
        self.password = password
        self.link = link

        # login token
        self.token = ""

        # 
        self.response = self.session.get(link)
        self.soup = bs(self.response.content, 'lxml')

        # mycourses
        self.mycourses = []
        self.courseLinks = []
    # get response from the website
    def get_token(self):
        self.token = self.soup.find("input", attrs={"name": "logintoken"})["value"]
        return self.token
    
    # login
    def login(self):
        # url
        data = {
            "username": self.username,
            "password": self.password,
            "logintoken": self.get_token()
        }
        # post to login
        response = self.session.post(self.link, data=data)
        return response.content

    def list_all_courses(self):
        import os
        if (os.path.exists("courses.txt")):
            # load from local storage
            with open("courses.txt", "r") as file:
                content = file.readlines()
                for course in content:
                    self.mycourses.append(course.split("%")[0])
                    self.courseLinks.append(course.split("%")[1])
        else:
            courses = {

            }
            # login first
            soup = bs(self.login(), 'lxml')
            content = soup.find("div", attrs={"id": "frontpage-course-list"})
            courselinks = content.findAll("a")
            for course in courselinks:
                title = course.get_text()
                link = course["href"]

                self.mycourses.append(title)
                self.courseLinks.append(link)

                # check if the file exists
                # write to file for temporary storage
                with open("courses.txt", "a") as file:
                    file.writelines(title + "%" + link + "\n")    
        return self.mycourses, self.courseLinks
    
    def list_all_homeworks(self, courseLink):
        allHomeworks = []
        self.login()
        
        # access the website
        response = self.session.get(courseLink).content

        data = bs(response, 'lxml')

        # find activity
        activities = data.findAll("li", {"class": "activity quiz modtype_quiz"})

        for activity in activities:
            rs = self.session.get(activity.a["href"])
            data = bs(rs.content, 'lxml')

            # find the due date
            due_date = data.find("div", {"class": "box py-3 quizinfo"})

            # check for attempt quiz button
            btn = data.find("div", {"class": "singlebutton quizstartbuttondiv"})
            if not btn is None:
                print(activity.get_text())
                print(due_date.get_text())
                print("----------------------------------------------")
                allHomeworks.append(due_date.get_text())
        return allHomeworks

