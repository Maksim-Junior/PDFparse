from pydantic import BaseModel, Field


class PDFModel(BaseModel):
    barcode_top: str = Field(default="", alias="BARCODE_TOP")
    pn: str = Field(default="", alias="PN")
    sn: str = Field(default="", alias="SN")
    description: str = Field(default="", alias="DESCRIPTION")
    location: str = Field(default="", alias="LOCATION")
    condition: str = Field(default="", alias="CONDITION")
    receiver: str = Field(default="", alias="RECEIVER#")
    uom: str = Field(default="", alias="UOM")
    exp_date: str = Field(default="", alias="EXP DATE")
    po: str = Field(default="", alias="PO")
    cert_source: str = Field(default="", alias="CERT SOURCE")
    rec_date: str = Field(default="", alias="REC.DATE")
    mfg: str = Field(default="", alias="MFG")
    batch: str = Field(default="", alias="BATCH#")
    dom: str = Field(default="", alias="DOM")
    remark: str = Field(default="", alias="REMARK")
    lot: str = Field(default="", alias="LOT#")
    tagged_by: str = Field(default="", alias="TAGGED BY")
    barcode_bottom: str = Field(default="", alias="BARCODE_BOTTOM")
    qty: str = Field(default="", alias="Qty")
    notes: str = Field(default="", alias="NOTES")


class BaseClassModel(BaseModel):
    griffon_aviation_services_llc: PDFModel = Field(default=PDFModel(), alias="GRIFFON AVIATION SERVICES LLC")
