https://github.com/Patent2net/Patent2Net

//   _______  _______  _______  _______  __    _  _______    _______    __    _  _______  _______ 
//  |       ||   _   ||       ||       ||  |  | ||       |  |       |  |  |  | ||       ||       |
//  |    _  ||  |_|  ||_     _||    ___||   |_| ||_     _|  |____   |  |   |_| ||    ___||_     _|
//  |   |_| ||       |  |   |  |   |___ |       |  |   |     ____|  |  |       ||   |___   |   |  
//  |    ___||       |  |   |  |    ___||  _    |  |   |    | ______|  |  _    ||    ___|  |   |  
//  |   |    |   _   |  |   |  |   |___ | | |   |  |   |    | |_____   | | |   ||   |___   |   |  
//  |___|    |__| |__|  |___|  |_______||_|  |__|  |___|    |_______|  |_|  |__||_______|  |___|  

About
°°°°°
Patent2Net is elaborated and maintained (on a free base) by a small international team of professors and researchers
Patent2Net is a "free" package, dedicated to :
	augment the use of patent information in academic, nano and small firms, developing countries (all those without pay mode access)
	learn, study and practice how to collect, treat and communicate "textual bibliographic information", and automation process 
	provide statistical analysis and representations of a set of patents.
	
Patent2Net is an "open source" package and contributions are welcome.
Patent2Net is available "as it is".

First step : Train how to search patent information using interface
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

http://worldwide.espacenet.com/advancedSearch?locale=en_EP

Practice and use the available help :
http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=index
more especially : 
Full-text search
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=<fulltext></fulltext>
boolean operators
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=booleans
Truncation
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=truncation
Smart search - field identifiers
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=fieldidentifier
Limitations
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=limitations
Date formats and Ranges
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=dateformats
Kind Codes
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=kindcodes
Respect the Fair use Charter for the EPO's online patent information products
	http://www.epo.org/searching/free/fair-use.html

Install Patent2Net package
°°°°°°°°°°°°°°°°°°°°°°°°°°
To run as python script need to install python libraries :
networkx, pickle, os, sys, datetime, urllib, requests, time, simplejson, json

to run as a an exe file (windows) : need to install the "full package", updating can be done only copying the "Patent2Net" files. Operate as a "Command window"

setup.py is provided also to compile binaries for your windows operating system. Use it with the command python setup.py py2exe to produce binaries in the dist directory.

Use Patent2Net
°°°°°°°°°°°°°°	
	1 - Construct the patent list with OpsGather-PatentList.exe
	Use as : OpsGather-PatentList.exe Your_File.dump "search expression"
	For example : OpsGather-PatentList.exe test.dump "ti =(stereolithography or \"3D print*\") AND pd<=1996"
	Protect the " with a \ Should obtain at minimum as many patents as with the URL interface.
	Results are stored in the "PatentLists" directory within the dump file in pickle format.

2 - Download bibliographic data using OpsGather-BiblioPatents.exe Your_File.dump
	The result is a file with same name (bigger) stored in the "BiblioPatents" directory.

3 - download the claims (optional, not consistent at this time) : OpsGather-Claims Your_File.dump
	The dump file is the file produced on stage 2 (without path, patentlist directory is the default source)
	Available claims (mainly European Patents EP) will be downloaded and stored "claims" directory in iramutek format (http://www.iramuteq.org/)

4 - convert to gephi (gexf) file : PatentsToNet.exe Your_File.dump.
	The dump file is the file produced on stage 2 ((without path, BiblioPatents directory is the default source)
	Result is stored in "GephiFile" directory as a Your_File.dump.gexf.
	

Todo List :
°°°°°°°°°°°
	URL Links for IPC 7 and 11
	URL Links for inventors or applicant (to evaluate what they are doing out of search field, in general)
	Grouping results in Patent Family. 
	Other Gathering process list for family requests
	Susbscribed version. 
	Patent Citation
	Revisit weights.
	
V 0.9 26/03/2014
°°°°°°°°°°°°°°°°
	OpsGather-PatentList
		-Accept a "smart search" query
	PatentsToNet
		-fully connected graph is provided in Gephi, connecting any relation (intra and Inter field) : filtering can be done in Gephi or hacking in the Python script. 
		-International Patent Classification is treated to be "truncated" at level 1,3,4,7. nodes for each level are created
		-Countries from Patent numbers (first deposit?) are considered as nodes
		-Kind codes (status) are separated as nodes
		-URL links as node attribute in gexf 
			for patent number : link to espacenet
			for International Patent Classification IPC at level 1,3,4 : link to IPC database (French and English)
		-Dynamic graph are available over first available date (column deb and fin as to be merged as timeline in data laboratoty in Gephi)
		-mixed graph is build:
			°oriented relations are :
			°Non Oriented relations are : Inventor-Inventor; IPC-IPC; Applicant-Applicant
		-Weight of nodes are provided as....
		-Weight among time are provided for node as ...
		-Weight of edges are provided as ....