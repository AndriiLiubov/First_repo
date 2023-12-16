import sys
from pathlib import Path


images = list()   #('JPEG', 'PNG', 'JPG', 'SVG');
video = list()    #('AVI', 'MP4', 'MOV', 'MKV');
documents = list()     #('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
audio = list()    #('MP3', 'OGG', 'WAV', 'AMR');
archives = list() #('ZIP', 'GZ', 'TAR');
others = list()
folders = list()
unknown = set()
extensions = set()

registered_extensions = {
    'images': images,
    'video': video,
    'documents': documents,
    'audio': audio,
    'archives': archives,
    'others': others
}

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('images', 'video', 'documents', 'audio', 'archives', 'others'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            if extension in ['JPEG', 'PNG', 'JPG', 'SVG']:
                    new_extension = 'images'
                    container = registered_extensions[new_extension]
                    extensions.add(extension)
                    container.append(new_name)
            if extension in ['AVI', 'MP4', 'MOV', 'MKV']:
                    new_extension = 'video'
                    container = registered_extensions[new_extension]
                    extensions.add(extension)
                    container.append(new_name)
            if extension in ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']:
                    new_extension = 'documents'
                    container = registered_extensions[new_extension]
                    extensions.add(extension)
                    container.append(new_name)
            if extension in ['MP3', 'OGG', 'WAV', 'AMR']:
                    new_extension = 'audio'
                    container = registered_extensions[new_extension]
                    extensions.add(extension)
                    container.append(new_name)
            if extension in ['ZIP', 'GZ', 'TAR']:
                    new_extension = 'archives'
                    container = registered_extensions[new_extension]
                    extensions.add(extension)
                    container.append(new_name)
            if extension not in ['JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV', 'MKV', 'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'MP3', 'OGG', 'WAV', 'AMR', 'ZIP', 'GZ', 'TAR']:
                unknown.add(extension)
                others.append(new_name)

if __name__ == '__main__':
    path = sys.argv[1]

    folder = Path(path)
    
    scan(folder)
    
    
    print(f"images: {images}")
    print(f"video: {video}")
    print(f"documents: {documents}")
    print(f"audio: {audio}")
    print(f"archives: {archives}")
    print(f"others: {others}")
    
    print(f"All extensions: {extensions}")
    print(f"Unknown extensions: {unknown}")
    