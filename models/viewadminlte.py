import re, subprocess
#descargo backup cdns por si fallan
def backup_cdns():
	dir = 'backup/cdns/'
	f = open('applications/tapa14/views/plugin_adminlte/layout_starter.html', "r")
	fileContent = f.read()
	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', fileContent.lower())
	subprocess.run(["mkdir", "-p", dir])
	for url in urls:
		subprocess.run(["wget", str(url), "-P", dir])