from crawler import Crawler
#import multiProcessing
import threading
import concurrent.futures
import time


start_loc = '台灣大學, 台灣台北市大安區羅斯福路四段'
stop_loc = '中正紀念堂, 台灣台北市中正區中山南路'
mail = 'yucheng0720@yahoo.com.tw'
pwd = 'cat7139aa'

estimate = Crawler()

start_time = time.perf_counter()

# def test(x, y):
#     answer = x + y + 5
#     print('work!')
#     return answer

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:

    uber_result = executor.submit(estimate.uber_taxi, start_loc, stop_loc)
    print(uber_result)

    # 如果使用者沒輸入email的話，代表不使用line taxi車資估算
    if mail is None:

        line_taxi_price = 0
        print('使用者不用line', line_taxi_price)

    else:

        line_taxi_price = executor.submit(estimate.line_taxi, start_loc, stop_loc, mail, pwd).result()
        print('line成功', line_taxi_price)

# uber_taxi_price = uber_result.result()
# print(uber_taxi_price)
uber_result = uber_result.result()
line_taxi_price = line_taxi_price

# 把uber回傳的資源賦值
uber_taxi_price = uber_result[0]
coordinates = uber_result[1]
start_choice_name = uber_result[2]
stop_choice_name = uber_result[3]
uber_address_name = uber_result[4]

#t1 = threading.Thread(target=estimate.uber_taxi, arg=(start_loc, stop_loc, email, pwd))

# # Uber的結果
# uber_result = estimate.uber_taxi(start_loc, stop_loc)

# # 把uber回傳的資源賦值
# uber_taxi_price = uber_result[0]
# coordinates = uber_result[1]
# start_choice_name = uber_result[2]
# stop_choice_name = uber_result[3]
# uber_address_name = uber_result[4]

# print('uebr成功', uber_taxi_price)

# # 如果使用者沒輸入email的話，代表不使用line taxi車資估算
# if mail is None:

#     line_taxi_price = 0
#     print('使用者不用line', line_taxi_price)

# else:
#     line_taxi_price = estimate.line_taxi(start_loc, stop_loc, mail, pwd)
#     print('line成功', line_taxi_price)


# 帶入其他function中估算車資
tw_taxi_price = estimate.tw_taxi(uber_address_name)
print('tw成功', tw_taxi_price)

city_price = estimate.m_taxi(coordinates)
print('city成功', city_price)

firm_list = ['Uber', 'LINE TAXI', '台灣大車隊', '大都會計程車']
price_list = [uber_taxi_price, line_taxi_price, tw_taxi_price, city_price]

result = []
for i in range(4):
    result.append((firm_list[i], price_list[i]))

# 把結果由小到大排序
result = sorted(list(result), key=lambda x: (x[1]))
print(result)

end_time = time.perf_counter()
print(f'總共花了 {end_time - start_time} 秒')
