Summary
-------
Python-based data processing pipeline for the Teiko technical exam.

Completed: Parts 1, 2, and 4. Average b_cell question answered as well 

Exam's timing and length caught me at an awkward junction: I'm in the middle of preparing 
for a cross-country move for my family to the Salt Lake City area (Cottonwood Heights) this coming week. Busy!

What is here I believe is solid. There are changes and improvements I would certainly make, but it's readable and has
(in my opinion) clear, consistent logic.

IDE and LLM Usage Statement
---------------------------
What I did not do:
- I did have the built-in AI chat assistant enabled for my IDE
- I did not feed the problem_statement into an LLM and have it generate code
- I did not have an LLM create my project nor structure it
- I did not allow an LLM read/write access to my repository (whether local clone nor github remote)

What I did do:
- I used Jetbrains PyCharm version 2025.3
- I wrote and understand every line written, and how to update / edit as needed
- I did have an LLM review / sanity check my code after it was written
- I queried an LLM for clarifying questions / documentation on certain libraries and features

While LLMs can be extremely powerful tools, I felt using one to generate the code for this exam would be against the 
spirit of the exam

How to run and reproduce the outputs
------------------------------------
- I developed with python3.14 venv, but did run it against python3.12 venv without issue
- Here's how I would reproduce the outputs:
  - git clone the repo: $ git clone git@github.com:foxkevin-teiko-technical/teiknical.git
  - navigate to the project root: $ cd teiknical
  - Then either run the make commands,
    - make setup
    - make pipeline
  - or just run load_data.py directly:
    - python load_data.py
  - there will be csv files in the output/ directory with the results. I have these stored in git for demonstration 
  purposes, but they're overwritten at runtime. If you delete them before you execute the code, you will see them be
  generated as the code runs

Database Schema
---------------
There are two tables in the database
- cell_count
- cell_relative_frequency

Schemas for both tables are directly related to the problem statement
- cell_count schema is a mirror of cell-count.csv to allow easy wide-format ingestion of the csv
- cell_relative_frequency has sample, total_count, population, count, and percentage as requested in step 2
  - Since cell_relative_frequency does use sample, it's marked as a foreign key referencing cell_count(sample)

The schema separates the raw imported measurements from derived analytical measurements
- cell_count, maintaining the format of the csv, allows for a single source of truth

For hundreds of projects and thousands of samples, I would consider moving from SQLite to PostgreSQL or similar
The same relational structure could remain and scale with:
- more optimized queries
- additional SQL aggregation (vs loading into Python memory)
- additional normalized tables (projects, subjects, etc)
- consider adding indices for frequently queried fields

Code Structure
--------------
I stuck with procedural coding here rather than OOP, as there's not a lot of state being passed around. Introducing 
classes would add complexity without a clear benefit

I created different modules based on separation of concern:
- analysis: calculations, queries, transforms
- csv_helper: file i/o and csv interactions
- database: database utilities
- load_data: orchestration / main
- schema: table structure

Dashboard Note
--------------
Interactive dashboard was not implemented for this submission. There are however generated csv outputs to demonstrate 
code functionality and accuracy.

TODO / Future Improvements
--------------------------
- Finish part 3
- Framework updates
  - Consider using pandas
  - Consider using sqlalchemy
- Code cleanup / improvements / robustness
  - String standardization
    - There's a good amount of hard-coded strings. Perhaps a defs file with enums, or something to help prevent typos
  - Consolidate exporters in analysis  
  - Edge-case checking (divide by zero, empty lists, etc)
  - Path handling when not in project root
  - Dynamic creation of the output/ directory
- Unit tests
  - Use pytest
- I think standing up something like a grafana instance to view, analyze, and aggregate these data sources would have a 
lot of value. Then anyone on the team could make dashboard, plots, etc without needing a software developer to create a
custom plot

Assumptions
-----------
- I had to make a few assumptions for this assignment. In general, that is not something I like doing in practice. It's 
a waste of everyone's time if you create the wrong thing. That was one area I always, always communicated to my team at 
my previous job (we wrote software for internal users) - not to assume, and to just spend the little bit of extra time 
with the stakeholder to ensure you're making what they need.
- For the melanoma average number of cells question, the answer I calculated is 10206.15
  - This is assuming that when it's asked "... number of B cells for responders ...", we're only looking at response = "yes"