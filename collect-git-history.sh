#!/bin/bash
# ./collect_git_history.sh <base_url> [<since>]
# Collect git history of all git directories under <base_url>.
#
# base_url: Parent folder of folders to collect git history
# since (option): Same format as parameter used for "git --since", Default value is 1 month.

# configurations
IGNORE_REPOS=("spring-petclinic/")
DEFAULT_SINCE="1.months"

if [[ -z "$1" ]]
then
	echo "ERROR: <base_url> must be exsit."
	echo "usage: ./collect-git-history.sh <base_url> [since]"
	exit -1
else
	base_dir=$1
fi

if [[ ! -z "$2" ]]
then
	git_log_since=$2
else
	git_log_since=$DEFAULT_SINCE
fi

cd $base_dir
base_dir=$(pwd)

output=$base_dir/git_history
rm ${output}

echo ">> base_dir: ${base_dir}" | tee -a ${output}
echo ">> since: ${git_log_since}" | tee -a ${output}
echo "" | tee -a ${output}

arr=($(ls -d */))

echo "=== Target Directories ==="

for repo in "${arr[@]}"; do
	cd $base_dir/$repo

	if [[ -e ".git" ]]
	then
		echo "- $repo"
	else
		# This folder is not managed by git.
		continue
	fi

	if [[ ${IGNORE_REPOS[*]} =~ "${repo}" ]]
	then
		# Ignore this folder.
		continue
	fi

	if [[ ! -z $(git log --since=${git_log_since}) ]]
	then
		origin_repo_name=$(basename `git rev-parse --show-toplevel`)
		echo "== $origin_repo_name ==" >> ${output}
	fi

	# format: [yyyy-MM-dd] [repo] commit message
	git log --pretty=format:"%ad: %s" --date=format:"%Y-%m-%d" --since=$git_log_since | sort >> $output
	
	if [[ ! -z $(git log --since=${git_log_since}) ]]
	then
		echo "" >> ${output}
	fi
done

# order by commit date
# sort -k 1 -o $output $output

echo ""
echo ">> output path: ${output}"