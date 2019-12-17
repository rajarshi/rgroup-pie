# rgroup-pie
PoC code to generate a structure depictions with partial pie charts centered on R group atoms

The code is inspired by Fig 3 in [Doyon et al](https://pubs.acs.org/doi/10.1021/jacs.9b10474)
which was developed by [Attabey Rodríguez Benítez](https://twitter.com/ScienceBey). The original
visualization was designed to summarize substrate scope but can be generalized to plot any number(s)
associated with R-groups (e.g., bioactivity)

The code uses the [OEChem](https://www.eyesopen.com/oechem-tk) so you'll need a license to run it.

There is an example MOL file with a single R group - I've hardcoded the program to look for `R1`. It 
doesn't color the segments by gradient or label the segments with names or structures but that is 
relatively straightforward.

The output of the script with the MOL file in this repository is

![alt text](https://github.com/rajarshi/rgroup-pie/blob/master/MolWithWedgeChart.png)