# UCM Methods

A scipion plugin with electron-microscopy validation methods, based on maps
that expose local quantities of interest related to the given electron-density
volumes.

The methods are developed by the Cryo-EM group at the
[UCM](https://www.ucm.es/doptica).

## Install

To install it, you can just clone this repository and install it with the
standard scipion command to install plugins:

```sh
git clone https://gitlab.com/jordibc/scipion-em-ucm.git

scipion3 installp -p scipion-em-ucm --devel
```

Next time you open scipion, there should be two new protocols (in
`Protocols SPA -> 3D -> Analysis -> Validation`) called `local b-factor` and
`local occupancy`.
