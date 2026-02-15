# 🎮 CS2 Faceit Checker

Desktop application for checking Faceit statistics by SteamID or profile link.

Built with Python and Tkinter.

---

## 🚀 Features

- 🔍 Check Faceit account by:
  - SteamID64
  - Steam profile link
  - Vanity URL
- 📊 Displays:
  - Nickname
  - Level
  - ELO
  - K/D
  - Headshot %
  - Matches
- 📈 Sort players by level
- 📋 Clipboard history
- 📊 Progress bar
- 🔐 Secure API key handling (.env)

---

## 🏗 Architecture

The project follows a layered architecture:

```
UI → Core → Services
```

### Structure

```
faceit_checker/
│
├── main.py              # Entry point
├── config.py            # Configuration
│
├── ui/                  # Tkinter UI
│   └── app.py
│
├── core/                # Business logic
│   └── checker.py
│
├── services/            # External services
│   ├── steam_service.py
│   └── faceit_service.py
```

---

## ⚙ Installation

1. Clone repository:

```bash
git clone https://github.com/NeyKoMe/faceit-checker.git
cd faceit-checker
```

2. Create virtual environment (recommended):

```bash
python -m venv venv
```

3. Activate environment:

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create `.env` file:

```
STEAM_API_KEY=your_steam_api_key_here
```

6. Run the application:

```bash
python main.py
```

---

## 🔐 Environment Variables

| Variable | Description |
|----------|-------------|
| STEAM_API_KEY | Steam Web API key |

---

## 🛠 Technologies Used

- Python 3
- Tkinter
- Requests
- BeautifulSoup4
- python-dotenv

---

## 📌 Future Improvements

- Better error handling
- Async requests
- Player model class
- Web version
- Discord bot integration

---

## 📄 License

This project is for educational purposes.