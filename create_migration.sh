#!/bin/bash

message=$(echo $* | xargs | iconv -t ascii//TRANSLIT | sed -E 's/[^a-zA-Z0-9]+/_/g' | sed -E 's/^_+|_+$//g' | tr A-Z a-z)

if [ -z ${message} ]; then
	echo "не задано название миграции"
	exit 1
fi

timestamp=$(date +'%Y%m%d.%H%M%S')
migration="V${timestamp}__${message}.sql"
migration_dir=resources/migrations

mkdir -p ${migration_dir}
touch ${migration_dir}/${migration}

echo "created '"${migration}"'"