# SupeRR Selector: Rajasthan Royals IPL 2027 Auction Analytics

Professional cricket analytics intelligence system built for **SupeRR Selector Season 2: Help Shape Rajasthan Royals' IPL 2027 Auction Strategy** (Round 1).

Identifies and ranks the **Most Reliable Batters and Bowlers Under Pressure** across 200,999 historical IPL and T20 International deliveries (2022–2026).

---

## 🏆 Official Top 10 Rankings Under Pressure

### Top 10 Batters
| Rank | Player | Player ID | Primary Team | Pressure Balls | Normal SR | Pressure SR | SR Lift | Pressure Avg | Boundary % | Reliability Score |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Virat Kohli** | 47 | India / RCB | 148 | 145.24 | **191.22** | **+45.98** | **47.17** | 25.68% | **91.21** |
| **2** | **Suryakumar Yadav** | 1699 | India / MI | 335 | 166.43 | **214.33** | **+47.90** | **31.22** | 34.03% | **90.57** |
| **3** | **Rishabh Pant** | 4703 | India / DC | 253 | 143.06 | **193.68** | **+50.61** | **30.62** | 29.64% | **90.08** |
| **4** | **Jos Buttler** | 813 | England / RR | 261 | 155.39 | **195.79** | **+40.39** | **26.89** | 29.50% | **87.39** |
| **5** | **Glenn Phillips** | 4853 | New Zealand / SRH | 219 | 148.67 | **201.37** | **+52.70** | **25.94** | 27.85% | **87.32** |
| **6** | **Quinton de Kock** | 2101 | South Africa / LSG | 79 | 150.87 | **225.32** | **+74.44** | **44.50** | 31.65% | **86.32** |
| **7** | **Tristan Stubbs** | 20702 | South Africa / DC | 457 | 149.91 | **182.71** | **+32.81** | **39.76** | 24.73% | **86.01** |
| **8** | **Rinku Singh** | 4708 | India / KKR | 640 | 152.68 | **182.34** | **+29.66** | **41.68** | 26.56% | **84.90** |
| **9** | **Harry Brook** | 6280 | England / SRH | 178 | 163.78 | **191.01** | **+27.23** | **37.78** | 27.53% | **84.08** |
| **10** | **Tilak Varma** | 7897 | India / MI | 562 | 142.98 | **181.32** | **+38.33** | **36.39** | 24.38% | **83.93** |

### Top 10 Bowlers
| Rank | Player | Player ID | Primary Team | Pressure Balls | Normal Econ | Pressure Econ | Econ Suppress | Pressure Avg | Dot % | Reliability Score |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Kuldeep Yadav** | 3644 | India / DC | 379 | 8.02 | **6.84** | **+1.18** | **10.54** | 41.98% | **99.55** |
| **2** | **Sunil Narine** | 781 | KKR | 310 | 6.86 | **5.85** | **+1.02** | **13.13** | 45.57% | **93.08** |
| **3** | **Abrar Ahmed** | 5979 | Pakistan | 215 | 6.68 | **4.86** | **+1.83** | **10.88** | 51.38% | **91.56** |
| **4** | **Noor Ahmad** | 7967 | Afghanistan / GT | 283 | 8.01 | **7.36** | **+0.65** | **12.85** | 40.94% | **90.50** |
| **5** | **Mohammad Nawaz** | 2490 | Pakistan | 121 | 7.12 | **5.70** | **+1.42** | **12.78** | 41.94% | **85.51** |
| **6** | **Wanindu Hasaranga** | 4900 | Sri Lanka / SRH | 361 | 7.94 | **7.63** | **+0.31** | **12.75** | 39.12% | **85.28** |
| **7** | **Shadab Khan** | 4926 | Pakistan | 148 | 7.91 | **6.20** | **+1.71** | **15.30** | 40.79% | **84.61** |
| **8** | **Shaheen Afridi** | 6355 | Pakistan | 266 | 8.01 | **7.62** | **+0.39** | **13.00** | 38.03% | **84.56** |
| **9** | **Hasan Mahmud** | 6643 | Bangladesh | 109 | 7.80 | **7.27** | **+0.54** | **12.00** | 41.59% | **84.01** |
| **10** | **Sufiyan Muqeem** | 34485 | Pakistan | 122 | 6.00 | **6.44** | -0.44 | **10.92** | 51.61% | **81.76** |

---

## 🚀 How to Run the Pipeline & Dashboard

### 1. Execute Pipeline & Generate Deliverables
```bash
# Run data cleaning and state feature engineering
PYTHONPATH=. ./venv/bin/python3 src/data_cleaning.py

# Run pressure engine classification
PYTHONPATH=. ./venv/bin/python3 src/pressure_engine.py

# Run official ranking engine
PYTHONPATH=. ./venv/bin/python3 src/ranking_engine.py

# Generate official PDF methodology report
PYTHONPATH=. ./venv/bin/python3 src/generate_pdf_report.py
```

### 2. Run Automated Verification Tests
```bash
./venv/bin/python3 tests/test_cricket_accounting.py
```

### 3. Launch the Interactive Streamlit Dashboard
```bash
./venv/bin/streamlit run dashboard/app.py
```
# SupeRR-Selector
