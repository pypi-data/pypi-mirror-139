"""Provides common JupiterOne queries."""

# Returns all running GCP Compute Instances which permits traffic inbound from the
# internet - using a protocol of TCP or 'ALL'.
INTERNET_LISTENERS_GCP_COMPUTE = """
  FIND google_compute_instance AS i
  THAT HAS google_compute_subnetwork
  THAT CONTAINS google_compute_network
  THAT PROTECTS google_compute_firewall
  THAT ALLOWS Internet
 WHERE i.status != 'TERMINATED'
   AND (ALLOWS.ipProtocol='tcp' OR ALLOWS.ipProtocol='all')
   AND i.publicIpAddress != undefined
RETURN
    i.id AS id,
    i._type AS type,
    i.zone AS location,
    i.displayName AS name,
    ALLOWS.toPort AS to_port,
    ALLOWS.fromPort AS from_port,
    i.publicIpAddress AS ip_addr,
    i.projectId,
    i.status,
    i.serviceAccountEmails,
    i.tag.AccountName
"""

# Returns all running AWS EC2 Instances which permit traffic inbound from the internet -
# using a protocol of TCP or 'ALL' ('*').
INTERNET_LISTENERS_AWS_EC2 = """
  FIND aws_instance
  WITH state != 'stopped'
   AND state != 'terminated'
   AND publicIpAddress != undefined AS i
  THAT PROTECTS aws_security_group
  THAT ALLOWS Internet
 WHERE ALLOWS.ingress=true
   AND (ALLOWS.ipProtocol='tcp' OR ALLOWS.ipProtocol='*')
RETURN
    i.instanceId AS id,
    i._type AS type,
    i.region AS location,
    i.name AS name,
    ALLOWS.toPort AS to_port,
    ALLOWS.fromPort AS from_port,
    i.publicIpAddress AS ip_addr,
    i.launchTime,
    i.ownerId,
    ALLOWS.ipProtocol
"""

# Returns all running Azure VMs which permit traffic inbound from the internet - using
# a protocol of TCP or 'ALL'.
INTERNET_LISTENERS_AZURE_VM = """
  FIND azure_vm AS i
  THAT USES azure_nic as n
  THAT PROTECTS azure_security_group
  THAT ALLOWS Internet
 WHERE n.publicIp != undefined
   AND ALLOWS.direction = "Inbound"
   AND (ALLOWS.ipProtocol = 'tcp' OR ALLOWS.ipProtocol='all')
RETURN
    i.vmId AS id,
    i._type AS type,
    i.region AS location,
    i.name as name,
    ALLOWS.toPort AS to_port,
    ALLOWS.fromPort AS from_port,
    n.publicIp AS ip_addr,
    i.id,
    i.platform
"""
