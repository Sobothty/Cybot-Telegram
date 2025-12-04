# 🔧 Render.com Deployment Fix (Free Web Service)

## ❌ Problem

You're seeing this error:

```
bash: line 1: start.sh: command not found
==> Exited with status 127
```

## ✅ Solution - Just Fix the Start Command!

Since you're using the **FREE Web Service** (workers cost money), you just need to fix one setting:

**In Render Dashboard:**

1. Go to your service settings
2. Find **"Start Command"** field
3. Change it from: `start.sh`
4. To: `python bot.py`
5. Click "Save Changes"
6. Click "Manual Deploy"

## 🚀 Quick Fix Steps

1. **Go to Render Dashboard** → https://dashboard.render.com
2. **Click on your service** (telegram-broadcast-bot)
3. **Go to "Settings"** tab
4. **Scroll to "Build & Deploy"** section
5. **Find "Start Command"** field
6. **Change to**: `python bot.py`
7. **Click "Save Changes"**
8. **Go to "Manual Deploy"** and click "Deploy latest commit"

## 📝 Correct Configuration for Free Web Service

### Service Type

- **Web Service** (FREE - keep this!)

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
python bot.py
```

### Environment Variables

```
BOT_TOKEN=8498872701:AAEF90m6PrcpovVWWpfnNNOBiccxIhryBOM
```

## ✅ Expected Success Output

After fixing, you should see:

```
==> Build successful 🎉
==> Deploying...
==> Starting service...
INFO - Bot started successfully!
INFO - Application started
==> Service is live 🎉
```

## 💡 Why This Happened

- The start command was incorrectly set to `start.sh`
- `start.sh` is only for local development
- Render.com needs the direct Python command: `python bot.py`

## ⚠️ Important Note About Free Web Service

Render's free web service will:

- ✅ Work perfectly for Telegram bots
- ⚠️ Sleep after 15 minutes of inactivity
- ✅ Wake up automatically when bot receives a message
- ✅ Run 750 hours/month for free

**This is normal and fine!** Your bot will wake up instantly when users interact with it.

## 📚 Reference

See **DEPLOYMENT.md** for complete deployment guide.

---

**After changing the start command to `python bot.py`, your bot will work!** 🎉
