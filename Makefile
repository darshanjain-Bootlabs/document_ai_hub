.PHONY: gitpush

gitpush:
	git add .
	git commit -m "$(m)"
	git push -u origin main