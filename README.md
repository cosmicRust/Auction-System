
# 🏏 IPL Auction Management System (PyQt6)

A modern, desktop-based IPL-style auction application built with **Python + PyQt6**.  
Designed for managing player auctions with real-time controls, custom teams, player management, and dual views for auctioneer and bidders.

---

## 🚀 Features

- 🧑‍💻 **Custom Players**  
  Add, edit, or remove players with base price, minimum bid increment, and player images.

- 🏁 **Live Auctioneer Panel**  
  Control bids, see current bidder and amount, and navigate players (Next, Previous, Undo, Sold).

- 🖼 **Image Support**  
  Upload and preview player images which are displayed during bidding.

- 👥 **Custom Teams with Logos**  
  Display team buttons (e.g., MI, RCB, CSK) with logos; click to register bids.

- 🪟 **Separated Views** *(Planned)*  
  Architecture supports clean separation of Auctioneer control view and Bidders display view.

- 💾 **Persistent Data**  
  Players and their statuses (sold, unsold) are saved using JSON.

- 🎨 **Modern UI**  
  Built with PyQt6 and styled using QSS for sleek, rounded buttons, responsive layout, and enhanced readability.

---

## 🛠 Technologies Used

- **Python 3.8+**
- **PyQt6** (for GUI)
- **QSS** (Qt Style Sheets for styling)
- **JSON** (for data storage)

---

## 📁 Project Structure

```

├── main.py
├── auctioneer\_panel.py
├── player\_manager.py
├── utils/
│   └── controller.py
├── data/
│   └── players.json
├── assets/
│   └── team\_logos/
│       └── mi.png, rcb.png, ...
├── style.qss

````

---

## 💻 Installation & Setup

### 1. 📦 Create Python Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate       # On Linux/macOS
venv\Scripts\activate          # On Windows
````

### 2. 📥 Install Requirements

```bash
pip install -r requirements.txt
```

### 3. 🚀 Run the App

```bash
python main.py
```

---

## 🛠 Planned Enhancements

* Separate display-only bidder view
* CSV export of final auction results
* Budget tracking per team
* Countdown timer per player

---

## 📄 License

MIT License — free to use and modify.

---


