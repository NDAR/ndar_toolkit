#!/usr/bin/python

"""
This program is designed to run on an Amazon Web Services EC2 instance, running linux.
As a pre-requisite, Python 2.6 or higher will be needed for the script to run, which comes
pre-packaged on the standard Linux Amazon Machine Image (AMI).

This program will:
- Download the NDAR Download Manager (http://ndar.nih.gov)
- Download + configure s3cmd (s3tools.org)
- Configure the aws-cli tools pre-packaged with standard AWS Linux AMIs (http://aws.amazon.com/documentation/cli/)
- Generate a set of access credentials for NDAR data stored as S3 objects.

Configuration:
- Set your ndar_username and ndar_password inside this file
  OR
- Set the enviornment variables ndar_username and ndar_password:
  example: export ndar_username="John Doe"
           export ndar_password="sup3r S3cret"

NOTES: 
- Data access is monitoried.
- Access to data requires an NDAR account.
- A Data Use Certification must be signed and agreed to.
- Downloading and persisting data, as well as any kind of redistribution is strictly prohibited.
- Please read the NDAR Omics policy as it applies to Data Download https://ndar.nih.gov/faq.html#faq64
"""  
from os.path import expanduser 
import sys
import stat
import fileinput
import getpass
from subprocess import call
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import os
try:
    import urllib2
except ImportError:
    from urllib import request
import zipfile
import tarfile

# Default home directory, set this to the home folder for the user you plan to use, (i.e., ec2-uesr, ubuntu, etc.)
#home = '/home/ec2-user'
#home = '/home/ubuntu'
#home = '/home/mobaxterm'


home = expanduser("~")
print ('Home is %s' %home) 
def download_file( url, dest ):
    if sys.version_info[0] < 3:    
        f = urllib2.urlopen( url )
    else:
        f = request.urlopen( url )
    with open( dest, "wb") as local_file:
        local_file.write(f.read())

def unzip_file( filename ):
    z = zipfile.ZipFile(filename)
    for name in z.namelist():
        outpath = os.path.normpath(home + "/ndar_toolkit")
        z.extract( name, outpath )
    z.close()
    os.remove( filename )

def shell_source(script):
   f = open (os.path.normpath( home + '/ndar_toolkit/ndar_update_keys.sh'), 'r')
   line = f.readline()
   ndar_username = line.split("=",1)[1]
   line = f.readline()
   ndar_password = line.split("=",1)[1]
   return ndar_username.strip(), ndar_password.strip()  

def create_default_config(home, config_file):
    f = open (os.path.normpath(home + config_file), 'wt')
    f.write('[default]\n')
    f.close()

def write_aws_config(home, config_file, profile):
    config_aws_cli = ConfigParser.ConfigParser()
    if (os.path.isfile(os.path.normpath(home + config_file))):
        config_aws_cli.read(os.path.normpath(home + config_file))
        if not config_aws_cli.has_section(profile):
            config_aws_cli.add_section(profile)
        config_aws_cli.set(profile, 'aws_access_key_id', myvars["accessKey"])
        config_aws_cli.set(profile, 'aws_secret_access_key', myvars["secretKey"])
        config_aws_cli.set(profile, 'aws_session_token', myvars["sessionToken"])
        config_aws_cli.set(profile, 'region', 'us-east-1')
    else:
        create_default_config(home,config_file)
        config_aws_cli.read( os.path.normpath(home + config_file))
        aws_cli_info = {
            'aws_access_key_id': ' #Add your AWS access key ',
            'aws_secret_access_key': ' #Add your AWS secret key ',
            'region': ' #Specify a default region '
        }
        #config_aws_cli.add_section('default')
        for key in aws_cli_info.keys():
            config_aws_cli.set('default', key, aws_cli_info[key])
        config_aws_cli.add_section(profile)
        config_aws_cli.set(profile, 'aws_access_key_id', myvars["accessKey"])
        config_aws_cli.set(profile, 'aws_secret_access_key', myvars["secretKey"])
        config_aws_cli.set(profile, 'aws_session_token', myvars["sessionToken"])
        config_aws_cli.set(profile, 'region', 'us-east-1')

    with open(os.path.normpath(home + config_file), 'wt') as configfile:
        config_aws_cli.write(configfile)

