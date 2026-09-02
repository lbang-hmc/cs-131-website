DEPLOY_HOST := bang@knuth
DEPLOY_PATH := ~/public_html/cs131

.PHONY: serve build clean deploy

serve:
	mkdocs serve

build:
	mkdocs build

clean:
	rm -rf site

# Build the site fresh, then rsync it to the server. Only adds/updates files
# on the remote (no --delete), so anything removed locally has to be cleaned
# up on the server by hand.
deploy: clean build
	rsync -avz site/ $(DEPLOY_HOST):$(DEPLOY_PATH)/
