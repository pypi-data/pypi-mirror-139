#SOURCE_NAME?=$(shell < oda.yaml yq -r '.metadata.source_short_name')
SOURCE_NAME?=$(shell python3 -c 'import yaml; print(yaml.safe_load(open("oda.yaml")).get("metadata",{}).get("source_short_name","unnamed"))')


mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
#current_version := $(shell cd $(current_dir); git describe --tags)

install: autocomplete.bash
	install -D -m 0755 -v make-functions.sh ${HOME}/.local/bin/cc-cli
	install -D -m 0755 -v autocomplete.bash ${HOME}/.bash_completion.d/cc-cli.bash
	install -D -m 0400 -v README.md ${HOME}/.local/share/doc/cc-cli.md
	< $(HOME)/.bash_completion grep cc-cli.bash || echo 'source $$HOME/.bash_completion.d/cc-cli.bash' >> $(HOME)/.bash_completion

autocomplete.bash:
	< autocomplete.bash.template  sed 's/%CLI_SCRIPT_NAME%/cc-cli/g' > autocomplete.bash

test:
	./actions.sh test-all

pull: 
	bash $(current_dir)/make-functions.sh $@

build: 
	bash $(current_dir)/make-functions.sh $@

push: build
	bash $(current_dir)/make-functions.sh $@

clean:
	bash $(current_dir)/make-functions.sh $@
	
rm:
	bash $(current_dir)/make-functions.sh $@

run:
	bash $(current_dir)/make-functions.sh $@

run-one: 
	bash $(current_dir)/make-functions.sh $@


run-cwl:
	ls 
	cwltool $(WORKFLOW).cwl 

run-reana:
	reana-client   -lDEBUG   create  -f reana.yaml --name $(WORKFLOW)
	reana-client   -lDEBUG   start --workflow $(WORKFLOW)

build-singularity:
	bash -c '. $(current_dir)/make-functions.sh && $@'

run-all:
	snakemake -j1 -p --snakefile ci-template-cc/Snakefile all

bootstrap-ci:
	wget https://gitlab.astro.unige.ch/integral/cc-workflows/cc-crab/-/raw/master/.gitlab-ci.yml
