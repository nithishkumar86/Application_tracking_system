# Project Setup Guide

This guide explains how to set up and run the project step by step.

---

## Step 1: Clone the GitHub Repository

First, clone the project from GitHub using the repository link:

```bash
git clone https://github.com/nithishkumar86/Application_tracking_system.git
```

## Step 2: Initialize Project and Create Virtual Environment

Initialize the project using **uv**:

```bash
uv init
```

Create a virtual environment:

```bash
uv venv
```

Activate the virtual environment:

### On Windows

```bash
.venv\Scripts\activate
```

### On Linux / macOS

```bash
source .venv/bin/activate
```

---

## Step 3: Install Requirements

Install all required dependencies using:

```bash
uv add -r requirements.txt
```

Make sure the installation completes without errors.

---

## Step 4: Run the Application

Run the main file of the project:

```bash
uv run python connector.py
```

---

## Notes
*please Ensure set up the **.env** file with your groq api key like GROQ_API_KEY ="<your_api_key>"
* Ensure **Python** and **uv** are installed before starting.
* Always activate the virtual environment before running the project.
* If you face issues, re-check the requirements file.

---


