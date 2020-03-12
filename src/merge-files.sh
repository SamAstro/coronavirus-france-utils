#!/bin/bash

root_repo='../coronavirus-france-dataset'
fname_master=$root_repo'/patient.csv'
fname_backup=$root_repo'/patient-backup.csv'
fname_inputs='_tmp/patient-tmp.csv'

# Create Backup file
cp $fname_master $fname_backup

# Merge files
tail -n ${1} $fname_inputs >> $fname_master

# Compare if all ok
if cmp -s $fname_master $fname_backup; then
    printf 'The file "%s" is the same as "%s"\n' $fname_master $fname_backup
else
    printf 'The file "%s" is different from "%s"\n' $fname_master $fname_backup
    printf 'check with git diff that only new lines are considered added'
    cd $root_repo
    git diff patient.csv
fi
