import os
import json
import base64
import re
import requests

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse

app = FastAPI(title="MedLens — AI Clinical Insight")

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MedLens — AI Clinical Intelligence</title>

<style>
*{box-sizing:border-box}

:root{
--bg:#050914;
--panel:rgba(12,22,40,.82);
--line:rgba(72,217,255,.18);
--text:#eaf5ff;
--muted:#8ea6c1;
--cyan:#48d9ff;
--blue:#5b8cff;
--green:#48e0a4;
--yellow:#ffd166;
--red:#ff6b81
}

html{scroll-behavior:smooth}

body{
margin:0;
font-family:Inter,"Segoe UI",Arial,sans-serif;
color:var(--text);
background:
radial-gradient(circle at 15% 5%,rgba(40,130,255,.18),transparent 28%),
radial-gradient(circle at 85% 15%,rgba(0,220,255,.11),transparent 25%),
radial-gradient(circle at 50% 100%,rgba(90,70,255,.12),transparent 35%),
var(--bg);
min-height:100vh;
overflow-x:hidden
}

body:before{
content:"";
position:fixed;
inset:0;
pointer-events:none;
background-image:
linear-gradient(rgba(100,180,255,.035) 1px,transparent 1px),
linear-gradient(90deg,rgba(100,180,255,.035) 1px,transparent 1px);
background-size:42px 42px;
mask-image:linear-gradient(to bottom,black,transparent 90%)
}

.header{
border-bottom:1px solid var(--line);
padding:38px 20px 30px;
background:rgba(5,12,25,.78);
backdrop-filter:blur(18px)
}

.header-inner{
max-width:1120px;
margin:auto
}

.brand{
display:flex;
align-items:center;
gap:15px
}

.logo{
width:58px;
height:58px;
display:grid;
place-items:center;
border-radius:17px;
background:linear-gradient(135deg,rgba(72,217,255,.18),rgba(91,140,255,.2));
border:1px solid rgba(72,217,255,.42);
box-shadow:0 0 35px rgba(72,217,255,.16);
font-size:29px
}

h1{
margin:0;
font-size:40px;
letter-spacing:-1.2px
}

h1 span{color:var(--cyan)}

.header p{
margin:6px 0 0;
color:var(--muted);
font-size:15px
}

.tag{
display:inline-flex;
align-items:center;
gap:8px;
margin-top:22px;
padding:8px 13px;
border:1px solid rgba(72,224,164,.25);
border-radius:30px;
background:rgba(72,224,164,.06);
color:var(--green);
font-size:11px;
font-weight:800;
letter-spacing:.6px
}

.dot{
width:7px;
height:7px;
border-radius:50%;
background:var(--green);
box-shadow:0 0 10px var(--green)
}

.container{
max-width:1120px;
margin:30px auto;
padding:0 18px
}

.card{
position:relative;
margin-bottom:21px;
padding:27px;
border-radius:20px;
background:linear-gradient(145deg,rgba(17,30,52,.9),rgba(7,16,31,.82));
border:1px solid var(--line);
box-shadow:0 18px 55px rgba(0,0,0,.25);
backdrop-filter:blur(18px)
}

.card:before{
content:"";
position:absolute;
top:0;
left:28px;
right:28px;
height:1px;
background:linear-gradient(90deg,transparent,var(--cyan),transparent);
opacity:.45
}

.title{
display:flex;
align-items:center;
gap:12px;
margin-bottom:21px
}

.icon{
width:40px;
height:40px;
display:grid;
place-items:center;
border-radius:11px;
background:rgba(72,217,255,.08);
border:1px solid rgba(72,217,255,.18)
}

h2{
margin:0;
font-size:20px
}

.sub{
margin-top:4px;
color:var(--muted);
font-size:13px
}

.grid{
display:grid;
grid-template-columns:repeat(2,1fr);
gap:16px
}

.full{
grid-column:1/-1
}

label{
display:block;
margin-bottom:8px;
color:#b9cce1;
font-size:12px;
font-weight:800;
letter-spacing:.5px
}

input,
textarea,
select{
width:100%;
padding:13px 14px;
border:1px solid rgba(130,170,210,.18);
border-radius:11px;
outline:none;
background:rgba(2,9,21,.72);
color:var(--text);
font-size:14px;
transition:.2s
}

input:focus,
textarea:focus,
select:focus{
border-color:rgba(72,217,255,.65);
box-shadow:0 0 0 3px rgba(72,217,255,.07)
}

select option{
background:#0b1628
}

