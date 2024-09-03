from datetime import datetime, timedelta
from queries.news_table import read_news_rows, read_news_row_by_hashlist

#example by default query
ret = read_news_rows()
print(ret)

#can also customize either columns, number of returning rows and time period,
ret = read_news_rows(columns=['hash_code', 'title'], limit=2, period={"start_date": datetime.now() - timedelta(days=365), "end_date": datetime.now()})
print(ret)


#query by hash code, for constant output
ret = read_news_row_by_hashlist(hash_list=["c1eede8b8f528caaacda3ef3b97d5d121f1d29fe9c3de99dc5649aa16e01357e"])
print(ret)