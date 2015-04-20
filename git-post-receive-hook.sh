#!/bin/bash

STATION=blabla
WORKINGDIR=/var/lib/git/$STATION
EXCLUDES="--exclude=.* --exclude=/htdocs --exclude=/logs/ --exclude=/scripts/ --exclude-from=$WORKINGDIR/docs/rsync-exclude.txt"
SYNCTARGET=/var/lib/git/$STATION/
SYNCDEST=/extra/var/www/blabla

# move to the sync dir
cd $WORKINGDIR || exit
unset GIT_DIR

# gets arguments from stdin
# post-receive hook can receive multiple branches at once (git push --all), so need to loop
while read oldrev newrev refname
do
  BRANCH=$(git rev-parse --symbolic --abbrev-ref $refname)
  echo Update pushed to branch $BRANCH

  # change branch
  git checkout $BRANCH

  # update branch
  git pull origin $BRANCH

  # sync
  if [ "$BRANCH" == "master" ]; then
    echo Sync master branch to staging
    # Options -naviO for DRY-RUN -n
    rsync -naviO --delete $EXCLUDES $SYNCTARGET $SYNCDEST

    echo Sync staging to live
    # Set -g for live sync [sync2live-stationname -g docs]
    #/usr/local/bin/lock.sh /usr/local/bin/sync2live-stationname docs
  elif [ "$BRANCH" == "development" ]; then
    echo Sync development branch to dev
    # Options -naviO for DRY-RUN -n
    rsync -naviO --delete $EXCLUDES $SYNCTARGET $SYNCDEST-dev
  fi
done
