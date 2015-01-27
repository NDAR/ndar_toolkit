ndar_toolkit
============

#Introduction
Scripts and Instructions to aid in automating integration with NDAR tools and data

#Manual Instructions
##[how_to_access_s3_objects.md](https://github.com/NDAR/ndar_toolkit/blob/master/how_to_access_s3_objets.md)

#Available Scripts
## [ndar_update_keys.py](https://github.com/NDAR/ndar_toolkit/blob/master/ndar_update_keys.py)
1. Downloads NDAR command-line download manager, used to generate aws credentials from an NDAR username/password.
2. Downloads s3cmd from s3tools.org (https://github.com/s3tools/s3cmd)
3. Writes configuration files for s3cmd and for Amazon's command-line tool, using credentials generated from the download manager

To Use (run each time you want new keys):
```shell
sudo python ndar_update_keys.py
```

After initial run:
```shell
cd s3cmd-master
python setup.py install
```

Now you can use s3cmd:
```shell
s3cmd ls s3://NDAR_Central/
```


