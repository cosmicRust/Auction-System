import sys
from PyQt6.QtWidgets import QApplication
from auctioneer_ui import AuctioneerWindow
from bidder_ui import BidderWindow
from data_manager import DataManager

def main():
    app = QApplication(sys.argv)
    
    # Load stylesheet
    with open("Auction_System/styles.qss", "r") as f:
        app.setStyleSheet(f.read())
    
    # Initialize data manager
    data_manager = DataManager()
    
    # Create windows
    auctioneer = AuctioneerWindow(data_manager)
    bidder = BidderWindow(data_manager)
    
    # Show windows
    auctioneer.show()
    bidder.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()