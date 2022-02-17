
from enum import Enum

class Monsters(Enum):
    
    bamboo = "390"
    spirit = "391"
    raccoon = "392"
    squid = "393"
    
    
    
    
    
if __name__ == "__main__":
    
    print(Monsters.bamboo.value)
    
    print(Monsters(390).name)