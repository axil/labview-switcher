# labview-switcher

In LabView it is difficult to switch using Alt-Tab from a vi to, for example, a browser 
when many vi files are open, because LabView breaks standard Alt-Tab behaviour.

It takes about 2n-1 keypresses where n is the number of vis open.

With this script you can switch between the active vi and the browser (ie Most Recently 
Used non-labview window) using one keypress (Alt-` by default).

## Installation

1. Install any recent python 2.x or 3.x
2. Install Autohotkey
3. Double-click switch.ahk

## Usage

Press Alt-` (Alt-backtick) to switch to the previous window:
  - previous non-labview window if we are in labview or
  - just any previous window if we are not.

To unload the script, use the green tray icon with the letter 'H'.
