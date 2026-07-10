# Luminosity
Used brilcalc with on the Golden JSONs stored in the main analysis repository (were taken from [twiki](https://twiki.cern.ch/twiki/bin/view/CMS/DCUserPage)).
```
 brilcalc lumi --normtag  /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -i PATH/TO/GOLDEN/JSON/FILENAME.txt
```
The results were piped into text files in my lxplus EOS space in the `Corrections` directory.
`luminoisty_in_fb.json` contains the totrecorded result.

# Parsing a reweight card
To get the EFT reweight points