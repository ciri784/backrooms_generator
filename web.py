#!/usr/bin/env python3
"""
Backrooms Web - Flask web interface for the Backrooms Generator
"""

from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# ============================================================
# ROOM GENERATION DATA
# ============================================================

ROOMS = [
    ("a large {room_size} lobby", "The ceiling is impossibly high. Yellow wallpaper peels in long strips."),
    ("a {room_size} office space", "Desks are arranged in perfect rows. None of the chairs face the same direction."),
    ("a long, narrow hallway", "The walls are covered in {wall_cover}. Doors line both sides. None of them have handles."),
    ("an abandoned warehouse", "Shipping containers sit in no particular order. The floor is wet. The light is yellow."),
    ("a {room_size} school corridor", "Classroom doors are closed. Behind one of them, you hear something."),
    ("a {room_size} hotel lobby", "The front desk is unmanned. Always. A radio somewhere is playing nothing."),
    ("an underground parking structure", "Cars that don't move. The lights flicker. The exit is never where you left it."),
    ("a {room_size} hospital waiting room", "Magazines from years ago. Water stains on the ceiling. The waiting never ends."),
]

ROOM_SIZES = ["small", "medium-sized", "large", "vast", "seemingly infinite"]

WALL_COVERINGS = [
    "yellow wallpaper, peeling at the edges",
    "water-stained ceiling tiles",
    "mysterious brown stains",
    "tiles that shouldn't be there",
    "windows that look out on nothing",
]

CEILING_ISSUES = [
    "The ceiling is too high.",
    "The ceiling is too low.",
    "There is no ceiling. You don't want to look up.",
    "The ceiling tiles are arranged wrong.",
]

LIGHT_ISSUES = [
    "Somewhere, a fluorescent light is buzzing.",
    "A light flickers in the corner of your vision.",
    "The lights are too bright. Or too dim. You can't tell anymore.",
    "There are no windows. There is no natural light.",
    "Yellow light fills every corner. It's always yellow here.",
]

SMELLS = [
    "The air smells like wet carpet.",
    "There's an underlying scent of something metallic.",
    "It smells like old paper and dust.",
    "The air is stale. Has it been circulating?",
    "Something sweet. Something rotting underneath.",
]

SOUNDS = [
    "You hear something in the distance.",
    "A fluorescent light is buzzing.",
    "Water dripping. Constant. Rhythmic.",
    "Distant radio static. No station.",
    "Your footsteps echo too much.",
    "A door closes somewhere. But all doors are closed.",
    "You hear breathing. You're alone.",
]

ENTITY_HINTS = [
    "No entities detected... for now.",
    "You are not alone here. You just can't see them yet.",
    "Something watched you come in. It's still watching.",
    "The entities in this level are known to be territorial.",
    "You hear footsteps. They don't match yours.",
    "A sound behind you. Don't turn around.",
]

STABILITY_LEVELS = [
    "12%", "8%", "23%", "3%", "31%", "17%", "41%", "0%", "67%", "unstable"
]

LEVEL_NAMES = [
    ("0", "THE LOBBY", "The most well-known level. Office maze. Yellow walls. The hum."),
    ("1", "THE PACKING ROOMS", "Rooms full of wooden crates. Some of them are open."),
    ("2", "PIPE HEAVEN", "An endless network of pipes. It hums. You hear water."),
    ("3", "THE OFFICES", "Filing cabinets. Papers everywhere. Something in the cabinets moves."),
    ("4", "ABANDONED CONCRETE", "Structural supports you don't understand. This place wasn't built."),
    ("5", "HOTELS & ROOMS", "A hotel that goes on forever. Room 5 is always occupied."),
    ("6", "THE WATER ZONE", "Pools of liquid in dark rooms. Some of it is water. Probably."),
    ("7", "THE GOLF COURSE", "An endless golf course. The flag is always the same distance away."),
]

# ============================================================
# ENTITY GENERATION DATA
# ============================================================

