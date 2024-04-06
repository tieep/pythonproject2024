WIN_WIDTH = 640
WIN_HEIGHT = 480
#just a comment
CAMERA_SIZE = 16
TILE_SIZE = 32
BOSS_SIZE=64


PLAYER_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1
ENERMY_LAYER = 4
BULLET_LAYER = 5
GUN_LAYER = 6
MAP_LAYER = 0
UI_LAYER = 10

PLAYER_SPEED = 5
ENEMY_SPEED = 2
GLOCK_BULLET_SPEED = 10
AK47_BULLET_SPEED = 12
SNIPER_BULLET_SPEED = 20

#chinh lai khoang thoi gian giua cac lan ban
ENEMY_SCOPE = 360
PLAYER_GLOCK_DELAY = 240
GLOCK_SCOPE = 160
WEAPON_SIZE = 42
PLAYER_AK47_DELAY = 100
AK47_SCOPE = 200
PLAYER_SNIPER_DELAY = 700
SNIPER_SCOPE = 300

PLAYER_GLOCK_DMG = 1
PLAYER_AK47_DMG = 2
PLAYER_SNIPER_DMG = 3

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
BROWN = (255,160, 85)
DARK_BROWN = (101,67,33)

FPS = 60

ENEMY_WEAPON_RATIO = {"glock": 0.5, "ak47": 0.3, "sniper": 0.2}
hpipemap = [
    '',
    '',
    '',
    '',
    'BBBBBBBBBBBBBBBBBBBB',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    'BBBBBBBBBBBBBBBBBBBB',
    '',
    '',
    '',
    ''
]

vpipemap = [
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B'
]

tilemaps = [
    [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B.........P........B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'BBBBBBBBBBBBBBBBBBBB'
    ], 
    [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B.........5........B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'BBBBBBBBBBBBBBBBBBBB'
    ],
    [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..................B',
        'B....BBB......E....B',
        'B.....B............B',
        'B.....B........E...B',
        'B........B.........B',
        'B........BBB.......B',
        'B........BB........B',
        'B...E....B.B.......B',
        'B..................B',
        'B............B..B..B',
        'B......E.....B..B..B',
        'B............BBBB..B',
        'B..................B',
        'BBBBBBBBBBBBBBBBBBBB'
    ],
    [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..................B',
        'B.....B......B.....B',
        'B.....B......BE....B',
        'B...BBB......BBB...B',
        'B..................B',
        'B..................B',
        'B........EE........B',
        'B..................B',
        'B..................B',
        'B...BBB......BBB...B',
        'B.....B......B.....B',
        'B.....B......B.....B',
        'B.............E.E..B',
        'BBBBBBBBBBBBBBBBBBBB'
    ],
    [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..................B',
        'B........E.........B',
        'B.....B......B.....B',
        'B......B....B......B',
        'B...E...B..B..E....B',
        'B........BB........B',
        'B........BB........B',
        'B...E...B..B..E....B',
        'B......B....B......B',
        'B.....B......B.....B',
        'B........E.........B',
        'B..................B',
        'B..................B',
        'BBBBBBBBBBBBBBBBBBBB'
    ],
    [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..................B',
        'B...BBB............B',
        'B...B B......E.....B',
        'B...BBB............B',
        'B.............E....B',
        'B......B..B........B',
        'B......BB.B...E....B',
        'B......B.BB........B',
        'B......B..B...E....B',
        'B............BBBB..B',
        'B.......E....B.....B',
        'B............B..B..B',
        'B............BBBB..B',
        'BBBBBBBBBBBBBBBBBBBB'
    ]
]