# Morse
[![](https://img.shields.io/badge/language-Python-blue)](https://www.python.org/)  ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ruxia-TJY/Morse) ![macos](https://img.shields.io/badge/-macOS-black?logo=macos) ![linux](https://img.shields.io/badge/-Linux-yellow?logo=linux) ![windows](https://img.shields.io/badge/-Windows-blue?logo=windows)




A simple package for morse decode and encode.

```python
from Morse import morse

M = morse.Morse()

print(M.encode('morse'))
# ————/——————/.——./.../.
print(M.decode('————/——————/.——./.../.'))
# MORSE
M.isLower = True
print(M.decode('————/——————/.——./.../.'))
# morse

M.Separator = '?'
print(M.encode('morse'))
# ————?——————?.——.?...?.

M.dot = '<'
M.dash = '>'
print(M.encode('morse'))
# >>/>>>/<></<<</<
```