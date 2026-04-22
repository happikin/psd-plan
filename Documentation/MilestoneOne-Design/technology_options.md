**Technology Options**

This document attempts to explore viable technologies and software stacks to build each functioning software component.

NLP & Preprocessing

- **NLTK**: or **RAKE** Simple library for tokenization and simplification of words
- **Textacy**: Text cleanup and topic extraction to explore underlying themes of a paper
- **Gensim**: Topic modelling and document similarity analysis for papers

File IO and Data Management

- **PyMuPDF**(fitz): Fast package for text, image, column extraction from research paper
- **PostgreSQL**: To store metadata and tokenized information from the pre-processing pipeline. This also allows for JSON storage.
- **SQLAlchemy** & asyncpg: These packages will allow faster programming of searching and querying algorithms.

User Interaction

- **GRAPHVIZ**: Can help to build relational graphs and export static images as well
- **Pyviz**: Mainly for interactive access to the generated graphs

Programming Language:

- **Python**: Version 3.9 OR 3.10 will be most suitable due to package compatibility and community support

Deployment

- **Docker**: This will prevent any compatibility issue between the development packages and the system software of target platform