makefile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
dir_path := $(dir $(makefile_path))
current_dir := $(notdir $(patsubst %/,%,$(dir_path)))

default: decktape

all: decktape

decktape: talk.md
	docker run --rm -v ${dir_path}:/slides/ astefanutti/decktape \
	https://matthewfeickert.github.io/${current_dir}/index.html?p=talk.md \
	talk.pdf
