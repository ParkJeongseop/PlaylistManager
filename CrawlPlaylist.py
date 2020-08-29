from selenium import webdriver
import pickle
from collections import OrderedDict
from itertools import repeat
import json
import time
from urllib import parse
import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree


description = "Migrated by Playlist Manager"

# Musci streaming services code
melon_code = 0
genie_code = 1
flo_code = 2
vibe_code = 3
bugs_code = 4
apple_code = 5
soribada = 6
youtubemusic_code = 7
youtube_code = 8


login_types = ['local', 'facebook', 'twitter', 'kakao', 'skt-id', 'payco', 'phone-number']
music_services = [['melon', ['local', 'kakao']],\
                  ['genie', ['local', 'facebook', 'twitter', 'kakao']],\
                  ['flo', ['local', 'skt-id', 'phone-number']],\
                  ['vibe', ['local']],\
                  ['bugs', ['local', 'facebook', 'payco']],\
                  ['apple', ['local']],\
                  ['soribada', ['local', 'facebook', 'kakao']]]

# max 멜론1000

# 바이브는 로컬이 네이버로그인
# 벅스 한게임 plus계정은 일단 보류(그 계정자체에서도 여러 로그인타입 존재)
# 올레뮤직은 local, local2 ? , facebook, twitter, olleh.com 등이 있음 일단 기본만


class UserInfo:
    def __init__(self, service_id: int, login_type: str, id: str, pw: str):
        self.service_id = service_id
        self.login_type = login_type
        self.id = id
        self.pw = pw


class Playlist:
    def __init__(self, playlist_name: str):
        self.name = playlist_name
        self.music_list = []

    def add_music(self, music):
        self.music_list.append(music)

    def __str__(self):
        return f'{self.name} 수록곡 : 총 {len(self)}곡'

    def __len__(self):
        return len(self.music_list)

    def contents_str(self):
        result = ""
        for i in self.music_list:
            result += str(i)
            result += '\n'
        return result


class Music:
    def __init__(self, name: str, artist: str, album: str):
        self.name = name
        self.artist = artist
        self.album = album
        self.keys = {}

    def set_music_key(self, service_id: int, key: str):
        self.keys[service_id] = key

    def __str__(self):
        return f'곡명: {self.name}\t 아티스트: {self.artist}\t 앨범: {self.album}'


def save_as_pickle(filename, playlist_list):
    pickle.dump(playlist_list, open(filename, 'wb'))


def load_from_pickle(filename):
    return pickle.load(open(filename, 'rb'))


