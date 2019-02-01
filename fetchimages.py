import sys
import re
import os.path
from urllib.request import urlopen
from urllib.request import urlretrieve

def get_url(url):
	success = True;
	decoded_html = ""
	try:
		with urlopen(url) as response:
			html_response = response.read()
			encoding = response.headers.get_content_charset('utf-8')
			decoded_html = html_response.decode(encoding)
	except:
		print("Failed to get content from {}".format(url))
		success = False
		
	return success, decoded_html
	
def get_img_srcs(content, url):
	# extract img elements and later on src using regex
	imgs = re.findall('<img([\w\W]+?)[\/]?>', content)
	# attempt to filter out non-files
	filter = ['(', ';', '\'', '|', '?']
	valid_srcs = []
	for img in imgs:
		srcs = re.findall('src=([\S]+)', img)
		for src in srcs:
			print(src)
			unquoted = src.replace("\"", "")
			print(unquoted)
			if not any(f in unquoted for f in filter):
				if not (unquoted.startswith("http")):
					unquoted = url + unquoted
				valid_srcs.append(unquoted)
				print(unquoted)
	return valid_srcs
	
def get_local_filename(file, url):
	# create foldername from url
	disallowed = str.maketrans(dict.fromkeys(':\/*?"<>|'))
	url_folder = url.translate(disallowed)
	if not os.path.exists(url_folder):
		os.makedirs(url_folder)   
	localpath = os.path.join(url_folder, file)
	
	# make sure previous downloads are not overwritten
	if (os.path.isfile(localpath)):
		filecandidate = file
		i = 0
		name, ext = os.path.splitext(file)
		while os.path.isfile(os.path.join(url_folder,filecandidate)):
			filecandidate = "{}({}){}".format(name, i, ext)
			i+=1
		file = filecandidate
	return os.path.join(url_folder, file)

def fetch_images(url):
	success, content = get_url(url)
	if (success):
		imgs = get_img_srcs(content, url)
		print("Downloading {} images".format(len(imgs)))
		print("Press y to continue (or any other key to abort)")
		ok = input()
		if (ok == 'y'):
			for img in imgs:
				filename = img[img.rfind("/")+1:]
				filename = get_local_filename(filename, url)
				urlretrieve(img, filename)
		else:
			print("Aborted.")
	
if __name__ == "__main__":
	# iterate urls gives as arguments (urls currently not validated)
	for arg in sys.argv[1:]:
		print("\nAttempting to fetch images from " + arg)
		fetch_images(arg)

	
	


	
