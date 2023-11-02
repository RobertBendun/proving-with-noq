all: derivative.html derivative.noq

%.html: %.adoc
	asciidoctor $<

%.noq: %.adoc
	awk '/----/{show=1-show;next}show' $< >$@
