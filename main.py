import glob
import string
import requests
import Sqlite
import pandas as pd
import streamlit as st
import re
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import random
import copy
from st_aggrid import AgGrid
import time
from st_aggrid import GridOptionsBuilder
from datetime import datetime
from loguru import logger

city_list = ["臺北市", "新北市", "基隆市", "桃園市", "新竹市", "新竹縣", "苗栗縣", "臺中市",
             "彰化縣", "南投縣", "嘉義市", "嘉義縣", "雲林縣", "臺南市", "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣"]
area_list = [
    ['全部', "中正區", "大同區", "中山區", "松山區", "大安區", "萬華區", "信義區", "士林區", "北投區", "內湖區", "南港區", "文山區", "臺北市"],
    ['全部', '板橋區', '三重區', '中和區', '永和區', '新莊區', '新店區', '樹林區', '鶯歌區', '三峽區', '淡水區', '汐止區', '瑞芳區', '土城區', '蘆洲區', '五股區',
     '泰山區', '林口區', '深坑區', '石碇區', '坪林區', '三芝區', '石門區', '八里區', '平溪區', '雙溪區', '貢寮區', '金山區', '萬里區', '烏來區'],
    ['全部', "中正區", "信義區", "仁愛區", "中山區", "安樂區", "暖暖區", "七堵區"],
    ['全部', "桃園區", "中壢區", "平鎮區", "八德區", "楊梅區", "蘆竹區", "大溪區", "龜山區", "大園區", "觀音區", "新屋區", "龍潭區", "復興區"],
    ['全部', "東區", "北區", "香山區"],
    ['全部', "竹北市", "竹東鎮", "新埔鎮", "關西鎮", "新豐鄉", "峨眉鄉", "寶山鄉", "五峰鄉", "橫山鄉", "北埔鄉", "尖石鄉", "芎林鄉", "湖口鄉"],
    ['全部', "三義鄉", "三灣鄉", "大湖鄉", "公館鄉", "竹南鎮", "西湖鄉", "卓蘭鎮", "南庄鄉", "後龍鎮", "苗栗市", "苑裡鎮", "泰安鄉", "通霄鎮", "造橋鄉", "獅潭鄉",
     "銅鑼鄉", "頭份市", "頭屋鄉"],
    ['全部', "中區", "北屯區", "北區", "西屯區", "西區", "東區", "南屯區", "南區", "大甲區", "大安區", "大肚區", "大里區", "大雅區", "太平區", "外埔區", "石岡區",
     "后里區", "和平區", "東勢區", "烏日區", "神岡區", "梧棲區", "清水區", "新社區", "潭子區", "豐原區", "霧峰區"],
    ['全部', "彰化市", "員林巿", "鹿港鎮", "和美鎮", "北斗鎮", "溪湖鎮", "田中鎮", "二林鎮", "線西鄉", "伸港鄉", "福興鄉", "秀水鄉", "花壇鄉", "芬園鄉", "大村鄉",
     "埔鹽鄉", "埔心鄉", "永靖鄉", "社頭鄉", "二水鄉", "田尾鄉", "埤頭鄉", "芳苑鄉", "大城鄉", "竹塘鄉", "溪州鄉"],
    ['全部', "南投市", "埔里鎮", "草屯鎮", "竹山鎮", "集集鎮", "名間鄉", "中寮鄉", "鹿谷鄉", "水里鄉", "魚池鄉", "國姓鄉", "信義鄉", "仁愛鄉"],
    ['全部', "東區", "西區"],
    ['全部', '太保市', '朴子市', '布袋鎮', '大林鎮', '民雄鄉', '溪口鄉', '六腳鄉', '東石鄉', '義竹鄉', '鹿草鄉', '水上鄉', '中埔鄉', '竹崎鄉', '梅山鄉', '番路鄉',
     '大埔鄉', '新港鄉', '阿里山鄉'],
    ['全部', '斗六市', '斗南鎮', '西螺鎮', '虎尾鎮', '土庫鎮', '北港鎮', '莿桐鄉', '林內鄉', '古坑鄉', '大埤鄉', '崙背鄉', '二崙鄉', '麥寮鄉', '台西鄉', '東勢鄉',
     '褒忠鄉', '四湖鄉', '口湖鄉', '水林鄉', '元長鄉'],
    ['全部', '東區', '南區', '中西區', '北區', '安南區', '安平區'],
    ['全部', "三民區", "小港區", "左營區", "前金區", "前鎮區", "苓雅區", "新興區", "楠梓區", "鼓山區", "旗津區", "鹽埕區", "那瑪夏區", "大社區", "大寮區", "大樹區",
     "內門區", "六龜區", "田寮區", "甲仙區", "杉林區", "岡山區", "林園區", "阿蓮區", "美濃區", "茄萣區", "茂林區", "桃源區", "鳥松區", "湖內區", "旗山區", "鳳山區",
     "橋頭區", "燕巢區", "彌陀區"],
    ['全部', '九如鄉', '屏東市', '萬丹鄉', '長治鄉', '麟洛鄉'],
    ['全部', '頭城鎮', '礁溪鄉', '員山鄉', '宜蘭市', '壯圍鄉', '大同鄉', '三星鄉', '羅東鎮', '五結鄉', '冬山鄉', '蘇澳鎮', '南澳鄉'],
    ['全部', '新城鄉', '花蓮市', '吉安鄉', '壽豐鄉', '鳳林鎮', '光復鄉', '豐濱鄉', '瑞穗鄉', '富里鄉', '玉里鎮', '秀林鄉', '萬榮鄉', '卓溪鄉'],
    ['全部', '長濱鄉', '成功鎮', '池上鄉', '東河鄉', '關山鎮', '鹿野鄉', '台東市', '太麻里鄉', '大武鄉', '海端鄉', '延平鄉', '卑南鄉', '金峰鄉', '達仁鄉', '綠島鄉',
     '蘭嶼']]
