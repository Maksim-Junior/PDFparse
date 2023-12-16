import PyPDF2
from pdf2image import convert_from_path
from pyzbar import pyzbar

from models import BaseClassModel


def read_pdf_first(pdf_file: str) -> dict:
    image = convert_from_path(pdf_file)
    barcodes = pyzbar.decode(image[0])
    barcodes.sort(key=lambda x: x.rect.top)
    barcode_data = [barcode.data.decode("utf-8") for barcode in barcodes]
    with open(pdf_file, "rb") as file:
        pdf_data = PyPDF2.PdfReader(file)
        pdf_text = [line.replace(": ", ":") if ": " in line else line for line in
                    [line.replace(" :", ":") if " :" in line else line for line in
                     pdf_data.pages[0].extract_text().splitlines()]]
        pdf_text = [line + "empty" if line[-1] == ":" else line for line in pdf_text]
        pdf_text = [line.replace("NOTES", " NOTES")
                    if "NOTES" in line and " NOTES" not in line else line for line in pdf_text]
        pdf_text = [line.replace(":", ":empty ", 1)
                    if line.count(":") > 1 and " " not in line else line for
                    line in pdf_text]

        if "NOTES" in pdf_text[-1]:
            pdf_text += [""]
        parsed_data = dict()
        for line in pdf_text[1:-1]:
            if line.count(":") == 1:
                key, value = line.split(":")
                parsed_data[key] = value
            elif line.count(":") > 1:
                if line.count(" ") == 1:
                    pairs = line.split()
                    key_1, value_1 = pairs[0].split(":")
                    parsed_data[key_1] = value_1
                    key_2, value_2 = pairs[1].split(":")
                    parsed_data[key_2] = value_2
                elif line.count(" ") > 1:
                    temporary_line = line.split()
                    alone_substring = [substring for substring in temporary_line if ":" not in substring][0]
                    alone_substring_index = temporary_line.index(alone_substring)
                    first_pair = f"{alone_substring} {temporary_line[alone_substring_index + 1]}"
                    temporary_line.pop(alone_substring_index + 1)
                    temporary_line.pop(alone_substring_index)
                    key_1, value_1 = first_pair.split(":")
                    parsed_data[key_1] = value_1
                    key_2, value_2 = temporary_line[0].split(":")
                    parsed_data[key_2] = value_2
        parsed_data["NOTES"] = pdf_text[-1]
        parsed_data["BARCODE_TOP"] = barcode_data[0]
        parsed_data["BARCODE_BOTTOM"] = barcode_data[1]
        for k in parsed_data:
            if parsed_data[k] == "empty":
                parsed_data[k] = ""
    file.close()

    return {pdf_text[0]: parsed_data}


def read_pdf_second(pdf_file: str) -> dict:
    pdf_model: BaseClassModel = BaseClassModel()
    model_keys = pdf_model.griffon_aviation_services_llc.model_dump(by_alias=True).keys()
    image = convert_from_path(pdf_file)
    barcodes = pyzbar.decode(image[0])
    barcodes.sort(key=lambda x: x.rect.top)
    pdf_model.griffon_aviation_services_llc.barcode_top, pdf_model.griffon_aviation_services_llc.barcode_bottom = [
        barcode.data.decode("utf-8") for barcode in barcodes]
    pdf_model_dict: dict = pdf_model.model_dump(by_alias=True)
    with open(pdf_file, "rb") as file:
        pdf_data = PyPDF2.PdfReader(file)
        pdf_text = pdf_data.pages[0].extract_text()
        for key in model_keys:
            if key in pdf_text and f" {key}" not in pdf_text:
                pdf_text = pdf_text.replace(key, f" {key}")
        parsed_data = [word for some_elem in
                       [elem.split(":") for element in pdf_text.splitlines()[1::] for elem in
                        element.split(" ")] for word in some_elem if word != ""]
        parsed_data += " "
        for index in range(len(parsed_data)):
            if parsed_data[index] == " ":
                parsed_data.pop(-1)
                break
            if parsed_data[index] not in model_keys:
                if parsed_data[index] + f" {parsed_data[index + 1]}" in model_keys:
                    second_word = parsed_data.pop(index + 1)
                    parsed_data[index] += f" {second_word}"
        if parsed_data[-1] != "NOTES":
            notes = " ".join(parsed_data[parsed_data.index("NOTES") + 1::])
            pdf_model_dict["GRIFFON AVIATION SERVICES LLC"]["NOTES"] = notes
            parsed_data = parsed_data[:parsed_data.index("NOTES")]
        parsed_data += " "
        for index in range(len(parsed_data)):
            if parsed_data[index] == " ":
                parsed_data.pop(-1)
                break
            if parsed_data[index] in model_keys and parsed_data[index + 1] == " ":
                pdf_model_dict["GRIFFON AVIATION SERVICES LLC"][parsed_data[index]] = ""
                parsed_data.pop(-1)
            elif parsed_data[index] in model_keys and parsed_data[index + 1] not in model_keys:
                pdf_model_dict["GRIFFON AVIATION SERVICES LLC"][parsed_data[index]] = parsed_data[index + 1]
                parsed_data.pop(index + 1)
            else:
                pdf_model_dict["GRIFFON AVIATION SERVICES LLC"][parsed_data[index]] = ""

    return pdf_model_dict


if __name__ == "__main__":
    pdf_file_path = "test_task.pdf"
    # Both options are working
    # data = read_pdf_first(pdf_file_path)
    data = read_pdf_second(pdf_file_path)
