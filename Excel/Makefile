# Folder to clean
CSV_FOLDER = CSV
EXCEL_FOLDER = XLSX
PODCAST_FOLDER = Podcast
XML_FOLDER = XML

run:
	python download_rss_and_podcasts.py

clean_all: clean_csv clean_excel clean_podcast clean_xml

clean_csv:
	rm -f $(CSV_FOLDER)/*

clean_excel:
	rm -f $(EXCEL_FOLDER)/*

clean_podcast:
	rm -f $(PODCAST_FOLDER)/*

clean_xml:
	rm -f $(XML_FOLDER)/*

