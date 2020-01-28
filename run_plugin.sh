docker pull supervisely/dtl:latest
nvidia-docker run \
    --rm \
    -ti \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ~/.Xauthority:/root/.Xauthority \
    --entrypoint="" \
    --shm-size='1G' \
    -e PYTHONUNBUFFERED='1' \
    -v ${PWD}:/workdir \
    -v ${PWD}/../../supervisely_lib:/workdir/supervisely_lib \
    -v /home/andrew/Desktop/task_data_dtl_example:/sly_task_data \
    -v /opt/pycharm:/pycharm \
    -v /home/andrew/pycharm-settings/dtl_plugin:/root/.PyCharmCE2018.2 \
    -v /home/andrew/pycharm-settings/dtl_plugin__idea:/workdir/.idea \
    supervisely/dtl:latest \
    bash