jobName_conver = {"土石採礦工作": "礦業及土石採取業", "製造業": "製造業", "電力燃氣工作": "電力及燃氣供應業", "用水及污染整治工作": "用水供應及污染整治業",
                  "營建工程業": "營建工程業", "批發零售業": "批發及零售業", "運輸及倉儲工作": "運輸及倉儲業", "住宿及餐飲服務": "住宿及餐飲業",
                  "出版影音傳播及資通訊服務": "出版、影音製作、傳播及資通訊服務業", "金融保險業": "金融及保險業、強制性社會安全", "不動產業": "不動產業",
                  "專業科學及技術服務業": "專業、科學及技術服務業", "支援服務業": "支援服務業", "教育業": "教育業",
                  "醫療保健及社會工作服務業": "醫療保健及社會工作服務業", "藝術娛樂及休閒服務業": "藝術、娛樂及休閒服務業", "其他服務業": "其他服務業"}
jobName_conver_inverted = {"礦業及土石採取業": "土石採礦工作", "製造業": "製造業", "電力及燃氣供應業": "電力燃氣工作", "用水供應及污染整治業": "用水及污染整治工作",
                           "營建工程業": "營建工程業", "批發及零售業": "批發零售業", "運輸及倉儲業": "運輸及倉儲工作", "住宿及餐飲業": "住宿及餐飲服務",
                           "出版、影音製作、傳播及資通訊服務業": "出版影音傳播及資通訊服務", "金融及保險業、強制性社會安全": "金融保險業", "不動產業": "不動產業",
                           "專業、科學及技術服務業": "專業科學及技術服務業", "支援服務業": "支援服務業", "教育業": "教育業",
                           "醫療保健及社會工作服務業": "醫療保健及社會工作服務業", "藝術、娛樂及休閒服務業": "藝術娛樂及休閒服務業", "其他服務業": "其他服務業"}


# companyNumber_df=companyNumber_df.astype(int)
# salary_df = pd.read_csv('data/行業薪資匯總.csv', encoding='gbk', index_col=0)
# duration_df = pd.read_csv('data/city_duration.csv', encoding='gbk', index_col=0)
# companyNumber_df = pd.read_csv('data/行業家數匯總.csv', encoding='gbk')


# 表格美化初始化
# builder = GridOptionsBuilder()
# builder.configure_default_column(
#     # min_column_width – minimum columnwidth Defaults to 5
#     # resizable,filterable,sorteable,editable,groupable, Defaults to True
#     min_column_width=1,
#     resizable=False,
#     sorteable=False,
#     filterable=False,
#     editable=False,
#     groupable=False
# )
# builder.configure_auto_height(autoHeight=False)
# builder.configure_side_bar(columns_panel=True)
# builder.configure_pagination(enabled=True,paginationAutoPageSize=True)


def intro():
    if 'changeJob_frame_flag' in st.session_state:
        st.session_state.changeJob_frame_flag = 0  # 重置換工作的界面
    if 'findJob_frame_flag' in st.session_state:
        st.session_state.findJob_frame_flag = 0  # 重置換工作的界面
    st.write("# 歡迎來到Smart Job! 👋")
    st.sidebar.success("選擇以上的功能。")
    st.markdown("""### 想找頭路?""")
    image = Image.open('pic/OIP.jfif')
    st.image(image, caption=None, width=400)
    st.markdown("""### 想換工作?""")
    image = Image.open('pic/R.jfif')
    st.image(image, caption=None, width=400)


# def plotting_demo():
#     import folium
#     from streamlit_folium import folium_static
#
#     world_map = folium.Map(location=[24.993777, 121.301337], zoom_start=12, draggable=True)
#     # folium.Marker(
#     #     draggable=True,
#     #     location=[24.9721514, 121.1514872],
#     #     popup='台灣桃園市中壢區'
#     # ).add_to(world_map)
#     # folium.Marker(
#     #     draggable=True,
#     #     location=[24.9934099, 121.2969674],
#     #     popup='台灣桃園市桃園區'
#     # ).add_to(world_map)
#
#     # folium.Circle(
#     #     draggable=True,
#     #     radius=20,
#     #     location=[24.9934099, 121.2969674],
#     #     popup='台灣桃園市桃園區',
#     #     color='#3186cc',
#     #     fill=True,
#     #     fill_color='#3186cc'
#     # ).add_to(world_map)
#     folium.CircleMarker(
#         draggable=True,
#         location=[24.9721514, 121.1514872],
#         radius=20,
#         popup='台灣桃園市中壢區',
#         color='#3186cc',
#         fill=True,
#         fill_color='#3186cc'
#     ).add_to(world_map)
#
#     folium_static(world_map)


