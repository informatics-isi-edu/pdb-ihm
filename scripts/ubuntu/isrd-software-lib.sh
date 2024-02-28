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

############## utility stuff

# include old and new-style group ID strings for now!
ISRD_ADMIN_GROUP=(
    "https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b"
    "g:3938e0d0-ed35-11e5-8641-22000ab4b42b"
)

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

set_selinux_type()
{
    type=$1
    file=$2
    semanage fcontext --add --type "$type" "$file" \
      || semanage fcontext --modify --type "$type" "$file" \
	     || error Could not install SE-Linux context "$type" for "$file"
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

git_clone_idempotent()
{
    # usage:  git_clone_idempotent  repo_url
    require [ $# -eq 1 ]

    # we do default clone which names dir after repo
    repodir=$(basename "$1" .git)

    if [[ -e "/home/${DEVUSER}/${repodir}" ]]
    then
	# if repodir exists, validate that it seems like correct repo
	require [ -d "/home/${DEVUSER}/${repodir}" ]
	require grep "^[[:space:]]*url = *$1" "/home/${DEVUSER}/${repodir}/.git/config"
    else
	# only clone if it is absent
	require_retry su -c "git clone $1" - ${DEVUSER}
    fi
}

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
    ) > /root/isrd-cron-${jobname}.log 2>&1
    status=$?

    if [[ $status -ne 0 ]]
    then
	cat /root/isrd-cron-${jobname}.log
	echo "aborting on status $status"
	exit $status
    fi
}

pgid()
{
    line=$(su -c "psql -q -t -A -c \"select * from pg_roles where rolname = '$1'\"" - postgres)
    status=$?
    [[ $status -eq 0 ]] || return $status
    [[ -n "$line" ]] || return 1
    echo "$line"
    return 0
}

pgdbid()
{
    line=$(su -c "psql -q -t -A -c \"select * from pg_database where datname = '$1'\"" - postgres)
    status=$?
    [[ $status -eq 0 ]] || return $status
    [[ -n "$line" ]] || return 1
    echo "$line"
    return 0
}

################ git tasks

rbk_project_clone()
{
    git_clone_idempotent git@github.com:informatics-isi-edu/rbk-project.git
}

rbk_project_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/rbk-project "$@"
}

chaise_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/chaise.git
}

chaise_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/chaise "$@"
}


ermresolve_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/ermresolve.git
}

ermresolve_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/ermresolve "$@"
}


ermrest_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/ermrest.git
}

ermrest_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/ermrest "$@"
}


deriva_imaging_pipeline_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/deriva-imaging-pipeline.git
}

deriva_imaging_pipeline_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/deriva-imaging-pipeline "$@"
}


imagetools_clone()
{
    git_clone_idempotent git@github.com:informatics-isi-edu/imagetools.git
}

imagetools_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/imagetools "$@"
}


ermrestjs_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/ermrestjs.git
}

ermrestjs_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/ermrestjs "$@"
}

hatrac_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/hatrac.git
}

hatrac_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/hatrac "$@"
}

derivapy_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/deriva-py.git
}

derivapy_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/deriva-py "$@"
}

deriva_catalog_manage_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/deriva-catalog-manage.git
}

deriva_catalog_manage_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/deriva-catalog-manage "$@"
}

deriva_webapps_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/deriva-webapps.git
}

deriva_webapps_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/deriva-webapps "$@"
}


gudmap3_www_clone()
{
    git_clone_idempotent git@github.com:informatics-isi-edu/gudmap3-www.git
}

gudmap3_www_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/gudmap3-www "$@"
}


ioboxd_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/ioboxd.git
}

ioboxd_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/ioboxd "$@"
}

derivaweb_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/deriva-web.git
}

derivaweb_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/deriva-web "$@"
}

microscopy_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/microscopy.git
}

microscopy_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/microscopy "$@"
}


openseadragon_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/openseadragon-viewer.git
}

openseadragon_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/openseadragon-viewer "$@"
}


rbk_www_clone()
{
    git_clone_idempotent git@github.com:informatics-isi-edu/rbk-www.git
}

atlas_d2k_www_clone()
{
    git_clone_idempotent git@github.com:informatics-isi-edu/atlas-d2k-www.git
}

atlas_d2k_hra_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/atlas-d2k-hra.git
}

atlas_d2k_clone()
{
    git_clone_idempotent git@github.com:informatics-isi-edu/atlas-d2k.git
}

rbk_www_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/rbk-www "$@"
}

atlas_d2k_www_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/atlas-d2k-www "$@"
}

atlas_d2k_hra_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/atlas-d2k-hra "$@"
}

atlas_d2k_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/atlas-d2k "$@"
}

pbc_www_clone()
{
    git_clone_idempotent git@github.com:informatics-isi-edu/pbc-www.git
}

