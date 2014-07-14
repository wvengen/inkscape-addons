# Inkscape add-ons
Add-ons for the open-source vector-drawing program [Inkscape](http://www.inkscape.org/).

## Multi-page PDF export
To export a PDF file with multiple pages (Inkscape only supports a single page by default), create
multiple layers. If you want a common background, name that layer `background` or `bg`. Save the file
with filetype "Multi-page PDF", and you'll have a multi-page document.

*Requirements*: needs [PDFtk](http://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) installed (in `PATH`).

*Installation*: copy the files
  [extensions/multi\_page\_pdf\_output.inx](https://raw.githubusercontent.com/wvengen/inkscape-addons/master/extensions/multi_page_pdf_output.inx)
  and
  [extensions/multi\_page\_pdf\_output.py](https://raw.githubusercontent.com/wvengen/inkscape-addons/master/extensions/multi_page_pdf_output.py)
  to your `~/.config/inkscape/extensions/` directory.

