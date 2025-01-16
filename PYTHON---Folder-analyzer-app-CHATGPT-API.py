import os
import openai

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

def analyze_folder(folder_path, analyze_text_files=False):
    """
    Analyze the contents of a folder.
    
    Args:
        folder_path (str): Path to the folder to analyze.
        analyze_text_files (bool): Whether to analyze the content of text files.
        
    Returns:
        dict: Analysis report of the folder.
    """
    folder_analysis = {"folder_path": folder_path, "files": []}
    
    if not os.path.exists(folder_path):
        return {"error": "Folder does not exist."}
    
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_info = {"name": file_name, "path": file_path}
            
            # Add text content if required
            if analyze_text_files and file_name.endswith(".txt"):
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        response = openai.ChatCompletion.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": f"Analyze this text content:\n{content}"}
                            ]
                        )
                        file_info["analysis"] = response['choices'][0]['message']['content']
                except Exception as e:
                    file_info["error"] = f"Could not analyze file: {e}"
            folder_analysis["files"].append(file_info)
    
    return folder_analysis

def print_analysis(analysis):
    """
    Print the folder analysis in a readable format.
    """
    if "error" in analysis:
        print(analysis["error"])
        return
    
    print(f"Analysis of folder: {analysis['folder_path']}")
    for file in analysis["files"]:
        print(f"\nFile: {file['name']}")
        print(f"Path: {file['path']}")
        if "analysis" in file:
            print(f"Analysis: {file['analysis']}")
        if "error" in file:
            print(f"Error: {file['error']}")

# Example usage
if __name__ == "__main__":
    folder_to_analyze = input("Enter the folder path to analyze: ")
    include_text_analysis = input("Analyze text file contents? (yes/no): ").strip().lower() == "yes"
    
    result = analyze_folder(folder_to_analyze, analyze_text_files=include_text_analysis)
    print_analysis(result)
