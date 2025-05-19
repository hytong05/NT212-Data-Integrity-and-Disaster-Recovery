import os

def recover_pdf_files(image_path, output_dir):
    # Định nghĩa header và footer cho file PDF
    pdf_header = b'%PDF'
    pdf_footer = b'%%EOF'

    # Đọc toàn bộ file image vào memory (chỉ nên dùng cho image nhỏ, nếu lớn thì nên đọc từng phần)
    with open(image_path, 'rb') as f:
        data = f.read()
    length = len(data)
    found = 0

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    start = 0
    while True:
        start = data.find(pdf_header, start)
        if start == -1:
            break
        end = data.find(pdf_footer, start)
        if end == -1:
            break
        end += len(pdf_footer)
        found += 1
        filename = f"{output_dir}/recovered_{found:03d}.pdf"
        with open(filename, 'wb') as out:
            out.write(data[start:end])
        print(f"Recovered: {filename} (offset {start}–{end})")
        start = end

    print(f"Đã phục hồi tổng cộng {found} file PDF vào thư mục '{output_dir}'.")

if __name__ == '__main__':
    image_file = 'Image01.vhd'
    output_folder = 'recovered_pdf'
    recover_pdf_files(image_file, output_folder)