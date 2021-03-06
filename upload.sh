#!/bin/sh

address='115.68.168.147'
id='storyg'

echo $BLOG_FTP_PASSWORD
ftp -n -v $address << EOF

pass
user $id $passwd
cd /public_html
prompt       
bi
lcd ./_site
mput *.*
bye

EOF

exit 0
