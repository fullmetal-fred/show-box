#!/usr/bin/env bash
# SPDX-License-Identifier: MPL-2.0
# Rename the placeholder product name across the repo.
#   tools/rename.sh newname           dry run: show every match
#   tools/rename.sh newname --apply   rewrite showbox / ShowBox / SHOWBOX
set -euo pipefail
new="${1:?usage: tools/rename.sh <newname> [--apply]}"
apply="${2:-}"
[[ "$new" =~ ^[a-z][a-z0-9-]*$ ]] || { echo "name must be lowercase [a-z0-9-]" >&2; exit 1; }
cd "$(git rev-parse --show-toplevel)"
lower="$new"
upper="$(echo "$new" | tr 'a-z-' 'A-Z_')"
camel="$(echo "${new:0:1}" | tr 'a-z' 'A-Z')${new:1}"

files=$(git ls-files | grep -v -E '^LICENSE|^tools/rename\.sh$' | xargs grep -l -E 'showbox|ShowBox|SHOWBOX' || true)
if [[ "$apply" != "--apply" ]]; then
  git grep -n -E 'showbox|ShowBox|SHOWBOX' -- $files
  echo; echo "Dry run. Re-run with --apply to rewrite: showbox->$lower ShowBox->$camel SHOWBOX->$upper"
  exit 0
fi
for f in $files; do
  sed -i.bak -e "s/showbox/$lower/g" -e "s/ShowBox/$camel/g" -e "s/SHOWBOX/$upper/g" "$f" && rm -f "$f.bak"
done
echo "Rewrote $(echo "$files" | wc -w) files. Review with: git diff"
echo "Repo directory and GitHub repo name are not changed."