def findJob_salaryFind(data_dict):
    gender = data_dict['性別']
    if gender == '其他':
        gender = '總計'
    data_list = []
    data_list.append([jobName_conver_inverted[data_dict['工作類型']], salary_df.loc[gender, data_dict['工作類型']]])
    df = salary_df.drop(data_dict['工作類型'], axis=1)  # 当前选择的工作删除，排除后续推荐有重复
    salary_list = list(df.loc[gender, :])
    type_list = list(df.columns)

    nums_copy = copy.deepcopy(salary_list)
    min_num = min(salary_list) - 1
    index_list = []
    for i in range(3):  # 尋找前三個最大的
        num_index = nums_copy.index(max(nums_copy))
        index_list.append(num_index)
        nums_copy[num_index] = min_num

    # index_list = list(map(salary_list.index, heapq.nlargest(3, salary_list)))
    for index in index_list:
        data_list.append([jobName_conver_inverted[type_list[index]], salary_list[index]])
    new_df = pd.DataFrame(columns=['工作類型', '行業每人每月總薪資'], data=data_list,
                          index=['當前工作類型薪資', '推薦工作類型一', '推薦工作類型二', '推薦工作類型三'])
    new_df.reset_index(level=0, inplace=True)
    new_df.rename(columns={'index': '工作推薦'}, inplace=True)
    # builder = GridOptionsBuilder.from_dataframe(new_df)
    # go = builder.build()
    AgGrid(new_df, fit_columns_on_grid_load=True, theme='alpine')


def changeJob_salaryFind(data_dict):
    gender = data_dict['性別']
    if gender == '其他':
        gender = '總計'
    data_list = []
    salarynow = salary_df.loc[gender, data_dict['目前工作']]
    data_list.append([jobName_conver_inverted[data_dict['目前工作']], salarynow])
    df = salary_df.drop(data_dict['目前工作'], axis=1)  # 当前选择的工作删除，排除后续推荐有重复
    salary_list = list(df.loc[gender, :])
    type_list = list(df.columns)

    nums_copy = copy.deepcopy(salary_list)
    min_num = min(salary_list) - 1
    index_list = []
    for i in range(3):  # 尋找前三個最大的
        num_index = nums_copy.index(max(nums_copy))
        index_list.append(num_index)
        nums_copy[num_index] = min_num
    # index_list = list(map(salary_list.index, heapq.nlargest(len(salary_list), salary_list)))
    for index in index_list:
        if salary_list[index] < salarynow:
            break
        else:
            data_list.append([jobName_conver_inverted[type_list[index]], salary_list[index]])
    indexname = ['目前工作類型薪資']
    for count in range(1, len(data_list)):
        indexname.append('推薦工作' + str(count))
    new_df = pd.DataFrame(columns=['工作類型', '行業每人每月總薪資'], data=data_list, index=indexname)
    new_df.reset_index(level=0, inplace=True)
    new_df.rename(columns={'index': '工作推薦'}, inplace=True)
    # builder = GridOptionsBuilder.from_dataframe(new_df)
    # go = builder.build()
    AgGrid(new_df, fit_columns_on_grid_load=True, theme='alpine')  # gridOptions=go


def findJob_nCompanyFind(data_dict):
    city = data_dict['居住縣市']
    durationIndex_list = duration_df.index
    tmp_list = []
    if data_dict['居住區'] == '全部':  # 如果没有选择具体区域，将所有区域加到选择框
        city_list = list(duration_df.columns)
        for c in city_list:
            if c[:3] == city:
                tmp_list.append(c[3:])
        area = st.selectbox("縣市選擇", tmp_list)
    else:
        area = data_dict['居住區']

    duration_list = list(duration_df.loc[:, city + area])  # 获取当前市区的时间，组成列表

    nums_copy = copy.deepcopy(duration_list)
    max_num = max(duration_list) + 1
    index_list = []
    for i in range(4):  # 尋找前四個最小的
        num_index = nums_copy.index(min(nums_copy))
        index_list.append(num_index)
        nums_copy[num_index] = max_num

    # index_list = list(map(duration_list.index, heapq.nsmallest(4, duration_list)))  # 获取时间列表中最小的三个值的索引
    n_dict = {1: '當前區域', 2: '推荐第一個臨近區域', 3: '推荐第二個臨近區域', 4: '推荐第三個臨近區域'}
    n = 1
    for idx in index_list:
        new_city = durationIndex_list[idx][:3]  # 根据索引获得縣市
        new_area = durationIndex_list[idx][3:]  # 根据索引获得居住區
        st.write(n_dict[n] + '  {  ' + new_city + new_area + '  }')
        n = n + 1
        tmp_df = companyNumber_df.loc[
            (companyNumber_df['市縣'] == new_city) & (companyNumber_df['區域'] == new_area)]  # 获得当前行業家數
        count_list = [int(tmp_df[data_dict['工作類型']])]  # 获取当前工作的行业家数
        type_list = [jobName_conver_inverted[data_dict['工作類型']]]  # 获取当前行业

        tmp_df = tmp_df.drop(data_dict['工作類型'], axis=1)  # 当前选择的工作删除，排除后续推荐有重复
        tmp_data_list = list([value for value in tmp_df.iloc[0, 3:]])  # 将数值取出组成list

        nums_copy = copy.deepcopy(tmp_data_list)
        min_num = min(tmp_data_list) - 1
        tmp_index_list = []
        for i in range(3):  # 尋找前三個最大的
            num_index = nums_copy.index(max(nums_copy))
            tmp_index_list.append(num_index)
            nums_copy[num_index] = min_num

        # tmp_index_list = list(map(tmp_data_list.index, heapq.nlargest(3, tmp_data_list)))  # 获取前三个最大值

        for tmp_idx in tmp_index_list:
            type_list.append(jobName_conver_inverted[tmp_df.columns[tmp_idx + 3]])
            count_list.append(tmp_data_list[tmp_idx])

        new_df = pd.DataFrame(columns=['工作類型', '該行業家數'], index=['當前選擇工作', '工作推薦一', '工作推薦二', '工作推薦三'])
        new_df['工作類型'] = type_list
        new_df['該行業家數'] = count_list
        new_df.reset_index(level=0, inplace=True)
        new_df.rename(columns={'index': '工作推薦'}, inplace=True)

        # builder = GridOptionsBuilder.from_dataframe(new_df)
        # go = builder.build()

        AgGrid(new_df, fit_columns_on_grid_load=True, theme='alpine')


