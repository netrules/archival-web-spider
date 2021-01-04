from urllib.parse import urljoin, urlparse, quote_plus
from selenium import webdriver
from os.path import exists as path_exists
from os import makedirs
#from os.path import splitext as split_text
    
# def is_valid(url):
    # """
    # Checks whether `url` is a valid URL.
    # """
    # parsed = urlparse(url)
    # return bool(parsed.netloc) and bool(parsed.scheme)

def download_asset(url, output_dir, path_dir, test_scenario):
    """
    Downloads a file given an URL and puts it in the folder `path_dir`
    """

    # get the file name -- todo: custom filenames
    filename = os.path.join(path_dir, url.split("/")[-1])
    if(filename == path_dir):
        url = quote_plus(url)
        url = (url[:255]) if len(url) > 255 else url
        filename = filename + url
    
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    text = "Downloading {filename}".format(filename=filename)
    
    if(test_scenario != True):
        # download the body of response by chunk, not immediately
        response = requests.get(url, stream=True)
        # get the total file size
        file_size = int(response.headers.get("Content-Length", 0))
        
        progress = tqdm(response.iter_content(1024), total=file_size, unit="B", unit_scale=True, unit_divisor=1024, desc=text)
        
        # added output_dir instead for relative `filename` reading
        with open(output_dir + filename, "wb") as f:
            for data in progress:
                # write data read to the file
                f.write(data)
                # update the progress bar manually
                progress.update(len(data))

    return filename

def relative_to_static(url, elem):
    # make the URL absolute by joining domain with the URL that is just extracted
    elem_url = urljoin(url, elem)
    try:
        pos = elem_url.index("?") # make sure it doesnt include urlvars
        elem_url = elem_url[:pos]
    except ValueError:
        pass

    # finally, if the url is valid
    if is_valid(elem_url):
        return elem_url

    return None

def setup_browser(driver_path):
    """Returns a Chrome browser instance."""

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    return webdriver.Chrome(driver_path, options=options)

def generate_directories(output_dir, output_subdirs, test_scenario):
    if test_scenario == True:
        return True
    
    if not path_exists(output_dir):
        makedirs(output_dir)
        
    for subdir in output_subdirs:
        if not path_exists(output_dir + subdir):
            makedirs(output_dir + subdir)
            
    return True