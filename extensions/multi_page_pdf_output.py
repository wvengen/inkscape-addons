#!/usr/bin/env python
"""
multi_page_pdf_output.py
Inkscape extension for saving a PDF with a page for each layer.
https://github.com/wvengen/inkscape-addons

To use a background layer for each page, name it 'background' or 'bg'.


Copyright (c) 2014 wvengen <dev-inkscape@willem.engen.nl>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import sys
sys.path.append('/usr/share/inkscape/extensions')

import os
import inkex
import shutil
import tempfile
from subprocess import check_call

class Multi_Page_PDF_Output(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def output(self):
        out = open(self.output_file, 'rb')
        if os.name == 'nt':
            import msvcrt
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        sys.stdout.write(out.read())
        out.close()
        self.clear_tmp()

    def clear_tmp(self):
        shutil.rmtree(self.tmp_dir)

    def effect(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.tmp_dir, 'output.pdf')

        bg_layers = list(self.get_layers('bg'))
        for layer in self.get_layers('page'):
            name = layer.get('id')
            svg_file = os.path.join(self.tmp_dir, name+'.svg')
            pdf_file = os.path.join(self.tmp_dir, name+'.pdf')
            self.show_layers([layer] + bg_layers)
            self.document.write(svg_file)
            self.svg2pdf(svg_file, pdf_file)

        self.pdf_merge(map(lambda l: os.path.join(self.tmp_dir, l.get('id')+'.pdf'), self.get_layers('page')), self.output_file)

    def get_layers(self, type=None):
        layers = self.document.xpath('//svg:svg/svg:g', namespaces=inkex.NSS)
        if type == 'page':
            layers = filter(lambda l: not self.is_bg_layer(l), layers)
        elif type == 'bg':
            layers = filter(lambda l: self.is_bg_layer(l), layers)
        return reversed(layers)

    def is_bg_layer(self, layer):
        name = layer.get(inkex.addNS('label', 'inkscape')).lower()
        return name.startswith('background') or name.startswith('bg')

    def show_layers(self, layers):
        # @todo add to original style instead of hard-replacing it
        for layer in self.get_layers():
            if layer in layers:
                layer.set('style', 'display:inline')
            else:
                layer.set('style', 'display:none')

    def svg2pdf(self, src, dst):
        return check_call(['inkscape', '--export-area-page', '--export-pdf='+dst, src])

    def pdf_merge(self, src, dst):
        if not isinstance(src, list): src = [src]
        info_file = os.path.join(self.tmp_dir, src[0]+'.info')
        check_call(['pdftk', src[0], 'dump_data', 'output', info_file])
        check_call(['pdftk'] + src + ['cat', 'output', dst+'.pre'])
        check_call(['pdftk', dst+'.pre', 'update_info', info_file, 'output', dst])


if __name__ == '__main__':   #pragma: no cover
  e = Multi_Page_PDF_Output()
  e.affect()

# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 encoding=utf-8 textwidth=99