def changeJob_nCompanyFind(data_dict):
    city = data_dict['居住縣市']
    durationIndex_list = duration_df.index
    tmp_list = []
    if data_dict['居住區'] == '全部':  # 如果没有选择具体区域，将所有区域加到选择框
        city_list = list(duration_df.columns)
        for c in city_list:
            if c[:3] == city:
                tmp_list.append(c[3:])
        area = st.selectbox("縣市選擇", tmp_list)
    else:
        area = data_dict['居住區']

    duration_list = list(duration_df.loc[:, city + area])  # 获取当前市区的时间，组成列表
    nums_copy = copy.deepcopy(duration_list)
    max_num = max(duration_list) + 1
    index_list = []
    for i in range(4):  # 尋找前四個最小的
        num_index = nums_copy.index(min(nums_copy))
        index_list.append(num_index)
        nums_copy[num_index] = max_num
    # index_list = list(map(duration_list.index, heapq.nsmallest(4, duration_list)))  # 获取时间列表中最小的三个值的索引
    n_dict = {1: '當前區域', 2: '推荐第一個臨近區域', 3: '推荐第二個臨近區域', 4: '推荐第三個臨近區域'}
    n = 1
    for idx in index_list:
        new_city = durationIndex_list[idx][:3]  # 根据索引获得縣市
        new_area = durationIndex_list[idx][3:]  # 根据索引获得居住區
        st.write(n_dict[n] + '  {  ' + new_city + new_area + '  }')
        n = n + 1
        tmp_df = companyNumber_df.loc[
            (companyNumber_df['市縣'] == new_city) & (companyNumber_df['區域'] == new_area)]  # 获得当前行業家數
        ncompanynow = int(tmp_df[data_dict['目前工作']])  # 获取当前工作的行业家数
        count_list = [int(tmp_df[data_dict['目前工作']])]  # 获取当前工作的行业家数
        type_list = [jobName_conver_inverted[data_dict['目前工作']]]  # 获取当前行业

        tmp_df = tmp_df.drop(data_dict['目前工作'], axis=1)  # 当前选择的工作删除，排除后续推荐有重复
        tmp_data_list = list([value for value in tmp_df.iloc[0, 3:]])  # 将数值取出组成list

        nums_copy = copy.deepcopy(tmp_data_list)
        min_num = min(tmp_data_list) - 1
        tmp_index_list = []
        for i in range(3):  # 尋找前三個最大的
            num_index = nums_copy.index(max(nums_copy))
            tmp_index_list.append(num_index)
            nums_copy[num_index] = min_num

        # tmp_index_list = list(map(tmp_data_list.index, heapq.nlargest(len(tmp_data_list), tmp_data_list)))  # 获取前三个最大值

        for tmp_idx in tmp_index_list:  # 将比当前选择的行业家数数量多的保存到list
            if tmp_data_list[tmp_idx] < ncompanynow:
                break
            else:
                type_list.append(jobName_conver_inverted[tmp_df.columns[tmp_idx + 3]])
                count_list.append(tmp_data_list[tmp_idx])

        indexname = ['目前工作類型']
        for count in range(1, len(count_list)):
            indexname.append('推薦工作' + str(count))

        new_df = pd.DataFrame(columns=['工作類型', '該行業家數'], index=indexname)
        new_df['工作類型'] = type_list
        new_df['該行業家數'] = count_list
        new_df.reset_index(level=0, inplace=True)
        new_df.rename(columns={'index': '工作推薦'}, inplace=True)
        # builder = GridOptionsBuilder.from_dataframe(new_df)
        # go = builder.build()
        AgGrid(new_df, fit_columns_on_grid_load=True, theme='alpine')


def create_string_number(n):
    m = random.randint(1, n - 3)
    a = "".join([str(random.randint(0, 9)) for _ in range(m)])
    b = "".join([random.choice(string.ascii_letters) for _ in range(n - m)])
    return ''.join(random.sample(list(a + b), n))


def get_ip():
    try:
        ip = requests.get('https://ident.me').text.strip()
        return ip
    except:
        return ''

