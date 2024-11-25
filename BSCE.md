## About BSCE

Burp Suite Community Edition is a powerful, free tool for web application security testing, developed by PortSwigger. It is designed for penetration testers, ethical hackers, and developers to identify and investigate vulnerabilities in web applications. Though limited compared to the Professional version, the Community Edition still provides essential features for learning and testing. Here's a detailed explanation of its features and how it is used:

### Overview of Burp Suite

   Burp Suite is essentially an integrated platform for performing security testing of web applications. It operates as an intercepting proxy, sitting 
   between a web browser and the web application, capturing and modifying traffic between the two. The tool provides a variety of functionalities that 
   help testers identify security flaws in web applications.

### Main Features of Burp Suite Community Edition

1. **Intercepting Proxy**: 

   The core feature of Burp Suite is its ability to act as an intercepting proxy between the user's browser and the web application. It intercepts 
   requests sent by the browser to the server and the responses sent by the server back to the browser. This allows testers to:

   * View and modify HTTP/S requests and responses.
   * Manipulate input parameters and cookies to see how the application handles modified data.
   * Understand the flow of data and identify potential vulnerabilities.

2. **Repeater**: 

   Allows users to manually craft and replay HTTP requests with various parameters, testing for issues like injection vulnerabilities and authentication 
   bypasses.
   
3. **Intruder (Limited in Community Edition)**: 

   The Intruder tool allows testers to automate attacks by sending multiple payloads to a specific request, helping to test for vulnerabilities such as 
   brute-force attacks, parameter tampering, and injection attacks. In the Community Edition, this feature has limitations in terms of speed and 
   automation.

4. **Decoder**: 

   Burp Suite includes a decoder that helps with the manual decoding and encoding of data. Testers can use this tool to analyze and manipulate encoded 
   data such as URL encoding, Base64 encoding, and hexadecimal.

5. **Comparer**: 

   The Comparer tool allows users to visually compare two pieces of data, which is useful for detecting subtle differences between requests or responses 
   that might point to security issues.

6. **Sequencer**: 

   This tool analyzes the randomness of tokens, such as those used in session management, to detect vulnerabilities in session handling mechanisms.

7. **Extensibility**: 

   Burp Suite Community Edition supports the use of plugins and extensions. Although some advanced features are restricted to the Professional version, 
   users can install third-party extensions from the BApp Store, Burp Suite’s official extension repository. These extensions can extend the 
   functionality of the Community Edition by adding extra tools or features that aren’t natively available.



## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Implementation](#implementation)
4. [Usage](#usage)
5. [Troubleshooting](#troubleshooting)


## Installation

   Follow the steps to install Burp Suite Community Edition in your PC.

**Prerequisites:**

1. Ensure Java 8 or later is installed (```java -version``` to verify).

2. At least 4 GB of free RAM for smoother operation.

### For macOS:

1. Download: Visit the PortSwigger website (https://portswigger.net/burp/communitydownload) and download the macOS installer (.dmg file).

2. Mount the Image: Double-click the downloaded .dmg file to mount it.

3. Drag and Drop: Drag the Burp Suite icon to the "Applications" folder.

4. Launch: Open "Applications" and double-click the Burp Suite icon to start the application

### For Windows:

1. Download: Visit the PortSwigger [Community Download](https://portswigger.net/burp/communitydownload) page and download the Windows installer (.exe 
   file).

2. Install: Double-click the downloaded .exe file and follow the on-screen instructions.

3. Launch: Once installed, start Burp Suite from the Start menu.

**Windows Installation Common Issues:**

1. If the installer doesn’t launch, verify that no antivirus is blocking the ```.exe``` file.

2. Ensure you’re running the installer with admin privileges (```Right-click > Run as Administrator```).


### For Linux:

1. Download: Visit the PortSwigger website and download the Linux installer (.jar file).

2. Make Executable: Open a terminal and use the following command to make the .jar file executable:

```bash
chmod +x burpsuite_community.jar
```
3. Run: Run the following command to start Burp Suite:

```bash
java -jar burpsuite_community.jar
```

**Linux Installation Tip:**

* Instead of using the ```.jar``` file, you can also install Java via:

```bash
sudo apt update
sudo apt install default-jre
```


**NOTE:** Once installed, ensure your browser is configured to work with Burp Suite by setting the proxy to 127.0.0.1:8080, then navigate to http://localhost:5003/team3 for local web application testing.


## Configuration

  After completion of installation, you need to configure Burp Suite to use its features.

### Proxy Configuration:

**1. Launch Burp Suite.**

* When you start Burp Suite, you are presented with several options for managing project files. These project files help you save and organize your work, 
  such as intercepted requests, scan results, and configuration settings. 

* Select 'Temporary Project' since this is the only option in the Community Edition

![BSC 1 (2)](https://github.com/user-attachments/assets/bdf40437-f1cf-42cd-9d54-842bcbc0d732)

  Fig 1: When you launch burp suite, select the 'temporary project' option in the initial setup window

**2. Start burp suite**

1. **Choosing Default for Simplicity**:

* In most cases, especially when using the Community Edition for smaller projects or when you’re just getting started, you won’t have any special 
  configurations to load. Therefore, the default settings are ideal because they:

* Get you up and running with minimal effort.

* Are perfectly sufficient for intercepting traffic and performing basic security testing tasks.

2. **Starting Burp Suite**:

* After selecting your desired configuration (which, in this case, is the default settings):

* Click the Start Burp button.

* Burp Suite will initialize all the necessary tools and settings according to the selected configuration.

* Once Burp Suite finishes starting up, the main interface will open, and you’ll be taken to the Dashboard tab. From here, you can start using Burp’s 
  tools (like Proxy, Repeater, and Intruder) to capture and manipulate web traffic, search for vulnerabilities, and more.

![BSC 2 (2)](https://github.com/user-attachments/assets/4a694aac-dbb5-4a58-869b-0c57f334aaea)

  Fig 2: Using the burp defaults

**3. Dashboard**

* The Burp Suite Dashboard is the main hub for managing various aspects of your security testing activities.

* It provides a centralized overview of the testing process, including live activity monitoring, scanning progress, task management, and issues 
  identified during testing. 

* While the Community Edition of Burp Suite provides a more limited version of the Dashboard compared to the Professional Edition, it is still an 
  essential part of the interface for web application security testing.

![BSC 3](https://github.com/user-attachments/assets/0cd253de-9a28-4e66-9d78-4f8684ad96c2)

  Fig 3: Burp suite dash board


**4. Proxy settings**

1. Selecting a Project Type: Outline that only the “Temporary Project” option is available in the Community Edition.

2. Choosing Default Settings: Mention that this setting is ideal for basic tests.

3. Starting the Proxy: Step-by-step guide on using the Proxy tab and listener configurations.

  * Go to the Proxy tab and select proxy settings.


![BSC 4](https://github.com/user-attachments/assets/a1fcb041-3762-4046-ad29-5ef49431d9b5)

  Fig 4: Proxy settings



**5. Updating port**

* In the Proxy tab, go to the Options sub-tab, where you can configure the settings for Burp’s intercepting proxy.

* The Options tab contains settings that control how Burp Suite’s proxy server behaves, including the following:

 **A. Proxy Listeners**

  This section lists all of the network interfaces on which Burp Suite’s proxy server is listening for incoming traffic. By default, Burp Suite sets up a 
  proxy listener on:

* To start intercepting requests for http://localhost:5003/team3, ensure Burp Suite is set up as a proxy for 127.0.0.1:8080. Once configured, visit 
  http://localhost:5003/team3 in your browser.

* 127.0.0.1:8080 (the loopback address on port 8080).
    * 127.0.0.1 refers to the local machine (i.e., Burp Suite is only accepting connections from your own machine).
    * 8080 is the default port Burp uses to listen for HTTP traffic.

    The listener is the “bridge” between your browser (or HTTP client) and the target web server. It intercepts all requests coming from your browser 
    before they are sent to the server, and it captures all responses from the server before they are displayed in the browser.

* To view or modify the listener settings:
   * In the Proxy Listeners section, click on the existing listener (127.0.0.1:8080).
   * You can modify the Interface (network address) and Port number, but for most testing, the default 127.0.0.1:8080 settings are sufficient.

    If you want Burp to listen on a different port or accept traffic from other machines (for instance, if you're testing mobile apps or other devices), 
    you can add or edit a listener:

* Click Add to create a new listener.

* Choose a new IP address (interface) or port.

 **B. Interception Rules**

  This section allows you to define rules that determine what traffic gets intercepted by Burp Suite. By default, Burp intercepts all HTTP/S traffic, but 
  you can configure interception rules to filter out specific requests or responses.

* Intercept client requests based on URL or method: For example, you can set Burp to only intercept traffic for certain domains or block requests with 
  certain file types like .css, .png, or .js.

* Intercept server responses: You can configure Burp to intercept responses that match specific conditions (e.g., based on content type or status code).

  If you're testing a large web application and don’t want to intercept every request, you can configure these rules to reduce noise and focus on 
  specific traffic that is relevant to your testing.

![BSC 5](https://github.com/user-attachments/assets/17eb0b83-b331-4312-a005-f9547f22d3e6)

  Fig 5: Updating the port



**6. Configure your browser to use Burp as a proxy:**

   * Boot inside your Firefox browser and go to Options.

   * There, in the General tab, scroll down to the Network Settings and hit the Settings button.

   * Over in the Connection Settings, opt the Manual proxy configuration and type in the IP address as 127.0.0.1 with the port as 8080.

   * Select “Also use this proxy for FTP and HTTPS” checkbox:


![BSC 6](https://github.com/user-attachments/assets/d7c8374a-5611-4b2d-85d1-f06ca889ecbe)

  Fig 6: Changing ports of http and https

   **Browser Proxy Troubleshooting:**

 1. If Firefox doesn’t respect the manual proxy configuration

      * Restart the browser to apply changes.

      * Clear browser cache to prevent old configurations from interfering.




* We can thus now capture the HTTP traffic, but wait, what about the HTTPS one? Although we’ve configured the proxy for that too, but still our burp 
  would not intercept the HTTPS Requests.

* Thereby, in order to capture such traffic, we need to establish trust between Burp, the target’s web application and the client’s browser. And for 
  this, we need to install the PortSwigger’s certificate as a trusted authority within the browser


**7. SSL Certificate Installation:**

* Since Burp Suite intercepts HTTPS traffic, it uses a Certificate Authority (CA) certificate. Installing Burp’s CA certificate into your browser 
  establishes trust between Burp and the browser for encrypted traffic.

**Installing Burp’s CA certificate:**

* You’ll need to install Burp’s CA certificate into your browser to avoid SSL/TLS warnings. Once installed, your browser will trust Burp as a valid proxy 
  for secure traffic.

* You can download the certificate by visiting http://burp in your browser while Burp Suite is running, or navigate to the Options tab and click on the 
  Import/export CA certificate button.

**CA certificate management:** 

  You can also configure how Burp handles certificates, including generating new CA certificates or using a custom CA certificate (useful in cases where 
  you want to use your own certificate for testing).
__

![BSC 7](https://github.com/user-attachments/assets/fbc17e64-e9ea-4c69-a3d1-79c10e4bdde6)

Fig 7: Downloading CA certificate from browser

**macOS SSL Certificate Installation:**

 * After downloading the Burp CA certificate:

     * Open Keychain Access (search in Spotlight).

     * Drag and drop the certificate into the System keychain.

     * Double-click the certificate and expand Trust settings.

     * Change When using this certificate to Always Trust.


**8. View certificates**

* Back into the options section in firefox, click Privacy & Security on the left-hand side, and scroll down to Certificates Click the View Certificates… 
  button in order to add up the downloaded certificate.

![BSC 8](https://github.com/user-attachments/assets/09888747-a9ac-4888-a2f3-a0800f4046ec)

  Fig 8: View certificates

**9. Importing the certificates**

* Move to the Authorities tab, click Import and thus select the downloaded Burp CA certificate file.

![BSC 9](https://github.com/user-attachments/assets/8cc1bca9-e0c1-4b8b-9563-1b1d052ddfd1)

  Fig 9: Importing CA certificate

**10. Trusting the CA certificates**

* As soon as the certificate loads up, a dialogue box will get prompted up, there, check the Trust this CA to identify websites box, and fire up the OK 
  button, in order to finish the configuration.

![BSC 10](https://github.com/user-attachments/assets/82f5a653-e422-4442-82ed-4ccfd26953d2)

  Fig 10: Trusting CA to identify websites



## Implementation

  Burp Suite provides various features for web application testing. Here are some essential functionalities:

### Intercepting Requests:

* As you proceed with the configuration, focus specifically on the requests from http://localhost:5003/team3 that Burp Suite will intercept. This ensures 
  you're testing a real local web application environment

* Intercepting Requests in Burp Suite

  Intercepting requests in Burp Suite allows you to examine, modify, and replay HTTP(s) traffic between your computer and the target web application. 
  This is a fundamental feature for web application security testing.

* Here's how to intercept requests:

1. Ensure Intercept Mode is Enabled:

* In the Burp Suite interface, go to the Proxy tab.
* Make sure the "Intercept HTTP requests" option is checked.

![BSC 11](https://github.com/user-attachments/assets/1745b175-5941-4b4a-8375-b16866204684)

  Fig 11: Intercept on


2. Start Browsing:

* Open your web browser and navigate to the target website.

![BSC 12 (2)](https://github.com/user-attachments/assets/ccee1b9c-49e7-486a-98d7-7f2d79a01b99)

  Fig 12: Open browser

* In this we’ll focus on testing vulnerabilities on http://localhost:5003/team3, a local test environment. This will help you familiarize 
   yourself with Burp Suite's Community Edition features while targeting a local application.

![BS 1](https://github.com/user-attachments/assets/1168619d-d938-4c93-9d5f-724645252838)

  Fig 13: Entering of website


3. View Intercepted Requests:

* Burp Suite will intercept all HTTP(s) requests and display them in the Proxy tab. You can see the request method, URL, headers, and body.

![BS 2](https://github.com/user-attachments/assets/d3f0e3ec-37d5-4afe-b3ee-e9ac9ac8ebea)

  Fig 14: Intercepted request

4. Forward Requests:

* Click Forward to allow the requests to pass through while monitoring the traffic and select http history option

![BS 3](https://github.com/user-attachments/assets/183764b7-e41a-410f-8c30-b9d5d46e1295)
  
 Fig 15: Forwarding the intercepted request

**Explanation of WebSocket Requests:**

  * WebSockets enable real-time communication between the client and server. Testing them involves:

       * Modifying headers like Origin to simulate Cross-Site WebSocket Hijacking (CSWSH).

       * Validating server responses for unexpected or insecure behaviors.

**Testing for SQL Injection with Repeater:**

* Send a POST request to http://localhost:5003/team3/login with a payload like:

```bash
username=admin' OR 1=1; --&password=test
```

* Check if the server returns unauthorized responses or bypasses authentication.

## Usage

### Using Repeater for Testing WebSocket Vulnerabilities

* For WebSocket testing, use the specific URL http://localhost:5003/team3. Modify headers like Origin, Host, and Referer to see how the application 
  responds to unauthorized WebSocket connections.

* By sending requests to http://localhost:5003/team3, Burp Suite will capture the traffic and allow you to analyze WebSocket vulnerabilities specific to 
  this local application.

* When using Burp Suite's Repeater, focus on modifying HTTP requests targeting http://localhost:5003/team3. This includes testing for SQL injection, 
  Cross-Site Scripting (XSS), and other vulnerabilities common in web applications.

**Session Management Testing:**

* Test http://localhost:5003/team3 to identify session handling flaws:

     * Modify cookies (SessionID) to simulate session hijacking.

     * Check if sessions expire properly after logging out.

**Interpreting Server Responses:**

* Look for HTTP status codes:

     * 500 Internal Server Error: Backend issue; can indicate poor input sanitization.

     * 403 Forbidden: Check if security restrictions (like CORS policies) are working properly.

 Step 1: Select a WebSocket request to test for vulnerabilities by sending it to the Repeater tab.

![BS,4](https://github.com/user-attachments/assets/44be6e58-8361-4ba4-983c-1b38f31bc800)

 Fig 16: Selecting webstock request

 * The request is attempting to upgrade the connection to a WebSocket.
 * We focus on testing how the server responds to unexpected modifications in Host, Connection, Sec-WebSocket-Key, Sec-WebSocket-Version and Origin.

 Step 2: In Repeater, modify headers.

 * Origin Header: Changing this header helps test if the server restricts connections based on the origin, enhancing security against CSWSH.

 * Host:changing the host from 5003 to 5002.

 * Referer: The http link changes from 5003 to 5002

![BS 5](https://github.com/user-attachments/assets/0c3cb12e-197a-4f2c-8bae-39ef7facb6e9)

 Fig 17: Selected request


Step 3: Click "Send" to observe server response and verify if connections from unauthorized origins are blocked.

![BS 6](https://github.com/user-attachments/assets/ceee0fca-0233-46af-bb5c-8a3dabffe0cd)

 Fig 18: Modified request


Step 4: Response from the server will be displayed at the right side

![BS 7](https://github.com/user-attachments/assets/6d104e9e-d36b-4b18-a1ed-bf3d9f9e751e)

 Fig 19: Response from server


 * The response we received is http requests is not correct, It prevents WebSocket connections from unauthorized origins

 * The server is blocking WebSocket requests from any origins that aren't the anticipated one.

 * This is a form of protection against Cross-Site WebSocket Hijacking (CSWSH), ensuring that only WebSocket requests from allowed origins can establish 
   a connection

Step 5: Original request response

![BS 8](https://github.com/user-attachments/assets/ae8c1db7-8876-4269-b8ef-01cfb7a0c35d)

 Fig 20: Response for original request

## Troubleshooting

**Unable to Launch Burp Suite**

 * Verify Java is installed.

```bash
 java -version
```

**Proxy Not Intercepting Traffic:**

* Ensure your browser proxy is set to ```127.0.0.1:8080```.

* Check if the application uses HTTPS and ensure Burp’s CA certificate is installed.

**High CPU Usage:**

* Go to ```Project Options > Connections > Reduce Threads``` and set threads to 1-2 for smoother performance.

**Error: “Untrusted Certificate” in Browser:**

* Ensure the CA certificate is installed under Trusted Root Authorities (Windows) or System Keychain (macOS).






