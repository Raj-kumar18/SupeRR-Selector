"""
generate_pdf_report.py - Converts the complete methodology report into a professional PDF submission.
Explicitly documents both:
Layer 1: Official Overall Rankings (Unstop Entry)
Layer 2: Rajasthan Royals Recruitment Intelligence & Categories
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from pathlib import Path
import pandas as pd

def generate_pdf():
    pdf_path = Path("reports/final_methodology_report.pdf")
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#ea1a7f'), # RR Pink
        alignment=1,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#17387e'), # RR Navy Blue
        alignment=1,
        spaceAfter=14
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#17387e'),
        spaceBefore=10,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        spaceAfter=5
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )
    
    elements = []
    
    # Header Title
    elements.append(Paragraph("👑 SupeRR Selector Season 2: Official Methodology Report", title_style))
    elements.append(Paragraph("Rajasthan Royals IPL 2027 Auction Analytics | Identifying Most Reliable Players Under Pressure", subtitle_style))
    elements.append(Spacer(1, 4))
    
    # Architecture Distinction
    elements.append(Paragraph("1. Analytical Architecture: Two Distinct Layers", h2_style))
    arch_text = (
        "This project strictly maintains two distinct analytical layers to eliminate bias:<br/>"
        "• <b>Layer 1 (Official Overall Rankings):</b> Follows the exact competition problem statement. Evaluates all eligible batters and "
        "bowlers across 200,999 historical IPL and T20I deliveries (2022–2026) based purely on high-pressure performance metrics, "
        "without restriction to Rajasthan Royals players.<br/>"
        "• <b>Layer 2 (Rajasthan Royals Recruitment Intelligence):</b> Evaluates player records from <i>playing_eleven.csv</i>, "
        "<i>competition_team_player_mapping.csv</i>, and tournament splits to classify players into (1) Historical Rajasthan Royals, "
        "(2) Other IPL Franchises, (3) International-Only, and (4) Potential Auction Recruitment Candidates based on tactical squad needs."
    )
    elements.append(Paragraph(arch_text, body_style))
    
    # Section 2: Pressure Definition
    elements.append(Paragraph("2. Pressure Engine Formulation", h2_style))
    pressure_text = (
        "<b>Second-Innings Chasing:</b> Evaluated before each ball using Required Run Rate (55%), Wickets in Hand (35%), and Death Overs urgency (10%), "
        "amplified by a time-decay factor (1.3x for final 30 balls).<br/>"
        "<b>First-Innings Setting:</b> Evaluated via early collapses (3+ wickets down in Powerplay), middle crises (5+ down before Over 15), and death acceleration.<br/>"
        "Across 200,999 deliveries, <b>48,324 deliveries (24.04%)</b> qualified as High Pressure."
    )
    elements.append(Paragraph(pressure_text, body_style))
    elements.append(Spacer(1, 4))
    
    # Section 3: Layer 1 Top 10 Batters Table
    elements.append(Paragraph("3. Layer 1: Recommended Top 10 Batters – Unstop Entry", h2_style))
    top_bat = pd.read_csv("data/outputs/top_10_batters_under_pressure.csv")
    
    bat_headers = ["Rank", "Player Name", "Primary Team", "Press Balls", "Norm SR", "Press SR", "SR Lift (Δ)", "Press Avg", "Bound %", "Score"]
    bat_data = [[Paragraph(h, table_header_style) for h in bat_headers]]
    
    for _, r in top_bat.iterrows():
        row = [
            Paragraph(f"#{int(r['Rank'])}", table_cell_style),
            Paragraph(str(r['player_name']), table_cell_style),
            Paragraph(str(r['team_name']), table_cell_style),
            Paragraph(str(int(r['press_balls_faced'])), table_cell_style),
            Paragraph(f"{r['norm_strike_rate']:.1f}", table_cell_style),
            Paragraph(f"{r['press_strike_rate']:.1f}", table_cell_style),
            Paragraph(f"+{r['sr_lift']:.1f}", table_cell_style),
            Paragraph(f"{r['press_average']:.1f}", table_cell_style),
            Paragraph(f"{r['press_boundary_pct']:.1f}%", table_cell_style),
            Paragraph(f"<b>{r['reliability_score']:.2f}</b>", table_cell_style)
        ]
        bat_data.append(row)
        
    t_bat = Table(bat_data, colWidths=[28, 95, 75, 36, 40, 40, 42, 42, 42, 42])
    t_bat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea1a7f')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f9f9f9')]),
    ]))
    elements.append(t_bat)
    elements.append(Spacer(1, 8))
    
    # Section 4: Layer 1 Top 10 Bowlers Table
    elements.append(Paragraph("4. Layer 1: Recommended Top 10 Bowlers – Unstop Entry", h2_style))
    top_bowl = pd.read_csv("data/outputs/top_10_bowlers_under_pressure.csv")
    
    bowl_headers = ["Rank", "Player Name", "Primary Team", "Press Balls", "Norm Econ", "Press Econ", "Econ Supp (Δ)", "Press Avg", "Dot %", "Score"]
    bowl_data = [[Paragraph(h, table_header_style) for h in bowl_headers]]
    
    for _, r in top_bowl.iterrows():
        row = [
            Paragraph(f"#{int(r['Rank'])}", table_cell_style),
            Paragraph(str(r['player_name']), table_cell_style),
            Paragraph(str(r['team_name']), table_cell_style),
            Paragraph(str(int(r['press_legal_balls'])), table_cell_style),
            Paragraph(f"{r['norm_economy']:.2f}", table_cell_style),
            Paragraph(f"{r['press_economy']:.2f}", table_cell_style),
            Paragraph(f"{r['econ_suppression']:+.2f}", table_cell_style),
            Paragraph(f"{r['press_average']:.1f}", table_cell_style),
            Paragraph(f"{r['press_dot_pct']:.1f}%", table_cell_style),
            Paragraph(f"<b>{r['reliability_score']:.2f}</b>", table_cell_style)
        ]
        bowl_data.append(row)
        
    t_bowl = Table(bowl_data, colWidths=[28, 95, 75, 36, 42, 42, 45, 40, 39, 42])
    t_bowl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#17387e')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f9f9f9')]),
    ]))
    elements.append(t_bowl)
    elements.append(Spacer(1, 8))
    
    # Section 5: Layer 2 Recruitment Shortlist Table
    elements.append(Paragraph("5. Layer 2: Rajasthan Royals Recruitment Strategy & Target Shortlist", h2_style))
    strat_text = (
        "<b>Empirical Classification from Match Data:</b><br/>"
        "• <b>Historical RR Players:</b> Jos Buttler (Rank 4, 195.8 SR), Wanindu Hasaranga (Rank 6, 7.63 Econ), Dhruv Jurel (Score: 76.16).<br/>"
        "• <b>Other IPL Franchises:</b> Virat Kohli (RCB), Suryakumar Yadav (MI), Rishabh Pant (DC), Tristan Stubbs (DC), Rinku Singh (KKR), Kuldeep Yadav (DC), Sunil Narine (KKR), Noor Ahmad (GT).<br/>"
        "• <b>International-Only Players:</b> Abrar Ahmed (4.86 Econ), Mohammad Nawaz (5.70 Econ), Shadab Khan (6.20 Econ), Shaheen Afridi (7.62 Econ).<br/>"
        "<b>RR IPL 2027 Auction Shortlist:</b><br/>"
        "1. <b>Tristan Stubbs (DC / SA):</b> Fills RR's critical finishing void (457 pressure balls, 182.7 SR, 39.8 avg).<br/>"
        "2. <b>Kuldeep Yadav (DC / India):</b> Premier wrist-spinner under pressure (6.84 Econ, 41 pressure wickets at 10.54 avg).<br/>"
        "3. <b>Tilak Varma (MI / India):</b> Prime domestic franchise cornerstone (age 23, 562 pressure balls, 181.3 SR, 36.4 avg).<br/>"
        "<i>Note: Actual auction availability is subject to official franchise retentions and player auction registrations.</i>"
    )
    elements.append(Paragraph(strat_text, body_style))
    
    doc.build(elements)
    print(f"Generated updated official PDF report at {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
