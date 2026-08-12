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
│   ├── 01/	   	        # Data Centers
│   ├── 02/			# Psychrometrics
│   ├── 03/			# Performance Metrics and Standards
│   └── ...
├── laboratories/               # Lab starter code & setup guides
│   ├── 01/			# ANSYS Fluent
│   ├── 02/			# Cadence Reality DC
│   ├── 03/			# Modelica
│   └── ...
└── projects/                   # Project starter files & specs
    ├── 01/			# Conduction/convection. Basic CFD, boundary layer, internal convection. ANSYS Fluent.
    ├── 02/			# Air-handlers within the data center. Airflow CFD within the room. Apply airflow handling strategies. Cadence Reality DC Design Pro.
    ├── 03/  			# Facility-level thermal analysis. Flow network modeling. Cadence Reality DC Design Pro.
    └── ...  			
```