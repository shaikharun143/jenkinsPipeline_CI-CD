# Task 2 — Simple Jenkins Pipeline for CI/CD

A basic CI/CD pipeline that automatically **builds**, **tests**, and **deploys** a small
Flask web app using **Jenkins** and **Docker**. Every push to GitHub triggers Jenkins,
which builds a Docker image, runs the tests, and redeploys the app as a running container.

---

## Tools used

| Tool   | Role |
|--------|------|
| Flask  | The sample web application being deployed |
| Docker | Builds the app into an image and runs it as a container |
| Jenkins| Automation server that runs the pipeline on every commit |
| GitHub | Hosts the code and the `Jenkinsfile`, triggers the pipeline |

---

## Repository contents

| File              | Purpose |
|-------------------|---------|
| `app.py`          | Flask app with `/` and `/health` routes |
| `requirements.txt`| Python dependencies (Flask, pytest) |
| `test_app.py`     | Tests run during the Test stage |
| `Dockerfile`      | Instructions to build the Docker image |
| `Jenkinsfile`     | Declarative pipeline: Checkout -> Build -> Test -> Deploy |
| `.gitignore`      | Files Git should ignore |
| `README.md`       | This guide |

---

## Pipeline stages

1. **Checkout** — pulls the latest code from GitHub.
2. **Build** — runs `docker build` to create the image and tags it.
3. **Test** — runs `pytest` inside a throwaway container; the pipeline fails if a test fails.
4. **Deploy** — removes the old container and starts a fresh one on port 5000.

---

## Full step-by-step setup

These steps assume an Ubuntu machine (a local VM, a cloud instance, or WSL on Windows).
On a cloud instance, open ports **8080** (Jenkins UI) and **5000** (the app) in the firewall.

### 1. Update the machine
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Docker
```bash
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
docker --version
```

### 3. Install Java (Jenkins requirement)
```bash
sudo apt install -y openjdk-17-jdk
```

### 4. Install Jenkins
```bash
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/" \
  | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install -y jenkins
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
```

### 5. Unlock Jenkins
Open `http://<server-ip>:8080` in a browser, then get the password:
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
Paste it, install the **suggested plugins**, and create an admin user.

### 6. Allow Jenkins to use Docker (important!)
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```
Without this the Build stage fails with a Docker "permission denied" error.

### 7. Push this repo to GitHub
```bash
git init
git add .
git commit -m "Add Flask app, Dockerfile and Jenkinsfile"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```

### 8. Create the pipeline job in Jenkins
- **New Item** -> name it -> select **Pipeline** -> OK
- Scroll to the **Pipeline** section and set:
  - Definition: **Pipeline script from SCM**
  - SCM: **Git**
  - Repository URL: your GitHub repo URL
  - Branch: `*/main`
  - Script Path: `Jenkinsfile`
- **Save**

### 9. Configure the trigger (run on each commit)
Pick one:

**Option A — Poll SCM (simple, no public URL):**
In the job config, under **Build Triggers**, tick **Poll SCM** and enter:
```
H/5 * * * *
```
Jenkins checks GitHub every 5 minutes and builds if there is a new commit.

**Option B — GitHub webhook (instant, needs a reachable Jenkins):**
- In the job, tick **GitHub hook trigger for GITScm polling**.
- In GitHub: **Settings -> Webhooks -> Add webhook**.
- Payload URL: `http://<jenkins-ip>:8080/github-webhook/`
- Content type: `application/json`

### 10. Run and test
- Click **Build Now** for the first run.
- Watch the stages and open **Console Output** for logs.
- When it goes green, open `http://<server-ip>:5000` to see the app.
- Now edit `app.py`, commit, and push. Jenkins should run automatically and redeploy.

---

## Run it locally without Jenkins (optional sanity check)
```bash
docker build -t my-flask-app .
docker run -d --name my-flask-app-container -p 5000:5000 my-flask-app
curl http://localhost:5000
```

---

## Outcome
You now have a working CI/CD pipeline: a single `git push` automatically builds a Docker
image, runs the tests, and deploys the updated app with no manual steps.
