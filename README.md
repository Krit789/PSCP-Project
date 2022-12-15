# Project &lt;e&gt;Note

Versitile, beautiful, personalized just for you.

&lt;e&gt;Note is more than a note it's a personal diary.

### Projects Report

&emsp; Please sign-in with KMITL's Office 365 account to view our report : https://bit.ly/mypscpprojectreport

### Features 
<li>Keep your credentials safe with hashing-salting using Scrypt algorithm.</li>
<li>Stand out with profile image with support for WebP HEIC and AVIF format.</li>
<li>You can create an infinite number of notes.</li>
<li>Markdown formatting allowed you to personalize your notes by inserting images, making your statements even clearer.</li>
<li>Support for all-session logout for additional security.</li>
<li>Notes stats for keeping track of your creation.</li>
<li>Customize your note background and choose your own profile picture.</li>
<li>With link sharing your notes can be shared with the rest of the world.</li>

<br>

# Setup
## <b>Projects</b>

<b>Python 3.11 is recommended to run our project. Anything older may or may not work, try at your own risk!</b>

Start by cloning the repository

    git clone https://github.com/Krit789/PSCP-Project.git

Enter project directory

    cd PSCP-Project

Installation for Ubuntu 22.04 LTS with Python 3.11 

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.11
    sudo apt-get install python3-dev
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin python3.11 2
Then select number that represent Python 3.11

## <b>Environments</b>
It's strongly recommended that you work under python virtual environment

Make sure you have <code>venv</code> installed.

&ensp; Windows

    pip install virtualenv
    
&ensp; MacOS

    pip3 install virtualenv

&ensp; Linux

    sudo apt-get install python3.11-venv
<br/>
<b>Creating virtual environment</b>

Windows

    python -m venv <virtual-environment-name>

macOS / Linux

    python3 -m venv <virtual-environment-name>

<br/>

<b>Activating virtual environment</b>

Windows Powershell

    Set-ExecutionPolicy RemoteSigned
    <virtual-environment-name>/Scripts/Activate.ps1

Windows Command Prompt

change directory into \<virtual-environment-name\>/Scripts/

    activate.bat

macOS / Linux

    source <virtual-environment-name>/bin/activate
<br/>

Now you're set to begin the next step<br />

## <b>Getting all the Requirements</b>

    pip install -r requirements.txt

## <b>Running the app</b>
*Accessible from all network interfaces

### <b>Windows</b>

### <b>For development</b>
    python main_dev.py

### <b>For production</b>
Powered by waitress

    python main_prod.py

### <b>macOS / Linux</b>

### <b>For development</b>
    python3 main_dev.py

### <b>For production</b>
Powered by waitress

    python3 main_prod.py


## Built with
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]


[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
