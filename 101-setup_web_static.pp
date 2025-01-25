# 101-setup_web_static.pp

# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Ensure the /data/web_static directory and its subdirectories exist
file { '/data':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create a fake HTML file at /data/web_static/releases/test/index.html
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => "<html>\n  <head>\n  </head>\n  <body>\n    ALX\n  </body>\n</html>\n",
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Create the symbolic link /data/web_static/current to /data/web_static/releases/test
# This will automatically recreate the symlink if it already exists
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Ensure Nginx is running and enabled
service { 'nginx':
  ensure => running,
  enable => true,
}

# Configure Nginx to serve content from /data/web_static/current
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "
server {
    listen 80;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html;
    }
}
",
  notify  => Service['nginx'],  # Notify Nginx to reload when the config changes
}

# Ensure the Nginx service is restarted to apply changes
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
  notify  => Exec['nginx-restart'],
}

# Restart Nginx to apply the new configuration
exec { 'nginx-restart':
  command => '/etc/init.d/nginx restart',
  path    => ['/usr/sbin', '/usr/bin', '/sbin', '/bin'],
  refreshonly => true,
}
