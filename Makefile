install:
	mkdir -p dist
	pip install --target ./dist -r requirements.txt

package: install
	cp main.py dist/
	cd dist; zip -r ../package.zip .

clean:
	rm -rf dist/
	rm package.zip
