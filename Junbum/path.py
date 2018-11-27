import os
files_path = []
for x in os.listdir():
	if 'script.py' in x:
		print(os.path.abspath(x))
		files_path.append(os.path.abspath(x))

print(files_path)