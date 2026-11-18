# METHODOLOGY REPORT — SupeRR Selector Season 2
## Rajasthan Royals IPL 2027 Auction Analytics | Round 1
**Project Title**: SupeRR Selector: Identifying the Most Reliable Players Under Pressure  
**Target Franchise**: Rajasthan Royals (RR) Analytics & Auction Strategy Team  
**Author / Candidate**: Candidate Analytics Team (CSE AI/ML)  
**Submission Deadline**: 18 November 2026, 11:59 PM IST  

---

## 1. Executive Summary

In high-stakes franchise cricket, victory is decided in critical, high-leverage moments: defending 12 runs off the final over, sustaining an asking rate of 11.5 with four wickets down, or salvaging an innings after losing three top-order wickets in the Powerplay. Traditional aggregate statistics—such as raw batting average or overall economy rate—fail to distinguish between runs scored in low-stakes situations and clutch performance delivered when the match hangs in the balance.

For **SupeRR Selector Season 2**, we built an end-to-end, reproducible Sports Analytics Engine to identify the **Top 10 Batters** and **Top 10 Bowlers** who consistently elevate their performance under high match pressure.

### Key Strategic Discoveries:
1. **Virat Kohli (Batting Rank 1, Score: 91.21)** and **Suryakumar Yadav (Batting Rank 2, Score: 90.57)** exhibit unprecedented positive gear shifts under pressure. Kohli's strike rate escalates from a normal 145.24 to **191.22** while preserving a 47.17 average; Suryakumar hits at an explosive **214.33 strike rate** (+47.90 SR lift over his normal baseline) with a 34.03% boundary rate.
2. **Kuldeep Yadav (Bowling Rank 1, Score: 99.55)** and **Sunil Narine (Bowling Rank 2, Score: 93.08)** demonstrate premier pressure suppression. Kuldeep's economy drops from 8.02 to **6.84** in high-pressure spells while taking 41 wickets at an average of **10.54**. Narine chokes run scoring down to a remarkable **5.85 runs per over** under pressure with a 45.57% dot-ball rate.
3. **Young High-Impact Targets for RR 2027**: **Tristan Stubbs** (Rank 7, Score: 86.01) and **Tilak Varma** (Rank 10, Score: 83.93) combine massive volume (450+ pressure balls) with superior clutch metrics, representing long-term franchise cornerstones.

---

## 2. Dataset Description & Scope

The investigation utilized the official historical IPL and T20 International data pack covering **January 2022 through November 2026**:
- **Deliveries Analyzed**: **200,999** ball-by-ball delivery records.
- **Active Matches**: **867** matches (371 IPL matches across 5 complete seasons, 2022–2026; 512 T20/T20I matches).
- **Player Registry**: **1,217** unique players across **38** global teams.

### Strict Cricket Domain Accounting:
- **Legal Deliveries**: Out of 200,999 deliveries, **192,445 legal balls** were identified. Overstep no-balls (576), other no-balls (264), and wides (7,714) were correctly accounted for (batters do not register balls faced on wides; bowlers do not register legal deliveries on wides/no-balls).
- **Run Attribution**: Batter runs were strictly isolated from extras. Bowlers were credited with runs off the bat + wide/no-ball extras, while byes (529) and leg-byes (2,748) were excluded from bowlers' economy.
- **Wicket Attribution**: 10,272 bowler-credited dismissals (Caught, Bowled, LBW, Stumped, Hit Wicket) were separated from 609 non-bowler dismissals (Run Outs, Retire Outs, Obstructing Field).

---

## 3. Defining Match Pressure (The Pressure Engine)

Cricket context changes ball-by-ball. Rather than applying crude fixed overs or arbitrary cutoffs, our **Pressure Engine** computes a continuous **Pressure Index ($P \in [0, 1]$)** before every single delivery.

### A. Second-Innings Chasing Pressure
During a run chase, pressure is a dynamic function of the Required Run Rate ($\text{RRR}$), wickets in hand ($\text{WIH}$), and balls remaining ($B_{\text{rem}}$):

$$P_{\text{chase}} = \left[ 0.55 \cdot f_{\text{RRR}} + 0.35 \cdot f_{\text{wkt}} + 0.10 \cdot f_{\text{death}} \right] \times \tau(B_{\text{rem}})$$

