from .base_page import BasePage
from model.value_object import Link
from bs4 import element


# Weblioサブカテゴリーページ（3ページ目）をスクレイピングするためのクラス
# コンテンツごとのページURLを取得する
# BasePageクラスを継承
class SubCategoryPage(BasePage):
    def __init__(self, request_url: str) -> None:
        super().__init__(request_url)

    # 取得したHTMLソースを解析し、リンク（aタグ）のタイトルとURLを取得
    # 抽象クラスで定義したメソッドをオーバーライド（上書き）
    def get_urls_from_html_source(self) -> None:
        # タグの種類や属性からターゲットを指定し、抽出する
        div_elem_box: element.Tag = self.soup_html_source.find(
            "div", class_="mainBoxB"
        )

        # divの構造がやや異なっている場合は、属性を変えて再チャレンジ
        if not div_elem_box:
            div_elem_box = self.soup_html_source.find(
                "div", id="mainL"
            )

        div_elems_word: element.ResultSet = div_elem_box.find_all(
            "div", class_="subCatWordsL"
        )

        if not div_elems_word:
            div_elems_word = div_elem_box.find_all(
                "div", class_="subCatWords"
            )

        # 初期化
        self.list_link = []

        # 取得した複数のdivタグからaタグを取得し、その情報をインスタンス変数へ格納
        for div_elem in div_elems_word:
            a_elems: element.ResultSet = div_elem.find_all("a")

            for a_elem in a_elems:
                self.list_link.append(
                    Link(
                        title=self.get_title_from_a_elem(a_elem),
                        url=a_elem.attrs["href"]
                    )
                )
