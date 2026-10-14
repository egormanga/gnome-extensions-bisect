#!/usr/bin/env python3
# GNOME Extensions bisect

import sys, math
from gi.repository import Gio

SCHEMA = 'org.gnome.shell'
KEY = 'enabled-extensions'

def main():
	shell = Gio.Settings.new(SCHEMA)

	extensions = shell[KEY]
	print(f"\033[2m{extensions}\033[m")
	extensions_orig = tuple(extensions)

	if (known_good := [i for i in sys.argv[1:] if i in extensions]):
		print(f"\033[1;92mAssumed known good\033[39m (or testing against):\033[22m {known_good}")
		extensions = [i for i in extensions if i not in known_good]

	try:
		l, r = 0, len(extensions)
		steps = math.ceil(math.log2(r) + 1)

		ii = int()
		validating = bool()
		while (l < r):
			print()
			ii += 1
			m = (l + r)//2

			shell[KEY] = (known_good + extensions[l:m])
			print(f"\033[1mStep {ii}\033[22m/{steps}: \033[2m{shell[KEY]}\033[22m")

			q = input("Good? ").casefold().strip()[:1]
			good = (q in '1ytд')
			print(f"\033[FGood? \033[9{1+good}m{q}\033[39m")
			if (good):
				if (l == r-1): return f"\033[1;93mFound:\033[22;39m \033[96m{extensions[m]}\033[39m \033[3m(state restored)\033[22m."
				l = m
			else: r = m
		else: return f"\033[1;91mNot found\033[22;39m, check {', '.join(f'\033[96m{i}\033[39m' for i in known_good) + ' or '*bool(known_good)}GNOME itself."
	except KeyboardInterrupt: print("\b\b\033[3mAborting (state restored).\033[22m"); return 1
	finally: shell[KEY] = extensions_orig; print('\033[m')

if (__name__ == '__main__'): exit(main())

# by Sdore, 2025-26
#   www.sdore.me
