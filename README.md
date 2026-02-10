# TibSchol Dynamic Archive

Last change: 2026-02-10

This repository contains the dataset created in the ERC-funded project *The Dawn of Tibetan Buddhist Scholasticism (11th-13th c.) (TibSchol).* Cf. [https://www.oeaw.ac.at/ikga/tibschol](https://www.oeaw.ac.at/projects/tibschol/home) for more information.

This project, hosted at the Institute for Cultural and Intellectual History of Asia of the Austrian Academy of Sciences <https://www.oeaw.ac.at/ikga>, has received funding from the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme (grant agreement No. 101001002). See <https://cordis.europa.eu/project/id/101001002>. 

## Directory Structure

| Directory | Content | Remarks | 
| --------- | ------- | --------| 
| `.github/workflows` | xxx | xxx |
| `data` | Dataset | 7 folders |
| `scripts` | xxx | xxx |

## Archived Data
The archived data is located in the directory *data*, under the folder corresponding to the entity type (work, instance, person, place). 

The relevant .json file is named after the TibSchol ID of the entity in [TibSchol database](https://tibschol.acdh-ch-dev.oeaw.ac.at/). For instance, [3831.json] (https://github.com/ERC-TibSchol/tibschol-archive/blob/main/data/apis_ontology_person/3831.json) for Phya pa Chos kyi seng ge, TibSchol ID 3831.

Contained in the .json file are the entity's attributes and relations to other entities (see [TibSchol Datamodel](https://github.com/ERC-TibSchol/TibSchol-Datamodel).

In addition, the directory *data* contains an archive of all *excerpts* in use in the database (see https://github.com/ERC-TibSchol/TibSchol-TEI-Library), and references to publications in [TibSchol Zotero Library](https://www.zotero.org/groups/4394244/tibschol/library).

## Backup policy
The archive is refreshed daily. Only documents for entities that underwent a change are updated.

## License for the data
The dataset in *data* is placed under the Creative Commons license CC0, at the exception of Comments (in pages related to Person, Work, Instance, Place) and Item description (in Instance pages), which are placed under the Creative Common license CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). 
