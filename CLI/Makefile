# Folder to clean
CSV_FOLDER = CSV
EXCEL_FOLDER = XLSX
PODCAST_FOLDER = Podcast
XML_FOLDER = XML

run: prepare_folders
	python download_rss_and_podcasts.py

prepare_folders:
	@echo "Creating required directories if they don't exist..."
	mkdir -p CSV
	mkdir -p Podcast
	mkdir -p XLSX
	mkdir -p XML
	@echo "Directories created or already exist."

clean_all: clean_csv clean_excel clean_podcast clean_xml

clean_csv:
	rm -f $(CSV_FOLDER)/*

clean_excel:
	rm -f $(EXCEL_FOLDER)/*

clean_podcast:
	rm -f $(PODCAST_FOLDER)/*

clean_xml:
	rm -f $(XML_FOLDER)/*

