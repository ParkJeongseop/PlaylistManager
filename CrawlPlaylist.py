from selenium import webdriver
import time

login_types = ['local', 'facebook', 'twitter', 'kakao', 'skt-id', 'payco', 'phone-number']
music_services = [['melon', ['local', 'kakao']],\
                  ['genie', ['local', 'facebook', 'twitter', 'kakao']],\
                  ['flo', ['local', 'skt-id', 'phone-number']],\
                  ['vibe', ['local']],\
                  ['bugs', ['local', 'facebook', 'payco']],\
                  ['apple', ['local']],\
                  ['mnet', ['local', 'facebook', 'twitter', 'kakao']],\
                  ['soribada', ['local', 'facebook', 'kakao']],\
                  ['olleh', ['local', 'facebook' , 'twitter']]]

# max 멜론500

# 바이브는 로컬이 네이버로그인
# 벅스 한게임 plus계정은 일단 보류(그 계정자체에서도 여러 로그인타입 존재)
# 올레뮤직은 local, local2 ? , facebook, twitter, olleh.com 등이 있음 일단 기본만

class UserInfo:
    def __init__(self, service_id, login_type, id, pw):
        self.service_id = service_id
        self.login_type = login_type
        self.id = id
        self.pw = pw


class Playlist:
    def __init__(self, playlist_name):
        self.name = playlist_name
        self.music_list = []

    def add_music(self, music):
        self.music_list.append(music)

    def __str__(self):
        return f'{self.name} 수록곡 : 총 {len(self.music_list)}곡'

    def contents_str(self):
        result = ""
        for i in self.music_list:
            result += str(i)
            result += '\n'
        return result


class Music:
    def __init__(self, name, artist, album):
        self.name = name
        self.artist = artist
        self.album = album
        self.keys = {}

    def set_music_key(self, service_id, key):
        self.keys[service_id] = key

    def __str__(self):
        return f'곡명: {self.name}\t 아티스트: {self.artist}\t 앨범: {self.album}'


def start():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
    # options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")
    # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    driver.implicitly_wait(3)


def get_element_by_text(str):
    element = driver.find_elements_by_xpath("//*[contains(text(), '" + str + "')]")
    if not len(element):
        print("Can not Find Element")
        return None
    else:
        return element[0]


def login(user):
    if user.service_id == 0:
        # 멜론
        if user.login_type == 'local':
            # driver.delete_all_cookies()
            login_url = 'https://member.melon.com/muid/web/login/login_informM.htm'
            driver.get(login_url)
            driver.find_element_by_name('id').send_keys(user.id)
            driver.find_element_by_name('pwd').send_keys(user.pw)
            driver.implicitly_wait(3)
            driver.find_element_by_id('btnLogin').click()


        elif user.login_type == 'kakao':
            login_url = 'https://member.melon.com/muid/web/login/login_inform.htm'
            driver.get(login_url)
            # driver.find_element_by_class_name('btn_gate kakao').click()
            driver.find_element_by_css_selector('#conts_section > div > div > div:nth-child(1) > button').click()
            driver.implicitly_wait(50)
            driver.switch_to.window(driver.window_handles[-1])
            print(driver.window_handles)
            print(driver.find_element_by_xpath("/html/head/title").get_attribute('text'))
            driver.find_element_by_css_selector('#loginEmail').send_keys(user.id)
            driver.find_element_by_css_selector('#loginPw').send_keys(user.pw)
            # driver.find_element_by_id('loginEmail').send_keys(user.id)
            # driver.find_element_by_id('loginPw').send_keys(user.pw)
            driver.find_element_by_class_name('btn_login submit btn_disabled btn_type2').click()

        else:
            print("No Login Type")
    elif user.service_id == 1:
        # 지니
        print()


