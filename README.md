# download oc-mirror
``` 
python oc-mirror-download.py --ocpversion 4.10.10
```
# download ocp
```
python ocdownload.py --product ocp --ocpversion 4.10.10 --registryurl docker://registry.swarchpoc.com
```
# download an operator
```
python ocdownload.py --product operator --ocpversion 4.10.10 --registryurl docker://registry.swarchpoc.com  --opname compliance-operator --opversion 0.1.53 --opchannel release-0.1
python ocdownload.py --product operator --ocpversion 4.10.10 --registryurl docker://registry.swarchpoc.com  --opname odf-operator --opversion 4.9.6 --opchannel stable-4.9
```

# Host prep steps

1. Install software
    1. oc
    2. python3
    3. pip3
    4. git
    5. podman
```
yum install podman
wget https://github.com/fullstorydev/grpcurl/archive/v1.5.1.tar.gz
tar -zxvf v1.5.1.tar.gz
cd grpcurl-1.5.1/cmd/grpcurl/
yum install -y go
cd grpcurl-1.5.1/cmd/grpcurl/
go build
mv grpcurl /usr/local/bin
yum install -y unzip
yum install python39
ln -s /usr/bin/python3 /usr/bin/python
sudo dnf  install s3cmd
sudo yum install git
sudo yum install -y skopeo
sudo chmod 777 /var/lib/containers/sigstore/
 
```
```
sudo dnf install python3-pip
sudo pip3 install python-dotenv
```

