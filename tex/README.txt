lualatex cv.ja.main && bibtex cv.ja.main && lualatex cv.ja.main
platex cv.ja.ja-pub && pbibtex cv.ja.ja-pub && platex cv.ja.ja-pub && platex cv.ja.ja-pub && dvipdfmx cv.ja.ja-pub.dvi
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=cv.ja.pdf cv.ja.main.pdf cv.ja.ja-pub.pdf