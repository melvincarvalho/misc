#!/bin/bash

set -o nounset
set -o pipefail
set -o xtrace
set -o errexit

#echo $FOO  # This fails due to nounset
#ls -1 | foobar | head -1  # This fails if pipefail is set
echo "DONE"

