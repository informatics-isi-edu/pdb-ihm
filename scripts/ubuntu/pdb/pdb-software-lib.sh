#!/bin/bash

# We MAY use modern bash features in this library script
#

pattern='^(.*:)?/usr/local/bin(:.*)?'
if [[ ! "$PATH" =~ $pattern ]]
then
    # we need this in our path even if cron left it out...
    # this is where pip3 puts our web service deploy scripts
    PATH=/usr/local/bin:${PATH}
fi

ISRD_PYLIBDIR=$(python3 -c 'import site; print(site.getsitepackages()[1])')

error()
{
    cat >&2 <<EOF
$0 error: "$@"
EOF
    exit 1
}

if id isrddev > /dev/null 2>&1
then
    DEVUSER=isrddev
elif id karlcz > /dev/null 2>&1
then
    DEVUSER=karlcz
else
    error could not determine DEVUSER
fi

cron_run()
{
    # usage: jobname cmd [ cmd... ]
    jobname="$1"
    shift

    (
	cat <<EOF
$0 cron_run $jobname started $(date -Iseconds)
EOF

	status=0
	for cmd in "$@"
	do
	    cat <<EOF

> running $cmd
EOF
	    $cmd
	    status="$?"
	    if [[ "$status" -ne 0 ]]
	    then
		cat <<EOF
error: $0 $cmd returned $status

EOF
		exit $status
	    else
		cat <<EOF
: status 0 from $cmd
EOF
	    fi
	done
    ) > /root/pdb-cron-${jobname}.log 2>&1
    status=$?

    if [[ $status -ne 0 ]]
    then
	cat /root/pdb-cron-${jobname}.log
	echo "aborting on status $status"
	exit $status
    fi
}
require()
{
    # usage: require cmd [args...]
    # just run command-line and check for success status code
    "$@"
    status=$?
    if [[ $status != 0 ]]
    then
	error Command "($*)" returned non-zero "status=$status"
    fi
}

require_retry()
{
    for trial in {1..5}
    do
	"$@"
	status="$?"
	if [[ "$status" = 0 ]]
	then
	    return 0
	else
	    echo "require_retry: $* returned status $status" >&2
	fi
    done
    error Command "($*)" failed too many times
}

python_install()
{
    require cd "$1"
    require pip3 install --upgrade .

    # fixup se-linux context problems seen on some fedora 34 VMs...
    restorecon -rv ${ISRD_PYLIBDIR}
}

# this is a misnomer we should fix eventually...
# we do fetch ; checkout to be robust against local repo state
git_pull_checkout()
{
    # usage: repodir [ checkout-arg... ]
    _repodir="$1"
    require cd "${_repodir}"
    shift
    require chown -R ${DEVUSER}. .
    # NOTE: changing dir in the command and using `-` login mode needed on Fedora 28
    # otherwise we get wrong umask and/or wrong working dir for git commands
    require_retry su -c "cd \"${_repodir}\" && git fetch" - ${DEVUSER}
    if [[ "$#" -gt 0 ]]
    then
	args=$(printf ' "%s"' "$@")
    else
	args="origin/master"
    fi
    require su -c "cd \"${_repodir}\" && git checkout -f $args" - ${DEVUSER}
}

derivaextras_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/deriva-extras.git
}

derivaextras_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/deriva-extras origin/main
}

derivaextras_install()
{
    python_install /home/${DEVUSER}/deriva-extras
}

pdb_www_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/pdb-ihm "$@"
}

pdb_ihm_ops_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/pdb-ihm-ops "$@"
}

pdb_processing_install()
{
    python_install /home/${DEVUSER}/pdb-ihm/scripts/pdb_processing/worker/pdb/clientlib
    python_install /home/${DEVUSER}/pdb-ihm/scripts/pdb_processing/worker/pdb/client
    python_install /home/${DEVUSER}/pdb-ihm/scripts/pdb_processing
    python_install /home/${DEVUSER}/pdb-ihm
    #python_install /home/${DEVUSER}/pdb-ihm-ops
    
    require cd /home/$DEVUSER/pdb-ihm/scripts/home-config
    require ./install-home-config.sh    
}

derivapy_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/deriva-py "$@"
}

derivapy_install()
{
    python_install /home/${DEVUSER}/deriva-py
    pip3 install globus_sdk fair-research-login fair-identifiers-client jsonschema
}

python_ihm_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/python-ihm "$@"
}

python_ihm_install()
{
    pip3 install ihm==1.3
}

python_ihm_validation()
{
    DEVUSER=pdbihm
    git_pull_checkout /mnt/vdb1/pdbihm/IHMValidation "$@"
}

