# Effective Field Theory event weights
In the central TTto2L2Nu and TTtoLNu2Q SMEFTsim samples, we generate the sample at one point in EFT space then calculate an event weight to reweight from the generation point to 350+ other EFT points.
`EFTWeights.py` interacts with these reweight points.

`parse_rwgt_card()` can read in the reweight card used to generate a sample (e.g. central_rwgt_card.dat) and index every reweight point to its corresponding index in the branch LHEReweightingWeight.
The result of this indexing is stored in a json.

When parameterizing the event weights per coefficient pair, we give the json to `calculate_structure_constants()` for its fitting procedure.
The results of this procedure are the fitted "structure constants" and their residuals.
