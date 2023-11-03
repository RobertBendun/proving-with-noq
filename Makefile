all: derivative.html derivative.noq derivative.with_output.html

%.html: %.adoc
	asciidoctor $<

%.noq: %.adoc
	awk '/----/{show=1-show;next}show' $< >$@

%.with_output.adoc: %.adoc
	./mixin-output.py >$@

clean:
	rm -vf derivative.html derivative.noq derivative.with_output.html derivative.with_output.adoc

.PHONY: clean all
