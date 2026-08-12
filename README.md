# ME 137 / ME 237A: Next-Generation Energy Management Systems

Welcome to the course repository for **ME 137 / ME 237A** at UC Berkeley. This repository contains code, Jupyter Notebooks, lab starter files, and reference scripts for the course.

* **Course Units:** 4 Units
* **Instructor:** Prof. T. Schutzius (tschutzius@berkeley.edu)
* **GSI:** Ben Brown (btbrown@berkeley.edu)
* **Prerequisites:** Basic programming (E7, CS 61A, or Data 8 + CS 88), Physics 7A, and Math 53/54.

---

## Course Overview

This course covers modern modeling and simulation methods geared toward analyzing and optimizing energy management systems (e.g., data centers, satellites). Topics span thermodynamics, heat transfer, fluid mechanics, material science, controls, machine learning, and high-performance numerical methods.

Core computational platforms used in labs and projects include:
* **Python / Jupyter Notebooks** (Thermodynamic modeling, psychrometrics, machine learning)
* **ANSYS Fluent** (Applied CFD & boundary layer heat transfer)
* **Cadence Reality DC Design Pro** (Data hall airflow & flow networks)
* **Modelica** (Facility-level flow network modeling)

---

## Environment Setup Instructions

To ensure all Python notebooks run smoothly with standard thermodynamic properties and modeling libraries, setup a dedicated Conda environment.

### 1. Clone the Repository
```bash
git clone [git clone https://YOUR_TOKEN@github.com/mtsn-lab/me137-237a.git](git clone https://YOUR_TOKEN@github.com/mtsn-lab/me137-237a.git)
```

---

## Repository Organization

```
ME137-237A-Energy-Management-Systems/
├── README.md                   # Overview, prerequisite python env setup, syllabus link
├── environment.yml             # Conda environment (Python packages, CoolProp, Jupyter, etc.)
├── requirements.txt            # Pip requirements alternative
├── lectures/                   # Lecture notebooks & companion code
│   ├── week-01-data-centers/
│   ├── week-02-psychrometrics/
│   └── ...
├── laboratories/               # Lab starter code & setup guides
│   ├── lab-01-ansys-fluent/
│   ├── lab-02-cadence-reality-dc/
│   ├── lab-03-modelica-flow/
│   └── ...
└── projects/                   # Project starter files & specs
    ├── project-1/
    ├── project-2/
    └── project-3/  
```