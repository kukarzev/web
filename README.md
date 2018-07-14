# Hosting Stuff on the Web
Configs, instructions and tools for hosting stuff on the web.

# Wordpress
1) Download and unpack

        wget https://wordpress.org/latest.tar.gz
        tar xvf latest.tar.gz
        rm latest.tar.gz

2) Follow [Wordpress' instructions](https://codex.wordpress.org/Installing_WordPress#Famous_5-Minute_Installation).

3) Set file permissions before and after installation [from this stackoverflow](https://stackoverflow.com/questions/18352682/correct-file-permissions-for-wordpress):

        cd /var/www/sitefolder/
        sudo chown www-data:www-data ../sitefolder
        sudo chown www-data:www-data  -R *
        sudo find . -type d -exec chmod 755 {} \;
        find . -type f -exec chmod 644 {} \;
After installation:

        sudo chown <username>:<username>  -R * # Let your useraccount be owner
        sudo chown www-data:www-data wp-content # Let apache be owner of wp-content

# Apache
For apache2 on ubuntu circa 16.04.

1) Site configs go into 
    
        /etc/apache2/sites-available/kukartsev.conf
        
2) Enable by

        sudo a2ensite kukartsev.conf

3) Host a separate site in a subfolder of the main site domain,e.g.
    - main site `host.com` lives in `/var/www/host`
    - second site should look like `host.com/blog` but live in `/var/www/blog`
    To do that, enable alias mod first:

            sudo a2enmod alias    
    Then add an alias **inside** the virtualhost block of the main site:
    
            Alias /vika /var/www/blog
            <Directory /var/www/blog>  
               Options All              
               AllowOverride All
               order allow,deny 
               allow from all
            </Directory>
