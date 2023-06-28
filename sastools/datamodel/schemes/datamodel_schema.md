```mermaid
classDiagram
    SAStools *-- Citation
    Citation *-- Subjects
    Citation *-- Person
    Citation *-- Publication
    Citation *-- Term
    Person *-- IdentifierTypes
    Publication *-- PublicationTypes
    Publication *-- Person
    
    class SAStools {
        +datetime datetime_created*
        +datetime datetime_modified
        +Citation citation
    }
    
    class Citation {
        +string title
        +URL doi
        +string description
        +Person[0..*] authors
        +Subjects[0..*] subjects
        +Term[0..*] keywords
        +Term[0..*] topics
        +Publication[0..*] related_publications
        +string notes
        +string[0..*] funding
        +string license
    }
    
    class Person {
        +string last_name*
        +string first_name*
        +string[0..*] middle_names
        +string affiliation
        +string email
        +IdentifierTypes identifier_type
        +string identifier_value
    }
    
    class Publication {
        +PublicationTypes type*
        +string title*
        +Person[0..*] authors*
        +integer year
        +URL doi
    }
    
    class Term {
        +string name*
        +string accession*
        +string term_cv_reference
        +any value
    }
    
    class Subjects {
        << Enumeration >>
        +BIOLOGY
        +CHEMISTRY
        +IT
        +PHYSICS
    }
    
    class PublicationTypes {
        << Enumeration >>
        +ARTICLE
    }
    
    class IdentifierTypes {
        << Enumeration >>
        +ORCID
    }
    
```