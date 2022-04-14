# Molstar Viewer

[Molstar](https://molstar.org) is a web application for visualizing structures of macromolecules. For an example visualization, see [here](https://pdb-dev.wwpdb.org/view3d.html?PDBDEV_00000001). 

We can incorporate Molstar in the PDB-Dev Deriva catalog so that users can visualize the structures directly. 

The software is maintained in a public [Git repository](https://github.com/molstar/molstar).  

More information on embedding Molstar viewer: https://unpkg.com/browse/molstar@3.6.1/build/viewer/.

The `unpkg` directory contains the `RAW` version of the `molstar.js` and `molstar.css` files.

The `embedded.html` file was slightly modified to allow supplying the `mmCIF` file as the `url` parameter in the `URL` query search.

### Installation

1. Create the `/var/www/html/molstar` directory.
2. Copy the following files from the `unpkg` directory into the `/var/www/html/molstar` directory:
```
embedded.html
favicon.ico
molstar.css
molstar.js
```

### Visualization

Supposing the installation was done on the `dev.pdb-dev.org` VM, and that the `mmCIF` file location is:
```/hatrac/dev/pdb/entry/2022/D_1-VSA6/final_mmCIF/PDBDEV_00000128.cif:3RAYRI5CC5GPMLCGEW34BFGKVY
```
on a browser, enter the following URL:
```
https://dev.pdb-dev.org/molstar/embedded.html?url=/hatrac/dev/pdb/entry/2022/D_1-VSA6/final_mmCIF/PDBDEV_00000128.cif:3RAYRI5CC5GPMLCGEW34BFGKVY
```