def crawl(user):
    # 반환할 플레이리스트 배열 생성
    playlist_list = []

    if user.service_id == 0:
        playlist_list_url = 'https://www.melon.com/mymusic/playlist/mymusicplaylistmanage_more.htm'

        # driver.find_element_by_xpath('//*[@id="gnb_menu"]/ul[2]/li[1]/a/span[2]').click()
        # driver.implicitly_wait(3)
        # time.sleep(3)
        # uid = driver.current_url[-8:]

        driver.get(playlist_list_url)
        playlist_list_name_temp = driver.find_elements_by_xpath('/html/body/div/a/strong')
        playlist_list_uid_temp = driver.find_elements_by_class_name('plist_name')
        playlist_list_name = []
        playlist_list_uid = []

        for i in range(len(playlist_list_name_temp)):
            playlist_list_name.append(playlist_list_name_temp[i].text)
            playlist_list_uid.append(playlist_list_uid_temp[i].get_attribute('href')[-12:-3])
        print(playlist_list_name)
        print(playlist_list_uid)

        playlist_url = 'https://www.melon.com/mymusic/playlist/mymusicplaylistview_listPagingSong.htm?startIndex=1&pageSize=1000&plylstSeq='
        #
        # # 플레이리스트 목록 페이지 진입
        # for i in range(len(playlist_list)):
        #     time.sleep(2)
        #     playlist_list = driver.find_elements_by_xpath('//*[@id="pageList"]/table/tbody/tr/td[2]/div/div/dl/dt/a')
        #     playlist_name = playlist_list[i].text
        #
        #     # 플레이리스트 생성
        #     playlist = Playlist(playlist_name)
        #     print(playlist)
        #
        #     driver.implicitly_wait(3)
        #     playlist_list[i].click()
        #
        #     pages = driver.find_elements_by_xpath('//*[@id="pageObjNavgation"]/div/span/a')
        #
        #     for j in range(len(pages) + 1): # 현 플레이리스트의 페이지들
        #         names = driver.find_elements_by_xpath('//*[@id="frm"]/div/table/tbody/tr/td[3]/div/div/a[1]')
        #         artists = driver.find_elements_by_xpath('//*[@id="artistName"]')
        #         albums = driver.find_elements_by_xpath('//*[@id="frm"]/div/table/tbody/tr/td[5]/div/div/a')
        #
        #         for k in range(len(names)): # 현 페이지의 리스트들
        #             temp_music = Music(names[k].text, artists[k].text, albums[k].text)
        #             playlist.add_music(temp_music)
        #             print(temp_music)
        #
        #         if j == len(pages):
        #             break
        #         else:
        #             driver.find_elements_by_xpath('//*[@id="pageObjNavgation"]/div/span/a')[j].click()
        #             driver.implicitly_wait(3)
        #             time.sleep(2)

        for i in range(len(playlist_list_name)): #각 플레이리스트들
            # 플레이리스트 생성
            playlist = Playlist(playlist_list_name[i])
            # print(playlist)

            driver.get(playlist_url+playlist_list_uid[i])
            names = driver.find_elements_by_xpath('//*[@id="frm"]/div/table/tbody/tr/td[3]/div/div/a[1]')
            artists = driver.find_elements_by_xpath('//*[@id="artistName"]')
            albums = driver.find_elements_by_xpath('//*[@id="frm"]/div/table/tbody/tr/td[5]/div/div/a')

            for k in range(len(names)):  # 플레이리스트 안 음악들
                temp_music = Music(names[k].text, artists[k].text, albums[k].text)
                playlist.add_music(temp_music)
                # print(temp_music)

            playlist_list.append(playlist)
            # print(playlist)
            # print(playlist.print_contents())

            # driver.get(playlist_url + uid)
            # driver.back()
        # print(playlist_list)
        for playlist in playlist_list:
            print(playlist)
            print(playlist.contents_str())



    elif user.service_id == 1: ##지니
        print()
        ## 멜론 로그인 ksxobkk1lamxh0om.js

    return playlist_list


