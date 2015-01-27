# Some instructions with code examples for accessing objects in s3 using NDAR credentials (username/password)

## Ensure you have Java installed.

## Obtain a copy of NDAR's command-line download manager

The command-line download manager is a stand-alone java file that can be used to download packages, or to provide keys for accessing shared objects in Amazon S3 storage.

### Download

```shell
wget https://ndar.nih.gov/jnlps/download_manager_client/downloadmanager.zip
```

OR

```shell
curl https://ndar.nih.gov/jnlps/download_manager_client/downloadmanager.zip -o downloadmanager.zip
```

### Unzip

```shell
unzip downloadmanager.zip
```

## Use the command-line download manager to generate temporary Amazon S3 security credentials

```shell
java -jar downloadmanager.jar -g awskeys.txt
```

You will be prompted for your ndar username and password, after which you will be able to find your keys in the file awskeys.txt

```shell
more awskeys.txt
```

You will see something like this from  your awskeys.txt file.

```shell
accessKey=ASIAJ3GPA2W73EXAMPLE
secretKey=0i8oIpzWbbVDaybWxmK2vsZsiaSPSdeXEXAMPLE
sessionToken=AQoDYXdzEPX//////////wEaoAKf5O7+2FhbYIqed/oh69l6FuVuaxpanNbA2yCR/1iYB4cjqQ415FUhDVIN4E4fXF9j8FzV4cTE6vY0dLzOWcUq7dNLvFzJux3oh0bu4bqbZ9EwBAxKb4bNf1pSbUWjQ+Sgrnjz38Uf63jSpxWAUM66mFVOPJhyaHh5lnUREZMNJrwzrkoUn6SR4fTEjXBuQRh9n4idllP+GW7i5XncDqZz+LutYgYMSGjb3x2j1hO1jCyRQ0dtFltFtaq77onMrCnk8k5YCmWyEFgfECtmu0fFE5hpy2NDLg2cFz1aVGN0K2B9vkOPEhG1LIm5+TY8U3MhWQsBnGvGCe0dO/4EOSJfJDhZZe+LsUhVhLJJWnQPRUcqpfNRWU8VnTHxadPLEXAMPLE=
expirationDate=Tue Nov 18 03:14:16 EST 2014
```

## Use the Amazon keys to configure your choice of tool to access files in s3

###[AWS Command Line (aws-cli)](aws-cli)

###[s3tools s3cmd](s3cmd)
***

### aws-cli
<a id=aws-cli></a>
This tool comes pre-packaged with Amazon Linux AMIs
#### Getting Set up
<http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html>
#### Installation
<http://docs.aws.amazon.com/cli/latest/userguide/installing.html>
#### Configuration
<http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html>

You should be able to find the credentials file located in your home directory

```shell
cd ~/.aws/
vim credentials
```

Create a new profile for your temporary credentials (credentials will expire in ~ 24 hours)

```shell
[NDAR]
```

Add your credentials to the profile, watch out to make sure the keys are all on one line without any line breaks, or extra white space at the end.

```shell
[NDAR]
aws_access_key_id=ASIAJ3GPA2W73EXAMPLE
aws_secret_access_key=0i8oIpzWbbVDaybWxmK2vsZsiaSPSdeXEXAMPLE
aws_session_token=AQoDYXdzEPX//////////wEaoAKf5O7+2FhbYIqed/oh69l6FuVuaxpanNbA2yCR/1iYB4cjqQ415FUhDVIN4E4fXF9j8FzV4cTE6vY0dLzOWcUq7dNLvFzJux3oh0bu4bqbZ9EwBAxKb4bNf1pSbUWjQ+Sgrnjz38Uf63jSpxWAUM66mFVOPJhyaHh5lnUREZMNJrwzrkoUn6SR4fTEjXBuQRh9n4idllP+GW7i5XncDqZz+LutYgYMSGjb3x2j1hO1jCyRQ0dtFltFtaq77onMrCnk8k5YCmWyEFgfECtmu0fFE5hpy2NDLg2cFz1aVGN0K2B9vkOPEhG1LIm5+TY8U3MhWQsBnGvGCe0dO/4EOSJfJDhZZe+LsUhVhLJJWnQPRUcqpfNRWU8VnTHxadPLEXAMPLE=
```

Specify your default region