pbc_www_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/pbc-www "$@"
}

pdb_www_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/protein-database.git
}

pdb_www_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/protein-database "$@"
}

pdb_www_install()
{
    require /usr/bin/cp -r /home/${DEVUSER}/protein-database/www/* /var/www/html/
    require sed -e '/%INCLUDES%/ {' -e 'r /var/www/html/chaise/dist/chaise-dependencies.html' -e 'd' -e '}' /var/www/html/index.html.in > /var/www/html/index.html
}

# SMITE WWW
smite_www_clone()
{
    git_clone_idempotent git@github.com:informatics-isi-edu/smite.git
}

smite_www_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/smite "$@"
}

smite_www_install()
{
    require cd /home/$DEVUSER/smite
    require su -c "cp /var/www/html/chaise/lib/navbar/navbar-dependencies.html /home/${DEVUSER}/smite/www/_includes/." ${DEVUSER}
    require su -c "cd smite/www && jekyll build" - ${DEVUSER}
    require su -c "rsync -a --exclude=chaise/chaise-config.js /home/${DEVUSER}/smite/www/_site/.  /var/www/html/."
    python_install /home/${DEVUSER}/smite
}

webauthn_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/webauthn.git
}

webauthn_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/webauthn "$@"
}


xtk_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/slicedrop.github.com.git
}

xtk_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/slicedrop.github.com "$@"
}


mesh_viewer_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/mesh-viewer
}

mesh_viewer_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/mesh-viewer "$@"
}


sec_viewer_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/sec-viewer.git
}

sec_viewer_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/sec-viewer "$@"
}

line_viewer_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/line-viewer.git
}

line_viewer_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/line-viewer "$@"
}

# Tutorial static site
tutorial_www_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/deriva-tutorial-www.git
}

tutorial_www_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/deriva-tutorial-www "$@"
}

#Facebase

facebase_www_clone()
{
    git_clone_idempotent git@github.com:informatics-isi-edu/facebase-www.git
}

facebase_www_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/facebase-www "$@"
}

cel_viewer_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/cel-viewer.git
}

cel_viewer_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/cel-viewer "$@"
}


#Add Gpcr specific scheckou

gpcr_www_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/gpcr-www.git
}

gpcr_www_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/gpcr-www "$@"
}

fcs_viewer_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/fcs-viewer.git
}

fcs_viewer_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/fcs-viewer "$@"
}

plotly_clone()
{
    fcs_viewer_clone
}

plotly_pull_checkout()
{
    fcs_viewer_pull_checkout "$@"
}

FlowCytometryTools_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/FlowCytometryTools.git
}

FlowCytometryTools_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/FlowCytometryTools "$@"
}

fcsparser_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/fcsparser.git
}

fcsparser_pull_checkout()
{
    git_pull_checkout  /home/${DEVUSER}/fcsparser "$@"
}

### synapse

volspy_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/volspy.git
}

volspy_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/volspy "$@"
}

fishspy_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/fishspy.git
}

fishspy_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/fishspy "$@"
}

synspy_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/synspy.git
}

synspy_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/synspy "$@"
}

synapse_viewer_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/synapse-viewer.git
}

synapse_viewer_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/synapse-viewer "$@"
}

### gudmap

gudmap_plots_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/gudmap-plots.git
}

gudmap_plots_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/gudmap-plots "$@"
}

# ITK and Convert3D are used in rbk/gudmap 3D processing

itk_clone()
{
    git_clone_idempotent https://github.com/InsightSoftwareConsortium/ITK.git
}

itk_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/ITK "$@"
}

convert3d_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/Convert3D.git
}

convert3d_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/Convert3D "$@"
}

viz_3d_clone()
{
    git_clone_idempotent https://github.com/informatics-isi-edu/viz-3d.git
}

viz_3d_pull_checkout()
{
    git_pull_checkout /home/${DEVUSER}/viz-3d "$@"
}


################ install tasks

cel_viewer_install()
{
    require mkdir -p /var/www/html/cel-viewer/
    require su -c "rsync -a --delete /home/${DEVUSER}/cel-viewer/.  /var/www/html/cel-viewer/."
}

chaise_install()
{
    require cd /home/${DEVUSER}/chaise
    # dist might fail because of node modules, the alternative is to ensure installing them from scratch
    require su ${DEVUSER} -c "make dist || (make distclean && make dist)"
    require make deploy
}

czifile_install()
{
    python_install /home/${DEVUSER}/microscopy/pyramid/czifile
}

czi2dzi_install()
{
    require rpm -q jxrlib{,-devel} libjpeg-turbo{,-devel}
    python_install /home/${DEVUSER}/microscopy/pyramid/czi2dzi
}

scanlib_install()
{
    python_install /home/${DEVUSER}/microscopy/pyramid/scanlib
}

scanTiler_install()
{
    python_install /home/${DEVUSER}/microscopy/pyramid/scanTiler
}

delete_hatrac_install()
{
    CRT_DEVUSER=${DEVUSER}
    DEVUSER=rbkcc

    python_install /home/${DEVUSER}/rbk-project/script/common/worker/delete_hatrac/clientlib
    python_install /home/${DEVUSER}/rbk-project/script/common/worker/delete_hatrac/client
    python_install /home/${DEVUSER}/rbk-project/script/common

    DEVUSER=${CRT_DEVUSER}
}

delete_youtube_install()
{
    CRT_DEVUSER=${DEVUSER}
    DEVUSER=rbkcc

    python_install /home/${DEVUSER}/rbk-project/script/video_processing/worker/delete_youtube/clientlib
    python_install /home/${DEVUSER}/rbk-project/script/video_processing/worker/delete_youtube/client
    python_install /home/${DEVUSER}/rbk-project/script/video_processing

    DEVUSER=${CRT_DEVUSER}
}

upload_youtube_install()
{
    CRT_DEVUSER=${DEVUSER}
    DEVUSER=rbkcc

    python_install /home/${DEVUSER}/rbk-project/script/video_processing/worker/upload_youtube/clientlib
    python_install /home/${DEVUSER}/rbk-project/script/video_processing/worker/upload_youtube/client
    python_install /home/${DEVUSER}/rbk-project/script/video_processing

    DEVUSER=${CRT_DEVUSER}
}

czi_processing_install()
{
    CRT_DEVUSER=${DEVUSER}
    DEVUSER=rbkcc

    python_install /home/${DEVUSER}/rbk-project/script/czi_processing/worker/pyramidal_tiles/clientlib
    python_install /home/${DEVUSER}/rbk-project/script/czi_processing/worker/pyramidal_tiles/client
    python_install /home/${DEVUSER}/rbk-project/script/czi_processing

    DEVUSER=${CRT_DEVUSER}
}

tiff_processing_install()
{
    CRT_DEVUSER=${DEVUSER}
    DEVUSER=rbkcc

    python_install /home/${DEVUSER}/rbk-project/script/tiff_processing/worker/tiff/clientlib
    python_install /home/${DEVUSER}/rbk-project/script/tiff_processing/worker/tiff/client
    python_install /home/${DEVUSER}/rbk-project/script/tiff_processing

    DEVUSER=${CRT_DEVUSER}
}

svg_processing_install()
{
    CRT_DEVUSER=${DEVUSER}
    DEVUSER=rbkcc

    python_install /home/${DEVUSER}/rbk-project/script/svg_processing/worker/svg_processing/clientlib
    python_install /home/${DEVUSER}/rbk-project/script/svg_processing/worker/svg_processing/client
    python_install /home/${DEVUSER}/rbk-project/script/svg_processing

    DEVUSER=${CRT_DEVUSER}
}

image_processing_install()
{
    CRT_DEVUSER=${DEVUSER}
    DEVUSER=rbkcc

    python_install /home/${DEVUSER}/rbk-project/script/image_processing/worker/image_processing/clientlib
    python_install /home/${DEVUSER}/rbk-project/script/image_processing/worker/image_processing/client
    python_install /home/${DEVUSER}/rbk-project/script/image_processing

    DEVUSER=${CRT_DEVUSER}
}

pdb_processing_install()
{
    python_install /home/${DEVUSER}/protein-database/scripts/pdb_processing/worker/pdb/clientlib
    python_install /home/${DEVUSER}/protein-database/scripts/pdb_processing/worker/pdb/client
    python_install /home/${DEVUSER}/protein-database/scripts/pdb_processing
}

pdb_molstar_install()
{
    cp /home/${DEVUSER}/protein-database/scripts/molstar/unpkg/embedded.html /var/www/html/molstar/
    cp /home/${DEVUSER}/protein-database/scripts/molstar/unpkg/favicon.ico /var/www/html/molstar/
    cp /home/${DEVUSER}/protein-database/scripts/molstar/unpkg/molstar.css /var/www/html/molstar/
    cp /home/${DEVUSER}/protein-database/scripts/molstar/unpkg/molstar.js /var/www/html/molstar/
}

deriva_imaging_pipeline_install()
{
    python_install /home/${DEVUSER}/deriva-imaging-pipeline/pipeline
}

imagetools_install()
{
    python_install /home/${DEVUSER}/imagetools
}

ermresolve_install()
{
    require cd /home/${DEVUSER}/ermresolve
    require pip3 install --upgrade .
}

ermrest_install()
{
    require cd /home/${DEVUSER}/ermrest
    require make install
}

ermrestjs_install()
{
    require cd /home/${DEVUSER}/ermrestjs
    require su ${DEVUSER} -c "make dist"
    require make deploy
}

hatrac_install()
{
    python_install /home/${DEVUSER}/hatrac
}

derivapy_install()
{
    python_install /home/${DEVUSER}/deriva-py
    pip3 install globus_sdk fair-research-login fair-identifiers-client jsonschema
}

deriva_catalog_manage_install()
{
    python_install /home/${DEVUSER}/deriva-catalog-manage
}

deriva_webapps_install()
{
    require cd /home/${DEVUSER}/deriva-webapps
    require su ${DEVUSER} -c "make dist"
    require make deploy
}


ioboxd_install()
{
    require cd /home/${DEVUSER}/ioboxd
    require make install
}

derivaweb_install()
{
    require cd /home/${DEVUSER}/deriva-web
    require make install
}

microscopy_webcli_install()
{
    require mkdir -p /var/www/html/webcli
    require su -c "rsync -a --delete --exclude='.*' /home/${DEVUSER}/microscopy/webcli/. /var/www/html/webcli/."
}

cirm_webcli_customize()
{
    require cd /var/www/html/webcli/js
    require su -c "patch -p1" <<EOF
--- js/app.js   2016-07-11 14:07:27.000000000 -0700
+++ js.cirm/app.js.orig 2016-07-28 10:43:53.681249254 -0700
@@ -20,9 +20,9 @@
 var GUEST_PASSWORD = '********';
 var GLOBUS_AUTHN = false;
 var GOAUTHN = true;
-var SLIDE_PRINTER_ADDR = 'slide.example.org';
+var SLIDE_PRINTER_ADDR = 'slidecode.hsc.usc.edu';
 var SLIDE_PRINTER_PORT = 9100;
-var SPECIMEN_PRINTER_ADDR = 'box.example.org';
+var SPECIMEN_PRINTER_ADDR = 'boxcode.hsc.usc.edu';
 var SPECIMEN_PRINTER_PORT = 9100;
 var PRINTER_ADDR = null;
 var PRINTER_PORT = 0;
EOF
}

microscopy_printer_install()
{
    python_install /home/${DEVUSER}/microscopy/printer
}

microscopy_rest_install()
{
    python_install /home/${DEVUSER}/microscopy/rest
}

openseadragon_install()
{
    require cd /home/${DEVUSER}/openseadragon-viewer
    require su ${DEVUSER} -c "make dist"
    require make deploy
}

gudmap3_www_install()
{
    require cd /home/$DEVUSER/gudmap3-www
    require su -c "cp /var/www/html/chaise/dist/chaise-dependencies.html /home/${DEVUSER}/gudmap3-www/_includes/." ${DEVUSER}
    require su -c "cd gudmap3-www && jekyll build" - ${DEVUSER}
    require mkdir -p /var/www/html-gudmap
    require su -c "rsync -a --exclude=chaise/chaise-config.js /home/${DEVUSER}/gudmap3-www/_site/.  /var/www/html-gudmap/."
}

rbk_www_install()
{
    require cd /home/$DEVUSER/rbk-www
    require su -c "cd rbk-www && jekyll build" - ${DEVUSER}
    require su -c "rsync -a --exclude=chaise/chaise-config.js /home/${DEVUSER}/rbk-www/_site/.  /var/www/html/."
}

atlas_d2k_install()
{
    if [[ -d /var/www/html/chaise &&  -d /var/www/html/deriva-webapps ]]
    then
        require cd /home/$DEVUSER/atlas-d2k/scripts/www-config
        require sh ./install-www-config.sh
    else
        error "chaise and deriva-webapps must be installed before atlas_d2k_install is run"
    fi
}

atlas_d2k_hra_install()
{
    require cd /home/${DEVUSER}/atlas-d2k-hra
    require make root-install
}

atlas_d2k_www_install()
{
    require cd /home/$DEVUSER/atlas-d2k-www
    require su -c "cp /var/www/html/chaise/lib/navbar/navbar-dependencies.html /home/${DEVUSER}/atlas-d2k-www/_includes/." ${DEVUSER}
    require su -c "cd atlas-d2k-www && jekyll build" - ${DEVUSER}
    require su -c "rsync -a --exclude=chaise/chaise-config.js /home/${DEVUSER}/atlas-d2k-www/_site/.  /var/www/html/."
}

gpcr_www_install()
{
    require cd /home/$DEVUSER/gpcr-www/www
    require su -c "cd gpcr-www/www && jekyll build" - ${DEVUSER}
    require su -c "rsync -a --exclude='chaise-config.js' /home/${DEVUSER}/gpcr-www/www/_site/.  /var/www/html/."
}

pbc_www_install()
{
    require cd /home/$DEVUSER/pbc-www
    require su -c "cd pbc-www && jekyll build" - ${DEVUSER}
    require su -c "rsync -a --exclude=chaise/chaise-config.js /home/${DEVUSER}/pbc-www/_site/.  /var/www/html/."
}

fcs_viewer_install()
{
    require mkdir -p /var/www/html/fcs-viewer/
    require su -c "rsync -a --delete /home/${DEVUSER}/fcs-viewer/.  /var/www/html/fcs-viewer/."
}

plotly_install()
{
    FlowCytometryTools_install
    fcsparser_install
    fcs_viewer_install
    rm -rf /var/www/html/plotly-viewer
    require ln -s /var/www/html/fcs-viewer /var/www/html/plotly-viewer
    python_install /home/${DEVUSER}/fcs-viewer/reader
}

FlowCytometryTools_install()
{
    python_install /home/${DEVUSER}/FlowCytometryTools
}

fcsparser_install()
{
    python_install /home/${DEVUSER}/fcsparser
}

tifffile_install()
{
    python_install /home/${DEVUSER}/microscopy/pyramid/tifffile
}

webauthn_install()
{
    require cd /home/${DEVUSER}/webauthn
    require make install
}

facebase_xtk_install()
{
    require mkdir -p /var/www/html/_viewer/xtk
    require rsync -a /home/${DEVUSER}/slicedrop.github.com/. /var/www/html/_viewer/xtk/.
}

xtk_install()
{
    require mkdir -p /var/www/html/xtk
    require cp -R /home/${DEVUSER}/slicedrop.github.com/. /var/www/html/xtk/.
}

mesh_viewer_install()
{
    require mkdir -p /var/www/html/mesh-viewer
    require cp -R /home/${DEVUSER}/mesh-viewer/. /var/www/html/mesh-viewer/.
}

sec_viewer_install()
{

    require mkdir -p /var/www/html/sec-viewer
    require su -c "rsync -a --exclude='.*' /home/${DEVUSER}/sec-viewer/. /var/www/html/sec-viewer/." -
    #require export PYTHONPATH=/usr/lib64/python2.7/site-packages
    require yum -y install hdf5-devel


    #require /usr/bin/pip2.7 install numpy
    require pip3 install numpy

    #require /usr/bin/pip2.7 install hdf5
    require yum -y install R
    require yum -y install netcdf-devel
    require cd /home/${DEVUSER}/sec-viewer/reader
    require R CMD INSTALL ncdf_1.6.6.tar.gz

    #require /usr/bin/pip2.7 install netCDF4
    require pip3 install netCDF4
    require python setup.py install


}



line_viewer_install()
{

    require mkdir -p /var/www/html/line-viewer
    require su -c "rsync -a --exclude='.*' /home/${DEVUSER}/line-viewer/. /var/www/html/line-viewer/." -


}

tutorial_www_install()
{
    #require cd /home/${DEVUSER}/tutorial-www/www/

    require su -c "cd /home/${DEVUSER}/deriva-tutorial-www/  && /usr/local/bin/jekyll build" -  ${DEVUSER}

    rsync -a --exclude=chaise-config.js  /home/${DEVUSER}/deriva-tutorial-www/_site/. /var/www/html/.

}

facebase_www_install()
{

    rsync -a   /var/www/html/chaise/lib/navbar/navbar-dependencies.html   /home/${DEVUSER}/facebase-www/www/_includes/.

    require su -c "cd /home/${DEVUSER}/facebase-www/www/  && /usr/local/bin/jekyll build" -  ${DEVUSER}

    rsync -a --exclude=chaise-config.js  /home/${DEVUSER}/facebase-www/www/_site/. /var/www/html/.

}

volspy_install()
{
    python_install /home/${DEVUSER}/volspy
}

fishspy_install()
{
    python_install /home/${DEVUSER}/fishspy
}

synspy_install()
{
    python_install /home/${DEVUSER}/synspy
}

synapse_viewer_install()
{
    require mkdir -p /var/www/html/synapse-viewer/
    require su -c "rsync -a --delete /home/${DEVUSER}/synapse-viewer/.  /var/www/html/synapse-viewer/."
}

gudmap_plots_install()
{
    require cd /home/${DEVUSER}/gudmap-plots/microarray-heatmaps
    require make install
}

itk_install()
{
    require su -c "cd /home/${DEVUSER}/ITK && mkdir -p build" $DEVUSER
    require su -c "cd /home/${DEVUSER}/ITK/build && cmake .." ${DEVUSER}
    require su -c "cd /home/${DEVUSER}/ITK/build && make" ${DEVUSER}
    require cd /home/${DEVUSER}/ITK/build
    require make install
}

convert3d_install()
{
    require su -c "cd /home/${DEVUSER}/Convert3D && mkdir -p build" $DEVUSER
    require su -c "cd /home/${DEVUSER}/Convert3D/build && cmake -D ITK_DIR=/home/${DEVUSER}/ITK/build .." ${DEVUSER}
    require su -c "cd /home/${DEVUSER}/Convert3D/build && make" ${DEVUSER}
    require cd /home/${DEVUSER}/Convert3D/build
    require make install
}

viz_3d_install()
{
    require cd /home/${DEVUSER}/viz-3d
    require make install
}

############## deploy tasks

fcsparser_deploy()
{
    FlowCytometryTools_install
    fcsparser_install
}

ermrest_deploy()
{
    ermrest_install

    require chmod og+rx /home/secrets
    require [ -r /home/ermrest/ermrest_config.json ]

    require cd /home/${DEVUSER}/ermrest
    require make deploy
    require restorecon -rv /home/ermrest
}

ermresolve_httpd_conf_write()
{
    local prefix
    prefix=${ERMRESOLVE_PREFIX:-id}

    if [[ ! -r /etc/httpd/conf.d/wsgi_ermresolve.conf ]]
    then
        cat > /etc/httpd/conf.d/wsgi_ermresolve.conf <<EOF
WSGIPythonOptimize 1
WSGIDaemonProcess ermresolve processes=1 threads=4 user=ermresolve maximum-requests=2000
WSGIScriptAlias /${prefix} ${ISRD_PYLIBDIR}/ermresolve/ermresolve.wsgi process-group=ermresolve

WSGISocketPrefix /var/run/wsgi/wsgi

<Location /${prefix}>
    Require all granted
    WSGIProcessGroup ermresolve
</Location>
EOF
    fi
}

ermresolve_deploy()
{
    ermresolve_install

    id ermresolve || require useradd --create-home --system ermresolve
    require chmod og+rx /home/ermresolve

    require test -r /home/ermresolve/ermresolve_config.json

    require set_selinux_type httpd_sys_content_t "/home/ermresolve/ermresolve_config[.]json"
    require restorecon -rv /home/ermresolve

    require ermresolve_httpd_conf_write
}

hatrac_httpd_conf_write()
{
    if [[ ! -r /etc/httpd/conf.d/wsgi_hatrac.conf ]]
    then
        cat > /etc/httpd/conf.d/wsgi_hatrac.conf <<EOF
AllowEncodedSlashes On

WSGIPythonOptimize 1
WSGIDaemonProcess hatrac processes=4 threads=4 user=hatrac maximum-requests=2000
WSGIScriptAlias /hatrac ${ISRD_PYLIBDIR}/hatrac/hatrac.wsgi process-group=hatrac
WSGIPassAuthorization On

WSGISocketPrefix /var/run/httpd/wsgi

<Location /hatrac>

    AuthType webauthn
    Require webauthn-optional

    WSGIProcessGroup hatrac

</Location>

EOF
    fi
}

microscopy_httpd_conf_write()
{
    cat > /etc/httpd/conf.d/wsgi_microscopy.conf <<EOF
# this file must be loaded (alphabetically) after wsgi.conf

WSGIPythonOptimize 1
WSGIDaemonProcess microscopy processes=4 threads=4 user=ermrest maximum-requests=2000
WSGIScriptAlias /microscopy ${ISRD_PYLIBDIR}/microscopy/microscopy.wsgi process-group=microscopy
WSGIPassAuthorization On
WSGISocketPrefix /var/run/httpd/wsgi

<Location /microscopy>

    Require all granted

    WSGIProcessGroup microscopy

    # site can disable redundant service logging by adding env=!dontlog to their CustomLog or similar directives
    SetEnv dontlog

</Location>

EOF
}

hatrac_deploy()
{
    hatrac_install

    require id hatrac # assume provisioning created daemon account already
    require [ -r /home/hatrac/hatrac_config.json ]
    require [ -r /home/webauthn/webauthn2_config.json ]

    # transitional support for configuring new standalone webauthn daemon
    [[ -f /home/hatrac/webauthn2_config.json ]] && rm -f /home/hatrac/webauthn2_config.json

    pgid hatrac || require su -c "createuser --createdb hatrac" - postgres
#    require su -c "psql -c 'GRANT ermrest to hatrac'" - postgres
    if pgdbid hatrac
    then
	echo "re-running hatrac-deploy which might fail harmlessly..."
	su -c "hatrac-deploy ${ISRD_ADMIN_GROUP[*]}" - hatrac
    else
	require su -c "createdb hatrac" - hatrac
	require su -c "hatrac-deploy ${ISRD_ADMIN_GROUP[*]}" - hatrac
    fi
    require mkdir -p /var/www/hatrac
    require chown hatrac /var/www/hatrac

    require set_selinux_type httpd_sys_content_t "/home/hatrac/.*_config[.]json"
    require set_selinux_type httpd_sys_content_t "/home/hatrac/.aws(/.*)?"
    require restorecon -rv /home/hatrac

    require set_selinux_type httpd_sys_rw_content_t "/var/www/hatrac(/.*)?"
    require restorecon -rv /var/www/hatrac

    require hatrac_httpd_conf_write
}

ioboxd_deploy()
{
    ioboxd_install

    require cd /home/${DEVUSER}/ioboxd
    require make deploy
}

derivaweb_deploy()
{
    derivaweb_install

    require cd /home/${DEVUSER}/deriva-web
    require make deploy
}

webauthn_deploy()
{
    webauthn_install

    require chmod og+rx /home/secrets
    require [ -r /home/webauthn/webauthn2_config.json ]
    require cd /home/${DEVUSER}/webauthn
    require make deploy
}

rbk_project_deploy()
{
require su -c "rsync -avz --delete /home/isrddev/rbk-project /home/rbkcc/rbk-project"
chown -R rbkcc: /home/rbkcc/rbk-project
}

microscopy_rest_deploy()
{
    microscopy_rest_install

    require microscopy_httpd_conf_write
}

############## bioformats tasks

raw2ometiff_fetch()
{
    DIR="/home/${DEVUSER}/raw2ometiff"
    URL=${1:-"https://github.com/glencoesoftware/raw2ometiff/releases/download/v0.4.1/raw2ometiff-0.4.1.zip"}
    FILENAME=$(basename $URL)
    require mkdir -p "$DIR"
    require cd "$DIR"
    # fetch and (lightly) verify raw2ometiff application bundle
    require curl -L "$URL" -o "$FILENAME" -s
    require unzip -qq -t "${FILENAME}"
}

raw2ometiff_install()
{
    BIN_DIR="/usr/local/bin"
    DIR=/home/${DEVUSER}/raw2ometiff
    RAW2OMETIFF=${1:-"raw2ometiff-0.4.1"}
    RAW2OMETIFF_ZIP="${DIR}/${RAW2OMETIFF}.zip"
    INSTALL_DIR="/usr/local/share/applications"
    # install raw2ometiff application files
    require test -r "$RAW2OMETIFF_ZIP"
    require test -d "$INSTALL_DIR"
    require cd "$INSTALL_DIR"
    require unzip -n -qq "$RAW2OMETIFF_ZIP"
    rm -rf "${BIN_DIR}/raw2ometiff"
    require ln -s "${INSTALL_DIR}/${RAW2OMETIFF}/bin/raw2ometiff" "${BIN_DIR}/raw2ometiff"
}

bioformats2raw_fetch()
{
    DIR="/home/${DEVUSER}/bioformats2raw"
    URL=${1:-"https://github.com/glencoesoftware/bioformats2raw/releases/download/v0.6.1/bioformats2raw-0.6.1.zip"}
    FILENAME=$(basename $URL)
    require mkdir -p "$DIR"
    require cd "$DIR"
    # fetch and (lightly) verify bioformats2raw application bundle
    require curl -L "$URL" -o "$FILENAME" -s
    require unzip -qq -t "${FILENAME}"
}

bioformats2raw_install()
{
    BIN_DIR="/usr/local/bin"
    DIR=/home/${DEVUSER}/bioformats2raw
    BIOFORMATS2RAW=${1:-"bioformats2raw-0.6.1"}
    BIOFORMATS2RAW_ZIP="${DIR}/${BIOFORMATS2RAW}.zip"
    INSTALL_DIR="/usr/local/share/applications"
    # install bioformats2raw application files
    require test -r "$BIOFORMATS2RAW_ZIP"
    require test -d "$INSTALL_DIR"
    require cd "$INSTALL_DIR"
    require unzip -n -qq "$BIOFORMATS2RAW_ZIP"
    rm -rf "${BIN_DIR}/bioformats2raw"
    require ln -s "${INSTALL_DIR}/${BIOFORMATS2RAW}/bin/bioformats2raw" "${BIN_DIR}/bioformats2raw"
}

bftools_fetch()
{
    DIR="/home/${DEVUSER}/bftools"
    URL=${1:-"https://downloads.openmicroscopy.org/bio-formats/latest/artifacts/bftools.zip"}
    FILENAME=$(basename $URL)
    require mkdir -p "$DIR"
    require cd "$DIR"
    # fetch and (lightly) verify bftools application bundle
    require curl -L "$URL" -o "$FILENAME" -s
    require unzip -qq -t "${FILENAME}"
}

bftools_install()
{
    BIN_DIR="/usr/local/bin"
    DIR=/home/${DEVUSER}/bftools
    BFTOOLS=${1:-"bftools"}
    BFTOOLS_ZIP="${DIR}/${BFTOOLS}.zip"
    INSTALL_DIR="/usr/local/share/applications"
    # install bftools application files
    require test -r "$BFTOOLS_ZIP"
    require test -d "$INSTALL_DIR"
    require cd "$INSTALL_DIR"
    require unzip -n -qq "$BFTOOLS_ZIP"
    rm -rf "${BIN_DIR}/bftools" "${BIN_DIR}/tiffcomment" "${BIN_DIR}/showinf" "${BIN_DIR}/bfconvert"
    require ln -s "${INSTALL_DIR}/${BFTOOLS}" "${BIN_DIR}/bftools"
    require ln -s "${INSTALL_DIR}/${BFTOOLS}/tiffcomment" "${BIN_DIR}/tiffcomment"
    require ln -s "${INSTALL_DIR}/${BFTOOLS}/showinf" "${BIN_DIR}/showinf"
    require ln -s "${INSTALL_DIR}/${BFTOOLS}/bfconvert" "${BIN_DIR}/bfconvert"
}

############## cantaloupe tasks

cantaloupe_fetch()
{
    DIR="/home/${DEVUSER}/cantaloupe"
    URL=${1:-"https://github.com/cantaloupe-project/cantaloupe/releases/download/v4.1.7/cantaloupe-4.1.7.zip"}
    FILENAME=$(basename $URL)
    require mkdir -p "$DIR"
    require cd "$DIR"
    # fetch and (lightly) verify cantaloupe application bundle
    require curl -L "$URL" -o "$FILENAME" -s
    require unzip -qq -t "${FILENAME}"
}

cantaloupe_install()
{
    USER=cantaloupe
    DIR=/home/${DEVUSER}/cantaloupe
    CANTALOUPE=${1:-"cantaloupe-4.1.7"}
    CANTALOUPE_ZIP="${DIR}/${CANTALOUPE}.zip"
    INSTALL_DIR="/usr/local/share/applications"
    # install cantaloupe application files
    require test -r "$CANTALOUPE_ZIP"
    require test -d "$INSTALL_DIR"
    require cd "$INSTALL_DIR"
    require unzip -n -qq "$CANTALOUPE_ZIP"
    require restorecon -r "${INSTALL_DIR}/${CANTALOUPE}"
}

cantaloupe_systemd_service()
{
    CANTALOUPE=${1:-"cantaloupe-4.1.7"}
    MAXMEM=${2:-"8g"}
    USER="cantaloupe"
    JAR="/usr/local/share/applications/${CANTALOUPE}/${CANTALOUPE}.war"
    require test -r "$JAR"
    require test -d /etc/systemd/system
    cat > /etc/systemd/system/cantaloupe.service <<EOF
[Unit]
Description=Cantaloupe Image Server (${CANTALOUPE})

[Service]
User=${USER}
ExecStart=/usr/bin/java -Dcantaloupe.config=/home/${USER}/cantaloupe.properties -Xmx${MAXMEM} -jar ${JAR}
RestartSec=60
Restart=always
KillMode=mixed
TimeoutStopSec=60
Nice=19
IOSchedulingClass=idle

[Install]
WantedBy=multi-user.target

EOF
}

cantaloupe_httpd_reverseproxy()
{
    cat > /etc/httpd/conf.d/cantaloupe.conf <<EOF
# Reverse proxy of cantaloupe imaging server /iiif interface
ProxyPass /iiif http://localhost:8182/iiif nocanon
ProxyPassReverse /iiif http://localhost:8182/iiif

EOF
}

cantaloupe_deploy()
{
    # setup cantaloupe home dir
    USER="cantaloupe"
    id "$USER" || require useradd --create-home --system "$USER"
    require chmod og+rx "/home/${USER}"
    require test -r "/home/${USER}/cantaloupe.properties"
    require set_selinux_type httpd_sys_content_t "/home/${USER}/cantaloupe.properties"
    require restorecon -r "/home/${USER}"

    # setup cantaloupe web root and temp dir
    WEB_ROOT="/var/www"
    TEMP_DIR="${WEB_ROOT}/${USER}/tmp"
    require test -d "$WEB_ROOT"
    require mkdir -p "$TEMP_DIR"
    require chown -R ${USER}: "${WEB_ROOT}/${USER}"
    require restorecon -r "$TEMP_DIR"

    # create cantaloupe serivce unit
    require cantaloupe_systemd_service
    require systemctl enable cantaloupe.service
    require systemctl start cantaloupe.service

    # add cantaloupe reverse proxy configuration
    require cantaloupe_httpd_reverseproxy
}
