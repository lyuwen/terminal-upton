all: strategy_1.pdf

.PHONY: all clean

strategy_1.pdf: strategy_1.tex
	latexmk -pdf strategy_1.tex
	latexmk -c strategy_1.tex

clean:
	latexmk -C strategy_1.tex

