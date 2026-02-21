MSG ?= update site

.PHONY: publish

publish:
	quarto render
	git add -A
	git commit -m "$(MSG)"
	git push