ENTITY_TYPES = [
    ("Skinless", "They look almost human, but their skin has been... removed. What remains is red, wet muscle tissue that glistens under the fluorescent light."),
    ("Smiler", "It smiles. Always. Its face is frozen in an expression of pure joy. But its eyes... its eyes are wrong."),
    ("Wretches", "Crawling things. They used to be human. Now they move on all fours, making sounds that aren't quite animal."),
    ("Faceless", "They have no face. Just a smooth expanse of skin where features should be. They seem to be looking for something."),
    ("Deathmoth", "Moths the size of dogs. They circle lights that don't exist. They don't attack. They just... watch."),
    ("The Thing That Tastes Color", "You hear it before you see it. A wet, clicking sound. Then it appears. It tilts its head. It's tasting the air."),
    ("Partygoers", "They wear masks. Colorful masks. They dance in rooms that shouldn't exist. They don't notice you. Not yet."),
    ("Cursor", "A shadow that moves wrong. It doesn't walk, it drifts. It has too many joints."),
]

ENTITY_BEHAVIORS = [
    "It doesn't seem to notice you.",
    "It stops. It tilts its head. It knows you're here.",
    "It runs. Toward you. Fast.",
    "It stands in the corner, watching. It has been watching for a long time.",
    "It screams. The sound doesn't come from its mouth.",
    "It mimics your movements perfectly. A slight delay.",
]

ENTITY_WARNINGS = [
    "DO NOT ENGAGE. DO NOT LOOK AT IT DIRECTLY.",
    "It will kill you if it catches you. It always catches you eventually.",
    "Entities are predictable. Learn their patterns. Don't be where they expect you to be.",
    "Some say they used to be human. Don't think about that.",
    "The only safe response is no response.",
]


# ============================================================
# GENERATION FUNCTIONS
# ============================================================

def generate_room():
    room_template, room_desc = random.choice(ROOMS)
    room_size = random.choice(ROOM_SIZES)
    level_num, level_name, level_subtitle = random.choice(LEVEL_NAMES)
    
    ceiling = random.choice(CEILING_ISSUES)
    wall_cover = random.choice(WALL_COVERINGS)
    light = random.choice(LIGHT_ISSUES)
    smell = random.choice(SMELLS)
    
    num_sounds = random.randint(2, 4)
    sounds = random.sample(SOUNDS, min(num_sounds, len(SOUNDS)))
    
    entity_hint = random.choice(ENTITY_HINTS)
    stability = random.choice(STABILITY_LEVELS)
    
    desc = f"You are in {room_template.format(room_size=room_size, wall_cover=wall_cover)}.\n"
    desc += f"{room_desc}\n\n"
    desc += f"{ceiling}\n"
    desc += f"{light}\n"
    desc += f"{smell}\n\n"
    
    for sound in sounds:
        desc += f"{sound}\n"
    
    desc += "\nYou can't remember how you got here.\n"
    desc += "There is no exit. There is only forward.\n\n"
    desc += f"[ {entity_hint} ]\n"
    desc += f"[ Stability: {stability} ]"
    
    return level_num, level_name, level_subtitle, desc


def generate_entity():
    entity_name, entity_desc = random.choice(ENTITY_TYPES)
    entity_behavior = random.choice(ENTITY_BEHAVIORS)
    entity_warning = random.choice(ENTITY_WARNINGS)
    
    return entity_name, entity_desc, entity_behavior, entity_warning


# ============================================================
# FLASK ROUTES
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate/room')
def gen_room():
    level_num, level_name, level_subtitle, desc = generate_room()
    return jsonify({
        'level_num': level_num,
        'level_name': level_name,
        'level_subtitle': level_subtitle,
        'description': desc
    })


@app.route('/generate/entity')
def gen_entity():
    name, desc, behavior, warning = generate_entity()
    return jsonify({
        'name': name,
        'description': desc,
        'behavior': behavior,
        'warning': warning
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
