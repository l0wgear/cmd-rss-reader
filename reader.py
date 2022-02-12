import requests
import xml.etree.ElementTree as ET


def main():
    urls = input("Enter an RSS link or multiple space separated links:\n")
    for url in urls.split():
        res = requests.get(url)
        formatted_feed = format_feed(res)
        print(formatted_feed)


def format_feed(response):
    root = ET.fromstring(response.content)
    title = root[0].find('title').text
    date = root[0].find('lastBuildDate').text

    final_str = f"{title}\n\nUpdated on: {date}\n\n"

    item_list = parse_items(root)

    # print(item_list)

    for item in item_list:
        final_str += f"{item['title']}\n{item['description']}\nRead more: {item['link']}\n\n"

    return final_str


def parse_items(root, tag_list=('title', 'description', 'link')):

    item_list = [{key: item.find(key).text for key in tag_list}
                 for item in root[0].findall('item')]
    return item_list


if __name__ == "__main__":
    main()
