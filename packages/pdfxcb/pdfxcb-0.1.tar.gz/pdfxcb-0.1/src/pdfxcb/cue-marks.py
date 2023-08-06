# return array of means for upper-right-hand corner
def urh_corner_mean (pil_image):
    (width,height) = pil_image.size
    # current application is to detect black cue mark in URH corner (tt-cover-sheets) indicating a sheet w/a barcode -->> grab upper RH corner 20-pixel square
    im_crop = pil_image.crop([
        width - 20, #left
        1, #upper,
        width - 1, #right,
        20 #lower
    ])
    im_crop_stat = ImageStat.Stat(im_crop)
    return im_crop_stat.mean

def scan_for_cue_marks (png_specs):
    indices = []
    # FIXME: want a png_specs_index here...
    spec_index = 0
    while spec_index < png_specs.length:
        spec = png_specs[spec_index]
        # from PIL import Image
        im = Image.open(spec[0])
        if (urh_corner_mean(im) < 40):
            indices.append(spec_index)
        spec_index = spec_index + 1
    return indices
