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
```
## Responsible AI

MedLens is designed as an information-structuring and review-support tool.

It does not:

- Provide medical diagnosis
- Prescribe treatment
- Recommend medication changes
- Determine medication dosage
- Invent laboratory reference ranges
- Present uncertain information as fact

AI-extracted information should be reviewed by a qualified human before clinical use.

## Assumptions

- Uploaded reports are assumed to contain the source information required for extraction.
- Reference ranges are used only when explicitly available in the uploaded report.
- AI extraction may contain errors and requires human verification.
- The system is intended for information organization and review support, not autonomous clinical decision-making.

## Deployment

MedLens is containerized using Docker and deployed as a web service on Render.

The OpenRouter API key is stored as a server-side environment variable and is not included in the source code.

## Security

- API credentials are stored using environment variables.
- `.env` files are excluded using `.gitignore`.
- Uploaded files are processed in memory and are not intentionally persisted by the application.
- File type and file-size limits are enforced by the backend.

## Limitations

- AI extraction may contain errors, especially with low-quality or difficult-to-read documents.
- Results should be verified against the original uploaded report.
- The application does not replace professional medical review.
- No diagnosis or treatment recommendation is generated.

## Project

Built for the PromptWars × AIMERverse hackathon at MVSR Engineering College.

**Challenge:** MedLens — AI Clinical Insight
