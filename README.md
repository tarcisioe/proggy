Proggy
======

Progressively progressing through progress bar generation.

Proggy generates text-based progress bars. Mildly inspired by Rust's
[indicatif](https://github.com/mitsuhiko/indicatif).

Proggy only renders progress bars to a string. Displaying them is, as of now,
not handled and left to the user.

Example
-------

```
>>> from proggy import ProgressBar
>>> pb = ProgressBar(30, 100, progress=75)
>>> pb.render()
'⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇       '
```