```shell
[NDAR]
aws_access_key_id=ASIAJ3GPA2W73EXAMPLE
aws_secret_access_key=0i8oIpzWbbVDaybWxmK2vsZsiaSPSdeXEXAMPLE
aws_session_token=AQoDYXdzEPX//////////wEaoAKf5O7+2FhbYIqed/oh69l6FuVuaxpanNbA2yCR/1iYB4cjqQ415FUhDVIN4E4fXF9j8FzV4cTE6vY0dLzOWcUq7dNLvFzJux3oh0bu4bqbZ9EwBAxKb4bNf1pSbUWjQ+Sgrnjz38Uf63jSpxWAUM66mFVOPJhyaHh5lnUREZMNJrwzrkoUn6SR4fTEjXBuQRh9n4idllP+GW7i5XncDqZz+LutYgYMSGjb3x2j1hO1jCyRQ0dtFltFtaq77onMrCnk8k5YCmWyEFgfECtmu0fFE5hpy2NDLg2cFz1aVGN0K2B9vkOPEhG1LIm5+TY8U3MhWQsBnGvGCe0dO/4EOSJfJDhZZe+LsUhVhLJJWnQPRUcqpfNRWU8VnTHxadPLEXAMPLE=
region=us-east-1
```

#### Use credentials profile to list and access s3 objects
Listing a bucket

```shell
aws --profile NDAR ls s3://NDAR_Central/
```
Accessing an object

```shell
aws --profile NDAR ls s3://NDAR_Central/
#List a submission folder
aws --profile NDAR ls s3://NDAR_Central/submission_9944/
#Stream a VCF file to stdout
aws --profile NDAR s3 cp s3://NDAR_Central/submission_9944/AU-9201_3.vcf -
#If you do not specify an output file (including stdout) the s3object will be copied to a file with the same name.
```

### s3cmd
<a id='s3cmd'></a>
This tool can be downloaded from github
#### Getting Set up
download s3cmd

```shell
curl https://github.com/s3tools/s3cmd/archive/master.zip -o master.zip
```

OR

```shell
wget https://github.com/s3tools/s3cmd/archive/master.zip
```

Unzip

```shell
unzip master.zip
```

#### Installation

```shell
cd s3cmd-master
python setup.py installed
```

#### Configuration
You can run the configuration for s3cmd and input your access and secret keys, you will have to manually edit the s3cfg file to add the security token.

```shell
s3cmd --configure
```

Add the security token, you should already see entries for access_key and secret_key from running the --configure option.  The configuration file should be in your home directory, and it is named .s3cf

```shell
vim ~/.s3cfg
access_token = AQoDYXdzEPX//////////wEaoAKf5O7+2FhbYIqed/oh69l6FuVuaxpanNbA2yCR/1iYB4cjqQ415FUhDVIN4E4fXF9j8FzV4cTE6vY0dLzOWcUq7dNLvFzJux3oh0bu4bqbZ9EwBAxKb4bNf1pSbUWjQ+Sgrnjz38Uf63jSpxWAUM66mFVOPJhyaHh5lnUREZMNJrwzrkoUn6SR4fTEjXBuQRh9n4idllP+GW7i5XncDqZz+LutYgYMSGjb3x2j1hO1jCyRQ0dtFltFtaq77onMrCnk8k5YCmWyEFgfECtmu0fFE5hpy2NDLg2cFz1aVGN0K2B9vkOPEhG1LIm5+TY8U3MhWQsBnGvGCe0dO/4EOSJfJDhZZe+LsUhVhLJJWnQPRUcqpfNRWU8VnTHxadPLEXAMPLE=
```

You can copy the existing configuration file to create multiple config files 'or profiles' and use a specific config file when running s3cmd using the --config option.

```shell
cp ~/.s3cfg ~/.s3cfg_ndar
```

#### Use credentials profile to list and access s3 objects
Listing a bucket

```shell
s3cmd --config ~/.s3cfg_ndar ls s3://NDAR_Central/
```

Accessing an object

```shell
s3cmd --config ~/.s3cfg_ndar ls s3://NDAR_Central/
#List a submission folder
s3cmd --config ~/.s3cfg_ndar ls s3://NDAR_Central/submission_9944/
#Stream a VCF file to stdout
s3cmd --config ~/.s3cfg_ndar get s3://NDAR_Central/submission_9944/AU-9201_3.vcf -
#If you do not specify an output file (including stdout) the s3object will be copied to a file with the same name.
```





