import urllib.request, json
import os.path
import ssl
import shutil

IMAGE_URL = 'https://random.dog/woof.json'
IMAGE_FOLDER = './img'
NUMBER_OF_IMAGES = 10

fileSizes = []

def getImage():
    with urllib.request.urlopen(IMAGE_URL) as url:
        data = json.load(url)
        if not data['url'].endswith('.jpg'):
            print(f"Unsupported file format! - {data['url']}")
            getImage()
            return
        print(f"Downloading new photo: {data['url']}")
        urllib.request.urlretrieve(data['url'], os.path.join(IMAGE_FOLDER, data['url'].split('/')[-1]))
        fileSizes.append(data['fileSizeBytes'])

def printStatistics():
    print(f"Maximum image size: {sizeof_fmt(max(fileSizes))}")
    print(f"Minimum image size: {sizeof_fmt(min(fileSizes))}")
    print(f"Average image size: {sizeof_fmt(sum(fileSizes) / len(fileSizes))}")

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def main():
    ssl._create_default_https_context = ssl._create_unverified_context

    if os.path.exists(IMAGE_FOLDER):
        shutil.rmtree(IMAGE_FOLDER)
    os.mkdir(IMAGE_FOLDER)

    for i in range(0, NUMBER_OF_IMAGES):
        getImage()

    printStatistics()

if __name__ == '__main__':
    main()