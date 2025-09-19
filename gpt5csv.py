import pandas as pd
from datetime import datetime

rows = []

def add(date_str, category, subcategory, title, description=""):
    rows.append({
        "date": date_str,
        "category": category,
        "subcategory": subcategory,
        "title": title,
        "description": description
    })

# Solar (Kp>=5)
solar_dates = [
("2025-01-01","run Jan 1–4"),
("2025-01-02","run Jan 1–4"),
("2025-01-03","run Jan 1–4"),
("2025-01-04","run Jan 1–4"),
("2025-03-09","Kp≥6"),
("2025-03-13","Kp≥5–6"),
("2025-03-22","Kp≥5–6"),
("2025-03-26","Kp≥5–6"),
("2025-03-27","Kp≥5–6"),
("2025-04-04","Kp≥5–6"),
("2025-04-05","Kp≥5–6"),
("2025-04-06","Kp≥5–6"),
("2025-04-16","Kp≥5–6"),
("2025-04-17","Kp≥5–6"),
("2025-05-29","Kp≥5–6"),
("2025-06-01","Kp≥5–8"),
("2025-06-02","Kp≥5–8"),
("2025-06-03","Kp≥5–8"),
("2025-06-04","Kp≥5–8"),
("2025-06-12","Kp≥5–6"),
("2025-06-13","Kp≥5–6"),
("2025-06-14","Kp≥5–6"),
("2025-07-07","Kp≈5"),
("2025-08-09","Kp≥5–6"),
("2025-08-30","CME→G1; Kp≥5"),
("2025-08-31","CME→G1; Kp≥5"),
("2025-09-01","CME→G1; Kp≥5"),
("2025-09-09","G2; Kp≥6"),
("2025-09-14","G3 run; Kp~6–7"),
("2025-09-15","G3 run; Kp~6–7"),
("2025-09-16","G3 run; Kp~6–7"),
]

for d,label in solar_dates:
    add(d,"solar","kp","Geomagnetic storm day",label)

# Schumann (qualitative)
add("2025-09-14","schumann","spectrogram","Band broadening / amplitude spike window","Mid-Sept observers reported thicker SR bands; qualitative")

add("2025-09-15","schumann","spectrogram","Band broadening / amplitude spike window","Mid-Sept observers reported thicker SR bands; qualitative")
add("2025-09-16","schumann","spectrogram","Band broadening / amplitude spike window","Mid-Sept observers reported thicker SR bands; qualitative")

# Electronics / devices
add("2025-09-15","electronics","networking","UniFi gear reboot loops","reports")

# Vehicles
add("2025-08-25","vehicles","BMW X5 iDrive","Central display black/blank on startup","reports; spans to ~Sep 07")
add("2025-09-07","vehicles","BMW X5 iDrive","Central display black/blank persists","reports")
add("2025-09-15","vehicles","Tesla","Exterior door handles inoperative","reports")

# Computers / phones
add("2025-08-24","computers","iPhone 13","Display flicker after iOS 18.6.2 update","reports")
add("2025-09-15","computers","PCs","Unexpected shutdowns","reports")
add("2025-09-16","computers","Laptop","Power brick failure","personal")

# RC incidents
add("2025-08-23","rc","RC aircraft","ESC failure","forum")
add("2025-08-28","rc","RC misc","BEC/ESC failures cluster","forum")
add("2025-09-12","rc","RC heli (SAB Goblin)","OW failure","forum")
add("2025-09-13","rc","RC heli (OMP M2 MK2)","Runaway head speed","forum")
add("2025-09-16","rc","RC heli","GPS phantom home points","roommate observation")

# Language models (Anthropic/OpenAI/Gemini/Mistral etc.)
# Anthropic
add("2025-09-03","language_models","Anthropic","Elevated errors (Opus/Sonnet)","")
add("2025-09-05","language_models","Anthropic","Opus 4.1 messaging failures","unable to send")
add("2025-09-10","language_models","Anthropic","APIs & claude.ai down","")
add("2025-09-11","language_models","Anthropic","Opus 4.1 elevated errors","")
add("2025-09-12","language_models","Anthropic","Sonnet 3.7 elevated errors","")
add("2025-09-15","language_models","Anthropic","Opus 4.1 elevated errors (overnight)","")

