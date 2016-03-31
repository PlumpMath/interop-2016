#!/usr/bin/env bash


for file in $(find . -name "*.yml")
do
    yamllint $file
    rc=$?
    if [ "$rc" -ne 0 ] ; then
        exit $rc
    fi
done

echo "Linting Passed"

exit 0