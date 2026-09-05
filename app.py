import os
import json
import base64
import re
import requests

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse


app = FastAPI(title="MedLens — AI Clinical Insight")


# ============================================================
# MEDLENS UI
# ============================================================

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MedLens — Clinical Insight</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            background: #f4f7fb;
            color: #172033;
        }

        .header {
            background: #102a43;
            color: white;
            padding: 28px 20px;
        }

        .header-inner {
            max-width: 1100px;
            margin: auto;
        }

        .header h1 {
            margin: 0;
            font-size: 34px;
        }

        .header p {
            margin: 8px 0 0;
            opacity: 0.85;
        }

        .container {
            max-width: 1100px;
            margin: 25px auto;
            padding: 0 15px;
        }

        .card {
            background: white;
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 3px 14px rgba(0,0,0,0.07);
        }

        .card h2 {
            margin-top: 0;
            color: #102a43;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }

        label {
            display: block;
            font-weight: bold;
            margin-bottom: 6px;
        }

        input, textarea, select {
            width: 100%;
            padding: 12px;
            border: 1px solid #ccd6e0;
            border-radius: 8px;
            font-size: 15px;
        }

        textarea {
            min-height: 85px;
            resize: vertical;
        }

        .full {
            grid-column: 1 / -1;
        }

        .upload {
            border: 2px dashed #7ba7d9;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            background: #f8fbff;
        }

        button {
            margin-top: 18px;
            background: #1565c0;
            color: white;
            border: none;
            padding: 14px 22px;
            border-radius: 9px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #0d47a1;
        }

        button:disabled {
            opacity: 0.6;
            cursor: wait;
        }

        .status {
            margin-top: 15px;
            font-weight: bold;
        }

        .table-wrap {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 12px;
        }

        th, td {
            padding: 11px;
            border: 1px solid #d8e0e8;
            text-align: left;
            vertical-align: top;
        }

        th {
            background: #edf3f8;
        }

        .badge {
            display: inline-block;
            padding: 5px 9px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }

        .low {
            background: #fff3cd;
            color: #856404;
        }

        .normal {
            background: #d4edda;
            color: #155724;
        }

        .high {
            background: #f8d7da;
            color: #721c24;
        }

        .unknown {
            background: #e2e3e5;
            color: #383d41;
        }

        .conflict {
            background: #fff8e1;
            border-left: 5px solid #ffb300;
            padding: 12px;
            margin: 8px 0;
            border-radius: 5px;
        }

        .summary {
            background: #eef7ff;
            padding: 18px;
            border-radius: 10px;
            line-height: 1.6;
        }

        .notice {
            background: #fff3cd;
            border-left: 5px solid #f0ad00;
            padding: 15px;
            border-radius: 7px;
            line-height: 1.5;
        }

        .empty {
            color: #68788a;
        }

        @media(max-width: 700px) {
            .grid {
                grid-template-columns: 1fr;
            }

            .full {
                grid-column: auto;
            }

            .header h1 {
                font-size: 27px;
            }
        }
    </style>
</head>

<body>

<div class="header">
    <div class="header-inner">
        <h1>🩺 MedLens</h1>
        <p>AI-Powered Clinical Information Intelligence</p>
    </div>
</div>

<div class="container">

    <div class="card">
        <h2>👤 Patient Information</h2>

        <div class="grid">

            <div>
                <label>Age</label>
                <input id="age" type="number" min="0" max="150"
                       placeholder="e.g. 21">
            </div>

            <div>
                <label>Sex</label>
                <select id="sex">
                    <option value="">Select</option>
                    <option>Male</option>
                    <option>Female</option>
                    <option>Other</option>
                    <option>Prefer not to say</option>
                </select>
            </div>

            <div class="full">
                <label>Symptoms</label>
                <textarea id="symptoms"
                    placeholder="Enter patient-reported symptoms"></textarea>
            </div>

            <div>
                <label>Known Conditions</label>
                <textarea id="conditions"
                    placeholder="Existing conditions"></textarea>
            </div>

            <div>
                <label>Allergies</label>
                <textarea id="allergies"
                    placeholder="Known allergies"></textarea>
            </div>

            <div class="full">
                <label>Current Medications</label>
                <textarea id="medications"
                    placeholder="Current medications"></textarea>
            </div>

        </div>
    </div>


    <div class="card">
        <h2>📄 Medical Report</h2>

        <div class="upload">
            <input
                id="report"
                type="file"
                accept=".pdf,.jpg,.jpeg,.png,.webp"
            >

            <p>Upload a PDF or medical report image</p>
            <small>Maximum file size: 8 MB</small>
        </div>

        <button id="processBtn" onclick="processReport()">
            Process Medical Report
        </button>

        <div id="status" class="status"></div>
    </div>


    <div id="results"></div>

</div>


<script>

function escapeHTML(value) {
    if (value === null || value === undefined) return "";
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


function statusBadge(status) {

    const value = String(status || "UNKNOWN").toUpperCase();

    let cls = "unknown";

    if (value === "LOW") cls = "low";
    if (value === "NORMAL") cls = "normal";
    if (value === "HIGH") cls = "high";

    return `<span class="badge ${cls}">${escapeHTML(value)}</span>`;
}


async function processReport() {

    const fileInput = document.getElementById("report");
    const button = document.getElementById("processBtn");
    const status = document.getElementById("status");
    const results = document.getElementById("results");

    if (!fileInput.files.length) {
        alert("Please upload a medical report first.");
        return;
    }

    const file = fileInput.files[0];

    if (file.size > 8 * 1024 * 1024) {
        alert("File is too large. Maximum allowed size is 8 MB.");
        return;
    }

    const patient = {
        age: document.getElementById("age").value,
        sex: document.getElementById("sex").value,
        symptoms: document.getElementById("symptoms").value,
        conditions: document.getElementById("conditions").value,
        allergies: document.getElementById("allergies").value,
        medications: document.getElementById("medications").value
    };

    const formData = new FormData();

    formData.append("file", file);
    formData.append("patient", JSON.stringify(patient));

    button.disabled = true;
    button.textContent = "Processing...";
    status.textContent = "🔎 Reading and structuring the medical report...";
    results.innerHTML = "";

    try {

        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        renderResults(data);

        status.textContent = "✅ Report processed successfully.";

    } catch (error) {

        alert(error.message || "Unable to process report.");

        status.textContent = "❌ Processing failed.";

    } finally {

        button.disabled = false;
        button.textContent = "Process Medical Report";
    }
}


function renderResults(data) {

    const results = document.getElementById("results");

    let rows = "";

    if (data.tests && data.tests.length) {

        data.tests.forEach(test => {

            rows += `
            <tr>
                <td>${escapeHTML(test.test_name)}</td>
                <td>${escapeHTML(test.value)}</td>
                <td>${escapeHTML(test.unit)}</td>
                <td>${escapeHTML(test.reference_range)}</td>
                <td>${statusBadge(test.status)}</td>
                <td>${escapeHTML(test.date)}</td>
                <td>${escapeHTML(test.observation)}</td>
                <td>${escapeHTML(test.source)}</td>
            </tr>
            `;
        });

    } else {

        rows = `
        <tr>
            <td colspan="8" class="empty">
                No structured test results were extracted.
            </td>
        </tr>
        `;
    }


    let conflicts = "";

    if (data.conflicts && data.conflicts.length) {

        data.conflicts.forEach(item => {

            conflicts += `
            <div class="conflict">
                ⚠️ ${escapeHTML(item)}
            </div>
            `;
        });

    } else {

        conflicts = `
        <p class="empty">
            No conflicts were detected in the supplied information.
        </p>
        `;
    }


    results.innerHTML = `

    <div class="card">

        <h2>📊 Structured Medical Record</h2>

        <div class="table-wrap">

            <table>

                <thead>
                    <tr>
                        <th>Test</th>
                        <th>Value</th>
                        <th>Unit</th>
                        <th>Reference Range</th>
                        <th>Status</th>
                        <th>Date</th>
                        <th>Observation</th>
                        <th>Source</th>
                    </tr>
                </thead>

                <tbody>
                    ${rows}
                </tbody>

            </table>

        </div>

    </div>


    <div class="card">

        <h2>⚠️ Conflict Detection</h2>

        ${conflicts}

    </div>


    <div class="card">

        <h2>🧠 Patient-Friendly Summary</h2>

        <div class="summary">
            ${escapeHTML(data.summary || "No summary generated.")}
        </div>

    </div>


    <div class="card">

        <h2>🔐 Responsible AI Notice</h2>

        <div class="notice">

            MedLens is an information-structuring and review-support
            tool. It does not provide a medical diagnosis, prescribe
            treatment, recommend medication changes, or determine
            medication dosage.

            <br><br>

            Reference-range status is marked LOW, NORMAL, or HIGH only
            when the uploaded report provides the relevant reference
            range. Otherwise, the status is shown as UNKNOWN.

            <br><br>

            AI-extracted information should be reviewed by a qualified
            human before clinical use.

        </div>

    </div>

    `;
}

</script>

</body>
</html>
"""


# ============================================================
# HOME
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML


# ============================================================
# HELPERS
# ============================================================

def clean_json_text(text):

    text = text.strip()

    # Remove markdown code fences if model adds them
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    # Find the JSON object if extra text was added
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return text.strip()


def make_data_url(file_bytes, mime_type):

    encoded = base64.b64encode(file_bytes).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


def normalize_result(data):

    if not isinstance(data, dict):
        data = {}

    tests = data.get("tests", [])

    if not isinstance(tests, list):
        tests = []

    normalized_tests = []

    for test in tests:

        if not isinstance(test, dict):
            continue

        status = str(test.get("status", "UNKNOWN")).upper()

        if status not in ["LOW", "NORMAL", "HIGH", "UNKNOWN"]:
            status = "UNKNOWN"

        normalized_tests.append({
            "test_name": str(test.get("test_name", "")),
            "value": str(test.get("value", "")),
            "unit": str(test.get("unit", "")),
            "reference_range": str(test.get("reference_range", "")),
            "status": status,
            "date": str(test.get("date", "")),
            "observation": str(test.get("observation", "")),
            "source": str(test.get("source", "uploaded report"))
        })

    conflicts = data.get("conflicts", [])

    if not isinstance(conflicts, list):
        conflicts = [str(conflicts)]

    conflicts = [str(x) for x in conflicts]

    summary = str(data.get("summary", ""))

    return {
        "tests": normalized_tests,
        "conflicts": conflicts,
        "summary": summary
    }


# ============================================================
# AI ANALYSIS
# ============================================================

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    patient: str = Form("{}")
):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return {
            "error": "OPENROUTER_API_KEY is not configured in Render."
        }

    # --------------------------------------------------------
    # Validate file
    # --------------------------------------------------------

    allowed_types = {
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    mime_type = file.content_type or "application/octet-stream"

    if mime_type not in allowed_types:

        return {
            "error": "Unsupported file type. Please upload PDF, JPG, PNG, or WEBP."
        }

    file_bytes = await file.read()

    if len(file_bytes) > 8 * 1024 * 1024:

        return {
            "error": "File is too large. Maximum allowed size is 8 MB."
        }


    # --------------------------------------------------------
    # Parse patient information
    # --------------------------------------------------------

    try:
        patient_data = json.loads(patient)
    except Exception:
        patient_data = {}


    # --------------------------------------------------------
    # Strict MedLens extraction instructions
    # --------------------------------------------------------

    prompt = f"""
You are the extraction engine for MedLens, a clinical information
structuring application.

Your job is NOT to diagnose the patient.

Your job is to read the uploaded medical report and convert the
information into a structured medical record.

PATIENT-PROVIDED INFORMATION:
{json.dumps(patient_data, ensure_ascii=False)}

IMPORTANT SAFETY AND ACCURACY RULES:

1. Extract medical test information ONLY from the uploaded report.

2. NEVER invent a laboratory value.

3. NEVER invent a unit.

4. NEVER invent a date.

5. NEVER invent a reference range.

6. If the report does not provide a reference range for a test,
   set reference_range to an empty string and status to UNKNOWN.

7. LOW, NORMAL, or HIGH may ONLY be assigned when the uploaded
   report itself provides a reference range that allows that
   classification.

8. Do not use general medical knowledge to create reference ranges.

9. Do not diagnose, infer, or speculate about a disease or medical condition.
10. If the uploaded report itself mentions a diagnosis, suspected condition, possible cause, or clinical interpretation, you may reproduce it ONLY as a clearly attributed statement such as "The report states..." or "The report mentions...".
11. Do not turn observations into your own medical conclusions.
12. Do not recommend treatment, medication changes, dosage changes, or clinical actions.
13. Do not present uncertain information as fact.
14. Keep the patient-friendly summary factual and based only on information present in the uploaded report and user-provided patient information.

15. Detect obvious contradictions inside the supplied information
    and list them under conflicts.

16. Produce a concise, patient-friendly summary describing what
    information is present in the report. Do not give a diagnosis
    or treatment advice.

OUTPUT FORMAT:

Return ONLY valid JSON.

Use exactly this structure:

{{
  "tests": [
    {{
      "test_name": "string",
      "value": "string",
      "unit": "string",
      "reference_range": "string",
      "status": "LOW | NORMAL | HIGH | UNKNOWN",
      "date": "string",
      "observation": "string",
      "source": "uploaded report"
    }}
  ],
  "conflicts": [
    "string"
  ],
  "summary": "string"
}}

Do not wrap the JSON in markdown.
"""


    # --------------------------------------------------------
    # Convert uploaded file
    # --------------------------------------------------------

    data_url = make_data_url(file_bytes, mime_type)


    # --------------------------------------------------------
    # OpenRouter request
    # --------------------------------------------------------

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


    if mime_type == "application/pdf":

        content = [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "file",
                "file": {
                    "filename": file.filename or "medical_report.pdf",
                    "file_data": data_url
                }
            }
        ]

    else:

        content = [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": data_url
                }
            }
        ]


    payload = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    }


    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )


        if not response.ok:

            return {
                "error": (
                    f"OpenRouter API error {response.status_code}: "
                    f"{response.text[:1500]}"
                )
            }


        result = response.json()


        choices = result.get("choices", [])

        if not choices:

            return {
                "error": "OpenRouter returned no model response."
            }


        message = choices[0].get("message", {})

        content = message.get("content", "")


        # Some models can return content as a list.
        if isinstance(content, list):

            parts = []

            for item in content:

                if isinstance(item, dict):

                    if "text" in item:
                        parts.append(str(item["text"]))

                else:
                    parts.append(str(item))

            content = "".join(parts)


        content = str(content)

        cleaned = clean_json_text(content)


        try:

            parsed = json.loads(cleaned)

        except Exception:

            return {
                "error": (
                    "The AI returned an unexpected format. "
                    f"Raw response: {content[:1500]}"
                )
            }


        return normalize_result(parsed)


    except requests.exceptions.Timeout:

        return {
            "error": "OpenRouter request timed out. Please try again."
        }

    except requests.exceptions.RequestException as e:

        return {
            "error": f"Network error while contacting OpenRouter: {str(e)[:500]}"
        }

    except Exception as e:

        return {
            "error": f"AI processing failed: {type(e).__name__}: {str(e)[:500]}"
        }