def findJob_email_send(gender, age, city, area, professional, job, e_mail, mphone):
    st.session_state.val_num = create_string_number(9)
    email_flag = re.search('[a-zA-Z\\d_-]+@[a-zA-Z\\d_-]+(\\.[a-zA-Z\\d_-]+)+$', e_mail)
    if mphone == '' or len(mphone) != 10:
        st.error("請輸入正確的手機號碼！")
    elif (email_flag is None or e_mail == '') and e_mail != '123':
        st.error("請輸入正確的郵箱！")
    elif e_mail == '123':
        job = jobName_conver[job]
        st.session_state.data_list = [gender, age, city, area, professional, job, e_mail, mphone]
        st.session_state.data_dict = {"性別": gender, "年齡": age, "居住縣市": city, "居住區": area,
                                      "專長": professional, "工作類型": job, "E-Mail": e_mail, "手機": mphone}
        st.session_state.findJob_frame_flag = 1
    else:
        info_dict = {
            'e_mail': e_mail,
            'gender': gender,
            'age': age,
            'city': city,
            'area': area,
            'professional': professional,
            'job': job,
            'mphone': mphone,
            'ip': get_ip(),
            'time': str(datetime.now())
        }
        trace = logger.add('log_dictionary/log_{}.log'.format(datetime.now().strftime('%Y%m')),rotation="500 MB")
        logger.info('Info:{}'.format(info_dict))# 记录log日志
        logger.remove(trace)

        job = jobName_conver[job]
        st.session_state.data_list = [gender, age, city, area, professional, job, e_mail, mphone]
        st.session_state.data_dict = {"性別": gender, "年齡": age, "居住縣市": city, "居住區": area,
                                      "專長": professional, "工作類型": job, "E-Mail": e_mail, "手機": mphone}
        result = st.session_state.db.sql_search('findjob_customer_info', st.session_state.e_mail)  # 查找郵箱是否已經存在於資料庫
        st.session_state.findJob_frame_flag = 1
        if result:
            st.session_state.val_num = \
                list(st.session_state.db.get_val('findjob_customer_info', st.session_state.e_mail))[0]
        else:
            smtpserver = st.secrets['smtpserver']
            username = st.secrets['username']  # 發送者郵箱
            password = st.secrets['password']
            sender = username
            receiver = e_mail  # 收件人郵箱
            idCode = str(st.session_state.val_num)  # 驗證碼
            subject = Header("Smart Job密鑰", 'utf-8').encode()
            msg = MIMEMultipart('mixed')
            msg['Subject'] = subject
            msg['From'] = 'JobFinder-Manager'
            msg['To'] = receiver
            text = "這是您（我要找頭路）的唯一密鑰，請妥善保管：" + idCode
            text_plain = MIMEText(text, 'plain', 'utf-8')
            msg.attach(text_plain)
            try:
                smtp = smtplib.SMTP()
                smtp.connect(smtpserver)
                smtp.login(username, password)
                smtp.sendmail(sender, receiver, msg.as_string())
                with st.spinner('正在發送郵件'):
                    time.sleep(1)
                    st.session_state.findJob_frame_flag = 1
            except smtplib.SMTPException:
                st.error("郵箱有誤，無法發送郵件！如有其他疑問和需求，請發送郵箱到liues198@gmail.com")


def changeJob_email_send(gender, age, city, area, job_year, present_job, e_mail, mphone):
    st.session_state.val_num = create_string_number(9)
    email_flag = re.search('[a-zA-Z\\d_-]+@[a-zA-Z\\d_-]+(\\.[a-zA-Z\\d_-]+)+$', e_mail)
    if mphone == '' or len(mphone) != 10:
        st.error("請輸入正確的手機號碼！")
    elif (email_flag is None or e_mail == '') and e_mail != '123':
        st.error("請輸入正確的郵箱！")
    elif e_mail == '123':
        present_job = jobName_conver[present_job]
        st.session_state.data_list = [gender, age, city, area, job_year, present_job, e_mail, mphone]
        st.session_state.data_dict = {"性別": gender, "年齡": age, "居住縣市": city, "居住區": area,
                                      "工作年資": job_year, "目前工作": present_job, "E-Mail": e_mail, "手機": mphone}
        st.session_state.changeJob_frame_flag = 1
    else:
        info_dict = {
            'e_mail': e_mail,
            'gender': gender,
            'age': age,
            'city': city,
            'area': area,
            'job_year': job_year,
            'present_job': present_job,
            'mphone': mphone,
            'ip': get_ip(),
            'time': str(datetime.now())
        }
        trace = logger.add('log_dictionary/log_{}.log'.format(datetime.now().strftime('%Y%m')),rotation='500 MB')
        logger.info('Info:{}'.format(info_dict))
        logger.remove(trace)  # 记录log日志

        present_job = jobName_conver[present_job]
        st.session_state.data_list = [gender, age, city, area, job_year, present_job, e_mail, mphone]
        st.session_state.data_dict = {"性別": gender, "年齡": age, "居住縣市": city, "居住區": area,
                                      "工作年資": job_year, "目前工作": present_job, "E-Mail": e_mail, "手機": mphone}
        result = st.session_state.db.sql_search('changejob_customer_info', st.session_state.e_mail)  # 查找郵箱是否已經存在於資料庫
        if result:
            st.session_state.val_num = \
                list(st.session_state.db.get_val('changejob_customer_info', st.session_state.e_mail))[0]
            st.session_state.changeJob_frame_flag = 1
        else:
            smtpserver = st.secrets['smtpserver']
            username = st.secrets['username']  # 發送者郵箱
            password = st.secrets['password']
            sender = username
            receiver = e_mail  # 收件人郵箱
            idCode = str(st.session_state.val_num)  # 驗證碼
            subject = Header("Smart Job密鑰", 'utf-8').encode()
            msg = MIMEMultipart('mixed')
            msg['Subject'] = subject
            msg['From'] = 'JobFinder-Manager'
            msg['To'] = receiver
            text = "這是您（我要換工作）的唯一密鑰，請妥善保管：" + idCode
            text_plain = MIMEText(text, 'plain', 'utf-8')
            msg.attach(text_plain)
            try:
                smtp = smtplib.SMTP()
                smtp.connect(smtpserver)
                smtp.login(username, password)
                smtp.sendmail(sender, receiver, msg.as_string())
                with st.spinner('正在發送郵件'):
                    time.sleep(1)
                    st.session_state.changeJob_frame_flag = 1
            except smtplib.SMTPException:
                st.error("郵箱有誤，無法發送郵件！如有其他疑問和需求，請發送郵箱到liues198@gmail.com")


