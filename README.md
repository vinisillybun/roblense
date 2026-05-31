# roblense

> ⚠️ **Disclaimer:** This project was built with the help of AI. If you don't like that, don't use it.

---

A Flask backend that bridges **Roblox** and **Lovense** toys. Players link their Lovense device by scanning a QR code, and once connected, in-game events can send haptic commands (vibrate, rotate, thrust, etc.) to their toy in real time.

## How It Works

1. A user hits `/link?uid=<uid>` to get a QR code
2. They scan it with the Lovense app to connect their toy
3. Lovense calls back to `/callback` with the session info
4. Roblox sends commands to `/command` to control the toy

## Stack

- **Flask** — web server
- **Requests** — Lovense API calls
- **Gunicorn** — production server
