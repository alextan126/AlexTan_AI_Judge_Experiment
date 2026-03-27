---
name: stare-framework-update
overview: Update Architecture.md with STARE framework, create new folders, and transform application question samples into STARE format.
todos:
  - id: update-arch-doc
    content: Update AlternativeSolution/Architecutre.md with STARE framework and data flow diagram
    status: completed
  - id: create-dirs
    content: Create AlternativeSolution/应用题 and JudgerTesting/NewSample/全栈工程师/应用题 directories
    status: completed
  - id: write-script
    content: Write AlternativeSolution/应用题/generate_stare_samples.py script
    status: completed
  - id: run-script
    content: Run the script to generate the new sample markdown files
    status: completed
isProject: false
---

# Plan to Implement STARE Framework for Application Questions

1. **Update Architecture Documentation**

- Append the STARE framework definition to `AlternativeSolution/Architecutre.md`.
- Include the grading criteria (STARE=3, STAR=2, STA=1, Others=0).
- Add a mermaid diagram illustrating the data flow for the Application Questions (应用题) judging process.

1. **Create New Directories**

- Create `AlternativeSolution/应用题/` for application question related scripts.
- Create `JudgerTesting/NewSample/全栈工程师/应用题/` to store the transformed sample files.

1. **Create Transformation Script**

- Write a Python script `AlternativeSolution/应用题/generate_stare_samples.py`.
- The script will contain the 5 original questions and generate 5 new simulated answers for each question based on the STARE framework:
  - Case 1: STARE (3 points) - 完美的标准答案
  - Case 2: STAR (2 points) - 知其然不知其所以然型答案
  - Case 3: STA (1 points) - 有根据的猜测型答案
  - Case 4: ST/Others (0 points) - 只能转述问题，选错方案
  - Case 5:A(0 points) -
  - Case 6: Others (0 points) - 完全答非所问或全错
- The output format will replace the old `决定项/加分项` with the new `STARE_level: [Level] / score: [Score]` format.

1. **Execute Transformation**

- Run the Python script to generate the 5 new markdown sample files in `JudgerTesting/NewSample/全栈工程师/应用题/`.
