# BaliVIP Content Scaling
.PHONY: check clean list list-photos new video help
.DEFAULT_GOAL := help

PY := python3

help:
	@echo ""
	@echo "  make new NAME=venue-myths KIND=carousel   start a new deck"
	@echo "  make venue-myths                          build, render and check it"
	@echo "  make check                                check every deck"
	@echo "  make video NAME=venue-myths SECONDS=3     render slides to MP4"
	@echo "  make list                                 list decks"
	@echo "  make list-photos                          list valid photo codes"
	@echo "  make clean                                empty build/"
	@echo ""

DECK = $(shell find content -maxdepth 2 -type d -name "$@" 2>/dev/null | head -1)

new:
	@test -n "$(NAME)" || (echo "usage: make new NAME=my-post KIND=carousel"; exit 1)
	@$(PY) scripts/new_deck.py "$(NAME)" "$(or $(KIND),carousel)"

check:
	@$(PY) scripts/qa_gate.py

video:
	@test -n "$(NAME)" || (echo "usage: make video NAME=my-post SECONDS=3"; exit 1)
	@$(PY) scripts/video.py build/$(NAME) --seconds $(or $(SECONDS),3)

list:
	@find content -maxdepth 2 -mindepth 2 -type d | sed 's|content/|  |'

list-photos:
	@cut -f1 photos/manifest.tsv | tr '\n' ' '; echo

clean:
	@rm -rf build/* && echo "build/ emptied"

# any other target is treated as a deck name
%:
	@d=$$(find content -maxdepth 2 -mindepth 2 -type d -name "$@" | head -1); \
	if [ -z "$$d" ]; then echo "no deck called '$@'. Try: make list"; exit 1; fi; \
	$(PY) scripts/build.py $$d && \
	$(PY) scripts/render.py build/$@ && \
	$(PY) scripts/qa_gate.py $$d
