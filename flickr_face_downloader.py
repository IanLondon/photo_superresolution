import flickrapi

import secrets
from img_tools import save_urls_to_file, download_all_imgs

# Declare flickr api object
flickr = flickrapi.FlickrAPI(secrets.KEY, secrets.SECRET, format='parsed-json')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Save urls to file and/or scrape urls in that file')
    parser.add_argument('--url_file', default='flickr_face_urls.txt', help='Text file to store image urls')
    parser.add_argument('--img_dir', default='flickr_faces', help='Directory to store downloaded images')
    parser.add_argument('--tags', nargs='+', default=['face','portrait','people'], help='Tags used to search for images')
    parser.add_argument('--save_urls', action='store_true', help='If included, save urls to url_file')
    parser.add_argument('--download', action='store_true', help='If included, download images using urls in url_file')

    args = parser.parse_args()

    if not args.save_urls and not args.download:
        print 'No actions specified. Use --save_urls and/or --download to do something.'
    else:
        if args.save_urls:
            print 'Getting all image urls with tags: [%s] and saving to %s' % (', '.join(args.tags), args.url_file)
            save_urls_to_file(flickr, args.url_file, args.tags)
        if args.download:
            download_all_imgs(args.url_file, args.img_dir)
