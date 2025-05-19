# Data Recovery from Formatted Disk

### Team Members

* Duong Pham Huy Thong (22521431)
* Cao Qui (22521208)

## Image File Recovery

### Concept

* The **FAT32** (File Allocation Table 32) file system was developed by Microsoft in 1977 and is highly compatible with many devices.

* When a virtual disk is formatted, the file allocation table (FAT) is overwritten, but the actual data may still exist until new data overwrites it. Therefore, recovering based on **file signatures** is a viable method.

* **Signature-based recovery**:

  * **JPG**: Starts with `\xFF\xD8\xFF`, ends with `\xFF\xD9`
  * **PNG**: Starts with `\x89\x50\x4E\x47\x0D\x0A\x1A\x0A`, ends with `\x49\x45\x4E\x44\xAE\x42\x60\x82`

* Procedure:

  * Read the entire binary file.
  * Find all regions that match image file signatures.
  * Extract and save valid regions to new files in the output directory.

### Source Code Implementation

* Read the binary file:

```python
with open(image_path, 'rb') as f:
    data = f.read()
```

* Define headers and footers:

```python
jpg_header = b'\xFF\xD8\xFF'
jpg_footer = b'\xFF\xD9'
png_header = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
png_footer = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'
```

* Recovery function:

```python
def extract_files(header, footer, ext):
    nonlocal found, offset
    pos = 0
    while pos < length:
        start = data.find(header, pos)
        if start == -1:
            break
        end = data.find(footer, start + len(header))
        if end == -1:
            break
        end += len(footer)
        found += 1
        filename = f"{output_dir}/recovered_{found:03d}.{ext}"
        with open(filename, 'wb') as out:
            out.write(data[start:end])
        print(f"Recovered: {filename} (offset {start}–{end})")
        pos = end
```

## PDF File Recovery

### Concept

* Similar to image files, PDFs also have **file signatures**:

  * Header: `%PDF` (`25 50 44 46`)
  * Footer: `%%EOF`

### Source Code Implementation

* Read data:

```python
pdf_header = b'%PDF'
pdf_footer = b'%%EOF'

with open(image_path, 'rb') as f:
    data = f.read()
length = len(data)
found = 0

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
```

* Locate and extract files:

```python
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
```

### Requirements

* Python 3.6 or higher

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/nt212-recovery-tool.git
   cd nt212-recovery-tool
   ```
2. Check Python version:

   ```bash
   python --version
   ```

### Usage

1. **Recover images (JPG and PNG):**

   ```bash
   python recovery.py
   ```

2. **Recover PDFs:**

   ```bash
   python recovery_advance.py 
   ```

### Project Directory Structure

```
nt212-recovery-tool/
├── recovery.py             # Main script for JPG/PNG recovery
├── recovery_advance.py     # Extended script for PDF recovery
├── recovered_images        # Folder containing recovered image files
├── recovered_pdf           # Folder containing recovered PDF files
├── src                     # Folder containing original source files
└── README.md
```

### Demo Video

[Watch the demo on YouTube](https://www.youtube.com/watch?v=cZDChTGsEys)

---
