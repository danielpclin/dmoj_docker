#!/bin/bash

problem_storage_root="$(realpath "${PROBLEM_STORAGE_ROOT:-$1}")"
judge_hosts_file="$(realpath "${JUDGE_HOSTS_FILE:-$2}")"

echo "$(date): Start watching ${problem_storage_root}, notifying ${judge_hosts_file}"

inotifywait -rm "${problem_storage_root}" -e move,create,delete -q | while read -r line; do
    if [ "$(echo "$line" | cut -d' ' -f3)" != "init.yml" ] && [ "$(echo "$line" | cut -d' ' -f2)" != "MOVED_TO,ISDIR" ]; then
        continue
    fi
    echo "$(date): Update problems [$line]"
    readarray -t judges < "${judge_hosts_file}"
    for judge in "${judges[@]}"; do
	      curl -4 -s -X POST "http://$judge/update/problems" | sed "s/^/$(date) [$judge]: /"';$a\'
    done
done
