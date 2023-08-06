# Lamin Lake

Lamin Lake is the biological data management system.

## Installation and configuration

Install the development version:
```
flit install -s --deps develop
```
Then configure laminlake for use with Notion:
```
laminlake configure
```
and AWS (`pip install awscli`):
```
aws configure
```

## Tutorials

* Notion integration: https://github.com/laminlabs/laminlake/blob/main/tutorials/notion.ipynb
* Ingesting Eraslan21: https://github.com/laminlabs/usecases/blob/main/ingest-eraslan21.ipynb
