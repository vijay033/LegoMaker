import zerorpc
import argparse
from filters import *
from image import Image
from color_generator import Color_Generator
from server import MosaicServer
import pkg_resources
import os
import glob

def run_server(ip, port):
    # Run a server if specified
    address = ip + ":" + port
    server = zerorpc.Server(MosaicServer())
    print ('Running server at %s' % address)
    server.bind(address)
    server.run()


def main():
    color_generator = Color_Generator()
    def load_color_palettes():
        pattern = 'colorLego.csv'
        for filename in glob.iglob(pattern):
            palette_name = os.path.splitext(os.path.basename(filename))[0]
            color_generator.load_palette(palette_name, filename)

    load_color_palettes()

    #Variables
    input_image_path =  './in/celebA'
    output_path = './out'
    input_path = glob.glob(os.path.join(input_image_path, '*.jpg'))
    
    tile_size = 5
    n = 7
    img_length = 48
    palette_scheme = 'colorLego'
    
    for filename in input_path:
        input_filename = filename
        output_filename = os.path.basename(filename)
        print ('************************')
        print (palette_scheme)
        print ('************************')
        img = Image(img_length)
        img.load_file(input_filename) \
        .apply_filter(QuantizeFilter(n)) \
        .apply_filter(ConstrainPaletteFilter(color_generator, palette_scheme)) \
        .apply_filter(BuildMapFilter(tile_size)) \
        .save_file(os.path.join(output_path , output_filename))
        img.generate_instructions(tile_size)


if __name__ == '__main__':
    main()
