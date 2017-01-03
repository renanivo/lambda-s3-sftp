install:
	pip install -r requirements.txt

package: install
	mkdir -p dist
	cp main.py dist/
	cp -r $(VIRTUAL_ENV)/lib/python2.7/site-packages/. dist/
	cp -r $(VIRTUAL_ENV)/lib64/python2.7/site-packages/. dist/
	cd dist; zip -r ../package.zip .

clean:
	rm -rf dist/
	rm package.zip
