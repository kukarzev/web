# Backup

Steps to back up databases and some other stuff.

## Wordpress blogs

Use PhpMyAdmin export tool: [kukartsev.com/phpmyadmin](http://kukartsev.com/phpmyadmin)

1) Log in as an admin user and go to the Export section (menu at the top).

2) Export the following databases:

    Use "custom" option, and check "add drop database" and "add drop table" options, for ease of restore. 

    ```
    sciencejobshq
    vika
    wardiary
    ```

