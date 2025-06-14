from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLineEdit, QLabel, QFileDialog, 
                            QTableWidget, QTableWidgetItem, QTabWidget, 
                            QComboBox, QSpinBox)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
from data_manager import DataManager
from player_card import PlayerCard
import os
import uuid

class AuctioneerWindow(QMainWindow):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.setWindowTitle("IPL Auction - Auctioneer")
        self.setMinimumSize(800, 600)
        self.current_player_index = 0
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Auction Tab
        self.auction_tab = QWidget()
        self.auction_layout = QVBoxLayout(self.auction_tab)
        
        # Player card
        self.player_card = PlayerCard(self.data_manager)
        self.auction_layout.addWidget(self.player_card)
        
        # Team bid buttons
        self.team_layout = QHBoxLayout()
        self.team_buttons = []
        self.update_team_buttons()
        self.auction_layout.addLayout(self.team_layout)
        
        # Controls
        self.controls_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous Player")
        self.prev_button.clicked.connect(self.prev_player)
        self.next_button = QPushButton("Next Player")
        self.next_button.clicked.connect(self.next_player)
        self.undo_button = QPushButton("Undo Bid")
        self.undo_button.clicked.connect(self.undo_bid)
        self.sold_button = QPushButton("Sold!")
        self.sold_button.clicked.connect(self.sell_player)
        self.unsold_button = QPushButton("Unsold")
        self.unsold_button.clicked.connect(self.mark_unsold)
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_ui)
        
        self.controls_layout.addWidget(self.prev_button)
        self.controls_layout.addWidget(self.next_button)
        self.controls_layout.addWidget(self.undo_button)
        self.controls_layout.addWidget(self.sold_button)
        self.controls_layout.addWidget(self.unsold_button)
        self.controls_layout.addWidget(self.refresh_button)
        self.auction_layout.addLayout(self.controls_layout)
        
        # Management Tab
        self.management_tab = QWidget()
        self.management_layout = QVBoxLayout(self.management_tab)
        
        # Player input
        self.player_input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Player Name")
        self.image_input = QLineEdit()
        self.image_input.setPlaceholderText("Player Image Path")
        self.image_browse = QPushButton("Browse")
        self.image_browse.clicked.connect(self.browse_image)
        self.starting_bid_input = QSpinBox()
        self.starting_bid_input.setRange(0, 1000000000)
        self.starting_bid_input.setSingleStep(1000000)
        self.min_bid_input = QSpinBox()
        self.min_bid_input.setRange(0, 100000000)
        self.min_bid_input.setSingleStep(1000000)
        self.add_player_button = QPushButton("Add Player")
        self.add_player_button.clicked.connect(self.add_player)
        
        self.player_input_layout.addWidget(QLabel("Name:"))
        self.player_input_layout.addWidget(self.name_input)
        self.player_input_layout.addWidget(QLabel("Image:"))
        self.player_input_layout.addWidget(self.image_input)
        self.player_input_layout.addWidget(self.image_browse)
        self.player_input_layout.addWidget(QLabel("Starting Bid:"))
        self.player_input_layout.addWidget(self.starting_bid_input)
        self.player_input_layout.addWidget(QLabel("Min Bid:"))
        self.player_input_layout.addWidget(self.min_bid_input)
        self.player_input_layout.addWidget(self.add_player_button)
        self.management_layout.addLayout(self.player_input_layout)
        
        # Image preview
        self.preview_image = QLabel("No Image Selected")
        self.preview_image.setFixedSize(100, 100)
        self.preview_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.management_layout.addWidget(self.preview_image)
        
        # Player list
        self.player_table = QTableWidget()
        self.player_table.setColumnCount(7)
        self.player_table.setHorizontalHeaderLabels(["Name", "Starting Bid", "Min Bid", "Status", "Action", "Up", "Down"])
        self.player_table.horizontalHeader().setStretchLastSection(True)
        self.management_layout.addWidget(self.player_table)
        
        # Team management
        self.team_input_layout = QHBoxLayout()
        self.team_name_input = QLineEdit()
        self.team_name_input.setPlaceholderText("Team Name")
        self.team_logo_input = QLineEdit()
        self.team_logo_input.setPlaceholderText("Team Logo Path")
        self.team_logo_browse = QPushButton("Browse")
        self.team_logo_browse.clicked.connect(self.browse_team_logo)
        self.add_team_button = QPushButton("Add Team")
        self.add_team_button.clicked.connect(self.add_team)
        
        self.team_input_layout.addWidget(QLabel("Team Name:"))
        self.team_input_layout.addWidget(self.team_name_input)
        self.team_input_layout.addWidget(QLabel("Logo:"))
        self.team_input_layout.addWidget(self.team_logo_input)
        self.team_input_layout.addWidget(self.team_logo_browse)
        self.team_input_layout.addWidget(self.add_team_button)
        self.management_layout.addLayout(self.team_input_layout)
        
        # Team list
        self.team_table = QTableWidget()
        self.team_table.setColumnCount(3)
        self.team_table.setHorizontalHeaderLabels(["Name", "Logo", "Action"])
        self.team_table.horizontalHeader().setStretchLastSection(True)
        self.management_layout.addWidget(self.team_table)
        
        self.tabs.addTab(self.auction_tab, "Auction")
        self.tabs.addTab(self.management_tab, "Management")
        
        self.bid_history = []
        self.update_player_display()
        self.update_player_table()
        self.update_team_table()
    
    def update_team_buttons(self):
        for button in self.team_buttons:
            button.deleteLater()
        self.team_buttons.clear()
        
        teams = self.data_manager.get_teams()
        for team in teams:
            button = QPushButton()
            button.setObjectName("teamButton")
            button.setText(team["name"])
            if team["logo"]:
                button.setIcon(QIcon(team["logo"]))
                button.setIconSize(QSize(50, 50))
            button.clicked.connect(lambda checked, t=team["name"]: self.place_bid(t))
            self.team_buttons.append(button)
            self.team_layout.addWidget(button)
    
    def place_bid(self, team):
        if self.current_player_index < len(self.data_manager.get_all_players()):
            player = self.data_manager.get_all_players()[self.current_player_index]
            current_bid = player.get("current_bid", 0)
            min_bid = player.get("min_bid", 1000000)
            new_bid = current_bid + min_bid if current_bid > 0 else player["starting_bid"]
            
            self.bid_history.append((current_bid, player.get("latest_bidder", "Latest Bidder: None")))
            self.data_manager.update_bid(player["name"], new_bid, team)
            self.update_player_display()
    
    def undo_bid(self):
        if self.bid_history:
            last_bid, last_team = self.bid_history.pop()
            player = self.data_manager.get_all_players()[self.current_player_index]
            self.data_manager.update_bid(player["name"], last_bid, last_team.replace("Latest Bidder: ", ""))
            self.update_player_display()
    
    def sell_player(self):
        if self.current_player_index < len(self.data_manager.get_all_players()):
            player = self.data_manager.get_all_players()[self.current_player_index]
            team = self.player_card.latest_bidder.text().replace("Latest Bidder: ", "")
            if team != "None":
                self.data_manager.set_player_status(player["name"], "Sold", team)
                self.update_player_table()
                self.update_player_display()
    
    def mark_unsold(self):
        if self.current_player_index < len(self.data_manager.get_all_players()):
            player = self.data_manager.get_all_players()[self.current_player_index]
            self.data_manager.set_player_status(player["name"], "Unsold", None)
            self.update_player_table()
            self.update_player_display()
    
    def next_player(self):
        self.current_player_index += 1
        self.bid_history.clear()
        self.update_player_display()
    
    def prev_player(self):
        if self.current_player_index > 0:
            self.current_player_index -= 1
            self.bid_history.clear()
            self.update_player_display()
    
    def update_player_display(self):
        players = self.data_manager.get_all_players()
        if players and self.current_player_index < len(players):
            player = players[self.current_player_index]
            self.player_card.update_player(player)
            self.data_manager.notify_player_update(player)
        else:
            self.current_player_index = max(0, len(players) - 1)
            if players:
                player = players[self.current_player_index]
                self.player_card.update_player(player)
                self.data_manager.notify_player_update(player)
            else:
                self.player_card.clear()
    
    def browse_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Player Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.image_input.setText(file_name)
            pixmap = QPixmap(file_name).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.preview_image.setPixmap(pixmap)
    
    def browse_team_logo(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Team Logo", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.team_logo_input.setText(file_name)
    
    def add_player(self):
        name = self.name_input.text().strip()
        image = self.image_input.text().strip()
        starting_bid = self.starting_bid_input.value()
        min_bid = self.min_bid_input.value()
        
        if name and starting_bid > 0:
            self.data_manager.add_player({
                "id": str(uuid.uuid4()),
                "name": name,
                "image": image,
                "starting_bid": starting_bid,
                "min_bid": min_bid,
                "status": "Available",
                "sold_to": None,
                "current_bid": 0,
                "latest_bidder": None
            })
            self.update_player_table()
            self.name_input.clear()
            self.image_input.clear()
            self.starting_bid_input.setValue(0)
            self.min_bid_input.setValue(0)
            self.preview_image.setText("No Image Selected")
    
    def add_team(self):
        name = self.team_name_input.text().strip()
        logo = self.team_logo_input.text().strip()
        
        if name:
            self.data_manager.add_team({
                "id": str(uuid.uuid4()),
                "name": name,
                "logo": logo
            })
            self.update_team_table()
            self.update_team_buttons()
            self.team_name_input.clear()
            self.team_logo_input.clear()
    
    def update_player_table(self):
        players = self.data_manager.get_all_players()
        self.player_table.setRowCount(len(players))
        for i, player in enumerate(players):
            self.player_table.setItem(i, 0, QTableWidgetItem(player["name"]))
            self.player_table.setItem(i, 1, QTableWidgetItem(str(player["starting_bid"])))
            self.player_table.setItem(i, 2, QTableWidgetItem(str(player.get("min_bid", 1000000))))
            status = player["status"]
            if status == "Sold":
                status = f"Sold to {player['sold_to']}"
            self.player_table.setItem(i, 3, QTableWidgetItem(status))
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda checked, p=player["id"]: self.delete_player(p))
            self.player_table.setCellWidget(i, 4, delete_button)
            up_button = QPushButton("Up")
            up_button.clicked.connect(lambda checked, idx=i: self.move_player_up(idx))
            self.player_table.setCellWidget(i, 5, up_button)
            down_button = QPushButton("Down")
            down_button.clicked.connect(lambda checked, idx=i: self.move_player_down(idx))
            self.player_table.setCellWidget(i, 6, down_button)
    
    def move_player_up(self, index):
        if index > 0:
            self.data_manager.reorder_players(index, index - 1)
            self.update_player_table()
            self.refresh_ui()
    
    def move_player_down(self, index):
        if index < len(self.data_manager.get_all_players()) - 1:
            self.data_manager.reorder_players(index, index + 1)
            self.update_player_table()
            self.refresh_ui()
    
    def update_team_table(self):
        teams = self.data_manager.get_teams()
        self.team_table.setRowCount(len(teams))
        for i, team in enumerate(teams):
            self.team_table.setItem(i, 0, QTableWidgetItem(team["name"]))
            self.team_table.setItem(i, 1, QTableWidgetItem(team["logo"]))
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda checked, t=team["id"]: self.delete_team(t))
            self.team_table.setCellWidget(i, 2, delete_button)
    
    def delete_player(self, player_id):
        self.data_manager.delete_player(player_id)
        self.update_player_table()
        self.refresh_ui()
    
    def delete_team(self, team_id):
        self.data_manager.delete_team(team_id)
        self.update_team_table()
        self.update_team_buttons()
    
    def refresh_ui(self):
        self.update_player_display()
        self.update_player_table()
        self.update_team_buttons()
        # Force update of Bidder Window
        players = self.data_manager.get_all_players()
        if players and self.current_player_index < len(players):
            self.data_manager.notify_player_update(players[self.current_player_index])