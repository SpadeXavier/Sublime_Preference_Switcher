# Sublime_Preference_Switcher
A script for easily switching between sublime preference files, or between themes and color schemes on Linux.

# Installation on Arch Linux 
The PKGBUILD for this script can be found at https://github.com/SpadeXavier/PKGBUILDS/blob/master/PKGBUILD_sublime. 
Simply download the file and rename it PKGBUILD. Run makepkg -sic in the same directory as the PKGBUILD to install the script. 

# How To

NOTE: You must open Sublime Text 3 -> Preferences -> Settings and save the file
that opens up for this script to function

Place custom sublime preference files(.sublime-settings) in ~/.config/sublime_preferences. Run this script by typing change_subl_settings in the terminal and the script will search for your custom preference files and change sublime preferences to your chosen file. 

This script also easily allows changing the theme and color scheme of sublime by searching through all packages for usable themes and color schemes and asking which combination of theme and color schemes you would like to use for your preference file. 

Enjoy!
