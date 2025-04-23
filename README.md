# ComfyUI Psutil Container Memory Patch

## Overview

When comfyui run in container, if the container is set with a memory limit, psutil cannot correctly read the available memory and maximum memory. It only reads the memory size of the host machine, which will cause some tasks to oom. This extension detects when comfyui is running in a container, reads the memory limit of the container, and uses the monkey patch method to replace some values ​​returned by `psutil.virtual_memory`, such as `total` `used` `available` `percent`.

``` bash
# Run ComfyUI in container with 10GB memory limit

# Before installing node, console displays:
python /root/ComfyUI/main.py

	ComfyUI starting ..
	Total VRAM 24210 MB, total RAM 102400 MB

# After installing node, console displays: 
python /root/ComfyUI/main.py

	ComfyUI starting ..
	Total VRAM 24210 MB, total RAM 10240 MB
```


## Quickstart

1. Install [ComfyUI](https://docs.comfy.org/get_started).
1. Install [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)
1. Look up `comfyui-psutil-container-memory-patch` in ComfyUI-Manager. If you are installing manually, clone this repository under `ComfyUI/custom_nodes`.
1. Restart ComfyUI.

# Features

- Make comfyui  and other custom node get correct memory information in the container (psutil monkey path)



## See Also 
* https://fabiokung.com/2014/03/13/memory-inside-linux-containers/
*  [psutil reports memory stats about host instead of container sutil#2100](https://github.com/giampaolo/psutil/issues/2100)