def migrate(user, playlists):
    if user.service_id == 0:
        # 멜론
        search_url = 'https://www.melon.com/search/total/index.htm?q='
        make_playlist_url = 'https://www.melon.com/mymusic/common/popup/mymusiccommon_makePlaylistPopUp.htm'

        for playlist in playlists:
            driver.get(make_playlist_url)
            driver.find_element_by_id('plylstTitle').send_keys(playlist.name)
            driver.find_element_by_class_name('btn_emphs_small').click()

            # Todo: 이미있는 플레이리스트의 경우, 플레이리스트가 1페이지에 있지않은경우 구현 (페이지탐색)
            for music in playlist.music_list:
                driver.get(f'{search_url}{music.name} {music.artist}')
                driver.find_element_by_xpath('//*[@id="frm_songList"]/div/table/tbody/tr/td[3]/div/div/button[2]').click() #첫번째 음악 추가버튼
                driver.find_element_by_xpath(get_element_by_text(playlist.name)[:-8] + 'span/button').click()




        driver.get()
        driver.find_element_by_xpath('//*[@id="gnb_menu"]/ul[2]/li[1]/a/span[2]').click()
        driver.implicitly_wait(3)
        time.sleep(3)
        uid = driver.current_url[-8:]
        driver.get(playlist_url + uid)
        playlist_list = driver.find_elements_by_xpath('//*[@id="pageList"]/table/tbody/tr/td[2]/div/div/dl/dt/a')

        # 플레이리스트 목록 페이지 진입
        for i in range(len(playlist_list)):
            time.sleep(2)
            playlist_list = driver.find_elements_by_xpath('//*[@id="pageList"]/table/tbody/tr/td[2]/div/div/dl/dt/a')
            playlist_name = playlist_list[i].text

            # 플레이리스트 생성
            playlist = Playlist(playlist_name)
            print(playlist)

            driver.implicitly_wait(3)
            playlist_list[i].click()

            pages = driver.find_elements_by_xpath('//*[@id="pageObjNavgation"]/div/span/a')

            for j in range(len(pages) + 1):
                names = driver.find_elements_by_xpath('//*[@id="frm"]/div/table/tbody/tr/td[3]/div/div/a[1]')
                artists = driver.find_elements_by_xpath('//*[@id="artistName"]')
                albums = driver.find_elements_by_xpath('//*[@id="frm"]/div/table/tbody/tr/td[5]/div/div/a')

                for k in range(len(names)):
                    temp_music = Music(names[k].text, artists[k].text, albums[k].text)
                    playlist.add_music(temp_music)
                    print(temp_music)

                if j == len(pages):
                    break
                else:
                    driver.find_elements_by_xpath('//*[@id="pageObjNavgation"]/div/span/a')[j].click()
                    driver.implicitly_wait(3)
                    time.sleep(2)
            data.append(playlist)
            print(playlist)
            print(playlist.print_contents())

            driver.get(playlist_url + uid)
            # driver.back()
        print(data)
        for a in data:
            print(a)


def input_no_blank(str):
    while True:
        id = input(str + ": ")
        id = id.strip()
        if id != "":
            return id
        else:
            print("Enter your " + str + ".")


def print_service_list():
    for i in range(len(music_services)):
        print(i, music_services[i])


if __name__ == '__main__':
    start()
    print_service_list()
    test_melon_account = UserInfo(0, 'local', 'parkjungsub@parkjungsub.com', 'qawsqaws12')
    test_melon_account2 = UserInfo(0, 'local', 'parkjeongseop', 'qawsqaws12')
    # test_melon_account = UserInfo(0, 'kakao', 'parkjeongseop@parkjeongseop.com', 'kakao34783')
    # crawl(test_melon_account) #test
    # service_id = int(input("Service ID: "))
    # id = input_no_blank("ID")
    # pw = input_no_blank("PW")
    # crawl(0, id, pw)
    login(test_melon_account)
    crawled_data = crawl(test_melon_account)
    login(test_melon_account2)
    # migrate(test_melon_account2, crawled_data)













