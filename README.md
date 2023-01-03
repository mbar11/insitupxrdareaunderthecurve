# insitupxrdareaunderthecurve
Script that will calculate the area under the curve at each point through an in-situ pxrd run. Script has been optimized for Spyder, but could be adapted as needed for other UI's etc.

Be sure to import the environment (insitu.yml file) to Anaconda, and run with Spyder 5.4.1. Also assure the backend is Qt5 (Spyder settings (wrench)->IPython console->Graphics->Graphics backend-> Qt5). All of this info should be included in the environment file (.yml).

File type can be modified for other types, as of now .xyd files all files will be added to a pandas notebook (if other file types are selected in the second button the script will only import .xyd file types). The baseline can be adjusted through maniuplating the degree of the peakutils baseline fitter. From there, ranges of 2 theta surrounding peaks of interest can be selected (do not worry about y here, just select the optimal x range). Running the next cell will then calculate the area under the desired peaks as a function of the file index. This information can then be saved to an excel file with two sheets (1 with area as function of time and the second with all subtracted baseline patterns). 

Please don't hesitate to reach out with questions/issues/etc (michaelbarsoum2026@u.northwestern.edu).
