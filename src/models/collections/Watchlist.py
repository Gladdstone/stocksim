# Unowned assets being monitored by the user
class Watchlist(AssetMap):
    def __init__(self, asset: Asset):
        self.dictId = 1
        self.asset = {0: asset}