# Distributed Systems - Project
Student Name: Gregory Buckley

Student ID: 13325220

This assignment has been written using Python 3.

The Flask framework handles all communication in the system. Flask is framework in Python facilitating HTTPs/HTTP communications.

All file information including bytes of files, hash values and names are contained in JSON field of a HTTPS packet and sent to the URL of the destination server where the information may be extracted. 

The objective of this assignment is to create a distributed file server. The server must be secure and contain a number of features.

My design  is created with use of four main types of systems.

**The Client Proxy**
The client is responsible for handling all user input for writing and reading files within the system. The client has a constant access to connect to the directory server and the locking server. To run the Client Proxy, the user enters the required command ('read' or 'write) followed by a file name. The file names may be loaded in from the cache if needed to read or are read in from a User storage folder for writing out to the file servers.

**The Directory Server**
The Directory Server contains a list of all active file servers and directs workload evenly between them back to the client. The server holds an SQL database, keeping track of all files sent in the system, and their current states.  

**The Locking Server**
The locking server contains a database noting each file distributed between the system and it's current state, whether it is locked by a client currently writing to it, or unlocked.

**The File Servers**
Upon running of the file servers, a port number is entered which the file server will run on. The directory server is then contacted and the file server is ready to recieve files. Any number of File Servers can be created in the system. The File servers store the files it recieves locally.


The following features are supported by the system:

**Directory Server**
After the user enters the command to write a new file to the system, the Directory Server is contacted. The Client sends a json packet containing the name of the file and the hash value of the file. The Directory Server allocates a Master Server and a Replicate Server from the list of current active File Servers and returns their URLs to the Client. The Directory server notes these servers, the file and it's hashvale into it's database.

Upon recieving the server URLs, the client sends the file to both servers and awaits a 200 server response from the File Servers.

With any future writes to a file already in the system, the Directory Server informs the Client on the files location, and both the Master and Replicate Server are updated.

**Replication**
As mentioned above, the client is informed of both the Master Server and Replication Server in the system. The assures that the file is stored in multiple locations. 

**Caching**
Caching is supported by the use of a local storage by the Client. Each time the user reads, or writes to a file, the cache is updated with a copy of that file. If the user wishes to read a file in the system, it contacts the Directory Server to see the current hash value of the file, and compares it to the hash of the file in the cache. If they are equal, then the cached file is up to date and the client reads from it. If not, then the Client is given the Location of the File Server where it may read it from. The Cache is then update with this file.

**Locking**
To prevent two Clients from writing to a file simultaneously, a locking system is introduced. This is supported by the creating of a Locking Server. The Locking Server cntains an SQL database containing a list of all the files and their current locking status. If a Client wishes to write to a file, it must check that the current status of a file is "Unlocked". If so, then they are informed of the status and the Locking Server locks the file. After writing to the file, The Client informs the Locking Server to unlock the file. While a file is locked, no user will have the ability to write to it.

**Security**
Security is handled in my design by use of HTTPS certs. HTTPs and TCP handshakes assure complete certainty to the authentication of communication between the Servers. 

OPENSSL is the library used in my implementation which provides a robust, commercial-grade, and full-featured toolkit for the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols. It is also a general-purpose cryptography library.

Upon running of the system, a CA has not signed the certificates as that would require payment which was not feasable for the project but the current implementation implements one being connected so warning errors may arise.

**Transactions**
Transactions are supported by all file systems being constantly updated with the most current file in the system. When a user wishes to write their file, both the Master and Replicate servers are informed by the Client Proxy.



