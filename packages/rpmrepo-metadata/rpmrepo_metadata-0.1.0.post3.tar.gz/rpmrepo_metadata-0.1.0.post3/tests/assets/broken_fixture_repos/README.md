# Broken repos

These repos have problems that make them not technically correct even if Yum and DNF can handle them.

* Gitlab-ce
  * filelists.xml is empty and declares 0 packages, which does not match the count in the other xml files
* centos7-opstools
  * packages with duplicate NEVRA and different pkgids
* ms-prod
  * packages with duplicate NEVRA and different pkgids
  * some packages have (millions of) duplicate file paths
* hashicorp-f35
  * packages with duplicate NEVRA and different pkgids
* perfsonar
  * packages with duplicate NEVRA and the SAME pkgids
* RHEL6
  * more package entries than declared in the header