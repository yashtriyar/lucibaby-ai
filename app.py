import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np
import pyttsx3
import wikipedia
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import pytz
from dateutil import parser
import requests



def weather(city):
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=372c72d69c373cea51da25e1a8b85d70'

# Make the HTTP request
    response = requests.get(url)

    # Check the response status code
    if response.status_code == 200:
        # The request was successful, so get the weather data
        weather_data = response.json()
        say('Current weather in {}:'.format(weather_data['name']))
        say('  Temperature: {}°C'.format(weather_data['main']['temp']))
        say('  Feels like: {}°C'.format(weather_data['main']['feels_like']))
        say('  Humidity: {}%'.format(weather_data['main']['humidity']))
        say('  Wind speed: {}m/s'.format(weather_data['wind']['speed']))

        # Print the current weather conditions
        print('Current weather in {}:'.format(weather_data['name']))
        print('  Temperature: {}°C'.format(weather_data['main']['temp']))
        print('  Feels like: {}°C'.format(weather_data['main']['feels_like']))
        print('  Humidity: {}%'.format(weather_data['main']['humidity']))
        print('  Wind speed: {}m/s'.format(weather_data['wind']['speed']))

    else:
        # The request failed, so print an error message
        print('Error getting weather data')
        say('Error getting weather data')

#extra part-------------------------------------------------------------------------------------------------
reminders = []

def setReminder(text, reminder_time):
    reminders.append((text, reminder_time))

def checkReminders():
    #current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    for reminder in reminders:
        reminder_text = reminder[0]
        reminder_time = reminder[1]
        say(f"Reminder: {reminder_text} is scheduled on {reminder_time}")
        # if current_time >= reminder_time:
        #     say(f"Reminder: {reminder_text}")
        #     reminders.remove(reminder)

def parseReminderDateTime(reminder_time):
    try:
        parsed_time = parser.parse(reminder_time)
        formatted_time = parsed_time.strftime("%Y-%m-%d %H:%M")
        return formatted_time
    except ValueError:
        return None
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
todo_list = []
def addTask(task_content):
    todo_list.append(task_content)
    say(f"Task '{task_content}' added to the to-do list.")
    print(f"Task '{task_content}' added to the to-do list.")

def printTodoList():
    if not todo_list:
        say("The to-do list is empty.")
        print("The to-do list is empty.")
    else:
        say("To-Do List:")
        print("To-Do List:")
        for i, task in enumerate(todo_list):
            say(f"{i+1}. {task}")
            print(f"{i+1}. {task}")
#------------------------------------------------------------------------------------------------------------
chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Triyar: {query}\n Luci Baby: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


#own try catch changes-------------------------------------------------------------------------------------------------

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        text += response["choices"][0]["text"]
    except Exception as e:
        # Handle the exception here
        text += f"An error occurred: {str(e)}"

    if not os.path.exists("Openai"):
        os.makedirs("Openai")

    filename = f"Openai/prompt-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    with open(os.path.join(os.path.dirname(__file__), filename), 'w') as f:
        f.write(text)
#------------------------------------------------------------------------------------------------------
#-------------------OWN Addition----------------------------------------------
def search_wikipedia(query):
    
    try:
        # search for the query on Wikipedia
        search_results = wikipedia.search(query)

        # print the search results
        print("Search Results:")
        for i, result in enumerate(search_results):
            print(f"{i+1}. {result}")

        # ask user to select a result
        selection = int(input("Enter selection number: ")) - 1
        page = wikipedia.page(search_results[selection])

        # print the summary of the selected page
        print("\nSummary:")
        print(page.summary)

    except wikipedia.exceptions.DisambiguationError as e:
        # handle disambiguation error
        print("The search query may refer to multiple pages. Please try again with a more specific query.")
    except wikipedia.exceptions.PageError as e:
        # handle page not found error
        print("The requested page could not be found on Wikipedia. Please try again with a different query.")
#----------------------------------------------------------------------------------






#--------------------------------------------------------------------------------------
def sendEmail(subject, message, to_email):
    # Sender's email address and password
    from_email = "Your Email Address"
    password = "Your Password"

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # Add message body
    msg.attach(MIMEText(message, "plain"))

    # Connect to the email server and send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
#-----------------------------------------------------------------------------------------------------------
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            if "quit" in query.lower():  # Check if the user wants to quit
                exit()
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Luci Baby"


if __name__ == '__main__':
    print('Welcome to Luci Baby A.I')
    say("Luci Baby A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        # todo: Add more sites
        sites = [["portfolio", "https://yashtriyar.netlify.app/"],["youtube", "https://www.youtube.com"],["wikipedia", "https://www.wikipedia.com"],["google", "https://www.google.com"],["facebook", "https://www.facebook.com"],["twitter", "https://www.twitter.com"],["instagram", "https://www.instagram.com"],["reddit", "https://www.reddit.com"],["linkedin", "https://www.linkedin.com"],["pinterest", "https://www.pinterest.com"],["tumblr", "https://www.tumblr.com"],["ebay", "https://www.ebay.com"],["amazon", "https://www.amazon.com"],["netflix", "https://www.netflix.com"],["hulu", "https://www.hulu.com"],["spotify", "https://www.spotify.com"],["soundcloud", "https://www.soundcloud.com"],["github", "https://www.github.com"],["stackoverflow", "https://www.stackoverflow.com"],["medium", "https://www.medium.com"],["quora", "https://www.quora.com"],["imdb", "https://www.imdb.com"],["yelp", "https://www.yelp.com"],["tripadvisor", "https://www.tripadvisor.com"],["expedia", "https://www.expedia.com"],["booking", "https://www.booking.com"],["airbnb", "https://www.airbnb.com"],["uber", "https://www.uber.com"],["lyft", "https://www.lyft.com"],["doordash", "https://www.doordash.com"],["grubhub", "https://www.grubhub.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} Triyar sir...")
                webbrowser.open(site[1])
        
        if "send email" in query.lower():
            say("Sure, what should be the subject of the email?")
            subject = takeCommand()
            say("What should be the message of the email?")
            message = takeCommand()
            say("Please provide the recipient's email address.")
            # to_email= input()
            to_email = takeCommand()
            sendEmail(subject, message, to_email)
            say("Email sent successfully.")
        
        elif "weather".lower() in query.lower():
            say("Please provide the name of city.")
            city = takeCommand()
            weather(city)

        
        elif "Search wikipedia".lower() in query.lower():
            search_wikipedia(query)
        elif "the time" in query:
            
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Triyar Sir. Time is {hour} and {min} minutes")

        
        elif "set reminder" in query:
            say("What should I remind you?")
            reminder_text = takeCommand()
            say("When should I remind you? Please provide a specific date and time.")
            reminder_time = takeCommand()

            formatted_time = parseReminderDateTime(reminder_time)
            if formatted_time is not None:
                setReminder(reminder_text, formatted_time)
                say("Reminder set successfully!")
            else:
                say("Invalid date or time format. Please try again.")

        elif "check reminders" in query:
            checkReminders()
        elif 'add task' in query:
            say("Sure, what do you want to add")
            task_content = takeCommand()
            
            addTask(task_content)
        elif 'print to-do list' in query:
            printTodoList()

        

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Close".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)





        