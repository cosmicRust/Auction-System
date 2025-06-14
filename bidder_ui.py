from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from data_manager import DataManager
from player_card import PlayerCard

class BidderWindow(QMainWindow):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.setWindowTitle("IPL Auction - Bidder View")
        self.setMinimumSize(600, 400)
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Player card
        self.player_card = PlayerCard(self.data_manager)
        self.main_layout.addWidget(self.player_card)
        
        self.data_manager.player_updated.connect(self.player_card.update_player)
        self.data_manager.bid_updated.connect(self.player_card.update_bid)
        self.data_manager.player_status_updated.connect(self.player_card.update_status)
        
        # Initialize with current player
        players = self.data_manager.get_all_players()
        if players:
            self.player_card.update_player(players[0])