
WIDTH = 1024
HEIGHT = 600

TILESIZE = 64

FPS = 60

# User Interface
BAR_HEIGHT = 20
EXP_BAR_HEIGHT = 5
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
EXP_BAR_WIDTH = 200
ITEM_BOX_SIZE = 80
UI_FONT = "../images/font/joystix.ttf"
UI_FONT_SIZE = 18
BAR_FONT_SIZE =10

# Colors
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#eeeeee"

# UI colors
HEALTH_BAR_COLOR = 'red'
ENERGY_BAR_COLOR = "blue"
EXP_BAR_COLOR = "gold"
UI_BORDER_COLOR_ACTIVE = "gold"


WEAPONS_FOLDER = "../images/weapons"
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15,'graphic':'../images/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30,'graphic':'../images/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../images/weapons/axe/full.png'},
    'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'../images/weapons/rapier/full.png'},
    'sai':{'cooldown': 80, 'damage': 10, 'graphic':'../images/weapons/sai/full.png'}
}

# magic
magic_data = {
    "flame": {"strength": 5, "cost": 20, "graphic": "../images/particles/flame/fire.png"},
    "heal" : {"strength": 20, "cost": 10, "graphic": "../images/particles/heal/heal.png"},
}

# monster
monster_data = {
    'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}
}