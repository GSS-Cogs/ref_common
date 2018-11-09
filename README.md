# Common Reference Data

Datasets are grouped into families where a family of datasets shares common components and codelists.

This repository is used where more than one family shares common components or codelists and contains:

- [components.csv](./components.csv) a list of the dimensions, measures, and attributes used/reused across more than one dataset family
- [codelists.csv](./codelists.csv) a list of the codelists used across more than one dataset family, the individual lists are in the [codelists](./codelists) directory.
- [columns.csv](./columns.csv) a configuration file describing how to turn common columns in csv input data into a linked-data cube (for the table2qb conversion process).