def write_s3cmd_config(home, config_file):
    config_s3cmd = ConfigParser.ConfigParser()

    if (os.path.isfile( os.path.normpath(home + config_file ))):
        config_s3cmd.read(os.path.normpath(home + config_file))
        config_s3cmd.set('default', 'access_key', myvars["accessKey"])
        config_s3cmd.set('default', 'secret_key', myvars["secretKey"])
        config_s3cmd.set('default', 'access_token', myvars["sessionToken"])
    else:
        create_default_config(home, config_file)
        config_s3cmd.read( os.path.normpath(home + config_file))
        s3cmd_info = {
            'access_key': myvars["accessKey"],
            'secret_key': myvars["secretKey"],
            'access_token': myvars["sessionToken"],
            'bucket_location': "US",
            'cloudfront_host': 'cloudfront.amazonaws.com',
            'default_mime_type': 'binary/octet-stream',
            'delete_removed': 'False',
            'dry_run': 'False',
            'enable_multipart': 'True',
            'encoding': 'UTF-8',
            'encrypt': 'False',
            'follow_symlinks': 'False',
            'force': 'False',
            'get_continue': 'False',
            'gpg_command': '/usr/bin/gpg',
            'gpg_decrypt': '%(gpg_command)s -d --verbose --no-use-agent --batch --yes --passphrase-fd %(passphrase_fd)s -o %(output_file)s %(input_file)s',
            'gpg_encrypt': '%(gpg_command)s -c --verbose --no-use-agent --batch --yes --passphrase-fd %(passphrase_fd)s -o %(output_file)s %(input_file)s',
            'gpg_passphrase': '',
            'guess_mime_type': 'True',
            'host_base': 's3.amazonaws.com',
            'host_bucket': '%(bucket)s.s3.amazonaws.com',
            'human_readable_sizes': 'False',
            'invalidate_on_cf': 'False',
            'list_md5': 'False',
            'log_target_prefix': '',
            'mime_type': '',
            'multipart_chunk_size_mb': '15',
            'multipart_copy_size': '15728640',
            'preserve_attrs': 'True',
            'progress_meter': 'True',
            'proxy_host': '',
            'proxy_port': '0',
            'recursive': 'False',
            'recv_chunk': '4096',
            'reduced_redundancy': 'False',
            'send_chunk': '4096',
            'simpledb_host': 'sdb.amazonaws.com',
            'skip_existing': 'False',
            'socket_timeout': '300',
            'urlencoding_mode': 'normal',
            'use_https': 'False',
            'verbosity': 'WARNING',
            'website_endpoint': 'http://%(bucket)s.s3-website-%(location)s.amazonaws.com/',
            'website_error': '',
            'website_index': 'index.html'
        }
        #config_s3cmd.add_section('default')
        for key in s3cmd_info.keys():
            config_s3cmd.set('default', key, s3cmd_info[key])
    with open( os.path.normpath(home + '/ndar_toolkit/.s3cfg'), 'wt') as configfile:
        config_s3cmd.write(configfile)

