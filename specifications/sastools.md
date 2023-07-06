# SAS-tools data model

Python object model specifications based on the [software-driven-rdm](https://github.com/JR-1991/software-driven-rdm) Python library.


## Core objects


### SAStools

Root element of the SAS-tools data model.

- __datetime_created__
  - Type: datetime
  - Description: Date and time this dataset has been created.
- datetime_modified
  - Type: datetime
  - Description: Date and time this dataset has last been modified.
- experiment
  - Type: [Experiment](#experiment)
  - Description: A SAS experiment with measurements and analyses.
- citation
  - Type: [Citation](#citation)
  - Description: Relevant information regarding the publication and citation of this dataset.


### Experiment

Container for SAS measurements and analyses.

- name
  - Type: string
  - Description: tba
- diffraction_type
  - Type: [DiffractionType](#diffractiontype)
  - Description: tba
- measurements
  - Type: [Measurement](#measurement)
  - Multiple: True
  - Description: tba
- diffractograms
  - Type: [Diffractogram](#diffractogram)
  - Multiple: True
  - Description: tba
- analyses
  - Type: [Analysis](#analysis)
  - Multiple: True
  - Description: tba


### Measurement

instrument (settings, parameters, ...)

- measurement_type
  - Type: MeasurementType
  - Multiple: True
  - Description: tba



### Diffractogram

preprocessing steps

- data_array
  - Type: float
  - Multiple: True
  - Description: tba


### Analysis

tba

- name
  - Type: string
  - Description: tba



### Citation

Container for various types of metadata primarily used in the publication and citation of the dataset.

- title
  - Type: string
  - Description: Title the dataset should have when published.
- doi
  - Type: URL
  - Description: DOI pointing to the published dataset
- description
  - Type: string
  - Description: Description the dataset should have when published.
- authors
  - Type: [Person](#person)
  - Description: List of authors for this dataset.
  - Multiple: True
- subjects
  - Type: [Subjects](#subjects)
  - Description: List of subjects this dataset belongs to.
  - Multiple: True
- keywords
  - Type: [Term](#term)
  - Description: List of CV-based keywords describing the dataset.
  - Multiple: True
- topics
  - Type: [Term](#term)
  - Description: List of CV-based topics the dataset addresses.
  - Multiple: True
- related_publications
  - Type: [Publication](#publication)
  - Description: List of publications relating to this dataset.
  - Multiple: True
- notes
  - Type: string
  - Description: Additional notes about the dataset.
- funding
  - Type: string
  - Description: Funding information for this dataset.
  - Multiple: True
- license
  - Type: string
  - Description: License information for this dataset. Defaults to `CC BY 4.0`.
  - Default: CC BY 4.0


### Person

Container for information regarding a person that worked on an experiment.

- __last_name__
  - Type: string
  - Description: Family name of the person.
- __first_name__
  - Type: string
  - Description: Given name of the person.
- middle_names
  - Type: string
  - Description: List of middle names of the person.
  - Multiple: True
- affiliation
  - Type: string
  - Description: Institution the Person belongs to.
- email
  - Type: string
  - Description: Email address of the person.
- identifier_type
  - Type: [IdentifierTypes](#identifiertypes)
  - Description: Recognized identifier for the person.
- identifier_value
  - Type: string
  - Description: Value of the identifier for the person.


### Publication

Container for citation information of a relevant publication.

- __type__
  - Type: [PublicationTypes](#publicationtypes)
  - Description: Nature of the publication.
- __title__
  - Type: string
  - Description: Title of the publication.
- __authors__
  - Type: [Person](#person)
  - Description: Authors of the publication.
  - Multiple: True
- year
  - Type: integer
  - Description: Year of publication.  
- doi
  - Type: URL
  - Description: The DOI pointing to the publication.


### Term

lorem ipsum {Add reference back to term_cv_reference.}

- __name__
  - Type: string
  - Description: The preferred name of the term associated with the given accession number.
- __accession__
  - Type: string
  - Description: Accession number of the term in the controlled vocabulary.
- term_cv_reference
  - Type: string
  - Description: Reference to the `CV.id` of a controlled vocabulary that has been defined for this dataset.
- value
  - Type: any
  - Description: Value of the term, if applicable.


## Enumerations


### Subjects

Enumeration containing common subjects (research fields) that implement NMR.

```python
BIOLOGY = "Biology"
CHEMISTRY = "Chemistry"
IT = "Computer and Information Science"
PHYSICS = "Physics"
```


### PublicationTypes

Enumeration containing accepted types of publication.

```python
ARTICLE = "Journal article"
```


### IdentifierTypes

Enumeration containing recognized identifiers for persons.

```python
ORCID = "ORCID"
```


### DiffractionType

tba

```python
SAXS = auto()
SANS = auto()
```


### MeasurementType

tba

```python
CALIBRATION = auto()
```

