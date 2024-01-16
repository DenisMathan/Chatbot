import PyPDF2

def splitkeep(s, delimiter):
    split = s.split(delimiter)
    return [split[0]] + [delimiter + substr for substr in split[1:]]

def pdf_to_text(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    #for page_num in range(26,27): #range( len(pdf_reader.pages)):
    #    print(page_num)
    #    text += pdf_reader.pages[page_num].extract_text()
    #    text.split('\n\n')
    text = pdf_reader.pages[26].extract_text()
    parantheses = splitkeep(text, '\n§')
    print(len(parantheses), parantheses)
    pdf_file.close()
    return text


def split_pdf(input_path, output_path, chunk_size=5):
    with open(input_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        for start_page in range(0, total_pages, chunk_size):
            end_page = min(start_page + chunk_size, total_pages)

            pdf_writer = PyPDF2.PdfWriter()
            for page_num in range(start_page, end_page):
                pdf_writer.add_page(pdf_reader.pages[page_num])
                print("pageText", pdf_reader.pages[page_num].extract_text())

            output_file_path = f"{output_path}_pages_{start_page + 1}-{end_page}.pdf"

            #with open(output_file_path, 'wb') as output_file:
                #pdf_writer.write(output_file)

if __name__ == "__main__":
    input_pdf_path = "./data/BGB.pdf"
    output_pdf_path_prefix = "ausgabe"
    text = pdf_to_text(input_pdf_path)
    #print(text)
    #split_pdf(input_pdf_path, output_pdf_path_prefix)

