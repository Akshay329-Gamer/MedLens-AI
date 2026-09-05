# MedLens — AI Clinical Insight

MedLens is an AI-powered clinical information intelligence tool that converts unstructured medical reports into a structured, understandable and reviewable medical record.

## Problem

Medical information is often scattered across laboratory reports, radiology reports, prescriptions and patient-provided information. This makes reviewing previous records difficult.

MedLens uses AI to organize uploaded medical reports into structured information while keeping the original source context and applying responsible-AI safeguards.

## Key Features

- Patient information intake
- Medical report upload
- AI-powered report extraction
- Structured medical record
- Test name, value, unit and reference-range extraction
- Reference-range aware LOW / NORMAL / HIGH classification
- UNKNOWN status when no reference range is provided
- Source and provenance tracking
- Conflict detection
- Patient-friendly summary
- Responsible AI safeguards
- Human review reminder

## How It Works

1. The user enters available patient information.
2. The user uploads a medical report in PDF or image format.
3. The report is converted into multimodal input for the AI model.
4. The AI extracts relevant information from the uploaded document.
5. Extracted information is returned in a structured JSON format.
6. MedLens validates and normalizes the AI response.
7. The frontend displays the information as a structured medical record.
8. The system separately displays conflicts and a patient-friendly summary.

## AI Logic

MedLens is instructed to:

- Extract information only from the uploaded report.
- Never invent medical values.
- Never invent reference ranges.
- Mark a result LOW, NORMAL or HIGH only when the report provides the relevant reference range.
- Mark the status UNKNOWN when a reference range is unavailable.
- Preserve the source of extracted information.
- Identify contradictions between supplied information and report information.
- Avoid diagnosis and treatment recommendations.
- Attribute medical interpretations to the uploaded report.
- Keep uncertain information clearly identified.

## Technology Stack

- Python
- FastAPI
- HTML / CSS / JavaScript
- OpenRouter API
- Multimodal AI model
- Docker
- Render deployment

## Architecture

```text
User
  |
  v
MedLens Web Interface
  |
  v
FastAPI Backend
  |
  v
OpenRouter Multimodal AI
  |
  v
Structured JSON
  |
  +----> Medical Record
  |
  +----> Conflict Detection
  |
  +----> Patient-Friendly Summary
