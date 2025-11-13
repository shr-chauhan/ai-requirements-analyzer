# Deployment Guide

This guide covers multiple deployment options for the AI Requirements Analyzer Streamlit app.

## Option 1: Streamlit Cloud (Recommended - Easiest)

Streamlit Cloud is the easiest and most straightforward way to deploy Streamlit apps. It's free for public repos.

### Prerequisites
- A GitHub account
- Your code pushed to a GitHub repository

### Steps:

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/ai-requirements-analyzer.git
   git push -u origin main
   ```

2. **Sign up for Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Sign in with your GitHub account

3. **Deploy your app**
   - Click "New app"
   - Select your repository
   - Choose the branch (usually `main`)
   - Set the main file path: `app.py`
   - Click "Deploy"

4. **Configure Secrets**
   - In Streamlit Cloud dashboard, go to your app settings
   - Click "Secrets" or "Advanced settings"
   - Add your secrets in TOML format:
   ```toml
   OPENAI_API_KEY = "sk-proj-your-actual-key-here"
   APP_PASSWORD = "your-secure-password-here"
   ```

5. **Your app will be live!**
   - Streamlit Cloud will provide a URL like: `https://your-app-name.streamlit.app`

### Important Notes for Streamlit Cloud:
- ✅ Free for public repositories
- ✅ Automatic deployments on git push
- ✅ Built-in secrets management
- ⚠️ Free tier has resource limits
- ⚠️ App sleeps after inactivity (wakes up on next visit)

---

## Option 2: Heroku

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed

### Steps:

1. **Create necessary files**

   Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

   Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

   Update `Procfile`:
   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. **Create Heroku app**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set OPENAI_API_KEY="sk-proj-your-actual-key-here"
   heroku config:set APP_PASSWORD="your-secure-password-here"
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Open your app**
   ```bash
   heroku open
   ```

---

## Option 3: AWS EC2 / DigitalOcean / Linode

### Steps:

1. **Launch a server** (Ubuntu recommended)
   - Minimum: 1GB RAM, 1 CPU
   - Recommended: 2GB RAM, 2 CPU

2. **SSH into your server**
   ```bash
   ssh user@your-server-ip
   ```

3. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git -y
   ```

4. **Clone your repository**
   ```bash
   git clone https://github.com/yourusername/ai-requirements-analyzer.git
   cd ai-requirements-analyzer
   ```

5. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Set environment variables**
   ```bash
   export OPENAI_API_KEY="sk-proj-your-actual-key-here"
   export APP_PASSWORD="your-secure-password-here"
   ```

7. **Run Streamlit**
   ```bash
   streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   ```

8. **Set up as a service (optional - for auto-restart)**
   
   Create `/etc/systemd/system/streamlit-app.service`:
   ```ini
   [Unit]
   Description=Streamlit App
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/path/to/ai-requirements-analyzer
   Environment="OPENAI_API_KEY=sk-proj-your-actual-key-here"
   Environment="APP_PASSWORD=your-secure-password-here"
   ExecStart=/path/to/ai-requirements-analyzer/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable streamlit-app
   sudo systemctl start streamlit-app
   ```

9. **Configure firewall**
   ```bash
   sudo ufw allow 8501
   ```

10. **Access your app**
    - Visit: `http://your-server-ip:8501`

---

## Option 4: Docker Deployment

### Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and run:
```bash
docker build -t ai-requirements-analyzer .
docker run -p 8501:8501 -e OPENAI_API_KEY="your-key" -e APP_PASSWORD="your-password" ai-requirements-analyzer
```

### Deploy to cloud with Docker:
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**
- **DigitalOcean App Platform**

---

## Option 5: Railway

Railway is a modern platform that makes deployment easy.

### Steps:

1. **Sign up** at https://railway.app
2. **Create new project** from GitHub repo
3. **Add environment variables**:
   - `OPENAI_API_KEY`
   - `APP_PASSWORD`
4. **Set start command**: `streamlit run app.py --server.port=$PORT`
5. **Deploy** - Railway auto-detects and deploys

---

## Security Best Practices

1. **Never commit secrets** - Always use environment variables or secrets management
2. **Use strong passwords** - Change default `APP_PASSWORD`
3. **Enable HTTPS** - Use reverse proxy (nginx) or platform's built-in SSL
4. **Monitor usage** - Track OpenAI API costs
5. **Set rate limits** - Consider adding rate limiting for production

---

## Troubleshooting

### App won't start
- Check logs for errors
- Verify all environment variables are set
- Ensure all dependencies are installed

### Can't access app
- Check firewall settings
- Verify port is correct
- Check server is running

### API errors
- Verify OpenAI API key is correct
- Check billing is set up on OpenAI account
- Monitor API usage limits

---

## Cost Considerations

- **Streamlit Cloud**: Free for public repos
- **Heroku**: Free tier available (with limitations)
- **AWS/DigitalOcean**: Pay-as-you-go (~$5-20/month for small apps)
- **OpenAI API**: Pay per use (~$0.001-0.01 per analysis)

---

## Recommended for Beginners

**Streamlit Cloud** is the easiest option:
- ✅ No server management
- ✅ Free for public repos
- ✅ Automatic deployments
- ✅ Built-in secrets management
- ✅ HTTPS included

