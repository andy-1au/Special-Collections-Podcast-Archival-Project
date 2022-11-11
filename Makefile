app2:
	cd GUI\ App/; \
	python3.9 app2.py
test:
	python3.9 clean.py

deleteXML:
	cd XML; \
	rm -rf *.xml

deletePD:
	cd Podcasts; \
	rm -rf *.pdf

deleteALL:
	rm -rf Podcasts/*.mp3; \
	rm -rf XML/*.xml \