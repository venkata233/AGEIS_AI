\# AEGIS – Installation and Setup Guide



\## 1. Project Repository



GitHub: https://github.com/venkata233/AGEIS\_AI



\## 2. Prerequisites



Install the following software on Windows 10/11:



1\. Python 3.11

2\. Git

3\. Visual Studio Code

4\. Docker Desktop

5\. WSL2 (required for Docker Desktop on Windows)



Verify installations:



```powershell

python --version

git --version

code --version

docker --version

docker compose version

```



\## 3. Clone the Repository



```powershell

cd "$env:USERPROFILE\\Documents"



git clone https://github.com/venkata233/AGEIS\_AI.git



cd AGEIS\_AI



code .

```



\## 4. Create Python Virtual Environment



```powershell

py -3.11 -m venv .venv



Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass



.\\.venv\\Scripts\\Activate.ps1

```



\## 5. Install Dependencies



```powershell

python -m pip install --upgrade pip



pip install -r requirements.txt

```



\## 6. Configure Gemini API Key



Obtain a personal API key from Google AI Studio:



https://aistudio.google.com/



Create the environment file in the project root:



```powershell

New-Item -Path .env -ItemType File

notepad .env

```



Add your own API key:



```env

GEMINI\_API\_KEY=YOUR\_GEMINI\_API\_KEY

```



Never commit your actual API key to GitHub.



\## 7. Start the Generated URL Shortener



Navigate to the generated application:



```powershell

cd .\\generated\_projects\\mcp\_workspace

```



Build and start the Docker services:



```powershell

docker compose up -d --build

```



Check running containers:



```powershell

docker compose ps

```



View application logs:



```powershell

docker compose logs -f

```



\## 8. Verify the URL Shortener



Open the API documentation:



http://localhost:8000/docs



Use Swagger UI to test the available API endpoints.



\## 9. Stop and Restart Services



Stop containers without deleting persistent data:



```powershell

docker compose stop

```



Start them again:



```powershell

docker compose start

```



Stop and remove containers while retaining named volumes:



```powershell

docker compose down

```



\## 10. Git Workflow



Check repository status:



```powershell

git status

```



Download future changes:



```powershell

git pull

```



Commit your changes:



```powershell

git add .

git commit -m "Describe your changes"

git push

```



\## 11. Important Notes



\- Each developer must use their own Gemini API key.

\- Never upload `.env`, API keys, passwords, or credentials.

\- The `.venv` folder is created locally and should not be committed.

\- ChromaDB data may need to be recreated if it is excluded from Git.

\- Docker Desktop must be running before starting the generated URL Shortener.

\- These instructions cover environment setup and the generated URL Shortener runtime. The AEGIS agent workflow startup command must be documented separately after its entry point is verified.



\## Repository



https://github.com/venkata233/AGEIS\_AI

