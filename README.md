# YT AUDIO DOWNLOADER

This work is a simple **Youtube Audio Downloader** written in Python, exploiting `ffmpeg` and turned into an .EXE by using the PyInstaller tool.

## **Requirements**

First of all, to luch the [YT AUDIO DOWNLOADER.exe](https://github.com/francecon/YT-AUDIO-DOWNLOADER/blob/main/YT%20AUDIO%20DOWNLOADER.exe) it is required having `ffmpeg.exe`on your pc.

To get it, just download the file`ffmpeg-git-essentials.7z`from [this link](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z), extract it and move the extracted folder in `Local Disk (C:)`. This moves the folder to the root of your hard drive.

Note: `ffmpeg`is a command line tool, therefore on Windows it is required to add the folder containing the `ffmpeg.exe` file to the PATH Environmental Variables of Windows 10. This is automatically done by the python file.

If you want to run the main python file [yt_downloader_with_GUI.py](https://github.com/francecon/YT-AUDIO-DOWNLOADER/blob/main/yt_downloader_with_GUI.py), you will need to install modules listed into [requirements.txt](https://github.com/francecon/YT-AUDIO-DOWNLOADER/blob/main/requirements.txt).

If you have `pip` installed, just type this in a terminal:

```shell
pip install -r requirements.txt
```

### Built With

* [PyInstaller](https://www.pyinstaller.org/)
* [Python3](https://www.python.org/download/releases/3.0/)
* [ffmpeg](https://ffmpeg.org/)

### Developer

(c) 2021, [Francesco Conforte](https://github.com/francecon/).
