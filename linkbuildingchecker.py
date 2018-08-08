from bs4 import BeautifulSoup
import requests, smtplib, openpyxl, datetime

"""
Check link changing and life duration for SEO link building activities
List of link to check is in the file linkbuildingchecker.xlsx
Set parameters of your e-mail to receive alerts!
If you want disable alert reports just delete last line in this file.
"""

def send_email(subject, text):
    """
    E-mail function to send alert reports
    """
    sender = "YOUR_SENDER_EMAIL_HERE@outlook.com" #sender address
    recipient = "YOUR_EMAIL_HERE@outlook.com" #your e-mail address
    password = "YOUR_PASSWORD_HERE" #your sender e-mail password
    smtp_server = smtplib.SMTP('smtp-mail.outlook.com', 587) #change with your SMTP server
    smtp_server.starttls()
    smtp_server.login(sender, password)
    message = "Subject: {}\n\n{}".format(subject, text)
    smtp_server.sendmail(sender, recipient, message)
    smtp_server.close()


def check_link_now(row_position, checking_page, checking_link):
    """
    Check if the earned link is still in the page,
    check if it's set as "nofollow",
    then save the link parameters and the date of
    last control in the XLSX file.
    """
    
    try:
        print(datetime.datetime.now(), " - Analyzing", checking_page, "--> searching for link", checking_link)
        link_founded = 0 #this is a counter to track how many times link is founded in the page
        #scrape the page and search for link
        page_checking_page  = requests.get(checking_page)
        #page_checking_page.encoding = "utf-8" #enable this line in case of econding problem
        data_checking_page = page_checking_page.text
        html_checking_page = BeautifulSoup(data_checking_page, "lxml") #parse the page using lxlm, alternatively try html5lib 
        for link in html_checking_page.find_all("a"):
            if link.has_attr("href"): #search for all <a href="...> links in the page
                if link.attrs["href"] == checking_link:
                    link_founded = link_founded + 1 #link founded! now save it, with all parameters
                    print("OK, link founded ", link_founded, " times !")
                    sheet.cell(row=row_position, column=3).value = str(link)
                    if link.has_attr('rel'): #chek if link is set as nofollow
                        if "nofollow" in link.attrs['rel']:
                            if sheet.cell(row=row_position, column=4).value != "1": #check if link was already nofollow, if not send an alert
                                email_body.append(str(checking_link)+" in "+str(checking_page)+" is changed in NOFOLLOW!")
                            sheet.cell(row=row_position, column=4).value = "1" #save a flag for nofollow link
                            print("Link to ", checking_link," is set as nofollow!")
                    
        if link_founded is 0:
            #counter = 0, link NOT founded! save it and add this site to the alert e-mail
            print("Link NOT founded")
            sheet.cell(row=row_position, column=3).value = "Link NOT found"
            email_body.append(str(checking_link)+" isn't found in "+str(checking_page)+"!")
    
    except:
        #if during page scraping was occured errors...
        print("Some errors occured while scan ", checking_page)
        sheet.cell(row=row_position, column=3).value = "Some errors occured while scan!"
        email_body.append("Some errors occured while scan "+str(checking_page)+"!")
    
    #all checking operation have been done! set time for last link control and save XLSX file
    sheet.cell(row=row_position, column=5).value = datetime.datetime.now()
    file_xlsx.save("linkbuildingchecker.xlsx")


email_body = ["E-mail alert from your LinkBuildingChecker!","\n\nScan start at: "+str(datetime.datetime.now())+"\n"] #header of alert e-mail

#open the XLSX file
file_xlsx = openpyxl.load_workbook('linkbuildingchecker.xlsx')
sheet = file_xlsx['data']

#execute chek_link_now function for every row
for row_position in range(2,sheet.max_row+1):
    page=sheet.cell(row=row_position, column=1).value
    link2check=sheet.cell(row=row_position, column=2).value
    check_link_now(row_position, page, link2check)

email_body.append("\n"+"LinkBuildingChecker has finish at "+str(datetime.datetime.now())) #append final time to text alert

send_email(email_body[0], '\n\n'.join(email_body[1:])) #send the alert e-mail