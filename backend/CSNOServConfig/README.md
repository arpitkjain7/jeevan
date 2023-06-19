# CSNOSERV

Representational State Transfer (REST) API layer exposed as web service
****************************************************************************
	         How to use SNOMED CT service (CSNOServ)
****************************************************************************
CSNOServ Directory Structure:

CSNOServ provides the following directory structure:
- csnoserv.war: Deployable web service

- Copyrightnotice.txt: A Copyright notice for CSNOtk

- README.txt: A readme (or read me) file contains information about other files in the directory and also how to configure and use CSNOServ

****************************************************************************
	         Pre-Requisite Software requirements
****************************************************************************
* OPEN JDK 8 should be installed on the machine the for CSNOtk application.
	
* Append the path value for JAVA in the PATH environment variable.
	e.g. :  C:\Program Files\openjdk\jdk8u202\bin

* Set the environment variables for Java.
	.g. :  JAVA_HOME - C:\Program Files\openjdk\jdk8u202 (System Environment Variable in case of Windows)
		JAVA_HOME - export JAVA_HOME=/usr/java/jdk8u202 (modify '/etc/profile' - in case of LINUX)
		   
* To host the application for different plus-ing-in (JAVA, Dot Net, PHP) different hosting web servers are required.
	
* Set the environment variables the for web server if required.
	e.g. : export TOMCAT_HOME=/usr/java/apache-tomcat-7.0.70 (modify '/profileile' - in case of LINUX)

* To open .jar and .war files use WINRAR archiver.


***************************************************************************
		Configure and deploy SNOMED CT service
***************************************************************************
* Deploy csnoserv.war to the webapps folder of the application server directory. (Current version tested with Tomcat 7.0 & 8.5).

* Configthe ure application server to use 1024M java maximum memory pool size.

* Start the application server and once deployed, test it at URL URL: 'http://localhost:8080/csnoserv/'.

* Provide configuration details
	Note: The property file for database configuration will be saved.

* The  In configuration detail page, provide the SNOMED CT International Release file path. SNOMED CT codes can be obtained the from SNOMED International website or the National Release Center (NRC) of your country. After providing the path and other details, submit the form.

* Home page will be displayed after successful submission or else try again with proper inputs. Please note that it might ta take a few minutes to the ave configuration page and create the database and index files. Ala so, the log file can be checked by the user for more details.

* If any database configurations ion to be reset, change con fig. flag value to true the in system.properties file in the server directory. And restart the service.		

* If required, for creating/reinstalling any additional component database like extension, refset, etc, Configuration is available to the user on the CSNOServ page and can be configured by providing the valid file path for them.

* APIs are available to use.
	
*****************************************************************************
		'Configuration' tab/link in csnoserv 
*****************************************************************************

After importing international release files into DB, a 'Configuration' tab/link will appear on the Headrer bar.  to import the extension visit on the configuration 
link then you will be redirected to the configuration page.

On the configuration page, you can select relevant options from the drop-down list followed by the absolute path of the extension file in the (Release File Path) input box.

***************************************************************************
		Steps to import SNOMED CT to ICD-10 Map refset 
***************************************************************************
* Visit http://localhost:8080/csnoserv.

* Open the 'Configuration' page

* Choose 'SNOMED CT to ICD-10 Map reset' option from the drop-down

* Provide the absolute path of the international rf2 file of snapshot folder in the input box

	e.g C:/Release_file/SnomedCT_InternationalRF2_PRODUCTION_YYYYMMDD/Snapshot

* Click on 'Submit' button to import and create index

***************************************************************************
		Steps to import National  Extension
***************************************************************************
* Visit http://localhost:8080/csnoserv.

* Open the 'Configuration' page

* Choose the 'National Extension' option from the drop-down

* Provide the absolute path of the National extension release file (e.g. India AYUSH Extension, Common Drug Codes for India (CDCI), Patient Instruction language Extension, etc.) of snapshot folder in the input box

	e.g C:\Release_file\SnomedCT_IndiaDrugExtensionRF2_PRODUCTION_IN1000189_20220715T120000Z\Snapshot

* Click on 'Submit' button to import and create index

***************************************************************************
		Steps to import SNOMED CT to Simple Map refset 
***************************************************************************
* Visit http://localhost:8080/csnoserv.

* Open the 'Configuration' page

* Choose SNOMED CT to Simple Map refset option from the drop-down

* Provide the absolute path of the Extension file of snapshot folder in the input box

	e.g C:/Release_file/SnomedCT_Extension_YYYYMMDD/Snapshot

* Click on 'Submit' button to import and create index

***************************************************************************
		Steps to import Refset File 
***************************************************************************
* Visit http://localhost:8080/csnoserv.

* Open the 'Configuration' page

* Choose the refset option from the drop-down

* Provide the absolute path of the refset file to import in the input box

	e.g. C:/Release_file/der2_refset_name_YYYYMMDD.txt 

* Click on 'Submit' button to import and create index

***************************************************************************
	Steps to configure DISB (Drug Information Service Bundle)
***************************************************************************
* Visit http://localhost:8080/csnoserv.

* Open the 'Configuration' page

* Choose the DISB option from the drop-down

* configure the DISB service information in the input box

* pass the configuration details in the input box   

* Click on 'Submit' button to import and create index

*****************************************************************************
	Enabling Cross-Origin Resource Sharing(CORS)
*****************************************************************************
* Access control allows credentials must be true if credentials are required, in the system.properties file.

* To allow the request to be served via a specific domain only then set the accessControlAllowOrigin value, in the system.properties file.
	e.g accessControlAllowOrigin = http://192.168.0.111:8080 

* Access-Control-Allow-Headers can be added or removed by writing true or false in front of a specific header value, in the system.properties file.
        e.g authorization=true (to add authorization header in Access-Control-Allow-Headers)
   
********************************************************************************
				FINISH
********************************************************************************
