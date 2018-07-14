# Hosting Stuff on the Web
Configs, instructions and tools for hosting stuff on the web.

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
