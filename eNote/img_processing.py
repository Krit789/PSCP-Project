from PIL import Image
from os.path import join
from os import remove
from flask import current_app as app
from secrets import token_urlsafe


def make_square(filename):
    file_ext = filename.rsplit('.', 1)[1].lower()
    new_name = token_urlsafe(16)
    thumb, full = 't_' + new_name + '.', new_name + '.'
    with Image.open(join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')) as im:
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
        full_width = 1024 if width > 1024 else width
        thumb_width = 256

        hsize_full = int((height*(full_width/width)))
        img_full = im.resize((full_width, hsize_full), Image.Resampling.LANCZOS)

        hsize_thumb = int((height*(thumb_width/width)))
        img_thumb = im.resize((thumb_width, hsize_thumb), Image.Resampling.LANCZOS)
        if file_ext == 'png':
            full += 'png'
            thumb += 'png'
            img_full.save(join(app.config['PROFILE_IMG_FOLDER'], full).replace('\\', '/'), optimize=True)
            img_thumb.save(join(app.config['PROFILE_IMG_FOLDER'], thumb).replace('\\', '/'), optimize=True)
        elif file_ext in ('jpg', 'jpeg'):
            full += 'jpg'
            thumb += 'jpg'
            img_full.save(join(app.config['PROFILE_IMG_FOLDER'], full).replace('\\', '/'), optimize=True, progressive=True, quality=90)
            img_thumb.save(join(app.config['PROFILE_IMG_FOLDER'], thumb).replace('\\', '/'), optimize=True, progressive=True, quality=90)

        remove(join(app.config['UPLOAD_FOLDER'], filename))
        return full