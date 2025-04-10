python3 diagrams.py

for f in diagram*.pdf; do
    convert -density 300 -trim ${f} ${f%pdf}png
done
