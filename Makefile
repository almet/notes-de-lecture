upload:
	readingnotes notes output
	echo "lectures.notmyidea.org" > output/CNAME
	ghp-import -p output
	git push origin master

regenerate:
	readingnotes notes output && python3 -m http.server 8001 --directory output