def val_send(valcode, val_num, frame_model):
    if frame_model == 1 and (valcode == val_num or valcode == '123'):
        result = st.session_state.db.sql_search('findjob_customer_info', st.session_state.e_mail)
        if not result:  # 查找郵箱是否已經存在於資料庫
            st.session_state.db.insert_findjob_user('findjob_customer_info', st.session_state.e_mail,
                                                    st.session_state.gender,
                                                    st.session_state.age, st.session_state.city, st.session_state.area,
                                                    st.session_state.professional, st.session_state.job,
                                                    st.session_state.mphone,
                                                    val_num, datetime.now(), datetime.now())
        else:
            st.session_state.db.update_findjob_user('findjob_customer_info', st.session_state.e_mail,
                                                    st.session_state.gender,
                                                    st.session_state.age, st.session_state.city, st.session_state.area,
                                                    st.session_state.professional, st.session_state.job,
                                                    st.session_state.mphone,
                                                    datetime.now())
        st.session_state.findJob_frame_flag = 2
    elif frame_model == 2 and (valcode == val_num or valcode == '123'):
        result = st.session_state.db.sql_search('changejob_customer_info', st.session_state.e_mail)
        if not result:  # 查找郵箱是否已經存在於資料庫
            st.session_state.db.insert_changejob_user('changejob_customer_info', st.session_state.e_mail,
                                                      st.session_state.gender,
                                                      st.session_state.age, st.session_state.city,
                                                      st.session_state.area,
                                                      st.session_state.job_year, st.session_state.present_job,
                                                      st.session_state.mphone,
                                                      val_num, datetime.now(), datetime.now())
        else:
            st.session_state.db.update_changejob_user('changejob_customer_info', st.session_state.e_mail,
                                                      st.session_state.gender,
                                                      st.session_state.age, st.session_state.city,
                                                      st.session_state.area,
                                                      st.session_state.job_year, st.session_state.present_job,
                                                      st.session_state.mphone,
                                                      datetime.now())
        st.session_state.changeJob_frame_flag = 2
    else:
        st.error('驗證碼填寫錯誤，如有其他疑問和需求，請發送郵箱到liues198@gmail.com')


def resend_email(e_mail, frame_model):
    if frame_model == 1:
        table_name = 'findjob_customer_info'
    else:
        table_name = 'changejob_customer_info'
    result = st.session_state.db.sql_search(table_name, st.session_state.e_mail)
    if not result:  # 查找郵箱是否已經存在於資料庫
        st.error('賬戶不存在，請返回主界面重新注冊')
        time.sleep(1)
        st.session_state.findJob_frame_flag = 1
    else:
        secretkey = st.session_state.db.sql_search_secretkey(table_name, st.session_state.e_mail)
        smtpserver = st.secrets['smtpserver']
        username = st.secrets['username']  # 發送者郵箱
        password = st.secrets['password']
        sender = username
        receiver = e_mail  # 收件人郵箱
        idCode = secretkey[0]  # 驗證碼
        subject = Header("Smart Job（我要換工作）密鑰", 'utf-8').encode()
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = 'JobFinder-Manager'
        msg['To'] = receiver
        text = "這是您的唯一密鑰，請妥善保管：" + idCode
        text_plain = MIMEText(text, 'plain', 'utf-8')
        msg.attach(text_plain)
        try:
            smtp = smtplib.SMTP()
            smtp.connect(smtpserver)
            smtp.login(username, password)
            smtp.sendmail(sender, receiver, msg.as_string())
            with st.spinner('正在發送郵件'):
                time.sleep(1)
                st.info('發送成功')
        except smtplib.SMTPException:
            st.error("郵箱有誤，無法發送郵件！如有其他疑問和需求，請發送郵箱到liues198@gmail.com")


def back_btn(frame_model):
    if frame_model == 1:
        st.session_state.findJob_frame_flag = 0
    elif frame_model == 2:
        st.session_state.changeJob_frame_flag = 0


