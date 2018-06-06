import os


if __name__ == '__main__':
    files = [f for f in os.listdir('image/original') if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    print('{} files downloaded'.format(len(files)))
