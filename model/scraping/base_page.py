from model.value_object import Link
from bs4 import BeautifulSoup, element
from abc import ABC, abstractmethod
from time import sleep
from requests.exceptions import HTTPError, SSLError
import requests


# サブクラスで共通して使用するインスタンス変数やメソッドを定義
# 抽象クラスであるため、クラス継承して使用する
class BasePage(ABC):
    # 全てのインスタンスで共有する変数（クラス変数）
    # 送信したリクエストの回数を記録するための変数
    __request_count = 0
    # 一気に送信するリクエストの回数
    __UNIT_REQUEST_COUNT = 1
    # リクエストの休止時間
    __SLEEP_SECONDS = 0.2
    # 503エラー（サーバーエラー）が発生した場合に再チャレンジできる回数
    __MAX_RETRY_COUNT = 3

    def __init__(self, request_url: str) -> None:
        # スクレイピングの対象とするページのURL
        self.request_url = request_url
        # スクレイピングをする際にHTMLソースを格納する変数
        self.soup_html_source: BeautifulSoup
        # スクレイピング結果を格納したオブジェクト（タイトル、URL）のリスト
        self.list_link: list[Link]
        # 503エラー（サーバーエラー）が発生した場合に再チャレンジした回数
        self.retry_count = 0

    # WEBページからHTMLソースを取得
    def get_html_source_from_page(self) -> None:

        # Weblioは、短時間に大量のリクエストを送信するとBANされる（403エラー）。
        # BANされた場合、10分間アクセスできない（SSLエラー）。
        if BasePage.__request_count == BasePage.__UNIT_REQUEST_COUNT:
            # x回リクエストを行う度、y秒間のインターバルを置く。
            sleep(BasePage.__SLEEP_SECONDS)
            # リクエスト回数の記録をリセット
            BasePage.__request_count = 0

        status_code = 0
        REQUEST_ERR_MSG = (
            "Weblioへのリクエスト回数が上限を超えています。"
            "10分以上時間をおいてから、再度実行してください。"
        )

        try:
            # WeblioのトップページからHTMLソースを取得
            response = requests.get(self.request_url)
            # リクエスト回数を記録
            BasePage.__request_count += 1
            # HTTPステータスコードが200番台以外の場合は、例外を発生
            status_code = response.status_code
            response.raise_for_status()
            # 取得したHTMLソースをインスタンス変数へ格納
            # 'lxml'パッケージはpipコマンドでインストールする必要あり
            self.soup_html_source = BeautifulSoup(
                response.content,
                features="lxml"
            )
        except HTTPError:
            # 何らかの理由でリクエスト回数の上限を超えてしまった場合
            match status_code:
                case 403:
                    raise Exception(REQUEST_ERR_MSG)
                case 500:
                    # 対象ページがメンテナンス中の場合
                    raise Exception(status_code)
                case 503:
                    # 503エラー（サーバーエラー）の場合は、設定した回数まで再チャレンジ
                    if self.retry_count <= self.__MAX_RETRY_COUNT:
                        self.retry_count += 1
                        self.get_html_source_from_page()
                    else:
                        raise Exception(status_code)
                case _:
                    raise
        except SSLError:
            # 何らかの理由でリクエスト回数の上限を超えてしまった場合
            raise Exception(REQUEST_ERR_MSG)
        except Exception:
            # メソッドの呼び出し元へエラーを再スロー
            raise

    # 取得したHTMLソースを解析し、リンクのタイトルとURLを取得
    # 全てのサブクラスにて使用する共通メソッドであるが、その処理内容が異なる。
    # そのため、ここではメソッド名のみ定義する。
    @abstractmethod
    def get_urls_from_html_source(self) -> None:
        pass

    # aタグから'title'属性の文字列を取得
    def get_title_from_a_elem(self, a_elem: element.Tag) -> str:
        # 'title'属性のないaタグであった場合、aタグで囲われている'text'で代用
        return (
            a_elem.attrs["title"] if "title" in a_elem.attrs else a_elem.text
        )
