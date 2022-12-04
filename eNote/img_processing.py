from PIL import Image, ExifTags
import pillow_heif
from os.path import join
from os import remove
from flask import current_app as app
from secrets import token_urlsafe

def make_square(filename):
    file_ext = filename.rsplit('.', 1)[1].lower()
    new_name = token_urlsafe(16)
    thumb, full = 't_' + new_name + '.', new_name + '.'
    if file_ext == 'heic':
        pillow_heif.register_heif_opener()
    if file_ext == 'avif':
        pillow_heif.register_avif_opener()
    with Image.open(join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')) as im:
        try:
            if hasattr(im, '_getexif'):
                for orientation in ExifTags.TAGS.keys(): 
                    if ExifTags.TAGS[orientation]=='Orientation':
                        break 
                e = im._getexif()
                if e is not None:
                    exif=dict(e.items())
                    orientation = exif[orientation] 

                    if orientation == 3:   im = im.transpose(Image.ROTATE_180)
                    elif orientation == 6: im = im.transpose(Image.ROTATE_270)
                    elif orientation == 8: im = im.transpose(Image.ROTATE_90)

        except:
            print('Exif error occured')
        width, height = im.size
        if width > height:
            cut_off = width - height
            if cut_off % 2:
                cut_off += 1
            (left, upper, right, lower) = (cut_off//2, 0, width-cut_off//2, height)
            im = im.crop((left, upper, right, lower))
        elif height > width:
            cut_off = height - width
            if cut_off % 2:
                cut_off += 1
            (left, upper, right, lower) = (0, cut_off//2, width, height-cut_off//2)
            im = im.crop((left, upper, right, lower))
        width, height = im.size
        if file_ext in ('jpg', 'jpeg', 'webp', 'heic', 'avif'):
            full_width = 2048 if width > 2048 else width
        elif file_ext == 'png':
            full_width = 1024 if width > 1024 else width
        thumb_width = 512
        hsize_full = int((height*(full_width/width)))
        img_full = im.resize((full_width, hsize_full), Image.Resampling.LANCZOS)

        hsize_thumb = int((height*(thumb_width/width)))
        img_thumb = im.resize((thumb_width, hsize_thumb), Image.Resampling.LANCZOS)
        if file_ext == 'png':
            full += 'png'
            thumb += 'png'
            img_full.save(join(app.config['PROFILE_IMG_FOLDER'], full).replace('\\', '/'), optimize=True)
            img_thumb.save(join(app.config['PROFILE_IMG_FOLDER'], thumb).replace('\\', '/'), optimize=True)
        elif file_ext in ('jpg', 'jpeg', 'webp', 'heic', 'avif'):
            full += 'webp'
            thumb += 'webp'
            img_full.save(join(app.config['PROFILE_IMG_FOLDER'], full).replace('\\', '/'), quality=80)
            img_thumb.save(join(app.config['PROFILE_IMG_FOLDER'], thumb).replace('\\', '/'), quality=90)

        remove(join(app.config['UPLOAD_FOLDER'], filename))
        return full