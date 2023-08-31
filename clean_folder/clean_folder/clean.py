from pathlib import Path
import sys
import re
import shutil



images_list = []
documents_list = []
audio_list = []
video_list = []
archives_list = []
unknown_extension_files_list = []
known_extensions_list = []
unknown_extensions_list = []


extensions_dict = {
    'images': ['.jpeg', '.jpg', '.png', '.bmp', '.svg'],
    'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.xls', '.pptx'],
    'audio': ['.mp3', '.ogg', '.wav', '.amr'],
    'video': ['.mp4', '.avi', '.mov', '.mpg', '.mpeg', '.wmv', '.mkv'],
    'archives': ['.zip', '.gz', '.tar'],
    'unknown_extension_files': []
}


ignore_folders_list = [i for i in extensions_dict.keys()]


def normalize(file_name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}


    for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = t  # transliteration small symbols
        TRANS[ord(c.upper())] = t.upper()  # transliteration large symbols


    normalised_name = re.sub(r'\W', '_', file_name.translate(TRANS))  # file name translation and replacing all extra characters in the file name with "_" (excluding letters, numbers and "_")
    return normalised_name


def file_manager(item, new_folder_path):
    normalised_file_name = f'{normalize(item.stem)}{item.suffix}'  # normalise file name string
    new_file_path = item.rename(item.parent / normalised_file_name)  # rename file
    try:
        new_folder_path.mkdir(parents=True, exist_ok=False)  # create directory for files will be replaced
        new_file_path.replace(new_folder_path / new_file_path.name)  # replace file
    except FileExistsError:
        new_file_path.replace(new_folder_path / new_file_path.name)  # replace file if target directory is exists
    return normalised_file_name


def archive_manager(item, new_folder_path):
    normalised_archive_name = f'{normalize(item.stem)}{item.suffix}'  # normalize archive name
    try:
        new_folder_path.mkdir(parents=True, exist_ok=False)  # create 'archives' directory if it not already exists
        old_archive_new_path = item.replace(new_folder_path / item.name)  # path to old archive replaced in new folder
        new_name_archive_path = old_archive_new_path.rename(new_folder_path / normalised_archive_name)  # rename archive in new folder
        new_archive_path = new_folder_path / new_name_archive_path.stem  # new name archive path without extension
        new_archive_path.mkdir(parents=True, exist_ok=False)  # create directory to unpack archive
        shutil.unpack_archive(new_name_archive_path, new_archive_path)  # unpack archive
    except FileExistsError:
        old_archive_new_path = item.replace(new_folder_path / item.name)  # path to old archive replaced in new folder
        new_name_archive_path = old_archive_new_path.rename(new_folder_path / normalised_archive_name)  # rename archive in new folder
        new_archive_path = new_folder_path / new_name_archive_path.stem  # new name archive path without extension
        new_archive_path.mkdir(parents=True, exist_ok=False)  # create directory to unpack archive
        shutil.unpack_archive(new_name_archive_path, new_archive_path)  # unpack archive
    return normalised_archive_name


def extensions_append(extension):  # update known extensions list
    global known_extensions_list
    if extension not in known_extensions_list:
        known_extensions_list.append(extension)


def sort(folder):
    folder_path = Path(folder)
    path = Path(folder)
    for item in path.iterdir():
        if item.is_dir():
            if item.name in ignore_folders_list:  # ignore folders
                continue
            sort(item)
        elif item.suffix in extensions_dict['images']:  # file extension checking
            new_folder_path = folder_path / 'images'  # images folder path
            normalised_file_name = file_manager(item,
                                                new_folder_path)  # normalised and replaced file with new file name return
            global images_list
            images_list.append(normalised_file_name)  # update list of images
            extensions_append(item.suffix)  # update list of known extensions
        elif item.suffix in extensions_dict['documents']:  # file extension checking
            new_folder_path = folder_path / 'documents'  # documents folder path
            normalised_file_name = file_manager(item,
                                                new_folder_path)  # normalised and replaced file with new file name return
            global documents_list
            documents_list.append(normalised_file_name)  # update list of documents
            extensions_append(item.suffix)  # update list of known extensions
        elif item.suffix in extensions_dict['audio']:  # file extension checking
            new_folder_path = folder_path / 'audio'  # audio folder path
            normalised_file_name = file_manager(item,
                                                new_folder_path)  # normalised and replaced file with new file name return
            global audio_list
            audio_list.append(normalised_file_name)  # update list of audio files
            extensions_append(item.suffix)  # update list of known extensions
        elif item.suffix in extensions_dict['video']:  # file extension checking
            new_folder_path = folder_path / 'video'  # video folder path
            normalised_file_name = file_manager(item,
                                                new_folder_path)  # normalised and replaced file with new file name return
            global video_list
            video_list.append(normalised_file_name)  # update list of video files
            extensions_append(item.suffix)  # update list of known extensions
        elif item.suffix in extensions_dict['archives']:  # file extension checking
            new_folder_path = folder_path / 'archives'  # archives folder path
            normalised_archive_name = archive_manager(item,
                                                      new_folder_path)  # normalised and replaced file with new file name return
            global archives_list
            archives_list.append(normalised_archive_name)  # update archives list
            extensions_append(item.suffix)  # update list of known extensions
        else:
            new_folder_path = folder_path / 'unknown_extension_files'  # unknown extension files folder path
            try:
                new_folder_path.mkdir(parents=True, exist_ok=False)  # create unknown extension files folder
                item.replace(new_folder_path / item.name)  # replace unknown extension files
            except FileExistsError:
                item.replace(new_folder_path / item.name)  # replace unknown extension files
            global unknown_extension_files_list
            unknown_extension_files_list.append(item.name)  # update unknown extension files list
            global unknown_extensions_list
            unknown_extensions_list.append(item.suffix)  # update unknown extensions list


def sanitize_folder(path, ignore_folders_list):
    for item in path.iterdir():  # iteration on target path
        if item.is_dir():
            if item.name not in ignore_folders_list:  # ignore folders
                shutil.rmtree(item, ignore_errors=True)  # remove directory with all tree
                continue
        continue


def main():
    folder = sys.argv[1]
    folder_path = Path(folder)
    sort(folder)
    sanitize_folder(folder_path, ignore_folders_list)
    print(f'images:\n{images_list}\n')
    print(f'documents:\n{documents_list}\n')
    print(f'audio:\n{audio_list}\n')
    print(f'video:\n{video_list}\n')
    print(f'archives:\n{archives_list}\n')
    print(f'unknown_extension_files:\n{unknown_extension_files_list}\n')
    print(f'known_extensions:\n{known_extensions_list}\n')
    print(f'unknown_extensions:\n{unknown_extensions_list}\n')


if __name__ == '__main__':
    folder = sys.argv[1]
    folder_path = Path(folder)
    main()