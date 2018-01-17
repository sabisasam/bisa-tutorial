#!/bin/bash

# Bash variables
USERNAME="root@example.com"
PASSWORD="password"
EMAIL="root@example.com"

prefix="[initialise.sh]"
project_name="main"

function print_help() {
cat << EOF
$0

DESCRIPTION
The script initialises the database for Django and creates a user,
if root or the given user does not exist on the database.

OPTIONS
-h|--help                       Print this help.
-u=*|--user=*                   Create the given user if the user does not exist in the database
                                    (Default: root)
-p=*|--password=*               Use the given password for the user creation.
                                    (Default: password)
-s|--accountskip                Skip the account creation
EOF
}

# Parsing the arguments
for i in "$@"
do
case $i in
    -u=*|--username=*)
    USERNAME="${i#*=}"
    shift
    ;;
    -p=*|--password=*)
    PASSWORD="${i#*=}"
    shift
    ;;
    -e=*|--email=*)
    EMAIL="${i#*=}"
    shift
    ;;
    -s|--account-skip)
    ACCOUNTSKIP=true
    shift
    ;;
    -h|--help)
    print_help
    exit
    shift
    ;;
    *)
    ;;
esac
done

echo "$prefix started."

if [ ! -d "static/" ]
then
    echo "$prefix Create static dir for main"
    mkdir "static"
fi

echo "$prefix collectstatic"
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

if [ ! $ACCOUNTSKIP ]
then
    echo "$prefix create Account"
    export USERNAME
    export PASSWORD
    export EMAIL
    python manage.py shell < createsuperuser.cmd
fi

echo "$prefix finished."
