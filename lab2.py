import pandas as pd
from lxml import etree


class BookProcessor:


    def __init__(self,book_list):
        self.book_list = pd.read_csv(book_list, sep = ';', encoding = 'latin1', decimal = ',')
    

    def long_title_count(self,lenght = 30):
        count = sum([1 for title in self.book_list['Book-Title'] if len(title) > lenght])
        return count


    def search_by_author(self,author_name):
        if not isinstance(author_name, str):
            raise ValueError('Неверный тип данных')
        df = self.book_list
        title_list = []
        for title, author, year in zip(df['Book-Title'], df['Book-Author'], df['Year-Of-Publication']):
            if author == author_name and int(year) >= 2000:
                title_list.append(title)
            else:
                pass
        if title_list:
            return title_list
        else: 
            raise ValueError('Нет произведений младше 2000 / неверное имя автора')
    

    def generate_bibliograhy(self,n = 20):
        random_books = self.book_list.sample(n)
        book_lst=[]
        for title, author, year in zip(random_books['Book-Title'], random_books['Book-Author'], random_books['Year-Of-Publication']):
            bibliography_link = f'{author}. {title} - {year} year'
            book_lst.append(bibliography_link)
        with open('bibliography_link.txt', 'w', encoding='utf-8') as f:
            for i, line in enumerate(book_lst, start=1):
                f.write(f'{i}. {line}\n')


    @staticmethod
    def parse_books_xml(xml_path):
        tree = etree.parse(xml_path)
        root = tree.getroot()
        books_dict = {}
        for book in root.findall(".//book"):
            title_elem = book.find("title")
            book_id = book.get("id")
            if title_elem is not None and book_id is not None:
                books_dict[title_elem.text.strip()] = book_id
        return books_dict

    
    def publishers(self):
        return sorted(set(self.book_list['Publisher']))
    

    def top_20_books(self,n = 20):
        top_books = self.book_list.sort_values(by='Downloads',ascending=False).head(n)
        return top_books


a=BookProcessor('books-en.csv')
print(a.long_title_count())
print(a.search_by_author('Sheila Heti'))
print(a.generate_bibliograhy())
books_dict = a.parse_books_xml("books.xml")
print(books_dict)
print(a.publishers())
print(a.top_20_books())