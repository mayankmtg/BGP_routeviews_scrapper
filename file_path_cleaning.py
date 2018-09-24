import sys





def pathCleaning(path_array):
	cleaned_array=[]
	top=-1
	n=len(path_array)
	for i in range(0,n):
		if(top==-1):
			cleaned_array.append(path_array[i])
			top+=1

		elif(cleaned_array[top]!=path_array[i]):
			cleaned_array.append(path_array[i])
			top+=1

	return cleaned_array


if(len(sys.argv)<2):
	print("Error: Command like python file_path_cleaning.py <file_name>")
	sys.exit(0)


with open(sys.argv[1]) as f:
	for line in f:
		line_array=line.split()
		ip_prefix=line_array[0]
		path_array=line_array[1:]
		clean_path_array=pathCleaning(path_array)
		print(ip_prefix),
		print(' '.join(clean_path_array))
		
