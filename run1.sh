docker run --rm -it \
			--net=host \
			-v `pwd`/../src:/src_test \
			--entrypoint="" \
			-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v ~/.Xauthority:/root/.Xauthority \
			-v `pwd`/../../../../opt/pycharm:/pycharm \
    		-v `pwd`/../../../../andrew/pycharm-settings/smtool_gui:/root/.PyCharmCE2018.2 \
    		-v `pwd`/../../../../andrew/pycharm-settings/smtool_gui__idea:/workdir/.idea \
			magic_stick bash