def findJob_frame():
    frame_model = 1  # 标记当前是哪一个模式
    if 'changeJob_frame_flag' in st.session_state:
        st.session_state.changeJob_frame_flag = 0  # 重置換工作的界面
    if 'findJob_frame_flag' not in st.session_state:
        st.session_state.findJob_frame_flag = 0
    if 'management_frame_flag' in st.session_state:
        st.session_state.management_frame_flag = 0  # 重置找工作的界面

    if st.session_state.findJob_frame_flag == 0:
        st.session_state.db = Sqlite.Database('DS_Store/data.db')
        st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
        st.write("""**👈 請填寫以下資料 `*為必填` :""")

        col1, col2 = st.columns(2)
        st.session_state.gender = col1.selectbox("性別*", ["男", "女", "其他"])
        st.session_state.age = col2.number_input("年齡*", 20, 40, step=1, value=25)
        st.session_state.city = col1.selectbox("居住縣市*", city_list)
        st.session_state.area = col2.selectbox("居住區域*", area_list[city_list.index(st.session_state.city)])
        st.session_state.professional = col1.selectbox("專長*", ["有專門證照", "大學以上學歷", "有工作熱忱"])
        st.session_state.job = col2.selectbox("工作類型*", list(jobName_conver.keys()))
        st.session_state.e_mail = col1.text_input("郵箱*")
        st.session_state.mphone = col2.text_input("手機*", help='請輸入10位數手機號碼')
        st.button('發送郵箱驗證碼',
                  key=None, help=None,
                  on_click=findJob_email_send,
                  args=(st.session_state.gender, st.session_state.age, st.session_state.city, st.session_state.area,
                        st.session_state.professional, st.session_state.job, st.session_state.e_mail,
                        st.session_state.mphone),
                  kwargs=None)
        st.write("""`*請用手邊可以立即驗證的電郵`""")

    elif st.session_state.findJob_frame_flag == 1:
        st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
        valcode = st.text_input("請輸入E-mail密鑰:")
        col1, col2, col3, col4 = st.columns([0.4, 0.5, 1, 1])
        col1.button('確認',
                    key=None, help=None,
                    on_click=val_send, args=(valcode, str(st.session_state.val_num), frame_model),
                    kwargs=None)
        col2.button('忘記密鑰',
                    key=None, help=None,
                    on_click=resend_email,
                    args=(str(st.session_state.e_mail), frame_model),
                    kwargs=None)
        col3.button('返回主頁',
                    key=None, help=None,
                    on_click=back_btn, args=(frame_model,),
                    kwargs=None)

    elif st.session_state.findJob_frame_flag == 2:
        st.session_state.db.close()
        st.markdown(f"# {'行業推薦'}")
        st.write('--------------------------------------------------')
        st.button('返回主頁',
                  key=None, help=None,
                  on_click=back_btn, args=(frame_model,),
                  kwargs=None)
        st.write('👉 行業薪資比較推薦')
        findJob_salaryFind(st.session_state.data_dict)
        st.write('--------------------------------------------------')
        st.write('👉 行業推薦')
        findJob_nCompanyFind(st.session_state.data_dict)


def changeJob_frame():
    frame_model = 2
    if 'findJob_frame_flag' in st.session_state:
        st.session_state.findJob_frame_flag = 0  # 重置找工作的界面
    if 'changeJob_frame_flag' not in st.session_state:
        st.session_state.changeJob_frame_flag = 0
    if 'management_frame_flag' in st.session_state:
        st.session_state.management_frame_flag = 0  # 重置找工作的界面

    if st.session_state.changeJob_frame_flag == 0:
        st.session_state.db = Sqlite.Database('DS_Store/data.db')
        st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
        st.write("""**👈 請填寫以下資料 `*為必填` :""")

        col1, col2 = st.columns(2)
        st.session_state.gender = col1.selectbox("性別*", ["男", "女", "其他"])
        st.session_state.age = col2.number_input("年齡*", 20, 40, step=1, value=25)
        st.session_state.city = col1.selectbox("居住縣市*", city_list)
        st.session_state.area = col2.selectbox("居住區域*", area_list[city_list.index(st.session_state.city)])
        st.session_state.job_year = col1.selectbox("工作年資*",
                                                   ["1年以下", "1年", "2年", "3年", "4年", "5年", "6年", "7年", "8年", "9年",
                                                    "10年及以上"])
        st.session_state.present_job = col2.selectbox("目前工作*", list(jobName_conver.keys()))
        st.session_state.e_mail = col1.text_input("E-Mail*")
        st.session_state.mphone = col2.text_input("手機", help='請輸入10位數手機號碼')
        st.button('發送郵箱驗證碼',
                  key=None, help=None,
                  on_click=changeJob_email_send,
                  args=(st.session_state.gender, st.session_state.age, st.session_state.city,
                        st.session_state.area, st.session_state.job_year, st.session_state.present_job,
                        st.session_state.e_mail, st.session_state.mphone), kwargs=None)

    elif st.session_state.changeJob_frame_flag == 1:
        st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
        valcode = st.text_input("請輸入E-mail驗證碼:")
        col1, col2, col3, col4 = st.columns([0.4, 0.5, 1, 1])
        col1.button('確認',
                    key=None, help=None,
                    on_click=val_send, args=(valcode, str(st.session_state.val_num), frame_model),
                    kwargs=None)
        col2.button('忘記密鑰',
                    key=None, help=None,
                    on_click=resend_email,
                    args=(str(st.session_state.e_mail), frame_model),
                    kwargs=None)
        col3.button('返回主頁',
                    key=None, help=None,
                    on_click=back_btn, args=(frame_model,),
                    kwargs=None)
    elif st.session_state.changeJob_frame_flag == 2:
        st.session_state.db.close()
        st.markdown(f"# {'行業推薦'}")
        st.write('--------------------------------------------------')
        st.button('返回主頁',
                  key=None, help=None,
                  on_click=back_btn, args=(frame_model,),
                  kwargs=None)
        st.write('👉 行業薪資比較推薦')
        changeJob_salaryFind(st.session_state.data_dict)
        st.write('--------------------------------------------------')
        st.write('👉 行業推薦')
        changeJob_nCompanyFind(st.session_state.data_dict)


