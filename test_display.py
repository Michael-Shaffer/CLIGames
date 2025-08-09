# TODO
from engine.display import Display, Color
import time

d = Display()

d.clear()

# Test colored_text
colored = d.colored_text("This is red", Color.RED)
d.print_at(10, 10, colored)
colored_2 = d.colored_text(colored, Color.BLUE) # Test color cleaning
d.print_at(20, 20, colored_2)

# Test dimension handling
d.print_at(1,1, "Top Left")
d.print_at(d.width - 9, 1, "Top Right")
d.print_at(1, d.height, "Bottom Left")

# Test center_text
colored_center = d.colored_text("Center", Color.GREEN)
d.center_text(colored_center, 15)
d.center_text(colored_center)

# Test truncation
long_text = "x" * 200
d.print_at(1, 23, long_text)
d.flush()

time.sleep(2)

try:
    d.print_at(0, 1, "This should fail")
except ValueError as e:
    d.print_at(1, 5, f"Caught error: {e}")
    d.flush()
