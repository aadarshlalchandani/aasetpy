#!/bin/bash

## credits: aadarshlalchandani/aasetpy

start_time=$(date +%s)

## activate the virtual environment
. env/bin/activate

PROGRAM=$1
TEST_ARG=pytest
LINT_ARG=pylint
PROGRAM_ARG=$2
logs_dirname=logs
logs="$logs_dirname"/"$PROGRAM"_logs.log
: >$logs
line="\n\n"
current_date_time=$(date "+%Y-%m-%d %H:%M:%S")

echo "Started..."
echo "Storing real-time logs in "$logs""
echo "[ $current_date_time ] PROGRAM: $PROGRAM $PROGRAM_ARG"
echo "[ $current_date_time ] PROGRAM: $PROGRAM $PROGRAM_ARG" >>$logs 2>&1
if [ $PROGRAM = $TEST_ARG ]; then
    coverage run -m $PROGRAM $PROGRAM_ARG >>$logs 2>&1
    coverage html -d pytest_report
elif [ $PROGRAM = $LINT_ARG ]; then
    $PROGRAM $PROGRAM_ARG >>$logs 2>&1
else
    python -u $PROGRAM.py $PROGRAM_ARG >>$logs 2>&1
fi

end_time=$(date +%s)
total_time=$(($end_time - $start_time))

echo -en "\nTotal Time taken: $total_time seconds\n" >>$logs 2>&1
echo "[ $current_date_time ] $PROGRAM $PROGRAM_ARG1 $PROGRAM_ARG2: Execution Completed." >>$logs 2>&1

echo -en $line >>$logs 2>&1

echo $PROGRAM $PROGRAM_ARG was executed within $total_time seconds.
echo
