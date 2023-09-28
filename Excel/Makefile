# Folder to clean
CSV_FOLDER = CSV_Dump
EXCEL_FOLDER = Excel_Dump
PODCAST_FOLDER = Podcast_Dump
XML_FOLDER = XML_Dump

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

