import brotli
import os
import sys
import errno
import argparse

# --- Core logic of original sdat2img.py adapted into a single function ---
# Source: https://gist.github.com/xpirt/2c11438a0f9077227d8905391c49926d
# This version integrates the conversion logic into a reusable function.

def run_sdat2img_logic(transfer_list_file, new_dat_file, output_image_file):
    """
    Executes the core logic of sdat2img.py to convert .dat and .transfer.list
    files into an Android .img disk image.

    Args:
        transfer_list_file (str): Path to the .transfer.list file.
        new_dat_file (str): Path to the decompressed .dat file.
        output_image_file (str): Path for the output .img file.

    Returns:
        bool: True if conversion is successful, False otherwise.
    """
    print(f"sdat2img module: Starting conversion from '{new_dat_file}' to '{output_image_file}'")

    BLOCK_SIZE = 4096

    def rangeset(src):
        """Parses a comma-separated string of block ranges."""
        src_set = src.split(',')
        num_set = [int(item) for item in src_set]
        if len(num_set) != num_set[0] + 1:
            print(f'sdat2img module: Error parsing rangeset:\n{src}', file=sys.stderr)
            return None
        return tuple([(num_set[i], num_set[i + 1]) for i in range(1, len(num_set), 2)])

    def parse_transfer_list_file(path):
        """Parses the .transfer.list file to extract version, new blocks, and commands."""
        try:
            with open(path, 'r') as trans_list:
                version = int(trans_list.readline())
                new_blocks = int(trans_list.readline())

                if version >= 2:
                    trans_list.readline()  # Skip stash entries line
                    trans_list.readline()  # Skip stash blocks line

                commands = []
                for line in trans_list:
                    line = line.split(' ')
                    cmd = line[0]
                    if cmd in ['erase', 'new', 'zero']:
                        r_set = rangeset(line[1])
                        if r_set is None: return None, None, None
                        commands.append([cmd, r_set])
                    else:
                        if not cmd[0].isdigit():
                            print(f'sdat2img module: Invalid command "{cmd}".', file=sys.stderr)
                            return None, None, None
                return version, new_blocks, commands
        except FileNotFoundError:
            print(f"sdat2img module: Error: Transfer list file '{path}' not found.", file=sys.stderr)
            return None, None, None
        except Exception as e:
            print(f"sdat2img module: Error while parsing transfer list: {e}", file=sys.stderr)
            return None, None, None

    version, new_blocks, commands = parse_transfer_list_file(transfer_list_file)
    if commands is None:
        return False

    try:
        output_img = open(output_image_file, 'wb')
    except IOError as e:
        if e.errno == errno.EEXIST:
            print(f'sdat2img module: Error: Output file "{e.filename}" already exists.', file=sys.stderr)
            return False
        else:
            raise

    try:
        new_data_file = open(new_dat_file, 'rb')
    except FileNotFoundError:
        print(f"sdat2img module: Error: Data file '{new_dat_file}' not found.", file=sys.stderr)
        output_img.close()
        return False

    all_block_sets = [i for command in commands for i in command[1]]
    if not all_block_sets:
        print("sdat2img module: No block operation commands found.", file=sys.stderr)
        output_img.close()
        new_data_file.close()
        return False

    max_file_size = max(pair[1] for pair in all_block_sets) * BLOCK_SIZE

    for command in commands:
        if command[0] == 'new':
            for block in command[1]:
                begin, end = block
                block_count = end - begin
                output_img.seek(begin * BLOCK_SIZE)
                while block_count > 0:
                    data_read = new_data_file.read(BLOCK_SIZE)
                    if not data_read:
                        print(f"sdat2img module: Error: Unexpected end of data file '{new_dat_file}'.", file=sys.stderr)
                        output_img.close()
                        new_data_file.close()
                        return False
                    output_img.write(data_read)
                    block_count -= 1
        else:
            pass  # skip 'erase' and 'zero' commands for sdat2img logic

    if output_img.tell() < max_file_size:
        output_img.truncate(max_file_size)

    output_img.close()
    new_data_file.close()
    print(f'sdat2img module: Conversion completed. Output image: {os.path.realpath(output_img.name)}')
    return True


