import io
import os


def write_bytesio_to_file(filename, bytesio):
    """Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet. 
    
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())
            

def write_zipped_fits_file(filename, product):
    """Compress a .fits file as .fits.gz for a data product.
   
    """
    with io.BytesIO() as buf:
        buf.write(product)
        buf.seek(0)
        if not os.path.isfile(filename):
            write_bytesio_to_file(filename, buf)
            os.system(f'gzip {filename}')


def write_products(products, prefix):
    write_zipped_fits_file('%s_cube.fits' % (prefix), products.cube)
    write_zipped_fits_file('%s_chan.fits' % (prefix), products.chan)
    write_zipped_fits_file('%s_mask.fits' % (prefix), products.mask)
    write_zipped_fits_file('%s_mom0.fits' % (prefix), products.mom0)
    write_zipped_fits_file('%s_mom1.fits' % (prefix), products.mom1)
    write_zipped_fits_file('%s_mom2.fits' % (prefix), products.mom2)

    # Open spectrum
    with io.BytesIO() as buf:
        buf.write(b''.join(products.spec))
        buf.seek(0)
        spec_file  = '%s_spec.txt' % (prefix)
        if not os.path.isfile(spec_file):
            write_bytesio_to_file(spec_file, buf)
