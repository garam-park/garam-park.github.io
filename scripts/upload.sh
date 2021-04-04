#!/bin/bash
if [[ -z "$FTP_USER" ]]; then
    echo "FTP_USER is needed."
    exit 1
fi

if [[ -z "$FTP_PASS" ]]; then
    echo "FTP_PASS is needed."
    exit 1
fi

if [[ -z "$FTP_HOST" ]]; then
    echo "FTP_HOST is needed."
    exit 1
fi

ncftpput -R -v -u $FTP_USER -p $FTP_PASS $FTP_HOST /public_html ./_site/*
