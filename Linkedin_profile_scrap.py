from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
#query_keyword = ["princeamitlali","dikshabansal11","saurav-kumar-7ab385151","kritikasinghweb"]
query_keyword = ["saurav-kumar-7ab385151"]
#query_keyword = ["saurav-kumar-7ab385151","shahab-saquib-43266661"]
print('Enter the linkedin email')
email = input()
print("Enter the LinkedIn password")
password = input()

# Open Chrome web
driver = webdriver.Chrome(r'E:\project\Java\chromedriver.exe')
driver.get('https://www.linkedin.com/uas/login?goback=&trk=hb_signin')

# Login bu username/password
email_box = driver.find_element_by_xpath('//*[@id="username"]')
email_box.send_keys(email)
pass_box = driver.find_element_by_xpath('//*[@id="password"]')
pass_box.send_keys(password)
submit_button = driver.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button')
submit_button.click()

time.sleep(1)


# Find Name and return
def getName(driver):
    nameXpath = "//li[contains(@class, 'inline t-24 t-black t-normal break-words')]"
    time.sleep(10)
    name = driver.find_element_by_xpath(nameXpath).text
    photo=driver.find_element_by_xpath("//div/div/div/img").get_attribute("src")
    resp = requests.get(photo, stream=True)
    local_file = open('local_image.jpg', 'wb')
    local_file.write(resp.content)
    print(photo)
    return name


def getLocation(driver):
    nameXpath = "//li[contains(@class, 't-16 t-black t-normal inline-block')]"
    loc = driver.find_element_by_xpath(nameXpath).text
    return loc


def getEducation(driver):
    nameXpath = "//span[contains(@class, 'text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view')]"
    edu = driver.find_element_by_xpath(nameXpath).text
    return edu


def getConnections(driver):
    nameXpath = "//span[contains(@class, 't-16 t-bold')]"
    conn = driver.find_element_by_xpath(nameXpath).text
    if(conn=="Contact info"):
        nameXpath = "//span[contains(@class, 't-16 t-black t-normal')]"
        conn = driver.find_element_by_xpath(nameXpath).text
    return conn
def getExtraInfo(driver):
    xm=[]
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    # print(soup.prettify())
    results = soup.findAll("div", {"class": "pv-oc ember-view"})
    for item in results:
        xm.append(item.text)
    return xm

def saveAsCSV(data):
    fileName = "linkedin_result.csv"
    f = open(fileName, "a")
    headers = "Name,Location,Education,Connections\n"
    f.write(data + '\n')


# For each profile name in query_keywords, retrive name, education, experience and number of connections
for query in query_keyword:
    try:
        #driver.get('https://www.linkedin.com/search/results/index/?keywords=' + query)
        driver.get('https://www.linkedin.com/in/'+query)

        #xpath = "(//span[text()='" + query + "'])[1]"
        # print (xpath)
        time.sleep(10)
        #driver.find_element_by_xpath(xpath).click()
        data = ''

        try:
            name = getName(driver)
            print(name)
            data += name + ','
        except Exception as ex:
            data += '0,'

        try:
            loc = getLocation(driver)
            print(loc)
            data += loc + ','
        except Exception as ex:
            data += '0,'

        try:
            edu = getEducation(driver)
            print(edu)
            data += edu + ','
        except Exception as ex:
            data += '0,'
        try:
            conn = getConnections(driver)
            print(conn)
            data += conn + ','
        except Exception as ex:
            data += '0,'
        try:
            xm = getExtraInfo(driver)
            print(xm)
        except Exception as ex:
           print("Not found")

        print(data)
        saveAsCSV(data)
    except Exception as e:
        print("Exception in retrieving data" + e)