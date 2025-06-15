import zipfile
import os

def read_zip_contents():
    # Path to the ZIP file
    zip_path = os.path.join('resources', '202401_NFs.zip')
    
    try:
        # Open the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Print list of files in the ZIP
            print("Files in the ZIP archive:")
            for file in zip_ref.namelist():
                print(f"- {file}")
                
            # Extract and read contents of each file
            print("\nContents of files:")
            for file in zip_ref.namelist():
                with zip_ref.open(file) as f:
                    content = f.read()
                    # Try to decode as UTF-8, if it's a text file
                    try:
                        print(f"\n=== Content of {file} ===")
                        print(content.decode('utf-8'))
                    except UnicodeDecodeError:
                        print(f"\n{file} appears to be a binary file")

    except zipfile.BadZipFile:
        print("Error: File is not a valid ZIP file")
    except FileNotFoundError:
        print("Error: ZIP file not found in resources directory")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    read_zip_contents()