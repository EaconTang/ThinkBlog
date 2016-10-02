import os

from django.conf import settings

from blog.models import ImageFile

STATIC_ROOT = getattr(settings, 'STATIC_ROOT')


def main():
    images = ImageFile.objects.all().exclude(is_exported=True)
    for img in images:
        image_full_path = os.path.join(STATIC_ROOT, 'image', img.image_name)
        image_dir = os.path.dirname(image_full_path)
        if not os.path.exists(image_dir):
            mkdir_recursively(image_dir)
        with open(image_full_path, 'wb+') as f:
            f.write(img.image_file.read())
        img.is_exported = True
        img.save()


def mkdir_recursively(dir_path):
    while True:
        try:
            os.mkdir(dir_path)
        except OSError:
            parent_dir = os.path.dirname(dir_path)
            if mkdir_recursively(parent_dir):
                continue
        else:
            break
    return True


if __name__ == '__main__':
    # main()
    mkdir_recursively('/Users/eacon/Study/_Python/MyBlog/static/test1/jimi/jimi1/jimi2/jimi3')
