# Data reporting in CalliCog

## Summary

The CalliCog webapp can be used to both rapidly monitor live data and to extract metadata for offline analysis. In this regard, the webapp acts as an interface between the user and the relational database that ties all experimental data to user-defined experimental parameters. Functions for data reporting are provided under the `REPORT` tabs.

## Monitoring and extracting data based on experiments

The `Experiments` tab contains a list of all experiments written to the local database, each of which is assigned a unique experiment ID. The list contains summarised information on each experiment, including the start and end time of the experiment and whether the experiment is currently ongoing. **Note:** When initialising experiments from the command line, the `resume` command can only be used for experiments with a `Status` of "ongoing".

Users can implement basic search filters (animal, template, start/end and experiment ID) to query the list of experiments. To view summarised data of the individual experiments, click on the link in the `Start` column. This will then display the animal's progression through the experiment, including trial outcomes, session performance, current task, and more.

In the `Experiments` tab, users can view the raw, non-summarised data from an experiment by selecting `Export`. This will export all metadata for the experiment in .csv format.

**Note:** Exported data contains **ALL** data and users may find it difficult to navigate. This is because multidimensional data from relational databases do not convert well to tabular formats (a reason why relational databases are so powerful). Thus, exported data is mainly intended for "looking under the hood" or post-processing pipelines.

In the exported data, rows are organised per individual stimuli, which are further grouped into windows, trials, and so on. For improved search compatibility, all levels of design (stimulus, window, trial, session, experiment) are assigned unique IDs. 
