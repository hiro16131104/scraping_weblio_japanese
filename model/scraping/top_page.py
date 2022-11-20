from .base_page import BasePage
from model.value_object import Link
from bs4 import element


# Weblioトップページ（1ページ目）をスクレイピングするためのクラス
# カテゴリーごとのページURLを取得する
# BasePageクラスを継承
class TopPage(BasePage):

    def __init__(self, keyword: str) -> None:
        super().__init__("https://www.weblio.jp/")
        # 検索するキーワード
        self.keyword = keyword

    # 取得したHTMLソースを解析し、リンク（aタグ）のタイトルとURLを取得
    # 抽象クラスで定義したメソッドをオーバーライド（上書き）
    def get_urls_from_html_source(self) -> None:
        # タグの種類や属性からターゲットを指定し、抽出する
        div_elem_tab: element.Tag = self.soup_html_source.find(
            "div", id="js-tab-pc"
        )
        div_elem_box: element.Tag = div_elem_tab.find(
            "div", class_="list-tab-box"
        )
        a_elems: element.ResultSet = div_elem_box.find_all(
            "a", class_="character"
        )
        # 初期化
        self.list_link = []

        # 取得したaタグの情報をインスタンス変数へ追加
        for a_elem in a_elems:
            self.list_link.append(
                Link(
                    title=a_elem.text,
                    url=a_elem.attrs["href"]
                )
            )

    # 想定しているHTMLの構造と異なるWebページについては、スクレイピング結果から排除する
    def remove_irregular_link(self) -> None:
        link_count = len(self.list_link)

        # 要素番号の繰り上がりを防ぐため、後ろから該当要素を削除していく
        for i in reversed(range(link_count)):
            title = self.list_link[i].title
            url = self.list_link[i].url

            if (
                url.find("https://www.weblio.jp/cat/") == -1 and
                url.find("https://www.weblio.jp/category/") == -1 and
                title != "すべて"
            ):
                continue

            self.list_link.pop(i)

    # タイトルがキーワードと一致するリンクを抽出
    def search_title_from_list_link(self) -> None:
        self.list_link = list(
            filter(lambda link: link.title == self.keyword, self.list_link)
        )