def convert_rom_files_function(datbr_path=None, transferlist_path=None, output_img_name=None):
    """
    Main function to decompress .dat.br and convert to .img.
    This function handles argument parsing internally when called as an entry point.

    Args:
        datbr_path (str, optional): Path to the .dat.br file. Defaults to None.
                                   If None, attempts to parse from command-line arguments.
        transferlist_path (str, optional): Path to the .transfer.list file. Defaults to None.
                                          If None, attempts to parse from command-line arguments.
        output_img_name (str, optional): Name/path for the output .img file. Defaults to None.
                                        If None, attempts to parse from command-line arguments.

    Returns:
        bool: True if conversion is successful, False otherwise.
    """
    
    # Check Python version first
    if sys.version_info < (3, 6):
        print("This script requires Python 3.6 or newer.", file=sys.stderr)
        print(f"You are using Python {sys.version_info.major}.{sys.version_info.minor}.", file=sys.stderr)
        return False

    # If arguments are not explicitly passed (e.g., when called as an entry point),
    # parse them from sys.argv.
    if datbr_path is None and transferlist_path is None and output_img_name is None:
        parser = argparse.ArgumentParser(
            description='✨ SDAT2IMG Brotli: Decompresses .dat.br and converts to .img file. ✨',
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument('-d', '--datbr', type=str, 
                            help='Specifies the path to the .dat.br file.\n'
                                 'Example: -d "C:\\roms\\my_system.new.dat.br"\n'
                                 'Default: system.new.dat.br')
        parser.add_argument('-t', '--transferlist', type=str, 
                            help='Specifies the path to the .transfer.list file.\n'
                                 'Example: -t "C:\\roms\\my_system.transfer.list"\n'
                                 'Default: system.transfer.list')
        parser.add_argument('-o', '--outputimg', type=str, 
                            help='Specifies the name and path for the output .img file.\n'
                                 'Example: -o "extracted_system.img"\n'
                                 'Default: system.img')
        args = parser.parse_args()

        datbr_path = args.datbr
        transferlist_path = args.transferlist
        output_img_name = args.outputimg
        
    # Determine file paths: Use provided arguments or defaults if still None
    br_file_name = datbr_path if datbr_path is not None else "system.new.dat.br"
    transfer_list_name = transferlist_path if transferlist_path is not None else "system.transfer.list"
    output_img_name = output_img_name if output_img_name is not None else "system.img"
    
    # Convert paths to absolute paths for robust file handling
    br_file_name = os.path.abspath(br_file_name)
    transfer_list_name = os.path.abspath(transfer_list_name)

    print(f"🚀 SDAT2IMG Brotli v1.0.3 Starting 🚀")
    print("----------------------------------------")
    print(f"Processing files: '{br_file_name}' and '{transfer_list_name}'")
    print(f"Output image will be: '{output_img_name}'")
    print("----------------------------------------")

    # Check file existence
    if not os.path.exists(br_file_name):
        print(f"Error: '{br_file_name}' not found. Please ensure the path is correct.", file=sys.stderr)
        return False

    if not os.path.exists(transfer_list_name):
        print(f"Error: '{transfer_list_name}' not found. Please ensure the path is correct.", file=sys.stderr)
        return False

    # Robustly generate the .dat file path
    base_name_without_br = br_file_name.rsplit('.br', 1)[0] if br_file_name.endswith('.br') else br_file_name
    dat_file_path = base_name_without_br
    if not dat_file_path.endswith(".dat"):
        dat_file_path += ".dat"

    print(f"\nStep 1/2: Decompressing '{br_file_name}' to '{dat_file_path}'...")
    try:
        with open(br_file_name, 'rb') as f_in:
            decompressed_data = brotli.decompress(f_in.read())
            with open(dat_file_path, 'wb') as f_out:
                f_out.write(decompressed_data)
        print("✅ Decompression completed.")
    except brotli.error as e:
        print(f"❌ Brotli decompression failed: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Unknown error during decompression: {e}", file=sys.stderr)
        return False

    print(f"\nStep 2/2: Converting '{dat_file_path}' to '{output_img_name}'...")
    
    success = False
    try:
        success = run_sdat2img_logic(transfer_list_name, dat_file_path, output_img_name)
    except Exception as e:
        print(f"❌ Error during conversion: {e}", file=sys.stderr)
    finally:
        if os.path.exists(dat_file_path):
            print(f"\nCleaning up temporary file '{dat_file_path}'...")
            os.remove(dat_file_path)
            print("✅ Cleanup done.")
            
    return success


if __name__ == "__main__":
    # When run as a script directly (e.g., `python main.py ...`),
    # parse arguments and call the main conversion function.
    # This block ensures compatibility when the script is not run via console_scripts.
    parser = argparse.ArgumentParser(
        description='✨ SDAT2IMG Brotli: Decompresses .dat.br and converts to .img file. ✨',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        '-d', '--datbr', 
        type=str, 
        help='Specifies the path to the .dat.br file.\n'
             'Example: -d "C:\\roms\\my_system.new.dat.br"\n'
             'Default: system.new.dat.br'
    )
    parser.add_argument(
        '-t', '--transferlist', 
        type=str, 
        help='Specifies the path to the .transfer.list file.\n'
             'Example: -t "C:\\roms\\my_system.transfer.list"\n'
             'Default: system.transfer.list'
    )
    parser.add_argument(
        '-o', '--outputimg', 
        type=str, 
        help='Specifies the name and path for the output .img file.\n'
             'Example: -o "extracted_system.img"\n'
             'Default: system.img'
    )

    args = parser.parse_args()

    # Display the parameters being used for CLI execution (when run directly)
    print("\n----------------------------------------")
    print("🚀 Command-line arguments set (from direct script execution):")
    print(f"   .dat.br file: {args.datbr if args.datbr else 'Using default'}")
    print(f"   .transfer.list file: {args.transferlist if args.transferlist else 'Using default'}")
    print(f"   Output .img file: {args.outputimg if args.outputimg else 'Using default'}")
    print("----------------------------------------\n")

    # Call the main function with parsed arguments
    overall_success = convert_rom_files_function(
        datbr_path=args.datbr,
        transferlist_path=args.transferlist,
        output_img_name=args.outputimg
    )

    print("\n----------------------------------------")
    if overall_success:
        print("🎉 Conversion completed successfully! You're amazing! ٩(๑•̀ω•́๑)۶")
        print("You can now use tools like DiskGenius, 7-Zip, or Linux Reader to explore the .img file.")
    else:
        print("⚠️ Conversion failed. Please check the error messages above! (╯︵╰)")
    print("----------------------------------------")
    input('Press Enter to exit... (｡◕‿◕｡)')