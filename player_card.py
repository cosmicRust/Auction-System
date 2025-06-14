from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class PlayerCard(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        
        # Layout
        self.layout = QVBoxLayout(self)
        
        # Player display
        self.player_image = QLabel()
        self.player_image.setFixedSize(200, 200)
        self.player_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.player_name = QLabel("No Player Selected")
        self.player_name.setObjectName("playerName")
        self.starting_bid = QLabel("Starting Bid: 0")
        self.current_bid = QLabel("Current Bid: 0")
        self.latest_bidder = QLabel("Latest Bidder: None")
        self.bidder_logo = QLabel()
        self.bidder_logo.setFixedSize(100, 100)
        self.bidder_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sold_to = QLabel("SOLD TO: None")
        self.sold_to.setObjectName("soldMessage")
        
        self.layout.addWidget(self.player_image)
        self.layout.addWidget(self.player_name)
        self.layout.addWidget(self.starting_bid)
        self.layout.addWidget(self.current_bid)
        self.layout.addWidget(self.latest_bidder)
        self.layout.addWidget(self.bidder_logo)
        self.layout.addWidget(self.sold_to)
        
        self.clear()
    
    def update_player(self, player):
        self.player_name.setText(player["name"])
        self.starting_bid.setText(f"Starting Bid: {player['starting_bid']}")
        self.current_bid.setText(f"Current Bid: {player.get('current_bid', 0)}")
        self.latest_bidder.setText(f"Latest Bidder: {player.get('latest_bidder', 'None')}")
        if player["image"]:
            pixmap = QPixmap(player["image"]).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.player_image.setPixmap(pixmap)
        else:
            self.player_image.setText("No Image")
        team = player.get("latest_bidder", None)
        team_data = next((t for t in self.data_manager.get_teams() if t["name"] == team), None) if team else None
        if team_data and team_data["logo"]:
            pixmap = QPixmap(team_data["logo"]).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.bidder_logo.setPixmap(pixmap)
        else:
            self.bidder_logo.setText("No Bidder")
        if player["status"] == "Sold":
            self.sold_to.setText(f"SOLD TO: {player['sold_to']}")
        elif player["status"] == "Unsold":
            self.sold_to.setText("SOLD TO: Unsold")
        else:
            self.sold_to.setText("SOLD TO: None")
    
    def update_bid(self, player_name, current_bid, team):
        self.current_bid.setText(f"Current Bid: {current_bid}")
        self.latest_bidder.setText(f"Latest Bidder: {team}")
        team_data = next((t for t in self.data_manager.get_teams() if t["name"] == team), None)
        if team_data and team_data["logo"]:
            pixmap = QPixmap(team_data["logo"]).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.bidder_logo.setPixmap(pixmap)
        else:
            self.bidder_logo.setText("No Bidder")
    
    def update_status(self, player_name, status, team):
        if status == "Sold":
            self.sold_to.setText(f"SOLD TO: {team}")
        elif status == "Unsold":
            self.sold_to.setText("SOLD TO: Unsold")
        else:
            self.sold_to.setText("SOLD TO: None")
    
    def clear(self):
        self.player_name.setText("No Players Available")
        self.starting_bid.setText("Starting Bid: 0")
        self.current_bid.setText("Current Bid: 0")
        self.latest_bidder.setText("Latest Bidder: None")
        self.bidder_logo.setText("No Bidder")
        self.sold_to.setText("SOLD TO: None")
        self.player_image.setText("No Image")