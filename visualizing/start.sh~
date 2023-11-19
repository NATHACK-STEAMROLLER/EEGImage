#!/bin/bash

osascript -e 'tell app "Terminal"
	do script "conda activate muse_env; muselsl stream"
end tell'

osascript -e 'tell app "Terminal"
	do script "conda activate muse_env; sleep 15; cd ; python ~/EEGImage/visualizing/neurofeedback.py; python draw.py"
end tell'
