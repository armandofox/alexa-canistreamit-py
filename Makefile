AWS = aws
ZIP = zip
PYTHON = python

SKILL_NAME = CanIStreamIt
ZIPFILE = _$(SKILL_NAME).zip

zip: $(ZIPFILE)

$(ZIPFILE): $(wildcard lambda/*)
	cd lambda && $(ZIP) -q -X -r ../$(ZIPFILE) *

upload_lambda: $(ZIPFILE)
	$(AWS) lambda update-function-code --function-name $(SKILL_NAME) --zip-file fileb://$(ZIPFILE)

skill/utterances.txt: skill/utterances.txt.glob
	$(PYTHON) lambda/ask/unglob_intent.py $< > $@

# download MOVIES.html from http://usa.netflixable.com/
skill/MOVIES: skill/MOVIES.html
	cat $< perl -ne 'print if $. > 747'  | perl -pe 's/<a/\n<a/g' | perl -ne 'print if /movies.netflixable.com/' | perl -pe 's/<a[^>]+>//, s!</.*$!!' < $@
