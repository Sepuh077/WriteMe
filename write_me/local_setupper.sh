: <<'END_COMMENT'

  This script is intended to setup project locally
  It works with the following options:
  1. '-m' - means remove migrations
  2. '-d' - means recreate recreate_db
  3. '-f' - means full setup - including first two options' functionality
  4. no option - means just project related commands' execution

END_COMMENT

DB_NAME='writeme'


function run_manager_command() {
  #  this function executes given commands from the manager behalf's
  echo "========================= '$1' ========================="
  python manage.py $1 $2 $3
  echo "========================= '$1' ========================="
}

function remove_migrations() {
    echo "----- Removing migrations -----"
    rm apps/*/migrations/000*.py
}

function run_db_command() {
    sudo -u postgres psql -c "$1"
}

function recreate_db() {
    echo "----- Recreating DB -----"
    run_db_command "drop database $DB_NAME;"
    if [ $? -eq 1 ];
      then
        echo "----- Disconnecting current DB users/sessions -----"
        sudo kill -9 `sudo lsof -t -i:5432`;
        echo "----- Starting DB -----"
        sudo systemctl start postgresql;
        echo "----- Recreating DB -----"
        run_db_command "drop database $DB_NAME;"
    fi
    run_db_command "create database $DB_NAME;"
    run_db_command "create user $DB_NAME with encrypted password '$DB_NAME';"
    run_db_command "grant all privileges on database $DB_NAME to $DB_NAME;"
}

function setup() {
    echo "----- Setting up project -----"
    run_manager_command clear_cache
    run_manager_command makemigrations
    run_manager_command migrate
    run_manager_command migrate --run-syncdb
    run_manager_command migrate
    run_manager_command syncdata

    # just in case perform data synchronization
    # run_manager_command add_contacts
    # run_manager_command add_pages
    # run_manager_command add_videos
    # run_manager_command add_images
    # run_manager_command add_executed_works
    # run_manager_command add_items
    run_manager_command add_superuser
}


# first detect options
while getopts ":mdf" opt; do
  case ${opt} in
    m ) # process option m
      remove_migrations
      ;;
    d ) # process option d
      recreate_db
      ;;
    f ) # process option t
      echo "֊֊֊֊֊ Starting full setup -----"
      remove_migrations
      recreate_db
      setup
      ;;
    \? ) echo "Usage: cmd [-m] [-d] [-f]"
      ;;
  esac
done

# invoke pure setup command in case of no received option
if [ $OPTIND -eq 1 ];
  then setup;
fi
#shift $((OPTIND-1))
#echo "$# non-option arguments"
