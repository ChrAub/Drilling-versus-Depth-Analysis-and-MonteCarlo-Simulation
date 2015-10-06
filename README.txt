The code provided here takes time versus depth drilling data (in form of csv-files). 

For a single well it performes some analysis. It calculates among other data:
the ratio between productive and non-productive time
average rate of penetration for each drilling phase
reaming time per meter of hole section
top 5 error codes and their related lengths

If a couple of wells are given it performes a Monte-Carlo simulation to estimate drilling time for future wells. 
For that purpose available well data are scanned and analysed. For each different action durations are recorded (there is also code commented out that prints histogramms). 
An approbriate distribution is assigned to them in order to generate random values. 
The Monte-Carlo simulation is then performed to compare two different strategies (low costs/long drilling time versus high costs/short drilling time).
For both scenarios a couple of distributions for different KPI is available.  

