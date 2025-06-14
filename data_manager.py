import json
import os
from PyQt6.QtCore import QObject, pyqtSignal

class DataManager(QObject):
    player_updated = pyqtSignal(dict)
    bid_updated = pyqtSignal(str, int, str)
    player_status_updated = pyqtSignal(str, str, str)
    
    def __init__(self):
        super().__init__()
        self.players_file = "Auction_System/players.json"
        self.teams_file = "Auction_System/teams.json"
        self.players = []
        self.teams = []
        self.load_data()
    
    def load_data(self):
        os.makedirs("Auction_System", exist_ok=True)
        
        if os.path.exists(self.players_file):
            with open(self.players_file, 'r', encoding='utf-8') as f:
                self.players = json.load(f)
        
        if os.path.exists(self.teams_file):
            with open(self.teams_file, 'r', encoding='utf-8') as f:
                self.teams = json.load(f)
    
    def save_data(self):
        with open(self.players_file, 'w', encoding='utf-8') as f:
            json.dump(self.players, f, indent=2)
        
        with open(self.teams_file, 'w', encoding='utf-8') as f:
            json.dump(self.teams, f, indent=2)
    
    def add_player(self, player):
        self.players.append(player)
        self.save_data()
    
    def delete_player(self, player_id):
        self.players = [p for p in self.players if p["id"] != player_id]
        self.save_data()
    
    def add_team(self, team):
        self.teams.append(team)
        self.save_data()
    
    def delete_team(self, team_id):
        self.teams = [t for t in self.teams if t["id"] != team_id]
        self.save_data()
    
    def get_all_players(self):
        return self.players
    
    def get_teams(self):
        return self.teams
    
    def set_player_status(self, player_name, status, team):
        for player in self.players:
            if player["name"] == player_name:
                player["status"] = status
                player["sold_to"] = team
                break
        self.save_data()
        self.player_status_updated.emit(player_name, status, team if team else "None")
    
    def update_bid(self, player_name, current_bid, team):
        for player in self.players:
            if player["name"] == player_name:
                player["current_bid"] = current_bid
                player["latest_bidder"] = team
                break
        self.save_data()
        self.bid_updated.emit(player_name, current_bid, team)
    
    def reorder_players(self, old_index, new_index):
        player = self.players.pop(old_index)
        self.players.insert(new_index, player)
        self.save_data()
    
    def notify_player_update(self, player):
        self.player_updated.emit(player)