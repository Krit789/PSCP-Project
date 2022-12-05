# Project &lt;e&gt;Note

Versitile, beautiful, personalized just for you.

&lt;e&gt;Note is more than a note it's a personal diary.

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

## <b>Environments</b>
It's strongly recommended that you work under python virtual environment

Make sure you have <code>venv</code> installed.

    pip install virtualenv

Creating virtual environment

    py -m venv <virtual-environment-name>

Activating virtual environment

(Windows - Powershell)

    env/Scripts/Activate.ps1

(macOS / Linux)

    .\/env/Scripts/activate

Now you're set to begin the next step<br />

## <b>Getting all the Requirements</b>

    pip install -r requirements.txt

## <b>Running the app</b>
*Accessible from all network interfaces
### <b>For developemnt</b>
    python main_dev.py

### <b>For production</b>
Powered by FastWSGI

    python main_prod.py

## Built with
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]


[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com