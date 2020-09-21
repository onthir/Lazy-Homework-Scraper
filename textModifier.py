# this will extract the date from the given text


def text_breaker(string):
    text = "Attempts allowed: 8\nThis quiz opened at Monday, August 17, 2020, 12:20 PM\nThis quiz will close on Monday, November 2, 2020, 11:59 PM.\nGrading method: Last attempt"

    # seperate into list
    laist = string.split("\n")

    # get only the due date
    laist = ''.join(x for x in laist if 'close' in x)

    # replace unnecessary text
    laist = laist.replace("This quiz will close on ", "Due Date: ")
    return laist

# date text to date
def date_break(string):
    # format is Monday, August 17, 2020, 20:08 AM.
    dateString = string.split(",")
    day_of_week = dateString[0]
    full_date = dateString[1] + "," + dateString[2]
    time = dateString[3]


    # august 17
    daySplit = dateString[1].strip().split(" ")[1]
    monthSplit = dateString[1].strip().split(" ")[0]
    yearSplit = dateString[2]

    formatted = daySplit + " " + monthSplit + "," + yearSplit
    from datetime import datetime

    new_date = datetime.strptime(formatted, '%d %B, %Y')
    return new_date.strftime("%Y-%m-%d")

date_break("Monday, August 17, 2020, 20:08 AM.")