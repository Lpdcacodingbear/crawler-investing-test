import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from typing import List, Dict, Any
from datetime import datetime


class CrawlerInvestingHandle():
    
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

        self.soup = set()
        self.table = set()

        self.key: List[Any] = list()
        self.value: List[Any] = list()
        self.process_data: List[Any] = list()
        self.mapping: Dict[str, Any] = dict()

        self.result: List[Any] = list()

    def execute(self):
        self._crawler_table()
        self._get_date_for_key()
        self._get_row_data_in_string_type()
        self._data_process()
        self._mapping_result()

        if not self.mapping.get(self.start) and not self.mapping.get(self.end):
            raise 'datetime out of range'
        else:
            for key, value in self.mapping.items():
                if self._is_bigger_then_equal(key, self.start) and self._is_smaller_then_equal(key, self.end):
                    self.result.append({key: value})
        
        return self.result
    
    def _crawler_table(self):
        headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        url = 'https://cn.investing.com/equities/apple-computer-inc-historical-data'

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find_all('table', id='curr_table')

        self.soup = soup
        self.table = table
    
    def _get_date_for_key(self):
        dt_object = ''

        for row in self.soup.select('tbody tr'):
            _row = row.find_all('td', attrs={'class': 'first left bold noWrap'})

            if _row:
                row_text = [x.__dict__['attrs']['data-real-value'] for x in _row]

                timestamp = int(row_text[0])
                dt_object = datetime.fromtimestamp(timestamp)
                date = dt_object.date()

                self.key.append(date)

    def _get_row_data_in_string_type(self):
        for each in self.table:
            for index, text in enumerate(each):
                if type(text) is Tag:
                    value_text = text.get_text()
                    if value_text:
                        self.value = value_text
    
    def _data_process(self):
        first_process_data = self.value.split('\n\n')

        for index, string in enumerate(first_process_data):
            row_data = string.split('\n')
            clean_row_data = self._remove_empty_str_in_arr(row_data)
            if clean_row_data:
                self.process_data.append(clean_row_data)
    
    def _remove_empty_str_in_arr(self, string_array):
        for index, string in enumerate(string_array):
            if not string:
                string_array.pop(index)
        return string_array
    
    def _mapping_result(self):
        for key, value in zip(self.key, self.process_data):
            self.mapping.update({key: value})
    
    def _is_bigger_then_equal(self, operand_first, operands_second):
        return operand_first >= operands_second

    def _is_smaller_then_equal(self, operand_first, operands_second):
        return operand_first <= operands_second


def main(start, end):
    date_start = datetime.strptime(start, "%Y-%m-%d").date()
    date_end = datetime.strptime(end, "%Y-%m-%d").date()

    service = CrawlerInvestingHandle(date_start, date_end)
    result = service.execute()

    return result


if __name__ == '__main__':
    result = main('2021-12-22', '2021-12-28')
    print(result)