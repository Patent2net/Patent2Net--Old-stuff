@@ -0,0 +1,73 @@
  _____      _             _     ___    _   _      _   
 |  __ \    | |           | |   |__ \  | \ | |    | |  
 | |__) |_ _| |_ ___ _ __ | |_     ) | |  \| | ___| |_ 
 |  ___/ _` | __/ _ \ '_ \| __|   / /  | . ` |/ _ \ __|
 | |  | (_| | ||  __/ | | | |_   / /_  | |\  |  __/ |_ 
 |_|   \__,_|\__\___|_| |_|\__| |____| |_| \_|\___|\__|

******** CLIENT USERS

To use the client version of Patent2Net in your own environment, follow the steps below: 

Step 1
Download and install the Patent2Net accessing the url http://patent2net.vlab4u.info/ and clicking the word CRAWLER.

Step 1.1 
Download and install Graphviz on your computer. http://www.graphviz.org/
Ensure sfdp program is in your Path environnement.

Step 2
Unpack the file P2N.zip in any directory you want.

Step 3
To use the CRAWLER, you have first to register yourself at Espacenet and get a key to data access following the next 3 steps. 
If you already have it, skip to Step 4.

3.1
Access the Espacenet Open Patent Service (OPS): http://www.epo.org/searching/free/ops.html, click on Register button and 
fulfill the form.

3.2
Wait until you receive the email confirmation of you register from EPO Developer Portal.

3.3
Log in the EPO Developer Portal http://www.epo.org/searching/free/ops.html, select the option My Apps, and register the 
application Patent2Net. Then, the system will return the API Credentials key and secret. Save it to use in the CRAWLER.

Step 4
At the folder you have unpacked the P2N.zip, find and edit the file requet.cql . Identify the line starting with 

	request: 

and complete it with the terms you want to search at OPS, for example, to search the term "green washing" in Title and Abstract 
field you could write like this:

	request: TA="green wash*"

then, find the line starting with

	DataDirectory:


and complete it with the name of the sub directory you wish to have the results of your search in the Patent2Net structure.

The rest of the parameters in the file, you can chose TRUE or FALSE depending on the information you want to extract from the OPS. 
To make a search for the first time, you have at least to set

  	GatherPatent: True
  

Step 5
In the same directory, create a simple text file named cles-epo.txt with the credentials key and secret that you have saved at 
step 3.3. The file has to have a unique line, without any space, just a comma between the key and secret, example 
(this one is invalid, of course):

	vmrr7AaAGIl794E6VunJ6PzjbkfajwLW,KHzH4fGM7opMhDDD

Step 6
Execute the file CollectETraite.bat 

Step 7
If you have no errors, check in the subdirectory DONEES another subdirectory with the name you have used at the Step 4 for 
Datadirectory parameter. You will see also a html file with the same name, that is the start point for your data analysis.
Export CSV function 
You must to connect at http://www.macromedia.com/support/documentation/fr/flashplayer/help/settings_manager04.html and select always allowed and add http://patent2net.vlab4u.info/Patent2Net/extensions/TableTools/swf/copy_csv_xls_pdf.swf