import requests
from bs4 import BeautifulSoup


def get_soup(url):
	response = requests.get(url)
	return BeautifulSoup(response.content, 'lxml')


def get_href(soup):
	return soup.find('a').attrs['href']


def main(filename='teachers.tsv'):
	root = 'https://www.sustech.edu.cn/zh/shizihuancunyemian.html'

	information = dict()
	mapping = dict(
		name='icon vc_icon_element-icon fa fa-user fl',
		title='icon vc_icon_element-icon fa fa-bookmark fl',
		telephone='icon vc_icon_element-icon fa fa-phone fl',
		email='icon vc_icon_element-icon fa fa-envelope fl',
		homepage='icon vc_icon_element-icon fa fa-home fl',
	)
	f = open(filename, 'w')
	f.write('\t'.join(mapping.keys()) + '\n')
	box = get_soup(root).find(id='box')
	for teacher in box.find_all('li'):
		url = get_href(teacher)
		name = url.split('/')[-1].split('.')[0]
		information[name] = dict()
		soup = get_soup(url)
		for key, value in mapping.items():
			message = soup.find(class_=value)
			information[name][key] = ''
			if message is not None:
				text = message.parent.find(class_='font fl').text
				if key == 'homepage':
					text = get_href(message.parent.find(class_='font fl'))
				information[name][key] = text.strip()
		f.write('\t'.join(information[name].values()) + '\n')
	f.close()


if __name__ == '__main__':
	main()
