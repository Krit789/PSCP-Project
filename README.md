# Project &lt;e&gt;Note

Versitile, beautiful, personalized just for you.

&lt;e&gt;Note is more than a note it's a personal diary.

### Projects Report

&emsp; Please sign-in with KMITL's office 365 account to view this file : https://bit.ly/mypscpprojectreport

### Features 
<li>Keep your credentials safe with hashing-salting using Scrypt algorithm.</li>
<li>Stand out with profile image with support for WebP HEIC and AVIF format.</li>
<li>You can create an infinite number of notes.</li>
<li>Markdown formatting allowed you to personalize your notes like inserting images, making a table and more.</li>
<li>Support for all-session logout for additional security.</li>
<li>Notes stats for keeping track of your creation.</li>

<br>

## <mark style="background-color: #FF5632">Please read the instruction before creating a pull request</mark>

# Setup
## <b>Projects</b>
Start by cloning the repository

    git clone https://github.com/Krit789/PSCP-Project.git

Enter project directory

    cd PSCP-Project

Python 3.11 Installation for Ubuntu 22.04 LTS

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.11
    sudo apt-get install python3-dev
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin python3.11 2
Then select number that represent Python 3.11

## <b>Environments</b>
It's strongly recommended that you work under python virtual environment

Make sure you have <code>venv</code> installed.
Windows / macOS

    pip install virtualenv


Linux

    sudo apt-get install python3.11-venv

<b>Creating virtual environment</b>

Windows / macOS / Linux

    python3 -m venv <virtual-environment-name>

<b>Activating virtual environment</b>

Windows Powershell

    env/Scripts/Activate.ps1

macOS / Linux

    source venv/bin/activate

Now you're set to begin the next step<br />

## <b>Getting all the Requirements</b>

    pip install -r requirements.txt

## <b>Running the app</b>
*Accessible from all network interfaces

### <b>Windows</b>

### <b>For development</b>
    python -m main_dev

### <b>For production</b>
Powered by FastWSGI

    python -m main_prod

### <b>macOS / Linux</b>

### <b>For development</b>
    python3 -m main_dev

### <b>For production</b>
Powered by FastWSGI

    python3 -m main_prod


## Built with
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]


[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
