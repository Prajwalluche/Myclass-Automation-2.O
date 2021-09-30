from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import Tk
from tkinter import simpledialog
import os
import time
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

root=Tk()
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

def get_details():
    global usrnm
    global pswd
    root.withdraw()
    if os.path.isfile('login_up.txt'):
        f=open('login_up.txt','r')
        usrnm=f.readline()
        pswd=f.readline()
    else:
        f=open('login_up.txt','w')
        usrnm=simpledialog.askstring(title="Username",prompt="Enter the Username here:")
        f.write("u-"+usrnm+"\n")
        pswd=simpledialog.askstring(title="Password",prompt="Enter the Password here:")
        f.write("p-"+pswd)
        f.close()
        f=open('login_up.txt','r')
        usrnm=f.readline()
        pswd=f.readline()
        f.close()
    
    usrnm=usrnm[2:10]
    pswd=pswd[2:]

def poll():
    try:
        try: # //*[@id="frame"]
            frame = WebDriverWait(driver,1).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="frame"]')))
            driver.switch_to.frame(frame)
        except Exception as e: 
            print("-",end="")
        time.sleep(10)
        try:
            driver.find_element_by_xpath('//*[@id="app"]/main/div[2]/div/span/div[2]/div[1]/button').click()
        except:
            pass
            print("not polled")
        print(" :)Polled!")
    except Exception as e:
        print(".",end="")

def wishTeacher():
    now = datetime.datetime.now() 
    if(now.minute <= 10):
        if(now.hour<12):
            wish="Good Morning"
        elif(now.hour>=12 and now.hour<=16):
            wish="Good Afternoon"
        else:
            wish="Good Evening"

    try:
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="tippy-10"]')))
        time.sleep(7)
        driver.find_element_by_xpath('//*[@id="app"]/main/section/div[1]/div/div/div[2]/div[1]/div[2]/div/div/div').click()
        driver.find_element_by_xpath('//*[@id="chat-toggle-button"]').click()
        chatbox = driver.find_element_by_id("message-input")
        # chatbox.send_keys(wish)
        chatbox.send_keys(wish)
        chatbox.send_keys(Keys.RETURN)
    except Exception as e:
        print("Teacher not wished:-(")

def get_time(timest):
    #eg->9:00 AM - 10:00 AM
    timest=timest.split(" -") 
    timest=timest[0]
    if 'AM' in timest:
        print(timest)
        final_time=timest[:-3]+':00'
        print(final_time)
    else:
        final_time=timest[:-3]
        final_time=final_time.split(":")
        temp=final_time[1]
        final_time=final_time[0]
        if not final_time=='12':
            addtwl=str(int(final_time)+12)
            final_time=addtwl+":"+temp+":00"
        else:
            addtwl=str(int(final_time)+0)
            final_time=addtwl+":"+temp+":00"
        print(final_time)
    return final_time

def jot(final_time):
    timestamp = time.strftime('%H:%M')
    print(timestamp)
    ft=final_time[0:5].split(':')
    ct=timestamp.split(':')
    print(ft,ct)
    diffh=-int(ft[0])+int(ct[0])
    diffm=-int(ft[1])+int(ct[1])
    diff=diffh*60+diffm
    print(diff)
    if diff>-1 and diff<=70:
        print("You are late by "+str(diff)+" m.\nLets join...")
        return 0
    elif diff>-1 and diff>70:
        print('Your class finished '+str(diff)+'m ago.')
        return -1
    else:
        print('You have '+str(-diff)+' m to start the class.')
        return diff


def join_audio():
    try:
        frame = WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="frame"]')))
        driver.switch_to.frame(frame)
        listenMode = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/span/button[2]')))
        listenMode.click()
    except Exception as e:
        print("No Audio Mode")
    print("Audio Mode Selected")


def site_login():
    driver.get("https://myclass.lpu.in/")
    get_details()
    driver.find_element_by_xpath('/html/body/div[2]/div/form/div[6]/input[1]').send_keys(usrnm)
    driver.find_element_by_xpath('/html/body/div[2]/div/form/div[6]/input[2]').send_keys(pswd)
    driver.find_element_by_xpath('/html/body/div[2]/div/form/div[7]/button').click()
    driver.find_element_by_xpath('//*[@id="homeCenterDiv"]/div/div[1]/div/div[2]/a').click()
# //*[@id="homeCenterDiv"]/div/div[1]/div/div[2]/a
    time.sleep(5)
    
    a=[]
    links=[]
    b=[]
    clstime=[]
    count=0
    a=driver.find_elements_by_css_selector(".fc-time-grid-event.fc-event.fc-start.fc-end")
    for i in range (len(a)):
        app=str(i+1)
        b.append(driver.find_element_by_xpath('//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[3]/table/tbody/tr/td[2]/div/div[2]/a['+app+']/div/div[1]'))
    for i in a:
        links.append(i.get_attribute("href"))
        count+=1
    for i in b:
        print(i.get_attribute("data-full"))
        clstime.append(get_time(i.get_attribute("data-full")))
        # final_time=i.get_attribute("data-full")
        # print(final_time)
        # # final_time=get_time(final_time)
        # clstime.append(i.get_attribute(i.get_attribute("data-full")))

    print(a)
    print(links)
    print(clstime)

    wincnt=1



    #time wise attendence
    # for prd in clstime:
    #     if jot(prd)==1:
    #         driver.get(links[clscount])
    #     elif jot(prd)==0:
    #         print('classdone')
    #     else:
    #         time.sleep(jot(-prd*60))
    #     clscount=clscount+1

    for j in links:
        try:
            jot(clstime[wincnt-1])
        except:
            print('jot//no')
        driver.get(j)
        time.sleep(1)
        try:
            driver.find_element_by_css_selector(".btn.btn-primary.btn-block.btn-sm").click()
            flag=True
        except Exception as e:
            print("Join btn not found A.K.A #SEDLYF #STRUGGLEISREAL")
            flag=False
        if flag:
            join_audio()
            wishTeacher()
            time.sleep(5)
            for k in range(11):
                # try:
                #     driver.find_element_by_id("message-input").send_keys("Okay")
                #     driver.find_element_by_id("message-input").send_keys(Keys.RETURN)
                # except Exception as e:
                #     print("Msg box and ok btn not found")
                #     break
                for l in range(300):
                    time.sleep(1)
                    poll()
                    
        print("\n----------------#---------------------#------------------#-----------------------")  
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[wincnt])
        wincnt+=1
site_login()