# OpenAI
add("2025-09-09","language_models","OpenAI","ChatGPT Agent elevated error rates","")
add("2025-09-10","language_models","OpenAI","Batch API errors","")
add("2025-09-10","language_models","OpenAI","File Search broken","")
add("2025-09-11","language_models","OpenAI","Deep Research degraded","")
add("2025-09-11","language_models","OpenAI","Fine-tuning jobs delayed","")
add("2025-09-12","language_models","OpenAI","Double reply bug (GPT-5 + Agent)","")
add("2025-09-14","language_models","OpenAI","API elevated errors","")
add("2025-09-16","language_models","OpenAI","SSO login errors","")
add("2025-09-16","language_models","OpenAI","GPT Store errors","")

# Gemini
add("2025-08-26","language_models","Gemini","2.5 Pro overloaded (day/evening)","")
add("2025-09-04","language_models","Gemini","Chatbot outage","")
add("2025-09-10","language_models","Gemini","Outage reports","")
add("2025-09-15","language_models","Gemini","Image generation defaults to square","feature regression")
add("2025-09-17","language_models","Gemini","Canvas UI vanished mid-session","restart required")

# Mistral
add("2025-09-15","language_models","Mistral","OCR API downtime","")
add("2025-09-15","language_models","Mistral","Service degradation","")

# Cross-LLM instability (personal)
add("2025-09-15","language_models","Cross-LLM","Coding instability spike across Claude+Gemini","your sessions")
add("2025-09-16","language_models","Cross-LLM","Coding instability continues","your sessions")
add("2025-09-18","language_models","Cross-LLM","Coding instability still above baseline","your sessions")

# API providers / services infra
add("2025-08-28","api_providers","OpenRouter","Major outage (chat & generation)","upstream DB")
add("2025-09-12","api_providers","Cloudflare","Dashboard/API outage","also services")
add("2025-09-10","api_providers","Azure","East US 2 allocator/control plane incident","also services")

# Services/outages (web/cloud)
add("2025-09-04","services","Google","Search/Gmail/Maps/YouTube outage (Europe)","")
add("2025-09-12","services","Cloudflare","Dashboard/API outage","")
add("2025-09-15","services","Reddit","Outage (US)","")
add("2025-09-15","services","Starlink","Outage (~43k users)","")

# Personal incidents
personal_events = [
("2025-02-03","Incident A start"),
("2025-02-05","Incident A end"),
("2025-02-08","Incident B"),
("2025-02-11","Incident B end"),
("2025-02-20","Incident C–D"),
("2025-02-22","Incident C–D (continued)"),
("2025-02-25","Incident D end"),
("2025-02-26","Incident C end"),
("2025-03-02","Incident E start"),
("2025-03-03","Incident E end"),
("2025-03-05","Incident F start"),
("2025-03-09","Incident F end"),
("2025-03-18","Incident G"),
("2025-03-29","Incident H start"),
("2025-03-31","Incident H end"),
("2025-04-01","Incident I start"),
("2025-04-03","Incident I end"),
("2025-04-04","Incident J start"),
("2025-04-09","Incident J end"),
("2025-04-13","Incident K"),
("2025-04-20","Incident L"),
("2025-06-01","Incident M"),
]
for d, t in personal_events:
    add(d,"personal","social",t,"")

# Crimes
crime_events = [
("2025-08-19","DeLand, FL — Fatal shooting at homeless camp"),
("2025-08-24","Toronto — Homicide investigation (Martha Eaton Way & Trethewey Dr)"),
("2025-09-05","Langley, BC — Taxi-shooting homicide"),
("2025-09-07","Melbourne CBD — Shooting death"),
("2025-09-07","Cobblebank — Two males fatally stabbed"),
("2025-09-07","Blue Mountains — Body found in burning vehicle"),
("2025-09-08","Clapham, London — Murder investigation after double shooting"),
("2025-09-10","Burnaby, BC — Fatal shooting (IHIT)"),
("2025-09-12","Chicago, IL — Mass shooting (S. Halsted)"),
("2025-09-15","Minneapolis, MN — Mass shooting near encampment"),
("2025-09-16","Minneapolis, MN — Second mass shooting near encampment"),
("2025-09-17","Grafton, NSW — Man dies after stabbing"),
("2025-09-18","NSW — Double stabbing at rail station"),
]
for d, t in crime_events:
    add(d,"crime","",t,"")

df = pd.DataFrame(rows).sort_values("date")
out_path = "/mnt/data/master_incidents_2025.csv"
df.to_csv(out_path, index=False)
out_path
