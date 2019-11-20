docker run --rm -it \
			--net=host \
			-v `pwd`/../src_progect:/src_progect \
			--entrypoint="" \
			-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v ~/.Xauthority:/root/.Xauthority \
			-v /opt/pycharm:/pycharm \
    		-v /home/andrew/pycharm-settings/smtool_gui:/root/.PyCharmCE2018.2 \
    		-v /home/andrew/pycharm-settings/smtool_gui__idea:/workdir/.idea \
			segment_annotator bash

