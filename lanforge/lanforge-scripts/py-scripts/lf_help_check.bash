#!/bin/bash

FILES=`ls *.py`
for FILE in $FILES
do
	echo $FILE
	(timeout 10 python3 ./${FILE} --help > /dev/null  && echo PASSED) || echo "ERROR: FAILED ${FILE}"
done
