from typing import list
from typing import dict
from typing import Union
from typing import Optional

class protfolio():

    def _init_(self, account_number: Optional[str]):

        self.position ={}
        self.position_count =0
        self.market_value= 0.0
        self.porfit_loss = 0.0
        self.risk_tolerance = 0.0
        self.account_number = account_number

def add_position(self,symbol: str, asset_type: str, purchase_date: Optional[str],quantity: int = 0, purchase_price: float = 0.0) -> dict:

    self.positions[symbol] = {}
    self.positions[symbol] ['symbol'] = symbol
    self.positions[symbol] ['quantity'] = quantity
    self.positions[symbol] ['purchase_price'] = purchase_price
    self.positions[symbol] ['purchase_date'] = purchase_date
    self.positions[symbol] ['asset_type'] = asset_type

    return self.positions 

def add_positions(self, positions: list[dict]) -> dict:

    if isinstance(positions,list):
        for positions in positions:
            
            self.add_positions(
                symbol=positions['symbol'],
                asset_type=positions['asset_type'],
                purchase_date=positions.get('purchase_date',None),
                purchase_price=positions.get('purchase_price', 0.0),
                quantity=positions.get('quantity', 0) 
                )
            
            return self.positions
        
    else:
        raise TypeError("positions must be a list of dictionaries.")
    
    def remove_position(self, symbol: str) -> tuple[bool, str]:

        if symbol in self.positions:
            del self.positions[symbol]
            return(True, "{symbol} was successfully removed.".format(symbol=symbol))
        else:
            return(False,"{symbol} did not exist in the portfolio.".format(symbol=symbol))
      
    def in_potfolio(self, symbol: str) ->bool:
            
            if symbol in self.positions:
                 
                 return True
            else:
                return False
            
    def is_proftibale(self, symbol: str, current_price:float) -> bool:

            #grab the purchase price
            purchase_price = self.positions[symbol]['purchase_price']

            if (purchase_price<= current_price):
                 return True
            elif ( purchase_price> current_price):
                 return False

    def total_allocation(self):
        pass

    def risk_exposure(self):
        pass

    def total_market_value(self):
         pass