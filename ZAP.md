This wiki provides a guide to setting up and Testing Vulnerabilities using ZAP.

[Zap Report](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/blob/main/docs/ZAP_Scanning_Report.pdf)
# What is ZAP?
- Zed Attack Proxy (ZAP) is a powerful, open-source tool used by developers and security analysts to identify vulnerabilities in web applications. With user-friendly interfaces and automation capabilities, ZAP helps improve application security throughout development. This guide provides a step-by-step process to install, configure, and implement ZAP effectively.
- ZAP serves as a "man-in-the-middle" proxy, monitoring and examining all online traffic that passes between a web server and a web client (such as a browser). ZAP may identify and reveal a variety of security flaws, including those included in the OWASP Top 10 vulnerabilities, by examining this traffic.
- ZAP’s primary goal is to help security testers find vulnerabilities in web applications during both development and production.

# Why ZAP?
- Free and Open-Source
- Ease of Use
- Active Community
- Extensible

# Key Features
- Intercepting Proxy
- Automated Scanning
- Manual Testing Tools
- API Integration

# Table of contents
1. [Installation](#Installation)
2. [Configuration](#Configuration)
3. [Implementation](#Implementation)
4. [Usage](#Usage)
5. [Troubleshooting](#Troubleshooting)

# Installation 
## macOS: 
- Terminal command example for Homebrew, e.g., brew install zaproxy
- Visit the official [ZAP Download Page](https://www.zaproxy.org/download/)
- Scroll down to the macOS section and download the .dmg file
> - There will be 2 options on macOS individual can download as their system 
     requirements
> > - Intel - amd64
> > - Apple Silicon - aarch64
- After the download is complete, double-click the .dmg file to open it
- Drag the ZAP icon into your Applications folder
- Once it's copied, you can eject the .dmg file
- Open Finder and navigate to the Applications folder

# Configuration
**Proxy Interception:** Fundamentally, ZAP serves as an intercepting proxy. In other words, ZAP intercepts and examines all HTTP/S communication while positioned in between the browser and the web application. If you set up ZAP as your browser's proxy, ZAP will track, examine, and even alter requests and answers in real time.
**Proxy Setup:** “Configure ZAP to act as a proxy between your browser and the web application. In ZAP’s settings, assign 127.0.0.1 as the address and 8080 as the port. This intercepts web traffic for analysis.”
SSL Configuration: Briefly cover SSL setup to enable secure traffic interception, especially useful for testing HTTPS sites.

## Step 1: Set up ZAP Proxy

- Open ZAP on your machine <img width="1440" alt="Screenshot 2024-10-02 at 3 58 43 PM" src="https://github.com/user-attachments/assets/66738d56-0f52-4444-9d46-a62eee9a3817">

**Fig 1: Home page of Zed Attack Proxy**

**Sections of the interface**

- **Sites Pane (Top Left):** A tree structure of every website you visit is displayed here. ZAP will add the requested domains and URLs to this list as you navigate.
- **History Pane (Bottom Left):** Every request and response, including headers and contents, is logged in this window. For more investigation, you can examine each request separately.
- **Request/Response Tabs (Right Panel):** The headers, body, and parameters of a request are shown here when you choose it from the History window. It enables you to examine or alter the traffic.
- **Spider and Active Scan:** We'll go into more depth later, but these programs automatically crawl and scan webpages for vulnerabilities.

Click on the Tools menu and choose Options <img width="929" alt="Screenshot 2024-10-02 at 4 00 56 PM" src="https://github.com/user-attachments/assets/6ebb5089-2e9d-41a5-accf-de16725a2cd9">

**Fig 2: Open Tools menu and choose Options**

Under the Local Proxy settings, ensure that the default proxy port is set (e.g., ```8080```). You can change this if needed <img width="762" alt="Screenshot 2024-10-02 at 4 03 16 PM" src="https://github.com/user-attachments/assets/78a9370f-773a-47d2-ae69-15854072d045">

**Fig 3: Options of ZAP tool**

#### Why IP address ```127.0.0.1``` and port ```8080``` are used?
##### IP address ```127.0.0.1```
- ```127.0.0.1``` is the loopback address, also known as localhost. It is a reserved IP address that refers to your own computer, allowing your machine to communicate with itself.
- When you configure ```127.0.0.1``` in any network tool such as OWASP ZAP or a browser, you are telling the tool to route traffic through your local machine. 
- This is useful for capturing and analyzing traffic locally, without sending it out over the actual network.
- In this case, ZAP acts as a man-in-the-middle proxy, where traffic from your browser is sent to ZAP running on your machine at 
```127.0.0.1``` instead of directly to the web server.
##### Port ```8080```
- Port numbers are used by computers to identify specific services or applications running on a system. 
- The port allows multiple programs to listen on the same IP address without conflict.
- Port ```8080``` is often used as an alternative to port 80 the default port for HTTP web traffic. 
- It’s typically used for web proxies, development servers, and testing environments.
- ZAP listens on port ```8080``` by default to intercept traffic sent from the browser, acting as a proxy server between the browser and the target web application.

#### Why is this Configuration Important in ZAP?
When you configure ZAP to listen on ```127.0.0.1:8080```, it means:
- ZAP is running locally on your machine.
- It listens to and intercepts traffic from your browser to any external website, allowing you to analyze the HTTP/HTTPS requests and responses in real-time.
- This configuration makes it safe for testing web applications without affecting external servers or other users because the traffic is isolated to your machine.

## Step 2: Configure Firefox to Use ZAP as a Proxy

- Open Firefox and go to the Settings. <img width="1277" alt="Screenshot 2024-10-02 at 4 11 20 PM" src="https://github.com/user-attachments/assets/03ddf3ee-0198-41bb-ba45-9ca838fdada6">

**Fig 4:** Home page of FireFox

- Search for Network Settings and click on Settings. <img width="1046" alt="Screenshot 2024-10-02 at 4 12 42 PM" src="https://github.com/user-attachments/assets/16567938-817e-4259-a4ba-5c68fce54ced">

**Fig 5:** Search Network setings inside Firefox browser

- Choose the Manual proxy configuration option.

- Set the HTTP Proxy to ```127.0.0.1``` and the Port to ```8080``` (or whatever port you configured in ZAP). <img width="674" alt="Screenshot 2024-10-02 at 4 13 27 PM" src="https://github.com/user-attachments/assets/5b7c4b70-f630-4d0b-a945-ae6c0909e767">

**Fig 6:** Open Connection Settings inside Firefox browser

- Check the box that says Use this proxy server for all protocols.
- Click OK to apply the settings.

## Step 3: Test the Proxy Setup

- In Firefox, visit a simple website (e.g., I have taken http://testphp.vulnweb.com/) to ensure that the traffic is routed through ZAP. <img width="1134" alt="Screenshot 2024-10-02 at 4 20 14 PM" src="https://github.com/user-attachments/assets/0b84efea-3b0e-465a-8673-fd8c0eb02633">

**Fig 7:** Opening Example website (http://testphp.vulnweb.com/) to test the vulnerabilities inside the Firefox

- In ZAP, you should see the traffic captured in the Sites or History tab.  <img width="1437" alt="Screenshot 2024-10-02 at 4 22 17 PM" src="https://github.com/user-attachments/assets/685be166-faed-4945-b63e-4ee9017ad59f">

**Fig 8:** Traffic of the website inside the ZAP tool

# Implementation
- Active vs. Passive Scanning: Briefly explain when and why to use each type of scan, e.g., passive for initial analysis and active for deeper testing.
- Automated Scanning Workflow: "1) Run a passive scan. 2) Review findings. 3) Set rules and triggers. 4) Initiate an active scan. 5) Generate and analyze reports.”
- Example Workflow: Provide a sample scan command and expected output snippet: zap-cli --active-scan <target_url> and explain each output.
## Automated Scanning
- ZAP provides a variety of automated scanning capabilities, including as spidering, active scanning, and passive scanning. These enable users to swiftly conduct security evaluations.
#### Passive Scan:
- The passive scanner does not change or interfere with the application; instead, it examines requests and answers as they move through the proxy.
- Passive scanning is safer for production situations because it doesn't transmit any extra traffic to the server.
- Typically, the passive scan searches for common problems such as information leakage, inadequate SSL/TLS setups, and missing security headers.
#### Active Scan:
- To check for vulnerabilities, the active scanner makes more queries to the target web application. 
- Active scanning should normally be used with caution, especially on production systems, as it can be obtrusive and may disrupt specific web application functionality.
#### Spidering:
- To find every resource on a web application, ZAP's spider crawler is utilized. It builds a sitemap by methodically visiting each link on the target website. Spidering is helpful for locating obscure or unknown pages that may be at risk.
## Step 1: Scanning a Target Website
### Spider the Website:
To find every page and link on a website, ZAP's Spider tool crawls it. When mapping a huge application or making sure you've covered every region for testing, this is really helpful.

# Usage
- This section walks you through sample tests with ZAP, from simple proxy setups to complete security assessments.”

- **Login Session Handling:** "To test a login-protected page, use ZAP's session handling features to ensure all pages, even those requiring login, are covered. Go to Options > Session Management and enter session cookies manually or through browser plugins.”
- **SQL Injection Detection:** "Enable ZAP's SQL injection test rules, then run an active scan to see if the application is vulnerable. Look for entries under ‘Injection Flaws’ in the report."
Example Code: Provide code snippets or JSON configurations for automated workflows with zap-cli.

#### [Zap Report](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/blob/main/docs/ZAP_Scanning_Report.pdf )
In ZAP, enter the URL of the website you want to scan in the URL to Attack field in the top bar. <img width="1355" alt="Screenshot 2024-10-04 at 11 31 07 AM" src="https://github.com/user-attachments/assets/337680e5-eb7b-4cc1-af69-7db4ca55939f">

**Fig 9:** Entering the URL manually to check the vulnerabilities in ZAP tool

ZAP will crawl the site and find all the accessible pages. 

<img width="469" alt="Screenshot 2024-10-04 at 11 48 55 AM" src="https://github.com/user-attachments/assets/b0ccee17-7022-47e4-8f44-a99030cb5c3a">

**Fig 10:** Pages that are accessible to check vulnerabilities in ZAP tool

**Configure the Spider:**
- In the Sites pane, right-click on the website you want to spider and choose Attack > Spider Site.
- In the Spider configuration, choose the scope (domains and subdomains) and hit Start.
On Spider tab we can see the following. <img width="1433" alt="Screenshot 2024-10-04 at 11 52 31 AM" src="https://github.com/user-attachments/assets/2b06bc73-ccf0-4366-8464-5f32b8c79625">

**Fig 11:** Performing Spidering Operation
- As the Spider runs, you’ll see new URLs appear in the Sites pane, indicating that they’ve been discovered. ZAP can also discover hidden or hard-to-find pages.

### Perform Active Scanning:
ZAP's most effective technique for identifying security flaws, such as SQL Injection, XSS, insecure cookies, and more, is Active Scanning.
**Initiating a Scan:**
- After manually browsing the website or spidering it, right-click on it in the Sites pane and choose Attack > Active Scan.
- To check for typical vulnerabilities, ZAP will send the server specially constructed queries. 

<img width="1129" alt="Screenshot 2024-10-04 at 12 01 23 PM" src="https://github.com/user-attachments/assets/6759780a-a81f-4d08-bdf9-0733258a7aa6">

**Fig 12:** This shows Performing active scanning

- ZAP will perform vulnerability tests on the website.  <img width="1430" alt="Screenshot 2024-10-04 at 12 02 27 PM" src="https://github.com/user-attachments/assets/8b125afa-3d2e-46a8-9bd1-361fb18cf2af">

**Fig 13:** Zap performing vulnerabilities test

## Step 2: Viewing Results
- **Results:** As the scan goes on, vulnerabilities with varying severity levels (low, medium, high, and critical) will be shown on the Alerts tab. Each warning may be clicked to provide comprehensive details, such as the issue's discovery method and possible corrective actions.
- **Customizing the Scan Policy:** By turning on or off particular attack types, you may alter the scan policy. If you're testing particular features of the web application, this is helpful.
- You can view detailed information about each alert, including the risk level and possible exploitations.  <img width="1434" alt="Screenshot 2024-10-04 at 12 04 14 PM" src="https://github.com/user-attachments/assets/698e9289-2420-4988-9ac1-1f738d922d45">

**Fig 14:** Viewing Alerts of the website inside ZAP tool

## Step 3: Authentication and Session Handling

Authentication is necessary for many online applications. It is possible to set up ZAP to operate with authenticated sessions.
**Setting Up Authentication:**
**1. Context Management:**
- ZAP uses Contexts to manage different aspects of a site, such as login/logout mechanisms.
- Right-click on a site in the Sites pane, and choose Include in Context.
<img width="1136" alt="Screenshot 2024-10-18 at 7 34 54 PM" src="https://github.com/user-attachments/assets/2690dd71-70e1-4479-b4c6-5a7d87b1b7a8">

**Fig 15**: Figure shows the context management setup

**2. Configure Authentication:**
- In the Context settings, you can specify login URLs, session management methods, and parameters that indicate a logged-in session.
- You can even script custom login mechanisms using ZAP's built-in scripting interface.
<img width="718" alt="Screenshot 2024-10-18 at 7 38 14 PM" src="https://github.com/user-attachments/assets/9d78eadf-33c7-4f3d-9ec3-cbe7fbe8d215">

**Fig 16**: This figure shows Context settings, you can specify login URLs, session management methods, and parameters that indicate a logged-in session

## Step 2: Saving and Analyzing Reports
### Generate a Report:
- After scanning, you can generate an HTML report by going to Reports > Generate Report.
- Choose the format and location to save the file.
<img width="694" alt="Screenshot 2024-10-04 at 1 03 48 PM" src="https://github.com/user-attachments/assets/b5bc04e0-1f5c-4a5f-87c8-d801347858cf">

**Fig 17:** This figure shows the Report File formate i.e; ```.html```

### Review Alerts:

- ZAP will categorize the vulnerabilities found (e.g., XSS, SQL Injection) under the Alerts tab. Each alert has detailed descriptions and recommended fixes. 

<img width="820" alt="Screenshot 2024-10-30 at 9 09 47 AM" src="https://github.com/user-attachments/assets/c91792ec-d31e-4a61-925e-3691c02eb7b7">

**Fig 18:** The summery of the alerts in side the report

<img width="756" alt="Screenshot 2024-10-30 at 9 10 03 AM" src="https://github.com/user-attachments/assets/b6e049ac-8ad9-4027-908f-c9523991529c">

**Fig 19:** The fig represents the types of alerts, Risk level and no of instances.

<img width="840" alt="Screenshot 2024-10-30 at 9 10 43 AM" src="https://github.com/user-attachments/assets/f86a2184-b9b0-4fda-92b2-f6984e7ed667">

**Fig 20:** The fig represents the alert Missing click-jacking header.

# Troubleshooting
#### Check macOS Permissions: 
- If ZAP can’t bind to a port or access certain system resources, check if macOS security settings are blocking it.
> > - Open System Preferences > Security & Privacy > Privacy and ensure ZAP has access to any relevant services, such as Full Disk Access if needed for certain scans.
<img width="707" alt="Screenshot 2024-10-04 at 3 34 18 PM" src="https://github.com/user-attachments/assets/2169798b-3a9b-4b75-8824-62beaf2dfc3a">

**Fig 20:** Security settings of MacOS

**General troubleshooting tips for Zed Attack Proxy (ZAP)**
#### 1. ZAP Not Starting or Crashing

- **Check Java Version:** Java is needed for ZAP to function. Make sure Java is installed in the proper version. Use the terminal to type ```java --version``` to verify.
- **Reinstall ZAP:** If ZAP still won’t launch, try reinstalling it. Make sure you're downloading the latest stable version from the official [ZAP website](https://www.zaproxy.org/).
- **Check Logs:** ZAP maintains logs that can be found in the ```~/.ZAP``` directory on macOS and Linux or ```%USER_HOME%\.ZAP``` on Windows. Review the logs for errors.

#### 2. ZAP is Slow or Unresponsive

- **Disable Unused Add-ons:** ZAP has many add-ons that may slow down performance if not necessary. Disable any unused add-ons from the "Manage Add-ons" menu.
- **Allocate More Memory:** ZAP may need more memory for larger scans. Edit the startup script to increase the allocated memory. For example, you can adjust the ```-Xmx``` parameter in the zap.sh script (Linux/macOS) or zap.bat script (Windows).
- **Limit Scope:** If your scan covers too many URLs, try limiting the scope by specifying the exact areas you want to test.

#### 3. Unable to Intercept Traffic

- **Install Root CA Certificate:** For ZAP to intercept HTTPS traffic, you need to install its Root CA certificate in your browser. You can do this by going to the "Tools > Options > Dynamic SSL Certificates" section and exporting the certificate, then installing it in your browser.
- **Proxy Configuration:** Ensure that ZAP's proxy settings match your browser’s proxy configuration. The default proxy for ZAP is localhost:8080. Check that the browser is configured to use this proxy.
- **Check Firewall/Antivirus:** Some firewalls or antivirus programs might block ZAP from working. Ensure ZAP has the necessary permissions to intercept traffic.

#### 4. ZAP Scanner Not Detecting Vulnerabilities

- **Update Add-ons:** Make sure that ZAP and its add-ons are fully updated. Vulnerability checks and attack vectors improve over time.
- **Scan Policy:** Review the scan policy to ensure that the appropriate tests are being run. You can configure ZAP’s scan policy in the "Policy Manager" to customize the types of attacks.
- **Authentication:** If you're testing a website that requires authentication, ensure that ZAP is properly configured for authenticated scanning. You can set up authentication under the "Context" menu.

#### 5. ZAP Fails to Crawl Website

- **JavaScript-heavy Websites:** ZAP's crawler may struggle with JavaScript-heavy or single-page applications (SPAs). Consider enabling the AJAX Spider, which can handle dynamic content better.
- **Robots.txt or Security Headers:** Some websites have restrictions in place (e.g., ```robots.txt```, CSP headers) that prevent ZAP from crawling or scanning them. Check if any such restrictions are blocking ZAP.

#### 6. ZAP Fails to Install Add-ons

- **Check Network Settings:** Ensure that ZAP can access the internet to download add-ons. If you’re behind a proxy, make sure the proxy settings are configured in ZAP.
- **Manual Add-on Installation:** If automatic installation fails, try downloading the add-ons manually from the ZAP marketplace and installing them from the “Manage Add-ons” menu.

#### 7. ZAP Fails to Start Proxy

- **Port Conflict:** The default port for ZAP’s proxy is ```8080```. If another service is using this port, ZAP won’t be able to start the proxy. Change the proxy port in "Tools > Options > Local Proxies" to an available port.

# Resources
#### ZAP User Guide: 
- The official documentation provides detailed explanations on ZAP’s features, configuration, and usage:
- [ZAP User Guide](https://www.zaproxy.org/docs/desktop/)
#### API Documentation: ZAP has a powerful REST API for automation and integration:
- [ZAP API Documentation](https://www.zaproxy.org/docs/api/#introduction)
#### Tutorials and Getting Started Guides:
- OWASP ZAP Quick Start Guide: For beginners, this guide helps you set up ZAP, configure your browser, and start scanning for vulnerabilities:
- [OWASP ZAP Quick Start Guide](https://www.zaproxy.org/docs/desktop/addons/quick-start/)
#### ZAP Add-ons Marketplace
- ZAP has a built-in marketplace where you can find add-ons to extend ZAP's functionality. You can access it directly in the ZAP UI by going to:
- [ZAP Marketplace](https://www.zaproxy.org/addons/)
- Popular Extensions:
> > - Advanced SQL Injection Scanner: Provides more in-depth testing for SQL injection vulnerabilities.
> > - Port Scanner: A built-in port scanner to find open ports on a target.
> > - HUD (Heads Up Display): A new UI that provides contextual security information as you browse.