#!/bin/bash

set -o nounset
set -o pipefail
set -o xtrace
set -o errexit

FOO=${FOOBAR:-""}
echo ${FOO}
ret=0
if [[ -z "${FOO}" ]]; then
    echo "FOO is dead, baby, FOO is dead"
fi

#echo $FOO  # This fails due to nounset
#ls -1 | foobar | head -1  # This fails if pipefail is set
echo "DONE"

