from reportlab.lib.pagesizes import letter #imports standard page layout (8.5x11 inches)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table


def build_pdf(data, output_path="Certificate.pdf"):
    data = data if isinstance(data, dict) else {}  #failsafe function that defines the output but if the input data is not a dictionary the data is set to {}

    verification = data.get("verification") or {}
    test_results = data.get("test_results") or []
    instrument = data.get("instrument") or {}
    owner = data.get("owner") or {}
    officer = data.get("officer") or {} #we use or {}\[] incase data is of invalid datatype

    v_id = verification.get("id", "N/A")
    date = str(verification.get("verification_date", "N/A")).split("T")[0] #converts timestamp into readable forrm by splitting at "T"
    fresult = verification.get("result", "PENDING")

    instrument_type = instrument.get("instrument_type", "N/A")
    serial_number = instrument.get("serial_number", "N/A")
    manufacturer = instrument.get("manufacturer", "N/A")
    model = instrument.get("model", "N/A")
    location = instrument.get("location", "N/A")

    owner_name = owner.get("name", "N/A")
    officer_name = officer.get("name", "N/A")
    officer_id = officer.get("id", verification.get("officer_id", "N/A"))
#-----------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------
    doc = SimpleDocTemplate( #standard pdf layout
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
#creating styles for our text
    styles = getSampleStyleSheet() #built into reportlab to load default styles
    title = ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=14, alignment=1, leading=18)
    subtitle = ParagraphStyle("Subtitle", fontName="Helvetica", fontSize=11, alignment=1, leading=14)
    normal = ParagraphStyle("Normal", fontName="Helvetica", fontSize=9, leading=12)
    bold = ParagraphStyle("Bold", fontName="Helvetica-Bold", fontSize=9, leading=12)
#-----------------------------------------------------------------------------------------


#start of adding text
    story = [
        Paragraph("MaapYaantra", title),
        Paragraph("MINISTRY OF CONSUMER AFFAIRS", title),
        Paragraph("Instrument Verification Certificate", subtitle),
        Spacer(1, 15),
    ] # in reportlab the page layout is stored in a list



#-----------------------------------------------------------------------------------------

    details = [        [
            Paragraph(f"<b>Verification ID:</b> {v_id}", normal),
            Paragraph(f"<b>Date:</b> {date}", normal),
        ],
        [
            Paragraph(f"<b>Instrument:</b> {instrument_type}", normal),
            Paragraph(f"<b>Serial No:</b> {serial_number}", normal),
        ],
        [
            Paragraph(f"<b>Manufacturer:</b> {manufacturer}", normal),
            Paragraph(f"<b>Model:</b> {model}", normal),
        ],
        [
            Paragraph(f"<b>Owner:</b> {owner_name}", normal),
            Paragraph(f"<b>Location:</b> {location}", normal),
        ],
    ]  #builds 4x2 grid layout with <b> followed </b> to bold certain character(better than defining style bcz we can intermix bold and non-bold)

#-----------------------------------------------------------------------------------------


    story.append(Table(details, colWidths=[270, 270]))
    story.append(Spacer(1, 15))

    tdata = [
        [
            "Test ID",
            "Standard",
            "Observed",
            "Error",
            "Permissible Error",
            "Result",
        ]
    ] #defines table header row

    for item in test_results:
        tdata.append([
            str(item.get("id", "N/A")),
            str(item.get("standard_value", "N/A")),
            str(item.get("observed_value", "N/A")),
            str(item.get("error", "N/A")),
            str(item.get("permissible_error", "N/A")),
            str(item.get("result", "N/A")),
        ]) #looping thru each value of testresults

   # if len(tdata) == 1:
   #    tdata.append(["N/A"] * 6)

    ttable = Table(tdata, colWidths=[60, 95, 95, 95, 105, 90]) #creates the column widths summing to 540 points
    ttable.setStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, "blue"), #draws 0.5 point sized border around all cells
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"), #centres all text in cells
    ])

    story.append(ttable)
    story.append(Spacer(1, 15))
    story.append(Paragraph(f"<b>FINAL RESULT:</b> {fresult}", bold))
    story.append(Spacer(1, 220))

    officerinfo = f"<b>Inspecting Officer:</b> {officer_name}<br/><b>Officer ID:</b> {officer_id}"
    signature = "<b>Authorized Signatory:</b><br/><br/><br/>___________________________<br/>Inspector Signature"

    footer = Table(
        [[Paragraph(officerinfo, normal), Paragraph(signature, normal)]],
        colWidths=[270, 270],
    )

    story.append(footer)
    doc.build(story)