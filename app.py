import os
import json
import base64
import requests
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MedLens")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>MedLens — Clinical Information Intelligence</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
*{box-sizing:border-box}

body{
    margin:0;
    font-family:Arial,sans-serif;
    background:#f4f7fb;
    color:#172033
}

header{
    background:#102a43;
    color:white;
    padding:22px 7%;
    display:flex;
    justify-content:space-between;
    align-items:center
}

.logo{
    font-size:26px;
    font-weight:700
}

.tag{
    opacity:.8
}

main{
    max-width:1150px;
    margin:35px auto;
    padding:0 20px
}

.card{
    background:white;
    border-radius:18px;
    padding:25px;
    margin-bottom:22px;
    box-shadow:0 5px 25px #102a4312
}

h1{
    margin-bottom:5px
}

h2{
    margin-top:0
}

.grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:15px
}

input,textarea{
    width:100%;
    padding:12px;
    border:1px solid #d5dde8;
    border-radius:9px;
    margin-top:6px
}

textarea{
    min-height:90px
}

button{
    background:#2563eb;
    color:white;
    border:0;
    border-radius:9px;
    padding:13px 22px;
    font-weight:bold;
    cursor:pointer;
    margin-top:15px
}

button:hover{
    opacity:.9
}

.upload{
    border:2px dashed #9bb7dc;
    padding:30px;
    text-align:center;
    border-radius:14px
}

table{
    width:100%;
    border-collapse:collapse;
    margin-top:15px
}

th,td{
    padding:13px;
    border-bottom:1px solid #e5eaf0;
    text-align:left
}

.badge{
    padding:5px 10px;
    border-radius:20px;
    font-weight:bold;
    font-size:12px
}

.low{
    background:#fee2e2;
    color:#b91c1c
}

.high{
    background:#ffedd5;
    color:#c2410c
}

.normal{
    background:#dcfce7;
    color:#15803d
}

.unknown{
    background:#e5e7eb;
    color:#374151
}

.source{
    font-size:12px;
    color:#64748b
}

.alert{
    background:#fff7ed;
    border-left:5px solid #f97316;
    padding:15px;
    border-radius:8px
}

.summary{
    background:#eff6ff;
    padding:20px;
    border-radius:12px;
    line-height:1.6
}

.hidden{
    display:none
}

#loading{
    color:#2563eb;
    font-weight:bold
}

@media(max-width:700px){
    .grid{
        grid-template-columns:1fr
    }
}
</style>
</head>

<body>

<header>
<div class="logo">🩺 MedLens</div>
<div class="tag">Clinical Information Intelligence</div>
</header>

<main>

<div class="card">

<h1>Patient Information</h1>

<p>Provide the available patient context.</p>

<div class="grid">

<div>
<label>Age</label>
<input id="age" type="number">
</div>

<div>
<label>Sex</label>
<input id="sex">
</div>

<div>
<label>Symptoms</label>
<input id="symptoms">
</div>

<div>
<label>Existing Conditions</label>
<input id="conditions">
</div>

<div>
<label>Allergies</label>
<input id="allergies">
</div>

<div>
<label>Medications</label>
<input id="medications">
</div>

</div>

<button onclick="processReport()">Process Medical Report</button>

</div>


<div class="card">

<h2>📄 Medical Report</h2>

<div class="upload">

<input id="report" type="file" accept=".pdf,.png,.jpg,.jpeg">

<p>Upload a PDF or medical report image</p>

</div>

<p id="loading" class="hidden">
⏳ MedLens is extracting and validating the report...
</p>

</div>


<div id="results" class="hidden">

<div class="card">

<h2>📊 Structured Medical Record</h2>

<div id="table"></div>

</div>


<div id="conflicts"></div>


<div class="card">

<h2>🧠 Patient-Friendly Summary</h2>

<div class="summary" id="summary"></div>

<p class="source">
Generated only from the provided patient information and uploaded report.
</p>

</div>


<div class="card">

<h3>🛡️ Responsible AI</h3>

<p>
MedLens organizes and summarizes medical information.
It does not diagnose diseases, prescribe treatment,
or recommend medication changes.
</p>

</div>

</div>

</main>


<script>

