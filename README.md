# LinkBuildingChecker 0.1
**Check link changing and life duration for SEO link building activities**

LinkBuildingChecker is a small script that can help you in control activity of what you earned during link building works.


### How it works

1. Add the page and link to monitor in the Excel file linkbuildingchecker.xlsx (use Microsoft Excel or Libre Office and save all changes in Office 2007 format).

![alt text](https://raw.githubusercontent.com/napp1/LinkBuildingChecker/master/img/xlsx-file.jpg)

*In the XLSX file you will found some exemples if you need to test the script, delete them when you will need insert your links.*
Save and close the file, don't leave it open while launch script execution.

2. Set your e-mail parameters: SMPT server, sender e-mail, password, receiver e-mail

![alt text](https://raw.githubusercontent.com/napp1/LinkBuildingChecker/master/img/email-parameters.jpg)


3. Test the script!
XLSX file will be updated with link tag information and last time of visit.
An alert e-mail will be send when:
- a page can't be reached or caused errors
- a link isn't found in the scraped page
- a link is changed from dofollow in nofollow

4. Schedule the script execution on your sysyem (I use **cron** on my Linux server).

If you need to disable e-mail reporting delete last line of code.

### Dependecies
You may need install some dependencies to make the script works:
```
pip install requests
pip install beautifulsoup4
pip install openpyxl
```

### Note
LinkBuildingChecker is just my personal experiment with Python coding.
If you have observations or you need help please write me!

Cheers from Napoli.