class PlaylistManager:
    def __init__(self, chromedriverpath: str):
        # self.driver = None
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
        # options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        # options.add_argument("disable-gpu")
        # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

        self.driver = webdriver.Chrome(chromedriverpath, chrome_options=options)
        self.driver.implicitly_wait(3)


    def __del__(self):
        self.driver.close()
        # self.driver.quit()


    def get_element_by_text(self, str: str):
        element = self.driver.find_elements_by_xpath("//*[contains(text(), '" + str + "')]")
        if not len(element):
            print("Can not Find Element")
            return None
        else:
            return element[0]


    def login(self, user: UserInfo):
        if user.service_id == 0:
            # 멜론
            if user.login_type == 'local':
                # driver.delete_all_cookies()
                login_url = 'https://member.melon.com/muid/web/login/login_informM.htm'
                self.driver.get(login_url)
                self.driver.find_element_by_name('id').send_keys(user.id)
                self.driver.find_element_by_name('pwd').send_keys(user.pw)
                self.driver.implicitly_wait(3)
                self.driver.find_element_by_id('btnLogin').click()


            elif user.login_type == 'kakao':
                login_url = 'https://member.melon.com/muid/web/login/login_inform.htm'
                self.driver.get(login_url)
                # self.driver.find_element_by_class_name('btn_gate kakao').click()
                self.driver.find_element_by_css_selector('#conts_section > div > div > div:nth-child(1) > button').click()
                self.driver.implicitly_wait(50)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                print(self.driver.window_handles)
                print(self.driver.find_element_by_xpath("/html/head/title").get_attribute('text'))
                self.driver.find_element_by_css_selector('#loginEmail').send_keys(user.id)
                self.driver.find_element_by_css_selector('#loginPw').send_keys(user.pw)
                # self.driver.find_element_by_id('loginEmail').send_keys(user.id)
                # self.driver.find_element_by_id('loginPw').send_keys(user.pw)
                self.driver.find_element_by_class_name('btn_login submit btn_disabled btn_type2').click()

            else:
                print("No Login Type")

        elif user.service_id == 1:
            # 지니
            if user.login_type == 'local':
                login_url = 'https://www.genie.co.kr/member/popLogin'
                self.driver.get(login_url)
                self.driver.find_element_by_name('gnb_uxd').send_keys(user.id)
                self.driver.find_element_by_name('gnb_uxx').send_keys(user.pw)
                self.driver.execute_script('loginID()')

        elif user.service_id == 2:
            # 플로
            if user.login_type == 'local':
                login_url = 'https://www.music-flo.com/member/signin'
                email_id, email_domain = user.id.split("@")
                self.driver.get(login_url)
                self.driver.find_element_by_name('emailId').send_keys(email_id)
                self.driver.find_element_by_xpath('//*[@id="emailUrl"]/option[14]').click()
                self.driver.find_element_by_name('emailUrlDirect').send_keys(email_domain)
                self.driver.find_element_by_name('password').send_keys(user.pw)
                self.driver.find_element_by_id('btnSubmitSignin').click()

        elif user.service_id == 3:
            # Vibe
            if user.login_type == 'Naver':
                login_url = 'https://nid.naver.com/nidlogin.login'
                self.driver.get(login_url)
                import pyperclip
                from selenium.webdriver.common.action_chains import ActionChains
                from selenium.webdriver.common.keys import Keys

                pyperclip.copy(user.id)
                self.driver.find_element_by_xpath('//*[@id="id"]').click()
                ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

                pyperclip.copy(user.pw)
                self.driver.find_element_by_xpath('//*[@id="pw"]').click()
                ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

                self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

                self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/span[1]/a').click()
                self.driver.find_element_by_xpath('//*[@id="login_maintain"]/span[2]/a').click()


    def crawl(self, user: UserInfo):
        # 반환할 플레이리스트 배열 생성
        playlist_list = []

        if user.service_id == 0:
            playlist_list_url = 'https://www.melon.com/mymusic/playlist/mymusicplaylistmanage_more.htm'

            self.driver.get(playlist_list_url)
            playlist_list_name_temp = self.driver.find_elements_by_xpath('/html/body/div/a/strong')
            playlist_list_uid_temp = self.driver.find_elements_by_class_name('plist_name')
            playlist_list_name = []
            playlist_list_uid = []

            for i in range(len(playlist_list_name_temp)):
                playlist_list_name.append(playlist_list_name_temp[i].text)
                playlist_list_uid.append(playlist_list_uid_temp[i].get_attribute('href')[-12:-3])

            playlist_url = 'https://www.melon.com/mymusic/playlist/mymusicplaylistview_listPagingSong.htm?startIndex=1&pageSize=1000&plylstSeq='

            for i in range(len(playlist_list_name)): #각 플레이리스트들
                # 플레이리스트 생성
                playlist = Playlist(playlist_list_name[i])

                self.driver.get(playlist_url+playlist_list_uid[i])
                names = self.driver.find_elements_by_xpath('//*[@id="frm"]/div/table/tbody/tr/td[3]/div/div/a[1]')
                artists = self.driver.find_elements_by_xpath('//*[@id="artistName"]')
                albums = self.driver.find_elements_by_xpath('//*[@id="frm"]/div/table/tbody/tr/td[5]/div/div/a')
                uid = self.driver.find_elements_by_xpath('//*[@id="frm"]/div/table/tbody/tr[1]/td[1]/div/input').value

                for k in range(len(names)):  # 플레이리스트 안 음악들
                    temp_music = Music(names[k].text, artists[k].text, albums[k].text)
                    temp_music.set_music_key(melon_code, uid)
                    playlist.add_music(temp_music)

                playlist_list.append(playlist)


        elif user.service_id == 1: ##지니
            print()
            ## 멜론 로그인 ksxobkk1lamxh0om.js

        return playlist_list


    def addPlaylists(self, user: UserInfo, playlists: Playlist): # 구 migrate
        for playlist in playlists:
            self.addPlaylist(user, playlist)


    def addPlaylist(self, user: UserInfo, playlist: Playlist):
        if user.service_id == 0:
            # 멜론
            search_get_url = 'https://www.melon.com/mymusic/common/mymusiccommon_searchListSong.htm?kwd='
            make_playlist_url = 'https://www.melon.com/mymusic/playlist/mymusicplaylistinsert_insert.htm'

            music_uid_list = []
            for music in playlist.music_list:
                self.driver.get(search_get_url + music.name + ' ' + music.artist)
                try:
                    music_uid_list.append(self.driver.find_element_by_xpath('/html/body/div[1]/input').get_attribute('value')) # 검색결과 첫번째 음악의 고유아이디
                except:
                    print(f"not found {music}")

            music_uid_list = list(OrderedDict(zip(music_uid_list, repeat(None)))) # 중복제거 (곡명과 아티스트로 검색하기때문에 다른 앨범의 곡이 2개 이상있는경우 제거

            self.driver.get(make_playlist_url)

            data = '''var songList = new Array();'''

            for music_uid in music_uid_list:
                data += f'songList.push({music_uid});'
            data += '''$.ajax({
                    type : "POST",
                    url  : "/mymusic/playlist/mymusicplaylistinsert_insertAction.json",
                    async : false,
                    data : {plylstTitle : encodeURIComponent("''' + playlist.name + '''"), playlistDesc : encodeURIComponent("''' + description + '''"), openYn : "N", songIds : songList, repntImagePath : "", repntImagePathDefaultYn : "N"}
                });
    '''
            self.driver.execute_script(data)


        elif user.service_id == 1:
            # 지니
            search_get_url = 'https://www.genie.co.kr/search/searchMain?query='
            make_playlist_url = 'https://www.genie.co.kr/myMusic/newPlayList' # https://www.genie.co.kr/myMusic/jGetMyAlbum
            playlists_url = 'https://www.genie.co.kr/member/myMusic' # https://www.genie.co.kr/myMusic/jGetMyAlbum

            print(playlist)
            music_uid_list = []
            self.driver.get(make_playlist_url)
            make_playlist_js = '''var form = $("form[name=hiddenForm]");
                $(form).find("[name=albumTitle]").val( "''' + playlist.name + '''" );
                $(form).find("[name=albumContent]").val( "''' + description + '''" );
                $(form).find("[name=orgMaImg]").val($("input[name=coverImgPath]").val() );

                $(form).find("[type=input],[type=textarea],[type=file],[type=hidden]").each(function(){
                    console.log($(this).attr("name") + ":" + $(this).val())
                });$(form).ajaxSubmit({
                    url: "/myMusic/playListInsert",
                    cache: false
                });'''

            self.driver.execute_script(make_playlist_js)
            print(make_playlist_js)

            self.driver.get(playlists_url)
            playlist_uid = json.loads(self.driver.find_element_by_xpath('/html/body/pre').text)['myAlbumList'][0]['maId']
            print(playlist_uid)

            for music in playlist.music_list:
                print(music)
                self.driver.get(search_get_url + music.name + ' ' + music.artist)
                try:
                    music_uid_list.append(self.driver.find_element_by_xpath('//*[@id="body-content"]/div[3]/div[2]/div/table/tbody/tr[1]').get_attribute('songid'))  # 검색결과 첫번째 음악의 고유아이디
                except:
                    print(f"not found {music}")

            music_uid_list = list(OrderedDict(zip(music_uid_list, repeat(None))))  # 중복제거 (곡명과 아티스트로 검색하기때문에 다른 앨범의 곡이 2개 이상있는경우 제거

            self.driver.get(make_playlist_url)

            data = '''$.ajax({
            type: "POST",
            url: "/myMusic/jMyAlbumSongAdd",
            dataType: "json",
            data: {"mxnm": "''' + playlist_uid + '''", "xgnms": "''' + ';'.join(music_uid_list) + '''", "mxlopths": "''' + ("W;"*len(music_uid_list))[:-1] + '''", "mxflgs": "''' + ("1;"*len(music_uid_list))[:-1] + '''", "unm": iMemUno}
        });'''
            print(data)
            self.driver.execute_script(data)


        elif user.service_id == 2:
            # 플로
            search_get_url = 'https://www.genie.co.kr/search/searchMain?query='
            make_playlist_url = 'https://www.genie.co.kr/myMusic/newPlayList' # https://www.genie.co.kr/myMusic/jGetMyAlbum
            playlists_url = 'https://www.genie.co.kr/member/myMusic' # https://www.genie.co.kr/myMusic/jGetMyAlbum

            print(playlist)
            music_uid_list = []
            self.driver.get(make_playlist_url)
            make_playlist_js = '''var form = $("form[name=hiddenForm]");
                $(form).find("[name=albumTitle]").val( "''' + playlist.name + '''" );
                $(form).find("[name=albumContent]").val( "''' + description + '''" );
                $(form).find("[name=orgMaImg]").val($("input[name=coverImgPath]").val() );

                $(form).find("[type=input],[type=textarea],[type=file],[type=hidden]").each(function(){
                    console.log($(this).attr("name") + ":" + $(this).val())
                });$(form).ajaxSubmit({
                    url: "/myMusic/playListInsert",
                    cache: false
                });'''

            self.driver.execute_script(make_playlist_js)
            print(make_playlist_js)

            self.driver.get(playlists_url)
            playlist_uid = json.loads(self.driver.find_element_by_xpath('/html/body/pre').text)['myAlbumList'][0]['maId']
            print(playlist_uid)

            for music in playlist.music_list:
                print(music)
                self.driver.get(search_get_url + music.name + ' ' + music.artist)
                try:
                    music_uid_list.append(self.driver.find_element_by_xpath('//*[@id="body-content"]/div[3]/div[2]/div/table/tbody/tr[1]').get_attribute('songid'))  # 검색결과 첫번째 음악의 고유아이디
                except:
                    print(f"not found {music}")

            music_uid_list = list(OrderedDict(zip(music_uid_list, repeat(None))))  # 중복제거 (곡명과 아티스트로 검색하기때문에 다른 앨범의 곡이 2개 이상있는경우 제거

            self.driver.get(make_playlist_url)

            data = '''$.ajax({
            type: "POST",
            url: "/myMusic/jMyAlbumSongAdd",
            dataType: "json",
            data: {"mxnm": "''' + playlist_uid + '''", "xgnms": "''' + ';'.join(music_uid_list) + '''", "mxlopths": "''' + ("W;"*len(music_uid_list))[:-1] + '''", "mxflgs": "''' + ("1;"*len(music_uid_list))[:-1] + '''", "unm": iMemUno}
        });'''
            print(data)
            self.driver.execute_script(data)


        elif user.service_id == 3:
            # Vibe
            search_get_url = 'https://vibe.naver.com/search/tracks?query='
            make_playlist_post_url = 'https://apis.naver.com/vibeWeb/musicapiweb/myMusic/myAlbum'
            playlists_url = 'https://vibe.naver.com/library/playlists'


            print(playlist)

            did_playlist_ade = False
            for music in playlist.music_list:
                print(music)
                self.driver.get(search_get_url + music.name + ' ' + music.artist)
                time.sleep(0.5)
                print("옴")
                try:
                    self.driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/table/tbody/tr[1]/td[1]/div/label').click()
                    print('곡선택')
                    time.sleep(1)
                    self.driver.find_element_by_class_name('btn_add_playlist').click()
                    print('플레이리스트추가')
                    if not did_playlist_ade:
                        self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/a[1]').click()
                        print('생성버튼')
                        time.sleep(0.5)
                        self.driver.find_element_by_xpath('//*[@id="new_playlist"]').send_keys(playlist.name)
                        self.driver.find_element_by_xpath('//*[@id="app"]/div[3]/div/div/div/a[2]').click()
                    time.sleep(0.5)
                    self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/a[2]').click()
                    print('추가버튼')
                except:
                    print(f"not found {music}")
                time.sleep(20)


    # def search_
    # def search_music_by_text(query: str):

    def search_results_by_query(self, query: str):
        pass


    def get_uids_by_music_obj(self, music: Music):
        UIDs = [None for i in range(5)]


        # 멜론
        search_get_url = 'https://www.melon.com/mymusic/common/mymusiccommon_searchListSong.htm?kwd='

        self.driver.get(search_get_url + music.name + ' ' + music.artist)
        try:
            # res = requests.get(search_get_url + music.name + ' ' + music.artist)
            # soup = BeautifulSoup(res.content, 'html.parser')
            # # print(soup.select_one('#DEFAULT0 > table > tbody > tr:nth-child(1)'))
            # UIDs[melon_code] = soup.select_one('#DEFAULT0 > table > tbody > tr:nth-child(1)').get('trackId')  # 검색결과 첫번째 음악의 고유아이디

            UIDs[melon_code] = self.driver.find_element_by_xpath('/html/body/div[1]/input').get_attribute('value') # 검색결과 첫번째 음악의 고유아이디
        except:
            print(f"not found {music}")

        # 지니
        search_get_url = 'https://www.genie.co.kr/search/searchMain?query='

        self.driver.get(search_get_url + music.name + ' ' + music.artist)
        try:
            UIDs[genie_code] = self.driver.find_element_by_xpath('//*[@id="body-content"]/div[3]/div[2]/div/table/tbody/tr[1]').get_attribute('songid')  # 검색결과 첫번째 음악의 고유아이디
        except:
            print(f"not found {music}")

        # 플로
        search_get_url = 'https://www.music-flo.com/api/search/v2/search?searchType=TRACK&sortType=ACCURACY&size=50&page=1&keyword='
      
        try:
            res = requests.get(search_get_url + music.name + ' ' + music.artist).json()
            UIDs[flo_code] = res['data']['list'][0]['list'][0]['id']  # 검색결과 첫번째 음악의 고유아이디
        except:
            print(f"not found {music}")

        # Vibe
        search_get_url = 'https://apis.naver.com/vibeWeb/musicapiweb/v3/search/track?start=1&display=100&sort=RELEVANCE&query='
        
        try:
            res = requests.get(search_get_url + music.name + ' ' + music.artist)
            tree = ElementTree.fromstring(res.content)
            UIDs[vibe_code] = tree.findall('result/tracks/track')[0].find('trackId').text  # 검색결과 첫번째 음악의 고유아이디
        except:
            print(f"not found {music}")
        
        # Bugs
        search_get_url = 'https://music.bugs.co.kr/search/track?q='
        
        res = requests.get(search_get_url + music.name + ' ' + music.artist)
        soup = BeautifulSoup(res.content, 'html.parser')
        # print(soup.select_one('#DEFAULT0 > table > tbody > tr:nth-child(1)'))
        print(soup.select('#DEFAULT0 > table > tbody > tr')[0].get('trackId'))
        a= UIDs[bugs_code] = soup.select('#DEFAULT0 > table > tbody > tr')[0].get('trackId')  # 검색결과 첫번째 음악의 고유아이디
        print(a)
        try:
            res = requests.get(search_get_url + music.name + ' ' + music.artist)
            soup = BeautifulSoup(res.content, 'html.parser')
            # print(soup.select_one('#DEFAULT0 > table > tbody > tr:nth-child(1)'))
            UIDs[bugs_code] = soup.select_one('#DEFAULT0 > table > tbody > tr:nth-child(1)').get('trackId')  # 검색결과 첫번째 음악의 고유아이디
        except:
            print(f"not found {music}")
        
        print(f'https://www.melon.com/song/detail.htm?songId={UIDs[melon_code]}')
        print(f'https://www.genie.co.kr/detail/songInfo?xgnm={UIDs[genie_code]}')
        print(UIDs[flo_code])
        print(f'https://vibe.naver.com/track/{UIDs[vibe_code]}')
        print(f'https://music.bugs.co.kr/track/{UIDs[bugs_code]}')

        print(UIDs)
        return UIDs




def input_no_blank(str: str):
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


# if __name__ == '__main__':

#     # # 피클 테스트
#     # data = load_from_pickle('test.plm')
#     # for playlist in data:
#     #     print(playlist)
#     #     print(playlist.contents_str())

#     # test_melon01_account = load_from_pickle('melon01.plmaccount')
#     test_melon02_account = load_from_pickle('melon02.plmaccount')
#     # test_genie01_account = load_from_pickle('genie01.plmaccount')
#     # test_flo01_account = load_from_pickle('flo01.plmaccount')
#     # test_vibe01_account = load_from_pickle('Naver01.plmaccount')

#     start()
#     login(test_melon02_account)
#     a = crawl(test_melon02_account)
#     print(a)
#     # login(test_flo01_account)
#     # login(test_vibe01_account)
#     # time.sleep(10)
#     # crawl(test_melon01_account)
#     # migrate(test_vibe01_account, data)
#     # print_service_list()
#     # login(test_melon01_account)
#     # crawled_data = crawl(test_melon01_account)
#     # save_as_pickle('test.plm', crawled_data)
#     # login(test_melon02_account)
#     # migrate(test_melon02_account, data)
