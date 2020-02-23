Proggy
======

Progressively progressing through progress bar generation.

Proggy generates text-based progress bars. Mildly inspired by Rust's
[indicatif](https://github.com/mitsuhiko/indicatif).

Proggy only renders progress bars to a string. Displaying them is, as of now,
not handled and left to the user.

Examples
--------

### API usage

```
>>> from proggy import ProgressBar
>>> pb = ProgressBar(30, 100, progress=75)
>>> pb.render()
'⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇       '
```

### CLI output

`test.py`:
```python
import time

from proggy.tty import TTYProgressBar


with TTYProgressBar(size=30, total=100) as p:
    for i in range(100):
        time.sleep(0.1)
        p.progress += 1
        p.draw()
```

Output:

![test.py output](gif/test.gif)
