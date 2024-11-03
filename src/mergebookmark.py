import json
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def read_bookmark_html(file_path):
    """Reads the content of an HTML file."""
    with file_path.open('r', encoding='utf-8') as file:
        return file.read()

def parse_bookmarks(html_content):
    """Parses HTML content and extracts bookmark entries."""
    soup = BeautifulSoup(html_content, 'html.parser')
    bookmarks = soup.find_all(['a'])
    return bookmarks

def get_html_files_from_folder(folder_path):
    """Returns a list of all HTML files in the specified folder using Pathlib."""
    folder = Path(folder_path)
    html_files = list(folder.glob("*.html"))  # Finds all .html files in the folder
    return html_files

def combine_bookmarks(folder_path):
    """Reads, parses, and combines bookmarks from all HTML files in the folder."""
    combined_bookmarks = []
    unique_links = set()  # To store unique hrefs and avoid duplicates
    
    html_files = get_html_files_from_folder(folder_path)
    url_list = []
    for file in html_files:
        print(f"Processing file: {file}")
        html_content = read_bookmark_html(file)
        bookmarks = parse_bookmarks(html_content)
        for bookmark in bookmarks:
            if bookmark.name == 'a':  # Ensure we are checking <a> tags for links
                print(bookmark)
                url_json = {}
                href = bookmark.get('href')
                l = href.split('.')
                if href and href not in unique_links:
                    unique_links.add(href)
                    url_json['url'] = href
                    url_json['domain'] = urlparse(href).netloc
                    if len(bookmark.contents)>0:
                        url_json['name'] = bookmark.contents[0]
                    else:
                        url_json['name'] = 'need to give name'
                    url_list.append(url_json)
                    # bookmark.attrs.pop('add_date', None)
                    # combined_bookmarks.append(bookmark)
            # elif bookmark.next.name != 'a':
                # combined_bookmarks.append(bookmark)  # Add non-link tags (e.g., <dt>)
    
    return url_list

def write_combined_bookmarks(combined_bookmarks, output_file):
    """Writes the combined bookmarks to a single output HTML file."""
    output_path = Path(output_file)
    with output_path.open('w', encoding='utf-8') as file:
        file.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n')
        file.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n')
        file.write('<TITLE>Combined Bookmarks</TITLE>\n')
        file.write('<H1>Bookmarks</H1>\n')
        file.write('<DL><p>\n')
        
        for bookmark in combined_bookmarks:
            file.write('<DT>')
            file.write(str(bookmark))
            file.write("</DT>\n")
        
        file.write('</DL><p>\n')
        
def write_combined_bookmarks_json(combined_bookmarks, output_file):
    """Writes the combined bookmarks to a single output HTML file."""
    output_path = Path(output_file)
    with output_path.open('w', encoding='utf-8') as file:
        json.dump(combined_bookmarks, file)

def main():
    """Main function to orchestrate combining bookmarks from multiple HTML files."""
    current_dir = Path.cwd()
    folder_path = current_dir / 'input'  # Use pathlib.Path to specify the folder path
    # output_file = current_dir / 'output' /'combined_bookmarks.html'
    output_file = current_dir / 'output' /'combined_bookmarks.json'

    combined_bookmarks = combine_bookmarks(folder_path)
    # write_combined_bookmarks(combined_bookmarks, output_file)
    write_combined_bookmarks_json(combined_bookmarks, output_file)

    print(f"Bookmarks combined successfully into {output_file}!")

if __name__ == "__main__":
    main()
