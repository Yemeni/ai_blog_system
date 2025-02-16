# 📌 AI Blog System - Docker Setup (Windows & Linux)
This guide will help you **automatically download, setup, and run** the latest **AI Blog System Docker image** on **Windows (PowerShell) and Linux (Bash)**.

---

## 📌 Step 1: Download the Latest Release

### 🔹 Windows PowerShell
```powershell
$latestRelease = Invoke-RestMethod -Uri "https://api.github.com/repos/Yemeni/ai_blog_system/releases/latest"
$downloadUrl = $latestRelease.assets[0].browser_download_url
Invoke-WebRequest -Uri $downloadUrl -OutFile "ai-blog-app-docker.tar"
```

### 🔹 Linux (Bash)
```bash
LATEST_RELEASE=$(curl -s https://api.github.com/repos/Yemeni/ai_blog_system/releases/latest | grep "browser_download_url" | cut -d '"' -f 4)
curl -L -o ai-blog-app-docker.tar "$LATEST_RELEASE"
```

✅ **This will download the latest Docker image as `ai-blog-app-docker.tar`.**

---

## 📌 Step 2: Load the Docker Image
Now, **import the image into Docker**.

### 🔹 Windows PowerShell & Linux (Bash)
```powershell
docker load -i ai-blog-app-docker.tar
```
✅ **This makes the image available in Docker.**

---

## 📌 Step 3: Create the `.env` File
Now, **set up your AI API tokens** by creating an `.env` file.

### 🔹 Windows PowerShell
```powershell
@"
AI_OPENAI_API_TOKEN=your_openai_api_token_here
AI_DEEPSEEK_API_TOKEN=your_deepseek_api_token_here
"@ | Out-File -Encoding utf8 .env
```

### 🔹 Linux (Bash)
```bash
echo "AI_OPENAI_API_TOKEN=your_openai_api_token_here" > .env
echo "AI_DEEPSEEK_API_TOKEN=your_deepseek_api_token_here" >> .env
```

✅ **Now, your `.env` file is correctly formatted for both Windows and Linux.**

---

## 📌 Step 4: Run the Docker Container
Now, **start the container** with the `.env` file.

### 🔹 Windows PowerShell & Linux (Bash)
```powershell
docker run -d --name ai-blog-app --env-file .env -p 8000:8000 ai-blog-app-docker
```

✅ **Your AI Blog System is now running at:**  
👉 [http://localhost:8000](http://localhost:8000)

---

## 📌 Additional Commands
### 🔄 Restart the Container
```powershell
docker restart ai-blog-app
```
### 🛑 Stop the Container
```powershell
docker stop ai-blog-app
```
### 📜 View Logs
```powershell
docker logs -f ai-blog-app
```
### 🗑️ Remove the Container
```powershell
docker rm -f ai-blog-app
```

---

## 🎯 Done!
✅ **AI Blog System automatically fetches the latest build**  
✅ **Works perfectly in both Windows PowerShell and Linux**  
✅ **Loads the Docker image & runs it with `.env`**  
✅ **Easily start, stop, and restart the container**  

🚀 **Now your AI Blog System is fully automated on any OS!** 🎉  

---
### 🔹 Notes
- **Windows users:** Make sure PowerShell has execution permissions (XSet-ExecutionPolicy RemoteSigned -Scope CurrentUserX if needed).  
- **Ensure Docker is running** before executing the commands.  

