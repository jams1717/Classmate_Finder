
def save_img(img_url, img_nm, img_locn = './pics', verbose = False):
    import os, requests
    if verbose:
        print(f"Checking if {img_locn} exists.")
    try:
        os.listdir(img_locn)
    except:
        if verbose:
            print(f"{img_locn} does not exist.")
            print(f"Creating folder {img_locn}.")
        os.mkdir(img_locn) 
    if verbose:
        print(f"Requesting image from: \n\t {img_url}")
    response = requests.get(img_url, stream=True)
    if not response.ok:
        if verbose:
            print("Request failed")
        print(response)
    else:
        if verbose:
            print("Request complete")
            print("Starting to write to file.")
        with open(img_locn+'/'+img_nm, 'wb') as trgt:
            for block in response.iter_content(1024):
                if not block:
                    break
                trgt.write(block)
        if verbose:
            print("Finished writing to file.")

save_img('https://cdn1.edsby.com/cp1/d6c0ffb46fb4deebd4f24fdb4e37c9c16dfb', 'Ms.Smythe')
