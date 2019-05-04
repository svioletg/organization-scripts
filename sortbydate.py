# Organizes all files within a specified directory into folders corresponding to creation date.
# e.g If a file's creation date is 2019-05-03, a "2019" folder will be created in the directory. 
# That folder will contain a "05 May" folder, and the file will be stored there.

# Only tested on Windows 10 with Python 3.7 so far.
# Can be run from anywhere.

import os
import tkinter as tk
import sys
from tkinter import filedialog
from datetime import datetime

root = tk.Tk()
root.withdraw()

directory = filedialog.askdirectory()+'/'

files = os.listdir(directory)
try:
	files.remove(__file__)
	files.remove('__pycache__')
except ValueError:
	pass

print('Found {} items in "{}".'.format(len(files),directory))

# Set to 'n' by default
choice = 'n'
choice = input('[y/n] Sort folders? ').lower().strip()
if choice == 'y':
	sort_folders = True
else:
	sort_folders = False

choice = 'n'
choice = input('[y/n] Sort files? ').lower().strip()
if choice == 'y':
	sort_files = True
else:
	sort_files = False

if sort_folders == False:
	for i in files:
		if os.path.isdir(directory+i):
			files.remove(i)

if sort_files == False:
	for i in files:
		if os.path.isfile(directory+i):
			files.remove(i)

while True:
	try:
		month_type = int(input("""
1 - Number-only;             e.g 09
2 - Number and abbreviation; e.g 09 Sep
3 - Number and full name;    e.g 09 September
4 - Abbreviation;            e.g Sep
5 - Full name;               e.g September

Choose the month naming format: """))
	except ValueError:
		print('Option must be an integer.')
		continue

	if month_type not in [1, 2, 3, 4, 5]:
		print('Invalid option.')
	else:
		break

def get_date(file):
	if month_type == 1:
		return datetime.utcfromtimestamp(os.path.getctime(file)).strftime('%Y/%m')
	if month_type == 2:
		return datetime.utcfromtimestamp(os.path.getctime(file)).strftime('%Y/%m %b')
	if month_type == 3:
		return datetime.utcfromtimestamp(os.path.getctime(file)).strftime('%Y/%m %B')
	if month_type == 4:
		return datetime.utcfromtimestamp(os.path.getctime(file)).strftime('%Y/%b')
	if month_type == 5:
		return datetime.utcfromtimestamp(os.path.getctime(file)).strftime('%Y/%B')

choice = ''

while True:
	choice = input("""
s - Start moving items.
l - List items to be moved.
x - Exclude a certain item from the list (will open another input prompt).
e - Exit script.
> """).lower().strip()
	if choice in ['e', 's', 'l', 'x']:
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
				exclusion = input('Exact name of item to exclude (you can also use "#" followed by a number): ')
				if exclusion.startswith('#'):
					exclusion = files[int(exclusion.replace('#',''))-1]

				choice = input('[y/n] Confirm the exclusion of "{}": '.format(exclusion))

				if choice == 'y':
					files.remove(exclusion)
					print('"{}" will not be moved.'.format(exclusion))
				else:
					continue
			except ValueError:
				print('"{}" is not in the list.'.format(exclusion))
		elif choice == 's':
			break
	else:
		print('Invalid response.')
		continue

print('\nRenaming...')

os.chdir(directory)

for file in files:
	date = get_date(file)
	y = date.split('/')[0]
	m = date.split('/')[1]
	if not os.path.exists(y):
		os.mkdir(y)
		os.mkdir(y+'/'+m)

	newdir = '{directory}/{name}'.format(directory=date,name=file)
	os.rename(file,newdir)
	print('({}/{}) {} -> {}'.format(
		str(files.index(file)+1),
		len(files),
		file,
		newdir)
	)

input('\nFinished, press enter to exit.')