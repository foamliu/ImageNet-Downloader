import os


if __name__ == '__main__':
    files = [f for f in os.listdir('image/original') if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.tiff'))]
    print('{} files downloaded'.format(len(files)))

    files = [f for f in os.listdir('image/resized') if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    print('{} files resized'.format(len(files)))