if __name__ == '__main__':


    if not os.path.exists (os.path.normpath(home + "/ndar_toolkit")):
        os.makedirs (os.path.normpath(home + "/ndar_toolkit"))

    if (os.path.isfile( os.path.normpath(home + '/ndar_toolkit/ndar_update_keys.sh' ))):
        ndar_username, ndar_password = shell_source(os.path.normpath(home + '/ndar_toolkit/ndar_update_keys.sh'))
    
    if (os.environ.get('ndar_username')):
        ndar_username = os.environ.get('ndar_username')
    try: 
        ndar_username
    except NameError:
        if sys.version_info[0] < 3:
            ndar_username = raw_input("ndar_username not set, please enter it now: ")
        else:
            ndar_username = input("ndar_username not set, please enter it now: ")
        f = open( os.path.normpath(home + '/ndar_toolkit/ndar_update_keys.sh'), 'wt')
        f.write('export ndar_username=' + str(ndar_username) + '\n' )
        #ndar_username = 'USERNAME' # Replace USERNAME with your NDAR username
    
    if (os.environ.get('ndar_password')):
        ndar_password = os.environ.get('ndar_password')
    try:
        ndar_password
    except NameError:
        ndar_password = getpass.getpass("ndar_password is not set, please enter it now: ")
        f.write('export ndar_password=' + str(ndar_password) + '\n')
        f.close()
        #ndar_password = 'PASSWORD' # Replace password with your NDAR password
    
    
    # Creates location for aws credentials files
    if not os.path.exists ( os.path.normpath(home + '/ndar_toolkit/.aws/')):
        os.makedirs ( os.path.normpath(home + '/ndar_toolkit/.aws/'))
        #os.makedirs ( '/root/.aws/' )
    
    if not (os.path.isfile( os.path.normpath(home + '/ndar_toolkit/downloadmanager.jar' ))):
        download_file("https://ndar.nih.gov/jnlps/download_manager_client/downloadmanager.zip", os.path.normpath(home + '/ndar_toolkit/downloadmanager.zip'))
        unzip_file( os.path.normpath(home + "/ndar_toolkit/downloadmanager.zip" ))
    
    if not (os.path.isfile( os.path.normpath(home + '/s3cmd-master/s3cmd' ))):
        download_file("https://github.com/s3tools/s3cmd/archive/master.zip", home + '/s3cmd-master.zip')
        unzip_file( os.path.normpath(home + '/s3cmd-master.zip'))
        for i, line in enumerate(fileinput.input( os.path.normpath(home + '/ndar_toolkit/s3cmd-master/S3/S3.py'), inplace=1)):
            sys.stdout.write(line.replace('self.s3.config.role_refresh()', 
                                          '# Role refresh is with NDAR Download Manager\n# self.s3.config.role_refresh()')) 
        st = os.stat(os.path.normpath(home + '/ndar_toolkit/s3cmd-master/s3cmd'))
        os.chmod(os.path.normpath(home + '/ndar_toolkit/s3cmd-master/s3cmd'), st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        
        if not os.path.exists ( os.path.normpath(home + '/bin/' )):
            os.makedirs ( os.path.normpath(home + '/bin/' ))
    
        if os.path.lexists( os.path.normpath(home + '/bin/s3cmd')):
            os.remove( os.path.normpath(home + '/bin/s3cmd'))
        try:
            os.symlink(os.path.normpath(home + '/ndar_toolkit/s3cmd-master/s3cmd'), home + '/bin/s3cmd')
        except:
            pass
    devnull = open(os.devnull, 'w')
    print ("Generating new keys and updating config files")
    os.chdir( os.path.normpath(home + "/ndar_toolkit"))
    status=call('java -jar ' + os.path.normpath(home + '/ndar_toolkit/downloadmanager.jar') + ' --generate awskeys.txt '
                + '--username "' + ndar_username + '" '
                + '--password "' + ndar_password +'" 2>&1 /dev/null',
                #shell=True)
                shell=True, stdout=devnull, stderr=devnull)

    myvars={}
    with open (os.path.normpath(home + "/ndar_toolkit/awskeys.txt")) as keysfile:
    	for line in keysfile:
            #line = line.replace(r'\r', '')
            name, var = line.partition("=")[::2]
            var = var.replace('\r', '')
            myvars[name.strip()] = str(var)
    
    os.environ["AWS_ACCESS_KEY_ID"] = myvars["accessKey"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = myvars["secretKey"]
    os.environ["AWS_SESSION_TOKEN"] = myvars["sessionToken"]

    #Additional entries may be necessary depending on environment, to write configuration file to home directory
    write_aws_config( home, '/ndar_toolkit/.aws/credentials', 'NDAR')
    write_aws_config( home, '/ndar_toolkit/.aws/config', 'profile NDAR')
    write_s3cmd_config( home, '/ndar_toolkit/.s3cfg')
