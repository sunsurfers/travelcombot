#!/bin/bash

echo "export vars.."
export $(grep -v '^#' .env | xargs)

echo "setup mysql database.."
mysql $db_database -u $db_user -p $db_database < schema.sql

echo "Done"