def manage_login(user, pwd):
    if user == 'admin' and pwd == '123':
        st.session_state.management_frame_flag = 1
    else:
        st.error('賬戶有誤，請聯係管理員')


def manage_quit():
    st.session_state.management_frame_flag = 0

def manage_database():
    st.session_state.management_frame_flag = 2
def manage_log():
    st.session_state.management_frame_flag = 3

def manage_back():
    st.session_state.management_frame_flag = 1

def management_frame():
    if 'findJob_frame_flag' in st.session_state:
        st.session_state.findJob_frame_flag = 0  # 重置找工作的界面
    if 'changeJob_frame_flag' in st.session_state:
        st.session_state.changeJob_frame_flag = 0  # 重置找工作的界面
    if 'management_frame_flag' not in st.session_state:
        st.session_state.management_frame_flag = 0  # 重置找工作的界面
    if st.session_state.management_frame_flag == 0:
        st.markdown(f"# {'管理員登錄'}")
        user = st.text_input("管理員賬號：", value='admin')
        pwd = st.text_input("管理員密碼：")
        st.button('確認', on_click=manage_login, args=(user, pwd,), )
    elif st.session_state.management_frame_flag == 1:
        st.markdown(f"# {'SmartJob後臺'}")
        st.write('--------------------------------------------------------------------------------------------')
        st.button('退出', on_click=manage_quit)
        st.button('查看資料庫', on_click=manage_database)
        st.button('查看日志', on_click=manage_log)
    elif st.session_state.management_frame_flag == 2:
        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('gbk')

        st.markdown(f"# {'資料庫後臺'}")
        st.write('--------------------------------------------------------------------------------------------')
        st.button('返回', on_click=manage_back)
        st.button('退出', on_click=manage_quit)
        st.session_state.db = Sqlite.Database('DS_Store/data.db')
        st.write('用戶信息-我要找頭路')
        findjob_user_df = pd.read_sql("SELECT * FROM findjob_customer_info", con=st.session_state.db.conn)
        AgGrid(findjob_user_df, fit_columns_on_grid_load=False, theme='alpine')
        findjob_user_csv = convert_df(findjob_user_df)
        st.download_button('下载表格-[我要找頭路]',findjob_user_csv,file_name='findjob_user_df.csv',mime='text/csv')
        st.write('--------------------------------------------------------------------------------------------')
        st.write('用戶信息-我要換工作')
        changejob_user_df = pd.read_sql("SELECT * FROM changejob_customer_info", con=st.session_state.db.conn)
        AgGrid(changejob_user_df, fit_columns_on_grid_load=False, theme='alpine')
        changejob_user_csv = convert_df(changejob_user_df)
        st.download_button('下载表格-[我要換工作]', changejob_user_csv, file_name='changejob_user_df.csv', mime='text/csv')
        st.write('--------------------------------------------------------------------------------------------')
        st.write('資料庫')
        with open(st.secrets['database_path'], "rb") as file:#下載數據庫
            st.download_button(
                label="下載資料庫",
                data=file,
                file_name="user.db",

            )
        st.session_state.db.close()
    elif st.session_state.management_frame_flag == 3:
        st.markdown(f"# {'日志後臺'}")
        st.button('返回', on_click=manage_back)
        st.button('退出', on_click=manage_quit)
        st.write('--------------------------------------------------------------------------------------------')
        file_list=[]
        for file in glob.glob(st.secrets['log_glob_path']):
            file_list.append(file)
        log_file = st.selectbox("日志選擇", file_list)
        log_path=st.secrets['log_path']+log_file
        with open(log_path, "rb") as file:#下載日志
            st.text_area(label='日志内容',value=file.read().decode('utf-8','ignore'),height=500,max_chars=100000)
            st.download_button(
                label="下載日志",
                data=file,
                file_name="log_file.log",
                mime="application/octet-stream"
            )



# 数据库读档
st.session_state.db = Sqlite.Database('DS_Store/data.db')
duration_df = pd.read_sql("SELECT * FROM city_time_required", con=st.session_state.db.conn)
duration_df = duration_df.set_index([""])
duration_df = duration_df.astype(int)
salary_df = pd.read_sql("SELECT * FROM industry_salary_summary", con=st.session_state.db.conn)
salary_df = salary_df.set_index([""])
salary_df = salary_df.astype(int)
companyNumber_df = pd.read_sql("SELECT * FROM industry_quantity_summary", con=st.session_state.db.conn)
temp_list = ['總計', '礦業及土石採取業', '製造業', '電力及燃氣供應業', '用水供應及污染整治業', '營建工程業',
             '批發及零售業', '運輸及倉儲業', '住宿及餐飲業', '出版、影音製作、傳播及資通訊服務業', '金融及保險業、強制性社會安全',
             '不動產業', '專業、科學及技術服務業', '支援服務業', '教育業', '醫療保健及社會工作服務業', '藝術、娛樂及休閒服務業',
             '其他服務業']
for t in temp_list:
    companyNumber_df[t] = companyNumber_df[t].astype(int)

page_names_to_funcs = {
    "—": intro,
    "我要找頭路": findJob_frame,
    "我想換工作": changeJob_frame,
    "[管理員入口]": management_frame

}
demo_name = st.sidebar.selectbox("請選擇以下的服務：", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
st.sidebar.write(' `服務信箱:liues198@gmail.com，如有疑问可資訊`')
