from selenium import webdriver
import pickle
from collections import OrderedDict
from itertools import repeat


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

# max 멜론1000

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


def save_as_pickle(filename, playlist_list):
    pickle.dump(playlist_list, open(filename, 'wb'))


def load_from_pickle(filename):
    return pickle.load(open(filename, 'rb'))


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

        driver.get(playlist_list_url)
        playlist_list_name_temp = driver.find_elements_by_xpath('/html/body/div/a/strong')
        playlist_list_uid_temp = driver.find_elements_by_class_name('plist_name')
        playlist_list_name = []
        playlist_list_uid = []

        for i in range(len(playlist_list_name_temp)):
            playlist_list_name.append(playlist_list_name_temp[i].text)
            playlist_list_uid.append(playlist_list_uid_temp[i].get_attribute('href')[-12:-3])

        playlist_url = 'https://www.melon.com/mymusic/playlist/mymusicplaylistview_listPagingSong.htm?startIndex=1&pageSize=1000&plylstSeq='

        for i in range(len(playlist_list_name)): #각 플레이리스트들
            # 플레이리스트 생성
            playlist = Playlist(playlist_list_name[i])

            driver.get(playlist_url+playlist_list_uid[i])
            names = driver.find_elements_by_xpath('//*[@id="frm"]/div/table/tbody/tr/td[3]/div/div/a[1]')
            artists = driver.find_elements_by_xpath('//*[@id="artistName"]')
            albums = driver.find_elements_by_xpath('//*[@id="frm"]/div/table/tbody/tr/td[5]/div/div/a')

            for k in range(len(names)):  # 플레이리스트 안 음악들
                temp_music = Music(names[k].text, artists[k].text, albums[k].text)
                playlist.add_music(temp_music)

            playlist_list.append(playlist)


    elif user.service_id == 1: ##지니
        print()
        ## 멜론 로그인 ksxobkk1lamxh0om.js

    return playlist_list


def migrate(user, playlists):
    if user.service_id == 0:
        # 멜론
        search_get_url = 'https://www.melon.com/mymusic/common/mymusiccommon_searchListSong.htm?kwd='
        make_playlist_url = 'https://www.melon.com/mymusic/playlist/mymusicplaylistinsert_insert.htm'
        make_playlist_post_url = 'https://www.melon.com/mymusic/playlist/mymusicplaylistinsert_insertAction.json'

        for playlist in playlists:
            music_uid_list = []
            for music in playlist.music_list:
                driver.get(search_get_url + music.name + ' ' + music.artist)
                try:
                    music_uid_list.append(driver.find_element_by_xpath('/html/body/div[1]/input').get_attribute('value')) # 검색결과 첫번째 음악의 고유아이디
                except:
                    print(f"not found {music.name} {music.artist}")

            music_uid_list = list(OrderedDict(zip(music_uid_list, repeat(None)))) # 중복제거 (곡명과 아티스트로 검색하기때문에 다른 앨범의 곡이 2개 이상있는경우 제거

            driver.get(make_playlist_url)

            data = '''var songList = new Array();'''

            for music_uid in music_uid_list:
                data += f'songList.push({music_uid});'
            data += '''$.ajax({
                    type : "POST",
                    url  : "/mymusic/playlist/mymusicplaylistinsert_insertAction.json",
                    async : false,
                    data : {plylstTitle : encodeURIComponent("''' + playlist.name + '''"), playlistDesc : encodeURIComponent("made by playlistmanager"), openYn : "N", songIds : songList, repntImagePath : "", repntImagePathDefaultYn : "N"}
                });
    '''
            driver.execute_script(data)


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

    # 피클 테스트
    data = load_from_pickle('test.plm')
    for playlist in data:
        print(playlist)
        print(playlist.contents_str())

    test_melon01_account = load_from_pickle('melon01.plmaccount')
    test_melon02_account = load_from_pickle('melon02.plmaccount')

    start()
    print_service_list()
    # login(test_melon01_account)
    # crawled_data = crawl(test_melon01_account)
    # save_as_pickle('test.plm', crawled_data)
    login(test_melon02_account)
    migrate(test_melon02_account, data)