#
# import requests
# from bs4 import BeautifulSoup
#
# music_services = ['melon', 'genie', 'vibe', 'bugs', 'apple', 'mnet', 'soribada', 'olleh']
#
#
# class UserInfo:
#     def __init__(self, service_id, id, pw):
#         self.service_id = service_id
#         self.id = id
#         self.pw = pw
#
#
# class Playlist:
#     def __init__(self, playlist_name):
#         self.name = playlist_name
#         self.music_list = []
#
#     def add_music(self, music):
#         self.music_list.append(music)
#
#
# class Music:
#     def __init__(self, name, artist, album):
#         self.name = name
#         self.artist = artist
#         self.album = album
#         self.keys = {}
#
#     def set_music_key(self, service_id, key):
#         self.keys[service_id] = key
#
#
# def crawl(user):
#     if user.service_id == 0:
#         # 멜론 로그인 ksxobkk1lamxh0om.js
#
#         params = dict()
#         params['memberId'] = user.id
#         params['memberPwd'] = user.pw
#         params['saveId'] = 'N'
#         print(params)
#
#         # Session 생성, with 구문 안에서 유지
#         with requests.Session() as s:
#             # 우선 클리앙 홈페이지에 들어가 봅시다.
#             # first_page = s.get('https://www.clien.net/service')
#             # html = first_page.text
#             # soup = bs(html, 'html.parser')
#             # csrf = soup.find('input', {'name': '_csrf'})  # input태그 중에서 name이 _csrf인 것을 찾습니다.
#             # # print(csrf['value'])  # 위에서 찾은 태그의 value를 가져옵니다.
#
#             # 이제 LOGIN_INFO에 csrf값을 넣어줍시다.
#             # (p.s.)Python3에서 두 dict를 합치는 방법은 {**dict1, **dict2} 으로 dict들을 unpacking하는 것입니다.
#             # LOGIN_INFO = {**LOGIN_INFO, **{'_csrf': csrf['value']}}
#             # print(LOGIN_INFO)
#
#             # 이제 다시 로그인을 해봅시다.
#             login_req = s.post('https://member.melon.com/muid/web/login/login_informProcs.htm', data=params)
#             # 어떤 결과가 나올까요? (200이면 성공!)
#             print(login_req.status_code)
#
#
#         # login_url = 'https://member.melon.com/muid/web/login/login_informProcs.htm'
#         #
#         # session = requests.session()
#         #
#         # params = dict()
#         # params['memberId'] = user.id
#         # params['memberPwd'] = user.pw
#         # params['saveId'] = 'N'
#         #
#         # # javascrit(jQuery) 코드를 분석해보니, 결국 login_proc.php 를 m_id 와 m_passwd 값과 함께
#         # # POST로 호출하기 때문에 다음과 같이 requests.session.post() 메서드를 활용하였습니다.
#         # # 실제코드: <form name="frm"  id="frm"  action="#" method="post">
#         # res = session.post(login_url, data=params)
#         #
#         # # 응답코드가 200 즉, OK가 아닌 경우 에러를 발생시키는 메서드입니다.
#         # res.raise_for_status()
#         #
#         # # 'Set-Cookie'로 PHPSESSID 라는 세션 ID 값이 넘어옴을 알 수 있다.
#         # # print(res.headers)
#         #
#         # # cookie로 세션을 로그인 상태를 관리하는 상태를 확인해보기 위한 코드입니다.
#         # # print(session.cookies.get_dict())
#         #
#         # # 여기서부터는 로그인이 된 세션이 유지됩니다. session 에 header에는 Cookie에 PHPSESSID가 들어갑니다.
#         # mypage_url = 'https://www.melon.com/mymusic/main/mymusicmain_list.htm?memberKey=50937293'
#         # res = session.get(mypage_url)
#         #
#         # # 응답코드가 200 즉, OK가 아닌 경우 에러를 발생시키는 메서드입니다.
#         # res.raise_for_status()
#         #
#         # soup = BeautifulSoup(res.text, 'html.parser')
#         #
#         # # Chrome 개발자 도구에서 CSS SELECTOR를 통해 간단히 가져온 CSS SELECTOR 표현식을 사용
#         # he_coin = soup.select_one('#conts > div.prfe_wrap > div > div.cntt.clfix > dl > dt')
#         #
#         # # 다음과 같이 class를 .mileage_section2 로 그리고 그 하부 태그중에 span이 있다는 식으로 표현도 가능함
#         # # he_coin = soup.select_one('.mileage_section2 span')
#         #
#         # print('mileage is', he_coin.get_text())
#
#     if user.service_id == 1: ##지니
#         print()
#         ## 멜론 로그인 ksxobkk1lamxh0om.js
#
#         # login_url = 'https://member.melon.com/muid/web/login/login_informProcs.htm'
#         #
#         # session = requests.session()
#         #
#         # params = dict()
#         # params['memberId'] = id
#         # params['memberPwd'] = pw
#         # params['saveId'] = 'N'
#         #
#         # # javascrit(jQuery) 코드를 분석해보니, 결국 login_proc.php 를 m_id 와 m_passwd 값과 함께
#         # # POST로 호출하기 때문에 다음과 같이 requests.session.post() 메서드를 활용하였습니다.
#         # # 실제코드: <form name="frm"  id="frm"  action="#" method="post">
#         # res = session.post(login_url, data=params)
#         #
#         # # 응답코드가 200 즉, OK가 아닌 경우 에러를 발생시키는 메서드입니다.
#         # res.raise_for_status()
#         #
#         # # 'Set-Cookie'로 PHPSESSID 라는 세션 ID 값이 넘어옴을 알 수 있다.
#         # # print(res.headers)
#         #
#         # # cookie로 세션을 로그인 상태를 관리하는 상태를 확인해보기 위한 코드입니다.
#         # # print(session.cookies.get_dict())
#         #
#         # # 여기서부터는 로그인이 된 세션이 유지됩니다. session 에 header에는 Cookie에 PHPSESSID가 들어갑니다.
#         # mypage_url = 'https://www.melon.com/mymusic/main/mymusicmain_list.htm?memberKey=50937293'
#         # res = session.get(mypage_url)
#         #
#         # # 응답코드가 200 즉, OK가 아닌 경우 에러를 발생시키는 메서드입니다.
#         # res.raise_for_status()
#         #
#         # soup = BeautifulSoup(res.text, 'html.parser')
#         #
#         # # Chrome 개발자 도구에서 CSS SELECTOR를 통해 간단히 가져온 CSS SELECTOR 표현식을 사용
#         # he_coin = soup.select_one('#conts > div.prfe_wrap > div > div.cntt.clfix > dl > dt')
#         #
#         # # 다음과 같이 class를 .mileage_section2 로 그리고 그 하부 태그중에 span이 있다는 식으로 표현도 가능함
#         # # he_coin = soup.select_one('.mileage_section2 span')
#         #
#         # print('mileage is', he_coin.get_text())
#
#
# def input_no_blank(str):
#     while True:
#         id = input(str + ": ")
#         id = id.strip()
#         if id != "":
#             return id
#         else:
#             print("Enter your " + str + ".")
#
#
# def print_service_list():
#     for i in range(len(music_services)):
#         print(i, music_services[i])
#
#
# if __name__ == '__main__':
#     print_service_list()
#     test_melon_account = UserInfo(0, 'parkjeongseop', 'qawsqaws12')
#     crawl(test_melon_account) #test
#     # service_id = int(input("Service ID: "))
#     # id = input_no_blank("ID")
#     # pw = input_no_blank("PW")
#     # crawl(0, id, pw)
