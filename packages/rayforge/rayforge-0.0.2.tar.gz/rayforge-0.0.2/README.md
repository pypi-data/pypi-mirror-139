# RayForge
A game engine made with Raylib.

## Getting Started
1) Install Python
2) Open cmd/terminal and type:

```
pip install RayForge
```

## Examples
# Creating a window
``` python
from rayforge import *

forge = RayForge()

@forge.update
def update(dt):
    pass

forge.run()
```

# Creating a text
``` python
from rayforge import *

forge = RayForge()

class HelloWorld(Text):
    def __init__(self):
        super().__init__(
            window = forge,
            text = "Hello, World!",
            font_size = 20,
            x = 0,
            y = 0,
            color = color.Color(0, 255, 255)
        )

text = HelloWorld()

@forge.update
def update(dt):
    pass

forge.run()
```