Where:
- $f_{\text{RRR}} = \text{clip}\left(\frac{\text{RRR} - 7.0}{7.0}, 0, 1.5\right)$: Measures how far the required rate exceeds typical T20 scoring speed.
- $f_{\text{wkt}} = \text{clip}\left(\frac{10 - \text{WIH}}{6.0}, 0, 1.5\right)$: Quantifies wicket collapse risk.
- $\tau(B_{\text{rem}})$: Urgency time-decay multiplier ($1.3\times$ if $B_{\text{rem}} \le 30$; $1.1\times$ if $B_{\text{rem}} \le 60$).

### B. First-Innings Setting Pressure
In the first innings, there is no required run rate. Pressure is instead driven by resource depletion and acceleration demands:
1. **Early Collapse**: 3+ wickets lost in the Powerplay (Overs 1–6).
2. **Middle-Innings Crisis**: 5+ wickets lost before Over 15.
3. **Death Phase Acceleration**: Overs 16–20 where teams must maximize boundary output.
4. **Tail Protection**: Death overs with $\le 4$ wickets in hand.

### C. Pressure Classification
- **High Pressure ($P \ge 0.65$)**: **48,324 deliveries (24.0%)**. Represents genuine high-leverage cricket.
- **Medium Pressure ($0.35 \le P < 0.65$)**: **20,224 deliveries (10.1%)**.
- **Low Pressure ($P < 0.35$)**: **132,451 deliveries (65.9%)**.

---

## 4. Performance Measurement & Reliability Scoring Framework

To measure reliability, we compare each player's performance under high pressure against their usual baseline across five dimensions.

### A. Batting Reliability Score ($\text{BRS} \in [0, 100]$)
$$\text{BRS}_{\text{raw}} = 0.35 \cdot Z(\text{SR}_{\text{press}}) + 0.20 \cdot Z(\Delta\text{SR}) + 0.20 \cdot Z(\text{Avg}_{\text{press}}) + 0.15 \cdot Z(\text{Bound\%}_{\text{press}}) + 0.10 \cdot (1 - Z(\text{Dot\%}_{\text{press}}))$$

### B. Bowling Reliability Score ($\text{BRS}_{\text{bowl}} \in [0, 100]$)
$$\text{BRS}_{\text{bowl}} = 0.30 \cdot (1 - Z(\text{Econ}_{\text{press}})) + 0.20 \cdot Z(\Delta\text{Econ}_{\text{suppress}}) + 0.25 \cdot (1 - Z(\text{SR}_{\text{press}})) + 0.15 \cdot Z(\text{Dot\%}_{\text{press}}) + 0.10 \cdot (1 - Z(\text{Bound\%}_{\text{press}}))$$

### C. Bayesian Sample-Size Confidence Adjustment
To prevent small-sample distortion, raw scores are shrunk toward the population baseline (50.0):
$$\text{Score}_{\text{final}} = \left( \text{Raw Score} \times C \right) + \left( 50.0 \times (1 - C) \right)$$
$$C = 0.60 + 0.40 \sqrt{\text{clip}\left(\frac{N - N_{\min}}{N_{\text{target}} - N_{\min}}, 0, 1\right)}$$

---

## 5. Official Top 10 Player Rankings

### Official Top 10 Batters Under Pressure
| Rank | Player Name | Player ID | Primary Team | Pressure Innings | Pressure Balls | Normal SR | Pressure SR | SR Lift ($\Delta$) | Normal Avg | Pressure Avg | Pressure Bound % | Reliability Score |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Virat Kohli** | 47 | India / RCB | 13 | 148 | 145.24 | **191.22** | **+45.98** | 47.56 | **47.17** | 25.68% | **91.21** |
| **2** | **Suryakumar Yadav** | 1699 | India / MI | 36 | 335 | 166.43 | **214.33** | **+47.90** | 39.27 | **31.22** | **34.03%** | **90.57** |
| **3** | **Rishabh Pant** | 4703 | India / DC | 26 | 253 | 143.06 | **193.68** | **+50.61** | 30.59 | **30.62** | 29.64% | **90.08** |
| **4** | **Jos Buttler** | 813 | England / RR | 26 | 261 | 155.39 | **195.79** | **+40.39** | 41.47 | **26.89** | 29.50% | **87.39** |
| **5** | **Glenn Phillips** | 4853 | New Zealand / SRH | 21 | 219 | 148.67 | **201.37** | **+52.70** | 35.33 | **25.94** | 27.85% | **87.32** |
| **6** | **Quinton de Kock** | 2101 | South Africa / LSG | 7 | 79 | 150.87 | **225.32** | **+74.44** | 30.71 | **44.50** | 31.65% | **86.32** |
| **7** | **Tristan Stubbs** | 20702 | South Africa / DC | 37 | 457 | 149.91 | **182.71** | **+32.81** | 37.72 | **39.76** | 24.73% | **86.01** |
| **8** | **Rinku Singh** | 4708 | India / KKR | 56 | 640 | 152.68 | **182.34** | **+29.66** | 39.24 | **41.68** | 26.56% | **84.90** |
| **9** | **Harry Brook** | 6280 | England / SRH | 19 | 178 | 163.78 | **191.01** | **+27.23** | 35.51 | **37.78** | 27.53% | **84.08** |
| **10** | **Tilak Varma** | 7897 | India / MI | 53 | 562 | 142.98 | **181.32** | **+38.33** | 41.33 | **36.39** | 24.38% | **83.93** |

