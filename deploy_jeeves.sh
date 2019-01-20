#!/usr/bin/env bash

scp jeeves.py pi@192.168.2.44:~/jeeves/
echo "deployed jeeves"

scp camera.py pi@192.168.2.44:~/jeeves/
echo "deployed camera"

scp start_jeeves.py pi@192.168.2.44:~/jeeves/
echo "deployed start_jeeves"

scp stop_jeeves.py pi@192.168.2.44:~/jeeves/
echo "deployed stop_jeeves"

echo "done"