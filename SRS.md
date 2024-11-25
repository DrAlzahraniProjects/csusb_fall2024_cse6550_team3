# Software Requirements Specification
for 

***SE textbook chatbot***

Prepared by

***Name***: Maddu, Ganesh (008771081@coyote.csusb.edu)


***Group Name***: [csusb_fall2024_cse6550_team3](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3)




***Instructor***: [Dr. Alzahrani, Nabeel](https://www.csusb.edu/profile/alzahran)

***Course***: CSE 6550: Software Engineer Concepts Fall 2024 

## Table of Contents
- [1 Introduction](#1-Introduction)
>  * 1.1 Purpose
>  * 1.2 Document Conventions
>  * 1.3 Intended Audience and Reading Suggestions
>  * 1.4 Product Scope
>  * 1.5 References
- [2 Overall Description](#2-overall-description)
>  * 2.1 Product Perspective
>  * 2.2 Product Features
>  * 2.3 User Classes and Characteristics
>  * 2.4 Operating Environment
>  * 2.5 Design and Implementation Constraints
>  * 2.6 User Documentation
>  * 2.7 Assumptions and Dependencies
- [3 External Interface Requirements](#3-External-Interface-Requirements)
>  * 3.1 User Interfaces
>  * 3.2 Hardware Interfaces
>  * 3.3 Software Interfaces
>  * 3.4 Communication Interfaces

- [4 System Features](#4-System-Features)
>  * 4.1 System Feature 1: Query Answering
>  * 4.2 System Feature 2: Feedback Mechanism
- [5 Other Nonfunctional Requirements](#5-Other-Nonfunctional-Requirements)
>  * 5.1 Performance Requirements
>  * 5.2 Safety Requirements
>  * 5.3 Security Requirements
>  * 5.4 Software Quality Attributes
- [6 Other Requirements](#6-Other-Requirements)
- [7 Appendices](#7-Appendices)


--- 
# 1. Introduction
The SE Textbook Chatbot project focuses on improving the accessibility of textbook content for students and educators. In academic environments, quickly finding relevant textbook information is crucial for both learning and teaching processes. With this in mind, the chatbot leverages advanced AI frameworks to deliver efficient and accurate answers to user queries in real-time. The chatbot serves as a supplemental tool that reduces the time and effort needed to manually search for information in the textbook "Software Engineering Body of Knowledge V4.0 (SWEBOK V4.0)."

The chatbot’s unique value proposition lies in its ability to handle complex questions and provide contextually relevant responses, while also offering the sources in the form of page numbers and direct links to sections of the textbook. This saves users time and allows them to focus on understanding the material rather than navigating through the textbook. Its integration with a scalable infrastructure ensures that it can support a large number of users without compromising on performance, making it suitable for deployment in universities or other educational institutions.

In developing this SRS, the project team adhered to IEEE standards, ensuring that the document covers both functional and non-functional requirements comprehensively. This document is structured to guide developers, testers, project managers, and stakeholders through the design and development process, ensuring that the chatbot meets its intended objectives.


### 1.1 Purpose
The purpose of the SE Textbook Chatbot is to enhance accessibility to the content of Software Engineering Body of Knowledge V4.0 (SWEBOK V4.0) for students and educators. The chatbot provides accurate and contextually relevant answers to user queries by retrieving specific sections from SWEBOK V4.0, including citations and page references. This tool aims to simplify the process of navigating extensive textbook material, saving users time and effort in their academic or professional endeavors.

This document follows the IEEE standards for software requirements specification and outlines the functional and non-functional requirements for developing the chatbot. Each requirement is assigned a unique identifier for traceability and easy reference. The document is structured to serve as a comprehensive guide for developers, testers, project managers, and stakeholders involved in the project.

### 1.2 Document Conventions
This document adheres to IEEE standards for software requirements documentation. Each functional requirement is assigned a unique identifier such as REQ-1, REQ-2, etc., for easy reference and tracking. Headings follow a hierarchical format to distinguish between sections and subsections, providing a clear and structured presentation of the system’s requirements. Important terms and definitions are explained in the appendices to provide additional clarity for readers.

### 1.3 Intended Audience and Reading Suggestions
The primary audience for this SRS includes developers, testers, project managers, and end-users involved in the development and deployment of the SE Textbook Chatbot. Developers and testers should focus on Sections 3 and 4 for a comprehensive understanding of functional and non-functional requirements. Project managers may prioritize Section 2 to understand the product's scope and overall description, while end-users can consult Section 5 for an overview of system features and capabilities.

### 1.4 Product Scope
The SE Textbook Chatbot is designed to provide real-time responses to user queries based on content from SWEBOK V4.0. This chatbot serves as an intelligent assistant, offering a quick and reliable way to access textbook material for academic and professional purposes. It integrates with scalable infrastructure, making it suitable for deployment in various educational and organizational environments. Key features include citation-based query resolution, an evaluation mechanism using a confusion matrix and six performance metrics, and a secure, scalable deployment model.
### 1.5 References
* GitHub Repository, "csusb_fall2024_cse6550_team3," [Online]. Available: https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3.
* GitHub Wiki, "Wiki for SE Textbook Chatbot," [Online]. Available: https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/wiki.
* SRS WiKi format, "SRS in IEEE standards format reference," [Online]. Available: https://dspmuranchi.ac.in/pdf/Blog/srs_template-ieee.pdf.

# 2. Overall Description

### 2.1 Product Perspective
The SE Textbook Chatbot operates as a key tool in a broader initiative aimed at modernizing educational resources for students. Within the university's digital learning environment, the chatbot plays a vital role by acting as an intelligent assistant capable of navigating complex information contained in textbooks. Unlike traditional search engines that rely solely on keyword matching, the SE Textbook Chatbot integrates Retrieval-Augmented Generation (RAG) architecture, which allows it to provide more contextual and nuanced responses to user queries.

The chatbot's deployment through Docker containers ensures it is flexible and adaptable to various environments. This architecture not only supports scalability but also guarantees minimal downtime during updates or maintenance periods. The use of Docker also facilitates the seamless migration of the system between different servers and platforms, thus future-proofing the chatbot’s deployment strategy for institutions that might require varied infrastructure setups.

Moreover, by leveraging cloud-based university servers, the chatbot can efficiently manage traffic surges, especially during peak usage times like exams. Its ability to process and return answers in real-time—combined with its capability to handle multiple concurrent users—ensures the chatbot is a valuable resource for large cohorts of students.



### 2.2 Product Features
The SE Textbook Chatbot enables users to interactively query information from SWEBOK V4.0. The chatbot processes queries in real-time and retrieves relevant sections from the textbook to answer user questions. It provides detailed citations, including page references and direct links to sections in the digital version of SWEBOK V4.0. To assess its performance, the system generates an evaluation report based on a confusion matrix and six key metrics—sensitivity, accuracy, precision, recall, F1-score, and specificity—ensuring continuous improvement and reliability.

### 2.3 User Classes and Characteristics
The SE Textbook Chatbot caters to two primary user groups: students and teachers.

Students will use the chatbot to assist with their studies, particularly when preparing for exams or working on assignments. The chatbot simplifies the process of retrieving textbook content, making it easier for students to find specific sections or references. This is particularly useful when students need to cite textbook material in their work or when they are trying to understand complex topics covered in the course.

Teachers can utilize the chatbot as a resource when preparing lectures or assignments. The chatbot can quickly retrieve textbook information, allowing teachers to reference material during lectures or provide students with detailed answers to their questions. By offering easy access to textbook content, the chatbot supports educators in maintaining a structured and resource-rich learning environment.

Each user class will interact with the chatbot through a web-based interface, making it accessible from any device with an internet connection. The system is designed to accommodate users of varying technical expertise, requiring no advanced knowledge of software engineering to use the chatbot effectively.

### 2.4 Operating Environment
The SE Textbook Chatbot is deployed in a Dockerized environment, which ensures that it is platform-independent and can be easily scaled. The chatbot is accessible via common web browsers such as Chrome, Edge, and Brave, providing users with a seamless experience on both desktop and mobile devices. The system is hosted on university or cloud-based servers, depending on the specific deployment setup. This infrastructure is designed to handle a high volume of users, with the capability to support up to 100 concurrent users while maintaining a response time of less than 3 seconds.

By leveraging cloud infrastructure, the chatbot can be easily updated and maintained without requiring downtime, ensuring that users always have access to the latest version of the system. The system is also designed to integrate with the university’s existing authentication systems, ensuring that only authorized users (students and teachers) can access the chatbot’s features.

### 2.5 Design and Implementation Constraints
The SE Textbook Chatbot is designed to provide efficient and reliable access to information from the SWEBOK textbook, adhering to institutional and project-specific guidelines. The system architecture leverages advanced AI frameworks tailored for natural language understanding and rapid information retrieval. The chatbot is built to ensure high performance and scalability, capable of handling concurrent users with minimal response time. Key components, such as LangChain and FAISS, enable seamless integration between user queries and textbook content retrieval. By focusing on established and robust AI tools, the design emphasizes accuracy, scalability, and ease of maintenance while ensuring compliance with institutional requirements. The chatbot operates within a secure, Dockerized environment to provide platform independence and straightforward deployment in diverse infrastructures.

### 2.6 User Documentation
Comprehensive user documentation is provided to ensure both end-users and contributors can effectively utilize and maintain the SE Textbook Chatbot. The documentation includes a detailed overview of the system's architecture, deployment guidelines, and key features. It also explains the evaluation methodology, which uses a confusion matrix and six performance metrics—sensitivity, accuracy, precision, recall, F1-score, and specificity—to assess the chatbot's responses. Instructions for using the chatbot, accessing the feedback mechanism, and monitoring performance metrics are clearly outlined to ensure ease of use. All references in the documentation are aligned with the project's scope and technical framework, avoiding the inclusion of unrelated or unused technologies.

# 3. External Interface Requirements

### 3.1 User Interfaces
The SE Textbook Chatbot’s user interface is designed to be intuitive and user-friendly, making it accessible to users with varying levels of technical expertise. The interface, built using StreamLit, allows users to submit text-based queries, receive immediate answers, and interact with various chatbot features, such as providing feedback on response accuracy.

## Fig. 1: Low-Fidelity Diagram for SE Textbook Chatbot Interface
![image](https://github.com/user-attachments/assets/61dcab01-814b-4154-9250-1bcdf4e662bb)


In addition to query handling, the user interface also displays feedback statistics. These statistics include the number of questions asked, the accuracy rate of the chatbot’s responses, and common keywords or topics frequently queried by users. A performance dashboard provides an overview of the chatbot’s overall efficiency, showing metrics like response times and user satisfaction levels. The dashboard is updated daily, ensuring that administrators have access to up-to-date information about the system’s performance.

### 3.2 Hardware Interfaces
The SE Textbook Chatbot does not require any specialized hardware beyond standard web-based systems. It is designed to run on university servers or cloud infrastructure, with Docker containers managing the chatbot's environment. These servers should be equipped with enough memory and processing power to handle multiple users simultaneously while delivering real-time responses. The servers should be capable of handling up to 100 concurrent users, with sufficient memory and processing power to ensure a fast response time of under 3 seconds. The server infrastructure needs to support the chatbot’s scalable architecture, which ensures that the system can handle fluctuations in user traffic, especially during peak usage periods such as exams or assignment deadlines. The hardware used must also comply with the university's data protection policies, ensuring secure handling and storage of any user data collected during chatbot interactions.

### 3.3 Software Interfaces
The chatbot interacts with several software components to deliver a smooth and efficient user experience. It integrates LangChain, which handles natural language processing, and FAISS, which is responsible for rapid document retrieval, enabling the system to respond quickly to user queries. These backend systems are crucial for efficiently managing the chatbot’s core functionality. Docker ensures that all components of the system are packaged in a lightweight container, making it easy to deploy the chatbot across multiple environments while maintaining consistent performance.

The chatbot communicates with users via HTTP/HTTPS protocols, and real-time interaction is enabled through WebSockets or other similar technologies. This allows the system to maintain fast, interactive communication with users, ensuring that responses are delivered within the required 3-second timeframe. Security tools such as Burp Suite Community Edition (BSCE) and Zed Attack Proxy (ZAP) are employed to identify and fix any vulnerabilities in the system, while Docker Scout helps detect and resolve vulnerabilities within the container environment. This combination of interfaces ensures that the chatbot remains secure, responsive, and scalable.
### 3.4 Communication Interfaces
Communication between the chatbot and its users occurs over standard HTTP/HTTPS protocols. The system will provide an API for handling user requests and delivering responses. The chatbot will also use WebSockets or similar real-time communication methods to ensure fast, interactive responses to user queries. Additionally, the system will maintain secure communication channels, adhering to encryption standards to protect user data and ensure privacy. The chatbot’s communication with backend services like FAISS and LangChain will be handled through internal APIs that are optimized for fast, efficient data retrieval and processing.




# 4. System Features

### 4.1 System Feature 1: Query Answering
The core feature of the SE Textbook Chatbot is its ability to answer questions based on the content in SWEBOK V4.0. When a user submits a query, the system retrieves relevant material from the textbook and provides an accurate and concise response. The chatbot ensures responses are contextually relevant and includes direct citations, making it an effective tool for academic and professional use.

### 4.2 System Feature 2: Feedback Mechanism
The feedback mechanism is designed to enhance the chatbot's performance using evaluations based on a confusion matrix and six performance metrics. These metrics analyze the chatbot's responses by evaluating its sensitivity, accuracy, precision, recall, F1-score, and specificity. These insights allow the chatbot to evolve and improve its ability to retrieve and present relevant content from SWEBOK V4.0.

# Fig. 2: Architecture Diagram
![Screenshot (164)](https://github.com/user-attachments/assets/5274a3b5-3a25-49ca-bb5a-5e94de36dc83)



# 5. Other Nonfunctional Requirements

### 5.1 Performance Requirements
Performance is a key consideration for the SE Textbook Chatbot, especially given its intended use in academic environments. The system must be able to handle up to 100 concurrent users, each of whom may submit multiple queries within a short time frame. To maintain performance, the chatbot has been optimized to provide responses within 3 seconds, ensuring that users do not experience delays, even during peak usage times.

The chatbot’s backend has been designed to scale horizontally, allowing for additional resources to be allocated dynamically as user demand increases. This ensures that the system remains responsive and reliable, even under heavy loads. Regular performance testing will be conducted to verify that the system can meet these benchmarks, especially during critical periods such as exams.

### 5.2 Safety Requirements
The SE Textbook Chatbot prioritizes several key safety requirements to ensure that it operates securely and reliably. First, the system must adhere to the data protection policies mandated by the CSE department and the university, ensuring that sensitive user information, such as query history and feedback data, is handled securely. This includes encrypting data transmission and ensuring that personal information is only accessible to authorized personnel. The chatbot must also implement a robust Denial-of-Service (DoS) protection mechanism to prevent overloading the system. To achieve this, users are limited to a maximum of 10 queries per minute. If they exceed this limit, they will be prompted with a message asking them to wait for 3 minutes before submitting additional queries. This protects the system’s resources and prevents malicious or unintentional overloads.

In addition to DoS protection, NeMo Guardrails will be used to enhance the chatbot’s security. NeMo Guardrails is a tool specifically designed to help AI applications follow predefined safety and interaction guidelines. This ensures that the chatbot operates within set boundaries, preventing it from generating inappropriate or unsafe responses. NeMo Guardrails will enforce content moderation rules, making sure that the chatbot only provides responses that align with educational and institutional standards. This layer of protection is critical for ensuring that the chatbot operates in a secure and trustworthy manner.

Furthermore, the chatbot will undergo regular vulnerability scans using tools such as Burp Suite Community Edition (BSCE), Zed Attack Proxy (ZAP), and Docker Scout. These tools will help detect and mitigate potential security vulnerabilities within the system, and any issues identified through these scans will be resolved promptly. Reports generated by these tools will be used to ensure continuous improvements in the system’s security posture. Lastly, the system will implement a reliable backup and recovery strategy to prevent data loss in the event of system failures. This strategy ensures that the chatbot remains available to users with minimal downtime and can recover quickly from unexpected crashes or errors.
### 5.3 Security Requirements
Security is a top priority for the SE Textbook Chatbot, especially given its role in an academic environment where sensitive user data is involved. The system must adhere to strict security protocols to protect against potential vulnerabilities. Regular security audits are conducted using tools such as Burp Suite Community Edition (BSCE), Zed Attack Proxy (ZAP), and Docker Scout to identify and mitigate any vulnerabilities within the system. These tools help ensure that the chatbot’s containerized environment is secure and that any potential risks are addressed promptly.

Furthermore, the chatbot employs encryption for all communications between users and the server, ensuring that sensitive data is protected from unauthorized access. This is particularly important for safeguarding student information and maintaining the privacy of user interactions. In the event of a system failure, backup and recovery mechanisms are in place to minimize data loss and restore the system to full functionality as quickly as possible.
### 5.4 Software Quality Attributes
The SE Textbook Chatbot is designed to meet high standards of reliability, maintainability, and scalability. The system is expected to maintain 99.9% uptime during the academic year, ensuring that it is always available to students and teachers when needed. Backup and recovery systems are in place to ensure data integrity in the event of a system failure, minimizing downtime and data loss.

The chatbot is also built with modularity in mind, allowing developers to update individual components without disrupting the entire system. This modular design ensures that the chatbot can evolve over time, incorporating new features or improvements based on user feedback. Finally, the system’s scalability ensures that it can handle increasing user loads as adoption of the chatbot grows.

# 6. Other Requirements
In addition to the functional and non-functional requirements outlined in previous sections, the SE Textbook Chatbot must comply with university guidelines regarding the use of third-party libraries and services. The chatbot integrates with GitHub for version control, ensuring that all code changes are tracked, reviewed, and approved through pull requests. The system also relies on cloud infrastructure to host its services, providing scalability and cost-efficiency.

Any updates or changes to the chatbot must be thoroughly tested in a staging environment before being deployed to production. This ensures that the system remains stable and that any issues are identified and resolved before they affect end-users. Additionally, the system should provide administrators with detailed usage reports, allowing them to monitor system performance, user engagement, and feedback trends.

# 7. Appendices

**Appendix A:** **Glossary**

* **RAG (Retrieval-Augmented Generation):** A system architecture that combines document retrieval techniques with generative AI models to answer questions based on existing documents.
* **LangChain:** A framework for building applications powered by large language models (LLMs) such as ChatGPT, enabling advanced query understanding and language processing.
* **FAISS (Facebook AI Similarity Search):** A library for fast similarity search and clustering of dense vectors, used for efficient retrieval of relevant textbook content.
* **Docker:** A containerization platform that packages applications and their dependencies into lightweight containers, allowing for easy deployment and scalability.
* **StreamLit:** A Python-based framework for building interactive web applications, particularly useful for data science and machine learning applications. StreamLit powers the chatbot’s frontend interface.
* **NeMo Guardrails:** A tool used to enforce predefined safety and interaction rules in AI systems, ensuring that the chatbot provides safe and appropriate responses.
* **NeMo Curator:** A tool designed to manage large datasets efficiently, supporting the retrieval and generation tasks of the chatbot by organizing and curating data for optimal performance.
* **Jupyter Notebook:** An interactive development environment that allows developers to create and share documents containing live code, equations, and visualizations. It is used to document and test the chatbot’s functionalities.
* **DoS Protection (Denial-of-Service Protection):** A security measure that limits the number of queries a user can submit in a short period to prevent server overload and ensure fair distribution of system resources.
* **Python:** A high-level programming language used to develop the chatbot. Python is favored for its simplicity, versatility, and extensive libraries that support machine learning, AI, and web development.
* **Visual Studio Code (IDE):** A popular Integrated Development Environment (IDE) used by developers for writing, debugging, and managing the chatbot’s code. Visual Studio Code supports Python and other languages, with features such as code completion, version control integration, and extensions.
* **GitHub:** A platform for version control and collaboration, enabling the project team to track changes, collaborate on code, and maintain a record of the development process. GitHub’s repository hosts the source code, documentation, and project management resources such as issues, pull requests, and workflows.

**Appendix B: Analysis Models**

The SE Textbook Chatbot follows a modular system design, ensuring that various components interact seamlessly to provide accurate and fast responses to user queries. The chatbot uses a **Retrieval-Augmented Generation (RAG)** architecture, which integrates document retrieval with AI-based generation of responses.

When a user submits a query through the chatbot interface, the backend processes the input using **LangChain**, which is responsible for understanding the query and determining the appropriate response. The system then utilizes **FAISS** to retrieve relevant sections from the e-version of "Software Engineering: A Practitioner’s Approach." After retrieving the necessary information, a generative AI model like ChatGPT creates a detailed response, which is presented to the user along with citations and highlighted sections from the textbook.

Throughout this process, **NeMo Guardrails** ensures that the chatbot operates within predefined safety and content guidelines, providing accurate and appropriate answers. Additionally, a feedback mechanism allows users to rate the correctness of the responses, with all feedback collected and stored for performance improvements. Various performance metrics, such as response times and accuracy rates, are tracked continuously to ensure that the chatbot remains responsive and efficient under varying loads.

Security is a crucial component of the chatbot’s architecture. **DoS Protection** is implemented to limit users to 10 queries per minute, preventing system overload and ensuring fair resource allocation. Furthermore, vulnerability scanning tools such as **Burp Suite Community Edition (BSCE)**, **Zed Attack Proxy (ZAP)**, and **Docker Scout** are used to identify and mitigate security risks. These tools ensure that the system operates securely and complies with the institution's data protection policies.


**Appendix C: Project Data**

Key variables and their descriptions:

* **chatbotResponseTime:** Measures the time taken for the chatbot to respond to a user query (target: under 3 seconds).
* **concurrentUsers:** The number of users interacting with the system at once (target: up to 100 users).
* **feedbackRating:** Tracks user feedback on the chatbot’s responses using ‘right’ or ‘wrong’ icons.
* **DoSProtection:** Prevents server overload by limiting users to 10 queries per minute.
* **citationList:** Stores textbook citations retrieved for each query.
* **userEngagementMetrics:** Data collected to analyze user interactions, including the number of questions asked, user satisfaction ratings, and response accuracy over time.
