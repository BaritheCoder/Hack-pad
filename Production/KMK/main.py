import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC

from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers as _Layers
from kmk.extensions.rgb import RGB


keyboard = KMKKeyboard()

# -----------------------
# 6 individual switches
# -----------------------
PINS = (
    board.GP7,  # switch 1
    board.GP0,  # switch 2
    board.GP1,  # switch 3
    board.GP2,  # switch 4
    board.GP4,  # switch 5
    board.GP3,  # switch 6
)

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# -----------------------
# RGB (3x SK6812mini) on GP26
# -----------------------
# If your SK6812mini are RGBW, you may need rgb_order=(1,0,2,3) like some examples.
# If they are RGB only, leave rgb_order out.
rgb = RGB(
    pixel_pin=board.GP26,
    num_pixels=3,
    # rgb_order=(1, 0, 2, 3),  # <- uncomment if your LEDs are RGBW
)
keyboard.extensions.append(rgb)

# Make RGB show the current "mode" (top layer) by changing color
class Layers(_Layers):
    last_top_layer = 0
    # 3 distinct hues for 3 modes (0/1/2)
    hues = (4, 20, 69)

    def after_hid_send(self, keyboard):
        top = keyboard.active_layers[0]
        if top != self.last_top_layer:
            self.last_top_layer = top
            rgb.set_hsv_fill(self.hues[top], 255, 255)

layers = Layers()
keyboard.modules.append(layers)

# -----------------------
# Rotary encoder
# A=GP27, B=GP6, Button=GP29
# -----------------------
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

encoder_handler.pins = (
    (board.GP27, board.GP6, board.GP29, False),  # (A, B, button, inverted?)
)

# Per-layer encoder actions: (left, right, press)
# Press cycles modes: 0->1, 1->2, 2->0
encoder_handler.map = [
    # Mode 0
    ((KC.VOLD, KC.VOLU, KC.DF(1)),),
    # Mode 1
    ((KC.PGDN, KC.PGUP, KC.DF(2)),),
    # Mode 2
    ((KC.LEFT, KC.RIGHT, KC.DF(0)),),
]

# -----------------------
# Keymaps for the 6 switches (3 modes/layers)
# -----------------------
keyboard.keymap = [
    # Mode 0 (Layer 0) - example
    [
        KC.A, KC.B, KC.C, KC.D, KC.E, KC.F
    ],

    # Mode 1 (Layer 1) - example
    [
        KC.MPLY, KC.MPRV, KC.MNXT, KC.MUTE, KC.VOLD, KC.VOLU
    ],

    # Mode 2 (Layer 2) - example
    [
        KC.ESC, KC.TAB, KC.ENTER, KC.BSPC, KC.DEL, KC.SPC
    ],
]

if __name__ == "__main__":
    keyboard.go()
