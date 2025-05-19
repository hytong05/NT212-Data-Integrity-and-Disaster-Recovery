import os

def recover_images(image_path, output_dir):
    # Dấu hiệu nhận diện JPG và PNG
    jpg_header = b'\xFF\xD8\xFF'
    jpg_footer = b'\xFF\xD9'
    png_header = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    png_footer = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'
    
    # Đọc toàn bộ file image vào bộ nhớ (cẩn thận với file lớn)
    with open(image_path, 'rb') as f:
        data = f.read()
    
    found = 0
    offset = 0
    length = len(data)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Hàm tìm và phục hồi file
    def extract_files(header, footer, ext):
        nonlocal found, offset
        pos = 0
        while pos < length:
            # Tìm vị trí header
            start = data.find(header, pos)
            if start == -1:
                break
            # Tìm vị trí footer sau header
            end = data.find(footer, start + len(header))
            if end == -1:
                break
            end += len(footer)
            found += 1
            filename = f"{output_dir}/recovered_{found:03d}.{ext}"
            with open(filename, 'wb') as out:
                out.write(data[start:end])
            print(f"Recovered: {filename} (offset {start}–{end})")
            # Tiếp tục tìm sau footer
            pos = end

    # Phục hồi JPG
    extract_files(jpg_header, jpg_footer, 'jpg')
    # Phục hồi PNG
    extract_files(png_header, png_footer, 'png')
    print(f"Đã phục hồi {found} file ảnh vào thư mục '{output_dir}'.")

if __name__ == '__main__':
    # Thay đổi đường dẫn file image và thư mục output theo nhu cầu
    image_file = 'Image01.vhd' 
    output_folder = 'recovered_images'
    recover_images(image_file, output_folder)