textarea{
min-height:82px;
resize:vertical
}

.upload{
padding:34px 20px;
text-align:center;
border:1px dashed rgba(72,217,255,.45);
border-radius:17px;
background:
radial-gradient(circle,rgba(72,217,255,.07),transparent 60%),
rgba(3,10,22,.5);
transition:.25s
}

.upload:hover{
border-color:var(--cyan);
box-shadow:0 0 35px rgba(72,217,255,.08)
}

.upload-icon{
font-size:40px;
margin-bottom:9px
}

.upload strong{
display:block;
font-size:15px
}

.upload p{
margin:6px 0;
color:var(--muted);
font-size:13px
}

.upload small{
color:#647d98
}

#report{
margin-top:15px;
border:0;
padding:8px
}

button{
width:100%;
margin-top:18px;
padding:15px 22px;
border:1px solid rgba(72,217,255,.45);
border-radius:12px;
color:white;
background:linear-gradient(100deg,#167bd8,#536dff);
font-size:15px;
font-weight:800;
cursor:pointer;
box-shadow:0 8px 30px rgba(55,115,255,.2);
transition:.2s
}

button:hover{
transform:translateY(-1px);
box-shadow:0 12px 35px rgba(55,115,255,.32)
}

button:disabled{
opacity:.55;
cursor:wait;
transform:none
}

.status{
text-align:center;
min-height:20px;
margin-top:13px;
color:var(--cyan);
font-size:13px
}

.table-wrap{
overflow-x:auto;
border:1px solid var(--line);
border-radius:13px
}

table{
width:100%;
min-width:900px;
border-collapse:collapse
}

th,
td{
padding:13px;
border-bottom:1px solid rgba(110,180,255,.1);
text-align:left;
vertical-align:top;
font-size:13px
}

th{
background:rgba(72,217,255,.055);
color:#a9c8e5;
font-size:11px;
text-transform:uppercase;
letter-spacing:.5px
}

td{
color:#d8e6f5
}

tr:hover td{
background:rgba(72,217,255,.025)
}

.badge{
display:inline-block;
padding:5px 10px;
border-radius:20px;
font-size:11px;
font-weight:800
}

.low{
background:rgba(255,209,102,.12);
color:var(--yellow);
border:1px solid rgba(255,209,102,.2)
}

.normal{
background:rgba(72,224,164,.11);
color:var(--green);
border:1px solid rgba(72,224,164,.2)
}

.high{
background:rgba(255,107,129,.11);
color:var(--red);
border:1px solid rgba(255,107,129,.2)
}

.unknown{
background:rgba(150,170,195,.1);
color:#aebed0;
border:1px solid rgba(150,170,195,.18)
}

.conflict{
padding:13px;
margin:9px 0;
border-radius:10px;
background:rgba(255,190,70,.06);
border:1px solid rgba(255,190,70,.2);
border-left:3px solid var(--yellow);
color:#e8d9ad;
font-size:13px
}

.summary{
padding:20px;
border-radius:13px;
background:linear-gradient(135deg,rgba(72,217,255,.055),rgba(91,140,255,.05));
border:1px solid rgba(72,217,255,.12);
line-height:1.7;
color:#d8e8f8;
font-size:14px
}

.notice{
padding:17px;
border-radius:11px;
background:rgba(255,190,70,.055);
border:1px solid rgba(255,190,70,.16);
border-left:3px solid var(--yellow);
line-height:1.65;
color:#d9cfae;
font-size:13px
}

.notice strong{
color:var(--yellow)
}

.empty{
color:#738ba5;
padding:10px 0
}

.footer{
text-align:center;
color:#50667f;
font-size:12px;
padding:5px 0 35px
}

@media(max-width:700px){
.grid{grid-template-columns:1fr}
.full{grid-column:auto}
.header h1{font-size:29px}
.card{padding:20px}
.container{margin-top:20px}
}
</style>
</head>

<body>

<header class="header">
<div class="header-inner">

<div class="brand">

<div class="logo">🧬</div>

<div>
<h1><span>Med</span>Lens</h1>
<p>AI-Powered Clinical Information Intelligence</p>
</div>

</div>

<div class="tag">
<span class="dot"></span>
AI INFORMATION STRUCTURING SYSTEM
</div>

</div>
</header>


<main class="container">


<div class="card">

<div class="title">

<div class="icon">👤</div>

<div>
<h2>Patient Information</h2>
<div class="sub">Provide available patient context</div>
</div>

</div>


<div class="grid">

<div>
<label>AGE</label>
<input id="age" type="number" min="0" max="150" placeholder="e.g. 21">
</div>

<div>
<label>SEX</label>

<select id="sex">
<option value="">Select</option>
<option>Male</option>
<option>Female</option>
<option>Other</option>
<option>Prefer not to say</option>
</select>

</div>

<div class="full">
<label>SYMPTOMS</label>
<textarea id="symptoms" placeholder="Enter patient-reported symptoms"></textarea>
</div>

<div>
<label>KNOWN CONDITIONS</label>
<textarea id="conditions" placeholder="Existing conditions"></textarea>
</div>

<div>
<label>ALLERGIES</label>
<textarea id="allergies" placeholder="Known allergies"></textarea>
</div>

<div class="full">
<label>CURRENT MEDICATIONS</label>
<textarea id="medications" placeholder="Current medications"></textarea>
</div>

</div>
</div>


<div class="card">

<div class="title">

<div class="icon">📄</div>

<div>
<h2>Medical Report</h2>
<div class="sub">Upload a report for AI-powered structuring</div>
</div>

</div>


<div class="upload">

<div class="upload-icon">☁️</div>

<strong>Upload Medical Report</strong>

<p>PDF, JPG, PNG or WEBP</p>

<small>Maximum file size: 8 MB</small>

<input
id="report"
type="file"
accept=".pdf,.jpg,.jpeg,.png,.webp"
>

</div>


<button id="processBtn" onclick="processReport()">
⚡ Process Medical Report
</button>

<div id="status" class="status"></div>

</div>


<div id="results"></div>


<div class="footer">
MedLens • Clinical information structuring • Human review required
</div>


</main>


<script>

function escapeHTML(value){

if(value===null||value===undefined){
return "";
}

return String(value)
.replace(/&/g,"&amp;")
.replace(/</g,"&lt;")
.replace(/>/g,"&gt;")
.replace(/"/g,"&quot;")
.replace(/'/g,"&#039;");

}


function statusBadge(status){

const value=String(
status||"UNKNOWN"
).toUpperCase();

let cls="unknown";

if(value==="LOW"){
cls="low";
}

if(value==="NORMAL"){
cls="normal";
}

if(value==="HIGH"){
cls="high";
}

return `
<span class="badge ${cls}">
${escapeHTML(value)}
</span>
`;

}


async function processReport(){

const fileInput=
document.getElementById("report");

const button=
document.getElementById("processBtn");

const status=
document.getElementById("status");

const results=
document.getElementById("results");


if(!fileInput.files.length){

alert(
"Please upload a medical report first."
);

return;

}


const file=
fileInput.files[0];


if(file.size>8*1024*1024){

alert(
"File is too large. Maximum allowed size is 8 MB."
);

return;

}


const patient={

age:
document.getElementById("age").value,

sex:
document.getElementById("sex").value,

symptoms:
document.getElementById("symptoms").value,

conditions:
document.getElementById("conditions").value,

allergies:
document.getElementById("allergies").value,

medications:
document.getElementById("medications").value

};


const formData=
new FormData();


formData.append(
"file",
file
);


formData.append(
"patient",
JSON.stringify(patient)
);


button.disabled=true;

button.textContent=
"⏳ AI Processing...";


status.textContent=
"🔎 Reading and structuring the medical report...";


results.innerHTML="";


try{

const response=
await fetch(
"/analyze",
{
method:"POST",
body:formData
}
);


const data=
await response.json();


if(data.error){

throw new Error(
data.error
);

}


renderResults(data);


status.textContent=
"✓ Report processed successfully.";


}catch(error){

alert(
error.message||
"Unable to process report."
);


status.textContent=
"✕ Processing failed.";


}finally{

button.disabled=false;

button.textContent=
"⚡ Process Medical Report";

}

}


function renderResults(data){

const results=
document.getElementById("results");


let rows="";


if(
data.tests&&
data.tests.length
){

data.tests.forEach(test=>{

rows+=`

<tr>

<td>
${escapeHTML(test.test_name)}
</td>

<td>
${escapeHTML(test.value)}
</td>

<td>
${escapeHTML(test.unit)}
</td>

<td>
${escapeHTML(test.reference_range)}
</td>

<td>
${statusBadge(test.status)}
</td>

<td>
${escapeHTML(test.date)}
</td>

<td>
${escapeHTML(test.observation)}
</td>

<td>
${escapeHTML(test.source)}
</td>

</tr>

`;

});

}else{

rows=`

<tr>

<td
colspan="8"
class="empty"
>
No structured test results were extracted.
</td>

</tr>

`;

}


let conflicts="";


if(
data.conflicts&&
data.conflicts.length
){

data.conflicts.forEach(item=>{

conflicts+=`

<div class="conflict">
⚠️ ${escapeHTML(item)}
</div>

`;

});

}else{

conflicts=`

<p class="empty">
✓ No conflicts were detected in the supplied information.
</p>

`;

}


results.innerHTML=`

<div class="card">

<div class="title">

<div class="icon">📊</div>

<div>
<h2>Structured Medical Record</h2>
<div class="sub">
AI-extracted information from the uploaded source
</div>
</div>

</div>


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

<div class="title">

<div class="icon">⚠️</div>

<div>
<h2>Conflict Detection</h2>

<div class="sub">
Potential inconsistencies requiring human review
</div>

</div>

</div>

${conflicts}

</div>


<div class="card">

<div class="title">

<div class="icon">🧠</div>

<div>
<h2>Patient-Friendly Summary</h2>

<div class="sub">
Simplified view of information found in the report
</div>

</div>

</div>


<div class="summary">

${escapeHTML(
data.summary||
"No summary generated."
)}

</div>

</div>


<div class="card">

<div class="title">

<div class="icon">🔐</div>

<div>
<h2>Responsible AI</h2>

<div class="sub">
Safety and transparency layer
</div>

</div>

</div>


<div class="notice">

<strong>
MedLens is a review-support tool.
</strong>

<br><br>

It does not provide a medical diagnosis,
prescribe treatment, recommend medication
changes, or determine medication dosage.

<br><br>

Reference-range status is marked LOW,
NORMAL, or HIGH only when the uploaded
report provides the relevant reference
range. Otherwise, the status is shown
as UNKNOWN.

<br><br>

AI-extracted information should be reviewed
by a qualified human before clinical use.

</div>

</div>

`;

}

</script>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML


def clean_json_text(text):

    text=text.strip()

    text=re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text=re.sub(
        r"^```\s*",
        "",
        text
    )

    text=re.sub(
        r"\s*```$",
        "",
        text
    )

    start=text.find("{")
    end=text.rfind("}")

    if start!=-1 and end!=-1:
        text=text[start:end+1]

    return text.strip()


def make_data_url(file_bytes,mime_type):

    encoded=base64.b64encode(
        file_bytes
    ).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


def normalize_result(data):

    if not isinstance(data,dict):
        data={}

    tests=data.get(
        "tests",
        []
    )

    if not isinstance(tests,list):
        tests=[]

    normalized_tests=[]

    for test in tests:

        if not isinstance(test,dict):
            continue

        status=str(
            test.get(
                "status",
                "UNKNOWN"
            )
        ).upper()

        if status not in [
            "LOW",
            "NORMAL",
            "HIGH",
            "UNKNOWN"
        ]:
            status="UNKNOWN"

        normalized_tests.append({

            "test_name":str(
                test.get(
                    "test_name",
                    ""
                )
            ),

            "value":str(
                test.get(
                    "value",
                    ""
                )
            ),

            "unit":str(
                test.get(
                    "unit",
                    ""
                )
            ),

            "reference_range":str(
                test.get(
                    "reference_range",
                    ""
                )
            ),

            "status":status,

            "date":str(
                test.get(
                    "date",
                    ""
                )
            ),

            "observation":str(
                test.get(
                    "observation",
                    ""
                )
            ),

            "source":str(
                test.get(
                    "source",
                    "uploaded report"
                )
            )
        })


    conflicts=data.get(
        "conflicts",
        []
    )

    if not isinstance(
        conflicts,
        list
    ):
        conflicts=[
            str(conflicts)
        ]


    return {

        "tests":
            normalized_tests,

        "conflicts":
            [
                str(x)
                for x in conflicts
            ],

        "summary":
            str(
                data.get(
                    "summary",
                    ""
                )
            )
    }


@app.post("/analyze")
async def analyze(
    file:UploadFile=File(...),
    patient:str=Form("{}")
):

    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    )


    if not api_key:

        return {
            "error":
                "OPENROUTER_API_KEY is not configured in Render."
        }


    allowed_types={
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/webp"
    }


    mime_type=(
        file.content_type
        or "application/octet-stream"
    )


    if mime_type not in allowed_types:

        return {
            "error":
                "Unsupported file type. Please upload PDF, JPG, PNG, or WEBP."
        }


    file_bytes=await file.read()


    if len(file_bytes)>8*1024*1024:

        return {
            "error":
                "File is too large. Maximum allowed size is 8 MB."
        }


    try:

        patient_data=json.loads(
            patient
        )

    except Exception:

        patient_data={}


    prompt=f"""
You are the extraction engine for MedLens,
a clinical information structuring application.

Your job is NOT to diagnose the patient.

Your job is to read the uploaded medical report
and convert its information into a structured
medical record.

PATIENT-PROVIDED INFORMATION:

{json.dumps(
    patient_data,
    ensure_ascii=False
)}

IMPORTANT SAFETY AND ACCURACY RULES:

1. Extract medical test information ONLY
   from the uploaded report.

2. NEVER invent a laboratory value.

3. NEVER invent a unit.

4. NEVER invent a date.

5. NEVER invent a reference range.

6. If the report does not provide a reference
   range for a test, set reference_range to an
   empty string and status to UNKNOWN.

7. LOW, NORMAL, or HIGH may ONLY be assigned
   when the uploaded report itself provides a
   reference range that allows that classification.

8. Do not use general medical knowledge to create
   reference ranges.

9. Do not diagnose, infer, or speculate about a
   disease or medical condition.

10. If the uploaded report itself mentions a
    diagnosis, suspected condition, possible cause,
    or clinical interpretation, reproduce it ONLY
    as an attributed statement such as
    "The report states..." or "The report mentions...".

11. Do not turn observations into your own
    medical conclusions.

12. Do not recommend treatment, medication changes,
    dosage changes, or clinical actions.

13. Do not present uncertain information as fact.

14. Keep the patient-friendly summary factual and
    based only on information present in the uploaded
    report and user-provided patient information.

15. Detect obvious contradictions inside the supplied
    information and list them under conflicts.

16. Do NOT treat missing optional patient information
    as a conflict.

17. Produce a concise patient-friendly summary
    describing information present in the report.
    Do not give a diagnosis or treatment advice.

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


    data_url=make_data_url(
        file_bytes,
        mime_type
    )


    headers={
        "Authorization":
            f"Bearer {api_key}",

        "Content-Type":
            "application/json"
    }


    if mime_type=="application/pdf":

        content=[

            {
                "type":
                    "text",

                "text":
                    prompt
            },

            {
                "type":
                    "file",

                "file":{

                    "filename":
                        file.filename
                        or "medical_report.pdf",

                    "file_data":
                        data_url
                }
            }
        ]

    else:

        content=[

            {
                "type":
                    "text",

                "text":
                    prompt
            },

            {
                "type":
                    "image_url",

                "image_url":{

                    "url":
                        data_url
                }
            }
        ]


    payload={

        "model":
            "openrouter/free",

        "messages":[

            {
                "role":
                    "user",

                "content":
                    content
            }
        ]
    }


    try:

        response=requests.post(

            "https://openrouter.ai/api/v1/chat/completions",

            headers=headers,

            json=payload,

            timeout=120
        )


        if not response.ok:

            return {

                "error":
                    (
                        f"OpenRouter API error "
                        f"{response.status_code}: "
                        f"{response.text[:1500]}"
                    )
            }


        result=response.json()


        choices=result.get(
            "choices",
            []
        )


        if not choices:

            return {
                "error":
                    "OpenRouter returned no model response."
            }


        message=choices[0].get(
            "message",
            {}
        )


        content=message.get(
            "content",
            ""
        )


        if isinstance(
            content,
            list
        ):

            parts=[]

            for item in content:

                if isinstance(
                    item,
                    dict
                ) and "text" in item:

                    parts.append(
                        str(
                            item["text"]
                        )
                    )

                else:

                    parts.append(
                        str(item)
                    )

            content="".join(parts)


        content=str(content)


        cleaned=clean_json_text(
            content
        )


        try:

            parsed=json.loads(
                cleaned
            )

        except Exception:

            return {

                "error":
                    (
                        "The AI returned an unexpected format. "
                        f"Raw response: {content[:1500]}"
                    )
            }


        return normalize_result(
            parsed
        )


    except requests.exceptions.Timeout:

        return {

            "error":
                "OpenRouter request timed out. Please try again."
        }


    except requests.exceptions.RequestException as e:

        return {

            "error":
                (
                    "Network error while contacting OpenRouter: "
                    f"{str(e)[:500]}"
                )
        }


    except Exception as e:

        return {

            "error":
                (
                    "AI processing failed: "
                    f"{type(e).__name__}: "
                    f"{str(e)[:500]}"
                )
        }
