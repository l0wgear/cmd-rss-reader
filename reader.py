import requests
import xml.etree.ElementTree as ET
import argparse


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read RSS channel feed."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        "-a", "--add", help="add RSS link(s) to stored links", nargs='*')
    parser.add_argument(
        "-r", "--remove", help="remove link(s) from stored links", nargs='*')
    parser.add_argument("-g", "--get", help="get feed from stored links",
                        action='store_const', const=False)
    parser.add_argument(
        "-f", "--fetch", help="fetch feed from the argument link(s) once", nargs='*')
    return parser


def format_feed(response):
    root = ET.fromstring(response.content)
    title = root[0].find('title').text
    try:
        date = root[0].find('lastBuildDate').text
        final_str = f"{title}\n\nUpdated on: {date}\n\n"
    except AttributeError:
        try:
            date = root[0].find('lastBuildDate').text
            final_str = f"{title}\n\nUpdated on: {date}\n\n"
        except AttributeError:
            final_str = f"{title}\n\n"

    item_list = parse_items(root)

    # print(item_list)

    for item in item_list:
        final_str += f"{item['title']}\n{item['description']}\nRead more: {item['link']}\n\n"

    return final_str


def parse_items(root, tag_list=('title', 'description', 'link')):

    item_list = [{key: item.find(key).text for key in tag_list}
                 for item in root[0].findall('item')]
    return item_list


def parse_args(args: argparse.Namespace):
    if args.add is not None:
        add_to_saved(args.add)
    if args.remove is not None:
        remove_from_saved(args.remove)
    if args.fetch is not None:
        fetch_links(args.fetch)
    if args.get or all(arg is None for arg in vars(args).values()):
        fetch_links(get_stored_links())


def fetch_links(links):
    if len(links) == 0:
        print("No links to fetch.")
    else:
        for link in links:
            res = requests.get(link)
            formatted_feed = format_feed(res)
            print(formatted_feed)


def add_to_saved(links):
    if len(links) == 0:
        print("No links to add to saved.")
    else:
        saved = get_stored_links()
        for link in links:
            if link in saved:
                print(f"Link {link} is already in saved. Skipping adding.")
            else:
                saved.append(link)
        set_stored_links(saved)


def remove_from_saved(links):
    if len(links) == 0:
        print("No links to remove from saved.")
    else:
        saved = get_stored_links()
        for link in links:
            try:
                saved.remove(link)
            except ValueError:
                print(f"Link {link} is not in saved. Skipping removal.")
        set_stored_links(saved)


def set_stored_links(links):
    with open('sources.txt', 'w') as f:
        f.write('\n'.join(link for link in links if len(link) > 0))


def get_stored_links():
    try:
        with open('sources.txt', 'r') as f:
            links = [line.rstrip() for line in f.readlines()]
            return links
    except FileNotFoundError:
        return []


def main():
    parser = init_argparse()
    args = parser.parse_args()
    # print(vars(args))
    parse_args(args)


if __name__ == "__main__":
    main()