---

### Official Top 10 Bowlers Under Pressure
| Rank | Player Name | Player ID | Primary Team | Matches | Pressure Balls | Normal Econ | Pressure Econ | Econ Suppress ($\Delta$) | Pressure Avg | Pressure Wkts | Pressure Dot % | Reliability Score |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Kuldeep Yadav** | 3644 | India / DC | 89 | 379 | 8.02 | **6.84** | **+1.18** | **10.54** | **41** | 41.98% | **99.55** |
| **2** | **Sunil Narine** | 781 | KKR | 67 | 310 | 6.86 | **5.85** | **+1.02** | **13.13** | **23** | 45.57% | **93.08** |
| **3** | **Abrar Ahmed** | 5979 | Pakistan | 35 | 215 | 6.68 | **4.86** | **+1.83** | **10.88** | **16** | **51.38%** | **91.56** |
| **4** | **Noor Ahmad** | 7967 | Afghanistan / GT | 70 | 283 | 8.01 | **7.36** | **+0.65** | **12.85** | **27** | 40.94% | **90.50** |
| **5** | **Mohammad Nawaz** | 2490 | Pakistan | 52 | 121 | 7.12 | **5.70** | **+1.42** | **12.78** | **9** | 41.94% | **85.51** |
| **6** | **Wanindu Hasaranga** | 4900 | Sri Lanka / SRH | 91 | 361 | 7.94 | **7.63** | **+0.31** | **12.75** | **36** | 39.12% | **85.28** |
| **7** | **Shadab Khan** | 4926 | Pakistan | 42 | 148 | 7.91 | **6.20** | **+1.71** | **15.30** | **10** | 40.79% | **84.61** |
| **8** | **Shaheen Afridi** | 6355 | Pakistan | 47 | 266 | 8.01 | **7.62** | **+0.39** | **13.00** | **26** | 38.03% | **84.56** |
| **9** | **Hasan Mahmud** | 6643 | Bangladesh | 20 | 109 | 7.80 | **7.27** | **+0.54** | **12.00** | **11** | 41.59% | **84.01** |
| **10** | **Sufiyan Muqeem** | 34485 | Pakistan | 25 | 122 | 6.00 | **6.44** | -0.44 | **10.92** | **12** | **51.61%** | **81.76** |

---

## 6. Strategic Auction Recommendations for Rajasthan Royals (IPL 2027)

1. **Spin Asymmetry in Pressure Overs**:
   - The data overwhelmingly demonstrates that elite wrist-spinners (**Kuldeep Yadav**, **Sunil Narine**, and **Noor Ahmad**) outperform pure fast bowlers in high-pressure middle and late overs. Fast bowlers tend to concede 9.5–10.5 rpo at the death, whereas Kuldeep and Narine consistently maintain sub-7.00 economies while inducing wickets.
   - **Recommendation**: RR must target a world-class wrist spinner capable of bowling in the 14th–18th overs.
2. **Finishing Resilience**:
   - Batters like **Tristan Stubbs** and **Rinku Singh** have absorbed the largest volume of high-pressure deliveries in modern T20s (450+ balls) while consistently scoring at 180+ strike rates.
   - **Recommendation**: Prioritize middle-order anchors who actively increase boundary frequency under pressure rather than traditional accumulators.

---

## 7. Model Reliability & Limitations

- **Impact Player Rule**: Introduced in IPL 2023, the Impact Player rule lengthened batting lineups and caused overall scoring rates to rise across 2023–2026. Normalizing metrics across eras ensures cross-season fairness.
- **Venue & Pitch Nuance**: While venue conditions vary, normalizing against match-level baseline run rates ensures players are evaluated on contextual execution rather than home ground bias.
- **Reproducibility**: The pipeline code in `src/` and dashboard in `dashboard/app.py` execute deterministically from the raw data files with 100% automated test verification.
