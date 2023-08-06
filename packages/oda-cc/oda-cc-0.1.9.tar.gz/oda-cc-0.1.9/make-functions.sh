#!/bin/bash

# useful defaults
export ODA_SPARQL_ROOT=${ODA_SPARQL_ROOT:-https://www.astro.unige.ch/cdci/astrooda/dispatch-data/gw/odakb}
#export ODA_SPARQL_ROOT=${ODA_SPARQL_ROOT:-http://fuseki.internal.odahub.io/dataanalysis}

export PATH=$HOME/.local/bin:$PATH

export CC_JUPYTER_PORT=${CC_JUPYTER_PORT:-$(python -m odacc.cli -s find-free-port )}

pip install --upgrade pip

function get_pypi_version() {
    pkg_name=${1:?}

    curl -q -L  https://pypi.org/pypi/${pkg_name}/json | python -c 'import sys, json; print(json.load(sys.stdin)["info"]["version"])'
}

function ensure_latest_pypi() {
    pkg_name=${1:?}

    [ "$(get_pypi_version $pkg_name)" == $(python -c 'import pkg_resources; print(pkg_resources.require("nb2workflow")[0].version)' ) ] || pip install $pkg_name --upgrade
}

if [ -s oda.yaml ]; then
    export IN_TEST_CASE=yes
    echo -e "\033[32mfound test case oda.yaml\033[0m"
else
    export IN_TEST_CASE=no
    echo -e "\033[34mNOT found test case oda.yaml, no-test-case mode\033[0m"
fi

if [ ${DEBUG:-no} == "yes" ]; then
    set -x
fi


if [ ${ANNOTATE:-yes}  == "yes" ]; then
# need to unbuffer this
exec 2> >(awk '{print "\033[90m", strftime("%Y-%m-%dT%H:%M:%S"), "\033[31m", $0, "\033[0m"; fflush()}')
exec > >(awk '{print "\033[90m", strftime("%Y-%m-%dT%H:%M:%S"), "\033[0m", $0; fflush()}')
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo -e "\033[32mfound ci-template-cc location in $DIR\033[0m"

function upgrade-oda-python() {
    t0=$(date +%s)

    echo "will update osa python"
    PIP="python -m pip"
    echo "selected pip: $PIP"

    # because pip is just too slow
    if python -c '
import sys
import importlib as imp
if imp.util.find_spec("yaml") is None:
    sys.exit(1)
'; then
        echo -e '\033[32m yaml found\033[0m'
    else
        echo -e '\033[31m no yaml, will install\033[0m'
        $PIP install --upgrade pyyaml --user || pip install --upgrade pyyaml \
            || { echo -e "\033[31missue updating python module of pyyaml from $DIR!\033[0m"; exit 1; }
    fi

    if [ -s $DIR/setup.py ]; then
        echo -e "\033[32mfound $DIR/setup.py\033[0m"
        oda-cc version -c $DIR || {
            $PIP install --upgrade ${DIR} --user || pip install --upgrade ${DIR} \
                || { echo -e "\033[31missue updating python module for ci-tempalte-cc from $DIR!\033[0m"; exit 1; }
        }

        ensure_latest_pypi nb2workflow
    else
        echo -e "\033[34mNOTE: no python module in script directory - probably system-wide install, not verifying"
    fi

    NB2WORKFLOW_VERSION=$(nb2workflow-version)

    tdone=$(date +%s)
    echo -e "\033[31mspent $((tdone - t0)) seconds in upgrade-oda-python\033[0m"
}

if [ "$IN_TEST_CASE" == "yes" ]; then
    upgrade-oda-python

    if oda-cc get uri_base unset; then
        echo "found operable oda-cc from ci-template-cc"
    else
        echo -e "\033[31mNOT found operable oda-cc from ci-template-cc\033[0m"
        exit 1
    fi

    t0=$(date +%s)
    SOURCE_NAME=$( oda-cc get metadata.source_short_name unnamed )
    echo -e "\033[33mSOURCE_NAME: $SOURCE_NAME\033[0m"
    TEST_CASE_NAME=$( oda-cc get metadata.test_case_short_name unnamed )
    echo -e "\033[33mTEST_CASE_NAME: $TEST_CASE_NAME\033[0m"
    CC_BASE_IMAGE=$( oda-cc get cc_base_image integralsw/osa-python:11.1-3-g87cee807-20200410-144247-refcat-43.0-heasoft-6.27.2-python-3.8.2 )
    echo -e "\033[33mCC_BASE_IMAGE: $CC_BASE_IMAGE\033[0m"
    ROOT_NB=$( oda-cc get root_notebook verify.ipynb )
    echo -e "\033[33mROOT_NB: $ROOT_NB\033[0m"
    tdone=$(date +%s)
    echo -e "\033[31mspent $((tdone - t0)) seconds to set settings\033[0m"
fi


DOCKER_REGISTRY=faircrosscalibration
#DOCKER_REGISTRY=admin.reproducible.online


#mkfile_path = $(abspath $(lastword $(MAKEFILE_LIST)))
#current_dir = $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
#current_version := $(shell cd $(current_dir); git describe --tags)

    
IMAGE="$DOCKER_REGISTRY/cc-$TEST_CASE_NAME:$( git describe --always --tags)-$NB2WORKFLOW_VERSION"
IMAGE=$(echo $IMAGE | tr '[:upper:]' '[:lower:]')

SINGULARITY_IMAGE=${IMAGE//\//}

echo "req_nb2w: $REQ_NB2W"
echo "image: $IMAGE"

function pull() {
    echo $NB2WORKFLOW_VERSION
    docker pull $IMAGE || true
    touch job.cwl
}

function build() {
    [ -s pip.conf ] ||  touch pip.conf
    export DOCKER_BUILDKIT=1
    set -x
    #docker pull $IMAGE && 
    ( 
        nb2worker ./ --build \
            --tag-image $IMAGE \
            --job \
            --from ${CC_BASE_IMAGE:?} \
            --store-dockerfile /tmp/Dockerfile-auto \
            --docker-run-prefix="mkdir -pv /home/oda; export HOME_OVERRRIDE=/home/oda; source /init.sh; " \
            --docker-command='id; export HOME_OVERRRIDE=/tmp; mkdir -pv $HOME_OVERRRIDE; source /init.sh; source /etc/bashrc; oda-kb-eval /repo/'$ROOT_NB' "$@"' 
        ls -ltr *cwl
    )
    set +x
    touch job.cwl
}


function push() {
    docker push $IMAGE || true
}

function clean() {
    for nb in *ipynb; do 
            jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace $nb; 
        done
}

function rm() {
    docker rm -f $TEST_CASE_NAME || true
}


function ensure_minio() {
    if [ -z $MINIO_KEY ]; then
        echo -e "\033[31mWARNING, MINIO_KEY not set\033[0m"
        if [ ${LOCAL_ONLY:-no} == "yes" ]; then
            echo -e "\033[33mWARNING, LOCAL_ONLY=\"${LOCAL_ONLY}\", so MINIO_KEY not set is allowed\033[0m"
        else
            echo -e "\033[31mERROR, LOCAL_ONLY=\"${LOCAL_ONLY}\" not \"yes\", but MINIO_KEY not set - exiting\033[0m"
            exit 1
        fi
    fi
}

docker_shared_args="--rm \
            -e CI_JOB_TOKEN \
            -e MINIO_URL \
            -e MINIO_SECURE \
            -e MINIO_KEY \
            -e MINIO_USER=${MINIO_USER:-$USER} \
            -e JENA_PASSWORD \
            -e ODA_SPARQL_ROOT \
            -e ODA_TOKEN"

function run() {
  # this will listen with a notebook
  
    echo -e "\e[34mMounting\e[0m $PWD will be mounted in to use the code, and jupyter workdir "

    if [ ${MOUNT_SSH_FLAG:=no} == "yes" ]; then
        extra="-v /${HOME:?HOME variable is not set?}/.ssh:/home/oda/.ssh:ro"
        echo -e "\033[32mYES mounting ssh keys\033[0m: will rely on ssh when possible"
    else
        echo -e "\033[31mNOT mounting ssh keys\033[0m: will rely on https, please be sure sources are synchronous"
    fi


    docker rm -f $TEST_CASE_NAME || true

    copy-user-id

    echo -e "\033[31mODA_SPARQL_ROOT\033[0m=\033[32m${ODA_SPARQL_ROOT}\033[0m"

    mkdir -pv /tmp/tmpcode-$TEST_CASE_NAME; \
        docker run \
                $docker_shared_args \
                -p $CC_JUPYTER_PORT:$CC_JUPYTER_PORT \
                -v $PWD/passwd.new:/etc/passwd \
                -v $PWD:/repo \
                -v $PWD:/home/jovyan \
                -v $PWD:/home/integral \
                -it \
                --user $(id -u) \
                --name $TEST_CASE_NAME \
                --entrypoint bash \
                $IMAGE \
                $extra \
                -c "
                    export HOME_OVERRRIDE=/home/jovyan
                    export HOME=/home/jovyan
                    source /init.sh
                    echo $MINIO_KEY > /tmp/home-run/.minio-key
                    chmod 400 /tmp/home-run/.minio-key
                    cd /repo
                    jupyter notebook --ip=0.0.0.0 --no-browser --port=$CC_JUPYTER_PORT"
}
        
function copy-user-id() {
	# in case you do not know, there are no passwords in /etc/passwd
	docker run --entrypoint cat $IMAGE  /etc/passwd > passwd
		< passwd sed 's/1000/'$(id -u)'/' > passwd.new
        [ -s passwd.new ] || exit 1
}


# TODO: this logic should be within oda eval 
function run-one() {
	set -e
	NBARGS_YAML=${1:-}

	if [ "$NBARGS_YAML" == "" ]; then
	    echo "NBARGS_YAML empty: will use variable"
	else
	    echo "NBARGS_YAML NOT empty"
	    export NBARGS_PYDICT="$(python -c 'import yaml; print(yaml.load(open("'$NBARGS_YAML'"), Loader=yaml.SafeLoader))')"
	fi
	set +e

        provided_pars_suffix=$(oda-cc format -e NBARGS_PYDICT AUTO)

	echo -e "\033[32m will run-one in ${RUN_ONE_INDIR:=$PWD}\033[0m"
	mkdir -pv $RUN_ONE_INDIR
	cp -fv oda.yaml *.ipynb $RUN_ONE_INDIR
	cd $RUN_ONE_INDIR

        cname=cc-ci-run-$TEST_CASE_NAME-$provided_pars_suffix
        ensure_minio

        if [ ${MOUNT_SSH_FLAG:=no} == "yes" ]; then
            extra="-v /${HOME:?HOME variable is not set?}/.ssh:/home/oda/.ssh:ro"
            echo -e "\033[32mYES mounting ssh keys\033[0m: will rely on ssh when possible"
        else
            echo -e "\033[31mNOT mounting ssh keys\033[0m: will rely on https, please be sure sources are synchronous"
        fi

        echo -e "\033[33mnotebooks to run set by NB2RUN (defaults to root notebook $ROOT_NB) ${NB2RUN:=$ROOT_NB}\033[0m"
        export NB2RUN

        docker rm -f $cname || echo "can not remove $cname - this is ok"
    
        copy-user-id

        echo "ODA_TOKEN length: "$(echo $ODA_TOKEN | wc -c)

        docker run \
            $docker_shared_args \
            -e NBARGS_PYDICT \
            $extra \
                --entrypoint  bash $IMAGE \
                -c '''
                      export PYTHONUNBUFFERED=1

                      mkdir -pv /tmp/output

                      mkdir -pv /tmp/home-run
                      chmod 700 /tmp/home-run
                      export HOME_OVERRRIDE=/tmp/home-run
                      
                      source /init.sh

                      if [ "'$MOUNT_SSH_FLAG'" == "yes" ]; then
                          if git clone git@gitlab.astro.unige.ch:integral/cc-workflows/cc-isgri-oda-nustar-reference.git /tmp/test-clone; then
                              echo -e "\033[32mSUCCESS\033[0mfully cloned private repo from gitlab";
                          else
                              echo -e "\033[31mFAILED033[0m to cloned private repo from gitlab";
                              echo "make sure that your home contains ssh keys"
                              exit 1
                          fi
                      else
                          echo "skipping ssh check: ssh will not be used"
                      fi

                      git clone /repo /tmp/home-run/repo
                      cd /tmp/home-run/repo
		      git remote set-url origin $(cd /repo; git remote -v | awk "{print \$2}" | head -1)

                      echo "${NBARGS_PYDICT:-{\}}" > nbargs.py
                      cat nbargs.py


                      nb="'$NB2RUN'"
                      set -ex
                      nbinspect $nb > args_default.json
                      python -c "import oda, yaml, ast, json;\
                                 md, d = oda.evaluate(
                                         \"kb\", 
                                         yaml.safe_load(open(\"oda.yaml\"))[\"uri_base\"], 
                                         nbname=\""${nb//.ipynb/}"\", 
                                         **ast.literal_eval(open(\"nbargs.py\").read()) or {k: v[\"value\"] for k, v in json.load(open(\"args_default.json\")).items()}, 
                                         _write_files=True,
                                         _return_metadata=True,
                                     );\
                                 json.dump(d, open(\"cwl.output.json\", \"w\"));\
                                 json.dump(md, open(\"metadata.json\", \"w\"))
                                 " 2>&1  #| cut -c1-400 | tee ${nb//.ipynb/_output.log}  
                      ls -l cwl.output.json
                      cp -fv cwl.output.json "${nb//.ipynb/_output.json}"
                      set +ex

                      ls -ltor

                      for jf in *json; do
                         filesize=$(stat -c%s "$jf")
                    
                         if (( filesize > 50001000 )); then
                             rm -fv $jf
                         fi
                      done

                      for outnb in *ipynb; do
                         nbreduce $outnb 3
                      done

                      cp *_output.* *.json /tmp/output
                      ls -ltor /tmp/output

                ''' || { echo -e "\033[31m workflow failed!\033[0m"; exit 1; }

        docker cp $cname:/tmp/output .
        docker rm -f $cname

        ls -ltr output
        cat output/metadata.json

        f=$NB2RUN

        fb=${f//.ipynb}

        nbinspect ${fb}.ipynb  > pars_default.json

        cat pars_default.json | awk '{print "pars_default.json>> ", $0}'

        echo "${NBARGS_PYDICT:-{\}}" > nbargs.py
        python -c 'import ast, json;\
                   json.dump(
                    { **json.load(open("pars_default.json")), 
                      **{ k: {"value": v} for
                          k, v in ast.literal_eval(open("nbargs.py").read()).items()} }, 
                    open("pars.json", "w")
                   )'

        echo -e "\033[33mpars.json:\033[0m"
        cat pars.json

        if [ "$fb" == ${ROOT_NB//.ipynb} ]; then
            nb_suffix=""
        else
            nb_suffix="-$fb"
        fi
        
        pars_suffix=$(oda-cc format '{pars[subcases_pattern][value]}_{pars[reference_instrument][value]}_{pars[nscw][value]}scw_sf{pars[systematic_fraction][value]}_{pars[osa_version][value]}')
        these_outputs=outputs$nb_suffix/$pars_suffix

        mkdir -pv $these_outputs
        mv -fv output/* $these_outputs
        cp -fv pars.json $these_outputs
}

function build-singularity() {
#       singularity -vvv create $(SINGULARITY_IMAGE) || true
        #docker save $(IMAGE_NAME) | singularity -vvv import $(SINGULARITY_IMAGE)

    docker run -v /var/run/docker.sock:/var/run/docker.sock -v /dev/shm/singularity/:/output --privileged -t --rm quay.io/singularity/docker2singularity $IMAGE
    mkdir -pv /data/singularity/$TEST_CASE_NAME
    mv -fv /dev/shm/singularity/* /data/singularity/$TEST_CASE_NAME/${SINGULARITY_IMAGE}
}

#run-cwl:
#    ls 
#    cwltool job.cwl --subcases_pattern="_1" --source_name="Her X-1" --osa_version='OSA11.0' --nscw=10 --ng_sig_limit=2. --systematic_fraction=0.01

function make-args() {
        icversion=${1:?}
	for c in $(ls subcases/); do 
		echo $c
		python -c 'import yaml; open("args/args-'$c'.yaml", "w").write(yaml.dump({"subcases_pattern": "'$c'", "systematic_fraction": 0.01, "osa_version": "OSA11.0-'${icversion}'", "nscw": 50}))'; 
	done
}

function submit-all-scw() {
    icversion=${1:?}   
    nscwmax=${2:-5000}

    oda-node version  || { # -v!!!
        echo -e "\033[31mfailed to connect to ODAHUB\033[0m"
        exit 1
    }

    for scw in $(cat */subcases/*/*scw*txt subcases/*/*scw*txt | shuf |  awk '/^[0-9]{12}$/' | head -n$nscwmax) ; do 
        echo $scw
        
        oda-node ask \
            ii_skyimage \
                -m git://ddosa/staging-1-3 \
                -m git://findic/staging-1-3-icversion \
                -m git://ddosa11/staging-1-3 \
                -m git://useresponse/staging-1-3-osa11 \
                -a 'ddosa.ScWData(input_scwid="'$scw'.001"),ddosa.ImagingConfig(use_SouFit=0,use_DoPart2=1,use_version="soufit0_p2"),ddosa.CatForSpectraFromImaging(use_minsig='${minsig:-5}')' \
                -a 'ddosa.ICRoot(use_ic_root_version="'$icversion'")'
        oda-node ask \
            ii_spectra_extract \
                -m git://ddosa/staging-1-3 \
                -m git://findic/staging-1-3-icversion \
                -m git://ddosa11/staging-1-3 \
                -m git://useresponse/staging-1-3-osa11 \
                -a 'ddosa.ScWData(input_scwid="'$scw'.001"),ddosa.ImagingConfig(use_SouFit=0,use_DoPart2=1,use_version="soufit0_p2"),ddosa.CatForSpectraFromImaging(use_minsig='${minsig:-5}')' \
                -a 'ddosa.ICRoot(use_ic_root_version="'$icversion'")'
                #-a 'useresponse.CompressEBins(use_factor=4)' \
    done
}

function submit-all-cases() {
    icversion=${1:?icversion}   
    nmax=${2:?nmax}

    oda-node version -v || {
        echo -e "\033[31mfailed to connect to ODAHUB\033[0m"
        exit 1
    }

    for subcase in $(ls subcases/ | shuf -n $nmax) ; do 
        echo $subcase

        scws=$(cat subcases/$subcase/*scw*txt | awk '{printf $1".001,"}')
        
        oda-node ask \
            ISGRISpectraSum \
                -m git://ddosa/staging-1-3 \
                -m git://findic/staging-1-3-icversion \
                -m git://ddosa11/staging-1-3 \
                -m git://useresponse/staging-1-3-osa11 \
                -m git://process_isgri_spectra/staging-1-3-osa11 \
                -a 'process_isgri_spectra.ISGRISpectraSum(use_extract_all=True)' \
                -a 'ddosa.IDScWList(use_scwid_list="'$scws'".strip(",").split(","))' \
                -a 'process_isgri_spectra.ScWSpectraList(input_scwlist=ddosa.IDScWList)' \
                -a 'ddosa.ImagingConfig(use_SouFit=0,use_DoPart2=1,use_version="soufit0_p2"),ddosa.CatForSpectraFromImaging(use_minsig='${minsig:-5}')' \
                -a 'ddosa.ICRoot(use_ic_root_version="'$icversion'")'
                #-a 'useresponse.CompressEBins(use_factor=4)' \
    done
}

function configure-reana() {
    reana-client secrets-add --env MINIO_KEY=${MINIO_KEY:?this should be set} --overwrite
    reana-client secrets-add --env MINIO_URL=${MINIO_URL:?this should be set} --overwrite
    reana-client secrets-add --env MINIO_SECURE=${MINIO_SECURE:?this should be set} --overwrite
    reana-client secrets-add --env MINIO_USER=${MINIO_USER:-USER} --overwrite
    reana-client secrets-add --env ODA_TOKEN=${ODA_TOKEN:?} --overwrite
    reana-client secrets-list
}

function download-cwl() {
    set -e
    echo -e "\033[33mwill download"
    curl -L --header "PRIVATE-TOKEN: $(cat ~/.gitlab-token)" \
         "https://gitlab.astro.unige.ch/api/v4/projects/integral%2Fcc-workflows%2Fcc-${TEST_CASE_NAME}/jobs/artifacts/master/download?job=build"  > artifacts.gz
    cwl=${ROOT_NB//.ipynb/.cwl}
    unzip -o artifacts.gz $cwl
    cp -fv $cwl job.cwl
    echo -e "\033[32mfound job.cwl:"
    ls -l job.cwl

    < job.cwl awk '/fair/ || /ipyn/ {print "job.cwl >> ", $0}'

    set +e
}

function run-reana() {
      inputs=${1:?}
      cwl=${2:?}

      if [ "$cwl" == "download" ]; then
          download-cwl
          cwl=job.cwl
      fi

      echo "
version: 0.3.0
inputs:
  parameters:
    input: inputs.yaml
workflow:
  type: cwl
  file: ${cwl}
outputs:
  files:
   - cwl/docker_outdir/cwl.output.json
" > reana.yaml

      cp -v $inputs inputs.yaml

      name=$( oda-cc get metadata.source_short_name unnamed )
      reana-client   create  -f reana.yaml --name $name
      reana-client   start --workflow $name
}

function update-fixed-ci-version() {
    sed -i 's@raw/.*/@raw/'$(cd ci-template-cc/; git describe --always)'/@g' .gitlab-ci.yml
}

function reana-clear-all() {
    echo
#    $ kubectl exec -i -t deployment/reana-db -- psql -U reana
#    psql> SET search_path to __reana, public; 
#    psql> UPDATE workflow SET status='stopped' WHERE name='myanalysis' AND status='running';
#    psql> \q

#    If you need just some run numbers, you can add ... AND run_number=... to the SQL query.

#    After flipping the regular reana-client delete command will work:

#    $ reana-client delete -w myanalysis --include-all-runs --include-workspace --include-records
}

function seq-run-all() {
    v=${1:?}
    #make-args dev210827.0528-37487--fullbkg--rmfoffsetv1
    make-args $v
    make build
    for a in args/*; do 
        cc-cli run-one $a > log.$(basename $a) 2>&1; 
    done

    reindex-all
}


function reindex-all() {
    for bucket in $(for l in log.*; do < $l awk '/bucket name/ {print $NF}' | head -1; done | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g"); do
        echo
        oda-kb-datalake reindex --single-bucket $bucket
    done
}

$@


