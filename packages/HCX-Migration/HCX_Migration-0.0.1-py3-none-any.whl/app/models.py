# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present HCL
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class customer(models.Model):
    name = models.CharField(max_length=100,help_text='Enter a Customer Name')

class datacenter(models.Model):
    username = models.CharField(max_length=100,help_text='Enter a Datacenter Username')
    password = models.CharField(max_length=100,help_text='Enter a Datacenter Password')
    ipaddress = models.CharField(max_length=100,help_text='Enter a Datacenter IpAddress')
    dctype =  models.CharField(max_length=1, choices=(('0','On-Prem/AVS1.0'),('1','AVS 2.0'),), blank=True, default='0', help_text='Datacenter Type',)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class MoveGroup(models.Model):
    name = models.CharField(max_length=100,help_text="Enter the MoveGroup Name")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class MoveGroupVM(models.Model):
    name = models.CharField(max_length=200,help_text="Enter VM Name in the MoveGroup")
    vmtools = models.IntegerField()
    hardware = models.IntegerField()
    mac = models.IntegerField()
    movegroup = models.ForeignKey(MoveGroup, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class MigrationCheckup(models.Model):
    runid = models.IntegerField() 
    vmgrpid = models.IntegerField()
    extype = models.CharField(max_length=4,choices=(('Pre','Pre'),('Post','Post')))
    
    
class DRSRules(models.Model):
    runid = models.ForeignKey(MigrationCheckup,on_delete=models.CASCADE)
    Name = models.CharField(max_length=200)
    Type = models.TextField()
    VM = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
class Storage(models.Model):
    runid = models.ForeignKey(MigrationCheckup,on_delete=models.CASCADE)
    VM = models.TextField()
    HardDiskName = models.TextField()
    DiskSize = models.TextField()
    DiskCount = models.TextField()
    Multi_Writer = models.TextField()
    Disk_Type = models.TextField()
    StoragePolicy = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
class VMDetail(models.Model):
    runid = models.ForeignKey(MigrationCheckup,on_delete=models.CASCADE)
    VM = models.TextField()
    Powerstate = models.TextField()
    ToolsVersion = models.TextField()
    HardwareVersion = models.TextField()
    Snapshot = models.TextField()
    OS = models.TextField()
    ISO = models.TextField()
    Host = models.TextField()
    Datastore = models.TextField()
    Uptime = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
class Network(models.Model):
    runid = models.ForeignKey(MigrationCheckup,on_delete=models.CASCADE)
    VM = models.TextField()
    NIC = models.TextField()
    IPAddress = models.TextField()
    PortGroup = models.TextField()
    MacAddress = models.TextField()
    ConnectionStatus = models.TextField()
    Ping_Status = models.TextField()
    RDP = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class status(models.Model):
    runid = models.IntegerField()
    total = models.IntegerField(default=0)
    drstotal = models.IntegerField(default=0)
    drs = models.IntegerField(default=0)
    vmdetail = models.IntegerField(default=0)
    network = models.IntegerField(default=0)
    storage = models.IntegerField(default=0)