async function processReport(){

    const file=document.getElementById("report").files[0];

    if(!file){
        alert("Please upload a medical report first.");
        return;
    }

    document.getElementById("loading").classList.remove("hidden");

    const fd=new FormData();

    fd.append("file",file);

    fd.append("patient",JSON.stringify({

        age:document.getElementById("age").value,

        sex:document.getElementById("sex").value,

        symptoms:document.getElementById("symptoms").value,

        conditions:document.getElementById("conditions").value,

        allergies:document.getElementById("allergies").value,

        medications:document.getElementById("medications").value

    }));


    try{

        const res=await fetch("/analyze",{
            method:"POST",
            body:fd
        });

        const data=await res.json();


        if(data.error){

            alert(data.error);

            return;

        }


        let rows="";


        (data.tests||[]).forEach(x=>{

            let cls=(x.status||"UNKNOWN").toLowerCase();

            rows+=`

            <tr>

            <td><b>${x.test_name||"Unknown"}</b></td>

            <td>${x.value??"Not provided"}</td>

            <td>${x.unit||""}</td>

            <td>${x.reference_range||"Not provided"}</td>

            <td>
            <span class="badge ${cls}">
            ${x.status||"UNKNOWN"}
            </span>
            </td>

            <td class="source">
            AI extracted<br>
            ${x.source||"Uploaded report"}
            </td>

            </tr>

            `;

        });


        document.getElementById("table").innerHTML=`

        <table>

        <tr>

        <th>Test</th>
        <th>Value</th>
        <th>Unit</th>
        <th>Reference Range</th>
        <th>Status</th>
        <th>Provenance</th>

        </tr>

        ${rows}

        </table>

        `;


        let conflictHTML="";


        (data.conflicts||[]).forEach(c=>{

            conflictHTML+=`

            <div class="card alert">

            <b>⚠️ Information conflict</b>

            <p>${c}</p>

            </div>

            `;

        });


        document.getElementById("conflicts").innerHTML=conflictHTML;


        document.getElementById("summary").innerText=
            data.summary||"No summary available.";


        document.getElementById("results").classList.remove("hidden");


    }catch(e){

        alert("Something went wrong: "+e.message);

    }finally{

        document.getElementById("loading").classList.add("hidden");

    }

}

</script>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    patient: str = Form(...)
):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "error": "GEMINI_API_KEY is not configured."
        }


    data = await file.read()


    if len(data) > 8 * 1024 * 1024:
        return {
            "error": "Please use a report smaller than 8 MB."
        }


    mime = file.content_type or "application/pdf"


    prompt = f"""
You are MedLens, a clinical information organization assistant.

PATIENT INFORMATION PROVIDED BY USER:
{patient}

Analyze the uploaded medical report.

IMPORTANT SAFETY RULES:

1. Extract information only from the uploaded report.
2. NEVER invent missing values.
3. NEVER invent a reference range.
4. Determine LOW, NORMAL or HIGH ONLY when the report itself provides a reference range.
5. If no reference range exists, status MUST be "UNKNOWN".
6. Distinguish report-extracted information from user-provided information.
7. Detect contradictions between patient information and report information.
8. Do NOT diagnose any disease.
9. Do NOT recommend treatment.
10. Do NOT recommend changing medication or dosage.
11. Do not present uncertain information as fact.
12. Create a concise patient-friendly informational summary.

Return ONLY valid JSON using exactly this structure:

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
  "conflicts": ["string"],
  "summary": "string"
}}

The reference_range field must contain the range exactly as reported
or "Not provided".
"""


    encoded = base64.b64encode(data).decode("utf-8")


    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash:generateContent?key="
        + api_key
    )


    payload = {

        "contents": [

            {

                "parts": [

                    {
                        "text": prompt
                    },

                    {
                        "inline_data": {
                            "mime_type": mime,
                            "data": encoded
                        }
                    }

                ]

            }

        ],

        "generationConfig": {

            "temperature": 0.1,

            "responseMimeType": "application/json"

        }

    }


    try:

        r = requests.post(
            url,
            json=payload,
            timeout=120
        )


        # Show the real Gemini API error instead of hiding it.
        if not r.ok:

            return {
                "error":
                f"Gemini API error {r.status_code}: "
                f"{r.text[:1000]}"
            }


        r.raise_for_status()

        result = r.json()


        text = (
            result["candidates"][0]
            ["content"]["parts"][0]["text"]
        )


        return json.loads(text)


    except Exception as e:

        return {
            "error":
            f"AI processing failed: "
            f"{type(e).__name__}: "
            f"{str(e)[:500]}"
        }
