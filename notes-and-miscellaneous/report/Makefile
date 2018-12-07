all: sample-sigconf.pdf

%.pdf: %.tex bibliography.bib
	pdflatex -halt-on-error $<
	bibtex $*
	pdflatex -halt-on-error $<
	pdflatex -halt-on-error $<

.PHONY: clean
clean:
	rm -f *.aux *.log *.out *.pag *.pdf
