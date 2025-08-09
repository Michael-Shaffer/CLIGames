# TODO
from engine import Display
import time

d = Display(immediate_flush=True)

d.clear()
d.print_at(1,1, "Top Left")
d.print_at(d.width - 9, 1, "Top Right")
d.print_at(1, d.height, "Bottom Left")
d.flush()

time.sleep(2)

try:
    d.print_at(0, 1, "This should fail")
except ValueError as e:
    d.print_at(1, 5, f"Caught error: {e}")
    d.flush()
