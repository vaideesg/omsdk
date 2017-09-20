UpdateRepo=SDKRepo
echo "Creating Update Repo Directory"
mkdir %UpdateRepo%

REM Initializing Modules
CollectInventory=omdrivers.helpers.iDRAC.CollectInventory
RepoBuilder=omdrivers.helpers.iDRAC.RepoBuilder
CompareInventory=omdrivers.helpers.iDRAC.CompareInventory

echo "1. Collect inventory for Representative iDRACs"
echo "   Inventory is stored under %UpdateRepo%\_inventory folder"
echo "   Each server inventory is stored as <ipaddr>_firmware.json"
python -m %CollectInventory% -f %UpdateRepo% -u root -p calvin -i 192.168.1.10 192.168.1.11
python -m %CollectInventory% -f %UpdateRepo% -u root -p another_password -i 192.168.1.12 192.168.1.13
REM ....

echo "2. Download catalog from downloads.dell.com and prepare Scoped Catalog"
echo "   Master Catalog is downloaded to %UpdateRepo%\_master\Catalog.xml"
echo "   Scoped Catalog is catalog scoped to inventory collected from above"
echo "   step.  It is stored under %UpdateRepo%\Catalog.xml"

REM Download using http from downloads.dell.com
python -m %RepoBuilder% -f %UpdateRepo% -v -l -b

REM Download using ftp from ftp.dell.com
REM python -m %RepoBuilder% -f %UpdateRepo% -v -l -b -p FTP -s ftp.dell.com

REM You can also create scoped catalog for specific components with a different
REM name.  Ex: Build a BIOS only catalog and name it 'BIOS_Catalog'
REM BIOS_Catalog.xml will be created in %UpdateRepo% containing BIOS updates
REM of all servers for which inventory was collected previously.
REM python -m %RepoBuilder% -f %UpdateRepo% -v -l -b -C BIOS_Catalog -c BIOS

REM Ex: Build a NIC and BIOS only catalog and name it BIOS_NIC
REM python -m %RepoBuilder% -f %UpdateRepo% -v -l -b -C BIOS_NIC -c BIOS NIC

echo "3. Download DUPs from downloads.dell.com corresponding to scoped catalog"
echo "   DUPs are stored under %UpdateRepo%. DUPs are downloaded only if "
echo "   new files are available in the downloads.dell.com site, files"
echo "   on local folder are corrupted/not present"
echo "   Downloads of DUP takes a long time, so plan for this activity!"

REM Download using http from downloads.dell.com
python -m %RepoBuilder% -f %UpdateRepo% -v -D

REM Download using ftp from ftp.dell.com
REM python -m %RepoBuilder% -f %UpdateRepo% -v -l -D FTP -s ftp.dell.com

REM Download BIOS only catalog DUPs
REM python -m %RepoBuilder% -f %UpdateRepo% -v -l -D -C BIOS_Catalog

echo "4. Check if the downloaded files are good."
echo "   Present        - No info in Master Catalog to verify goodness"
echo "   Same           - Downloaded file matches Master Catalog info"
echo "   Different      - Download file does not match Master Catalog info"
echo "   Does not exist - File in Master Catalog, not present in UpdateRep"

python -m %RepoBuilder% -f %UpdateRepo% -p HashCheck

echo "5. Find out what components will be updated from catalog"
echo "   Generates a CSV to stdout comparing inventory against a catalog"
echo "   The CSV contains following fields:"
echo "       Device        - Service Tag of the device"
echo "       Component     - Firmware component"
echo "       UpdateNeeded  - Whether Update is required or not (True or False)"
echo "       UpdatePackage - Whether Update package is present in catalog"
echo "                       Absent  - no update is published by Dell yet"
echo "                       Present - update is published by Dell"
echo "       UpdateType    - Type of the update"
echo "                       Upgrade   - Server firmware needs upgrade"
echo "                       Downgrade - Server firmware needs downgrade"
echo "                       On_Par    - Server firmware is up-to-date"
echo "                       Unknown   - Firmware absent in Catalog"
echo "       Server.Version - Version of Firmware in Server"
echo "       Catalog.Version- Version of Firmware in Catalog"
echo "       Reboot Required - Whether reboot is required when applying update"
python -m %CompareInventory% -f %UpdateRepo% -o csv

REM Now export the %UpdateRepo% as a Share that is accessible to iDRAC
REM Let's say the %UpdateRep% was present on host %myhost% and exported as
REM 'RepoShare', and the credentials to access it are domain\update_user
REM with password *****.  You can use idrac.update_mgr.update_from_repo()
REM to update the servers as follows:
REM 
REM     reposhare = FileOnShare(remote='\\\\%myhost%\\RepoShare',
REM                 isFolder=True,
REM                 creds=UserCredentials('update_user@domain', '*****'))
REM     UpdateManager.configure(reposhare)
REM     if UpdateManager.IsValid:
REM          idrac.update_mgr.update_from_repo(catalog_path='Catalog')
REM
REM You can use the following to update only BIOS and NIC
REM          idrac.update_mgr.update_from_repo(catalog_path='BIOS_NIC')
