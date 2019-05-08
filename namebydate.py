# Adds the creation date of a file (formatted to YYYY-MM-DD) to the beginning of all files within a specified directory.
# Only tested on Windows 10 with Python 3.7 so far.

# Can be run from anywhere.

import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

def get_date(file):
	return datetime.utcfromtimestamp(os.path.getctime(file)).strftime('%Y-%m-%d')

root = tk.Tk()
root.withdraw()

directory = filedialog.askdirectory()+'/'

rename_folders = False
joinwith = '-'

# Set choice to no by default
choice = 'n'
choice = input('[y/n] Rename folders? ').lower()

if choice == 'y':
	print('The script will rename folders.')
	rename_folders = True
else:
	print('The script will not rename folders.')
	rename_folders = False

files = os.listdir(directory)
try:
	files.remove(__file__)
	files.remove('__pycache__')
except ValueError:
	pass

if rename_folders == False:
	for i in files:
		if os.path.isdir(i):
			files.remove(i)

print('\nFound {} items in directory.'.format(len(files)))

choice = ''

while True:
	choice = input("""
s - Start renaming items.
l - List items to be renamed.
x - Exclude a certain item from the list. Will open another input prompt.
j - Choose character/string to be inserted between the date and the original filename. This is a hyphen by default
	e.g if the joining character is a hyphen: "2018-07-15-filename.txt"
	if the joining character is ".": "2018-07-15.filename.txt"
e - Exit script.
> """).lower().strip()
	if choice in ['e', 's', 'l', 'x', 'j']:
		if choice == 'e':
			raise SystemExit
		elif choice == 'l':
			print('Listing...')
			for i in files:
				itemtype = ''
				if os.path.isdir(directory+i):
					itemtype = 'DIRECTORY'
				elif os.path.isfile(directory+i):
					itemtype = 'FILE'
				print('({current}/{total}) [{itemtype}] {name}'.format(
					current=str(files.index(i)+1),
					total=len(files),
					itemtype=itemtype,
					name=i))
		elif choice == 'x':
			try:
				exclusion = input('Exact name of item to exclude: ')
				files.remove(exclusion)
				print('{} will not be renamed.'.format(exclusion))
			except ValueError:
				print('{} is not in the list.'.format(exclusion))
		elif choice == 'j':
			joinwith = input('Joining character/string: ')
		elif choice == 's':
			break
	else:
		print('Invalid response.')

print('\nRenaming...')

os.chdir(directory)

for file in files:
	# Skip any files with dates already added
	if get_date(file) in file:
		print('Item "{}" already has a date added to it.'.format(file))
		continue

	newname = '{date}{joinwith}{name}'.format(date=get_date(file),joinwith=joinwith,name=file)
	os.rename(file,newname)
	print('({}/{}) {} -> {}'.format(
		str(files.index(file)+1),
		len(files),
		file,
		newname)
	)

input('\nFinished, press enter to exit.')