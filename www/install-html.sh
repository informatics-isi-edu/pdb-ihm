#!/bin/bash
#
# Expand the *.html.in templates in the web root into *.html, using values for
# the deployment this host serves. Run after www/* has been copied there.
#
# Usage: install-html.sh
#
# Defaults below are production; an unrecognized host gets them. To add a new
# environment-specific value, put a %PLACEHOLDER% in the template and give it a
# default here. A placeholder left unsubstituted is a hard error, so a missing
# value fails the install instead of shipping.
#
# For markup that exists on some deployments only, wrap it in marker comments on
# their own lines (no nesting):
#
#   <!--%IF_DEV%-->
#   <p>dev only</p>
#   <!--%ENDIF_DEV%-->
#
set -eu

target_dir=/var/www/html
host=`uname -n`
navbar="${target_dir}/chaise/lib/navbar/navbar-dependencies.html"

if [ $# -ne 0 ]
then
    echo "ERROR: no arguments supported" >&2
    echo "Usage: $0" >&2
    exit 1
fi

MAIN_URL="https://data.pdb-ihm.org"
IHMV_URL="https://validate.pdb-ihm.org"
MAIN_CATALOG=1
IHMV_CATALOG=101
STRIP=( -e '/%IF_DEV%/,/%ENDIF_DEV%/d' -e '/%IF_PROD%/d' -e '/%ENDIF_PROD%/d' )

case "$host" in
  data-dev.pdb-ihm.org)
    MAIN_URL="https://data-dev.pdb-ihm.org"
    IHMV_URL="https://validate-dev.pdb-ihm.org"
    MAIN_CATALOG=50
    IHMV_CATALOG=199
    STRIP=( -e '/%IF_PROD%/,/%ENDIF_PROD%/d' -e '/%IF_DEV%/d' -e '/%ENDIF_DEV%/d' )
    ;;
  data-dev2.pdb-ihm.org)
    MAIN_URL="https://data-dev2.pdb-ihm.org"
    IHMV_URL="https://data-dev2.pdb-ihm.org/ihmv"
    MAIN_CATALOG=50
    IHMV_CATALOG=199
    STRIP=( -e '/%IF_PROD%/,/%ENDIF_PROD%/d' -e '/%IF_DEV%/d' -e '/%ENDIF_DEV%/d' )
    ;;
esac

[ -f "$navbar" ] || { echo "install-html.sh: missing ${navbar}" >&2; exit 1; }

render() {
  local src="$1" dest="$2"
  [ -f "$src" ] || { echo "install-html.sh: missing ${src}" >&2; exit 1; }
  sed "${STRIP[@]}" \
      -e "s|%MAIN_URL%|${MAIN_URL}|g" \
      -e "s|%IHMV_URL%|${IHMV_URL}|g" \
      -e "s|%MAIN_CATALOG%|${MAIN_CATALOG}|g" \
      -e "s|%IHMV_CATALOG%|${IHMV_CATALOG}|g" \
      -e "s|%DEFAULT_CATALOG%|data-default-catalog=\"${IHMV_CATALOG}\"|g" \
      -e "/%INCLUDES%/{" -e "r ${navbar}" -e 'd' -e '}' \
      "$src" > "$dest"

  if grep -qE '%[A-Z_]+%' "$dest"; then
    echo "install-html.sh: unsubstituted placeholder in ${dest}:" >&2
    grep -nE '%[A-Z_]+%' "$dest" >&2
    exit 1
  fi
  chmod u=rw,og=r "$dest"
}

render "${target_dir}/index.html.in"      "${target_dir}/index.html"
render "${target_dir}/ihmv/index.html.in" "${target_dir}/ihmv/index.html"

# templates and this script are copied into the web root, so drop them once
# expanded rather than leaving them publicly readable
rm -f "${target_dir}/index.html.in" "${target_dir}/ihmv/index.html.in" "${target_dir}/install-html.sh"
