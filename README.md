# Usage

Drag & drop the directory, containing your video files, to the file `videoserver.cmd`. A window should open that shows you which address (usually [http://127.0.0.1:3030](http://127.0.0.1:3030) on your local machine) you shall type in your browser address bar. Take care that the tool needs to pass your firewall.

# Prerequisites

Python 3.5 or higher is needed

The Python library "Flask" is needed. Execute this command to install it:

```
pip install -r requirements.txt
```

It is assumed that the tool `ffmpeg` and `ffprobe` are in the system path. Look at the [FFmpeg website](https://ffmpeg.org/) for downloads.