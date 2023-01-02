# insitupxrdareaunderthecurve
Script that will calculate the area under the curve at each point through an in-situ pxrd run.

If importing .xyd files all files will be added to a pandas notebook. The baseline can be adjusted through maniuplating the degree of the peakutils baseline fitter. From there, ranges of 2 theta surrounding peaks of interest can be selected (do not worry about y here, just select the optimal x range). Running the next cell will then calculate the area under the desired peaks as a function of the file index. This information can then be saved to an excel file with two sheets (1 with area as function of time and the second with all subtracted baseline patterns). 

Please don't hesitate to reach out with questions/issues/etc.
