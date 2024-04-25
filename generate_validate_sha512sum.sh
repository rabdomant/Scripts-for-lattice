#!/bin/bash

usage() {
    echo "Usage: $0 [-o outputfile] [-c dir_to_checksum] [-x 0:verify only|1:generate|2:generate+verify(D)]"
}

check_command() {
    if ! command -v $1 &>/dev/null; then
        echo "$1 could not be found"
        exit 1
    fi
}

wait_file() {
    local file="$1"
    shift
    local wait_seconds="${1:-10}"
    shift # 10 seconds as default timeout
    test $wait_seconds -lt 1 && echo 'At least 1 second is required' && return 1

    until test $((wait_seconds--)) -eq 0 -o -e "$file"; do sleep 1; done

    test $wait_seconds -ge 0 # equivalent: let ++wait_seconds
}

check_command command
check_command sha512sum
check_command find
check_command xargs
check_command nproc
check_command cat

outputf="local_shasum.txt"
checksumdir="../cnfg/"
gv=2
ncores=$(nproc --all)

while getopts "o:c:x:n:h" o; do
    case "${o}" in
    o)
        outputf=${OPTARG}
        ;;
    c)
        checksumdir=${OPTARG}
        ;;
    x)
        gv=${OPTARG}
        ;;
    n)
        ncores=${OPTARG}
        ;;
    *)
        usage
        exit 0
        ;;
    esac
done
shift $((OPTIND - 1))

if [[ $gv != @("0"|"1"|"2") ]]; then
    echo "Wrong value for -x"
    exit 1
fi

((gv == 0)) && echo "Veryfing the checksum in the file: $outputf"
((gv == 1)) && echo "Generating the checksums of dir: $checksumdir in the file: $outputf"
((gv == 2)) && echo -e "Veryfing the checksum in the file: $outputf\nGenerating the checksums of dir: $checksumdir in the file: $outputf"

if [ -f $outputf ]; then
    if ((gv == 0 || gv == 2)); then
        rm -f ${outputf}_eval
        while read line; do
            echo "echo \"$line\" | sha512sum --check || ( echo \"Wrong checksum for line $line \" && exit 1 ) ">>${outputf}_eval
        done <$outputf
        if [ -f ${outputf}_eval ]; then
            cat ${outputf}_eval | xargs -P${ncores} -I{} bash -c "{}"
            exit_code=$?
            ((exit_code != 0)) && echo "Something went wrong in the checksum validation" && exit 1
            echo "Succesful checksum validation"
        fi
    fi
else
    ((gv == 0)) && echo "Missing $outputf file" && exit 1
    >$outputf
fi

((gv == 0)) && exit 0

id=0
rm -f ${outputf}[0-9]* ${outputf}_eval
for i in $(find -L $checksumdir -type f); do
    found=$(grep -e"\*$i$" $outputf)
    if [ -z "$found" ]; then
        echo "Adding $i"
        ((id++))
        echo "sha512sum -b $i > ${outputf}${id}" >>${outputf}_eval
    fi
done

if ((id > 0)); then
    cat ${outputf}_eval | xargs -P${ncores} -I{} bash -c "{}"
    exit_code=$?
    ((exit_code != 0)) && echo "Something went wrong in the checksum generation" && exit 1
fi

for i in $(seq 1 $id); do
    wait_file ${outputf}${i}
    cat ${outputf}${i} >>${outputf}
    rm -f ${outputf}${i}

done

rm -f ${outputf}_eval

exit 0
