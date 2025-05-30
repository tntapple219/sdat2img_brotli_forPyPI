# 📦 SDAT2IMG Brotli

[](https://www.google.com/url?sa=E&source=gmail&q=https://pypi.org/project/sdat2img-brotli/)
[](https://www.google.com/url?sa=E&source=gmail&q=https://pypi.org/project/sdat2img-brotli/)
[](https://opensource.org/licenses/MIT)

This Python script extracts and converts Android OTA update files—specifically `.dat.br` (Brotli compressed) and `.transfer.list`—into a usable `.img` disk image. This is especially useful for unpacking `system`, `vendor`, or `product` partitions from A/B OTA packages.

---
## Changelog / Release Notes

### **v1.0.1 (2025-05-31)**
* **Improved:** Simplified library import. Users can now directly `from sdat2img_brotli import convert_rom_files_function`.
-----

## ✨ Features

  * ✔️ Supports `.dat.br` files (Brotli compressed).
  * ✔️ Converts `.dat` + `.transfer.list` into a flashable `.img`.
  * ✔️ Automatic decompression of `.dat.br` and cleanup of temporary `.dat` files.
  * ✔️ **Flexible input/output paths via command-line arguments (CLI).**
  * ✔️ **Defaults to current directory files if no arguments are provided for ease of use.**
  * ✔️ User-friendly logs and error messages.

-----

## 🚀 Installation

You can easily install `sdat2img-brotli` using pip:

```bash
pip install sdat2img-brotli
```

-----

## 🔧 Requirements

  * Python 3.6 or higher.
  * The `brotli` Python module (automatically installed via pip).

-----

## 📖 Usage

This script offers **two convenient ways** to run it:

### 1\. Simple Run (Using Default Files)

If your `system.new.dat.br` and `system.transfer.list` files are in the **same directory where you run the command**, simply execute:

```bash
sdat2img-brotli
```

The tool will automatically:

1.  Decompress `system.new.dat.br` into `system.new.dat`.
2.  Convert `system.new.dat` and `system.transfer.list` into `system.img`.

### 2\. Advanced Run (Using Command-Line Arguments)

For more flexibility, you can specify the paths for input files and the output filename using command-line arguments. This is ideal for processing files not in the current directory or for renaming the output.

```bash
sdat2img-brotli -d <path_to_dat_br_file> -t <path_to_transfer_list_file> -o <output_img_name>
```

**Arguments:**

  * `-d` or `--datbr`: Specifies the path to the `.dat.br` input file.
      * Example: `-d "C:\roms\my_system.new.dat.br"`
      * Default: `system.new.dat.br`
  * `-t` or `--transferlist`: Specifies the path to the `.transfer.list` input file.
      * Example: `-t "C:\roms\my_system.transfer.list"`
      * Default: `system.transfer.list`
  * `-o` or `--outputimg`: Specifies the name and path for the output `.img` file.
      * Example: `-o "extracted_system.img"`
      * Default: `system.img`

**Practical Examples:**

  * **Convert a `vendor` partition located in a specific folder:**
    ```bash
    sdat2img-brotli -d "D:\OTA\vendor.new.dat.br" -t "D:\OTA\vendor.transfer.list" -o "vendor.img"
    ```
  * **Generate an `img` with a custom name in the current directory:**
    ```bash
    sdat2img-brotli -o "my_custom_system.img"
    ```
  * **Get help and see all available options:**
    ```bash
    sdat2img-brotli --help
    ```

### 3\. Usage as a Python Library

You can also import and use the core conversion function in your own Python projects:

```python
from sdat2img_brotli.main import convert_rom_files_function

# Example 1: Use default files (system.new.dat.br, system.transfer.list, system.img)
print("--- Starting conversion with default files ---")
success_default = convert_rom_files_function()
if success_default:
    print("Default conversion successful! 🎉")
else:
    print("Default conversion failed! ❌")

print("\n" + "="*50 + "\n")

# Example 2: Specify custom file paths
print("--- Starting conversion with custom files ---")
my_datbr_path = "path/to/your/custom_rom.new.dat.br" # Replace with your actual path
my_transfer_list_path = "path/to/your/custom_rom.transfer.list" # Replace with your actual path
my_output_image_name = "custom_extracted_image.img"

success_custom = convert_rom_files_function(
    datbr_path=my_datbr_path,
    transferlist_path=my_transfer_list_path,
    output_img_name=my_output_image_name
)

if success_custom:
    print(f"Custom conversion successful! Output: {my_output_image_name} 🎉")
else:
    print("Custom conversion failed! ❌")
```

**Note:** When using as a library, ensure the input files (`.dat.br` and `.transfer.list`) exist at the specified paths.

-----

## 📁 Output

Upon successful conversion, a `.img` file (e.g., `system.img`, `vendor.img`) will be generated. This is a raw disk image that can be opened and explored with various tools, such as:

  * 7-Zip
  * DiskGenius
  * Linux Reader (for Windows)
  * `mount` command (on Linux)
  * Other `ext4` filesystem tools on Linux

-----

## 🙏 Credits

  * Based on [xpirt’s original sdat2img](https://gist.github.com/xpirt/2c11438a0f9077227d8905391c49926d).
  * Modified for Brotli compression compatibility and enhanced usability with CLI arguments.

-----

## 📄 License

This script is open-source and released under the [MIT License](https://opensource.org/licenses/MIT). Use it freely and feel free to contribute\!

-----
