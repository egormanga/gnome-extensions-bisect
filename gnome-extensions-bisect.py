#!/usr/bin/env python3
# GNOME Extensions bisect

import math
from gi.repository import Gio

SCHEMA = 'org.gnome.shell'
KEY = 'enabled-extensions'

def main():
	shell = Gio.Settings.new(SCHEMA)

	extensions = shell[KEY]
	print(f"\033[2m{extensions}\033[m")

	try:
		l, r = 0, len(extensions)
		steps = math.ceil(math.log2(r) + 1)

		ii = int()
		validating = bool()
		while (l < r):
			print()
			ii += 1
			m = (l + r)//2

			shell[KEY] = extensions[l:m]
			print(f"\033[1mStep {ii}\033[m/{steps}: \033[2m{shell[KEY]}\033[m")

			if (input("Good? ").casefold().strip()[:1] in '1ytд'):
				if (l == r-1): print("\033[1mFound:\033[m", extensions[m]); break
				l = m
			else: r = m
		else: print("\033[1;91mNot found\033[m, check GNOME itself.")
	finally: shell[KEY] = extensions

if (__name__ == '__main__'): exit(main())

# by Sdore, 2025
#  www.sdore.me
