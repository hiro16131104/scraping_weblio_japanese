from .base_page import BasePage
from model.value_object import Link
from bs4 import element


# Weblioカテゴリーページ（2ページ目）をスクレイピングするためのクラス
# サブカテゴリーごとのページURLを取得する
# BasePageクラスを継承
class CategoryPage(BasePage):
    def __init__(self, request_url: str) -> None:
        super().__init__(request_url)

    # 取得したHTMLソースを解析し、リンク（aタグ）のタイトルとURLを取得
    # 抽象クラスで定義したメソッドをオーバーライド（上書き）
    def get_urls_from_html_source(self) -> None:
        # タグの種類や属性からターゲットを指定し、抽出する
        div_elem: element.Tag = self.soup_html_source.find(
            "div", class_="mainBoxB"
        )

        # divの構造がやや異なっている場合は、属性を変えて再チャレンジ
        if not div_elem:
            div_elem = self.soup_html_source.find(
                "div", id="mainL"
            )

        ul_elems: element.ResultSet = div_elem.find_all("ul")

        # 初期化
        self.list_link = []

        # 取得した複数のulタグからaタグを取得し、その情報をインスタンス変数へ格納
        for ul_elem in ul_elems:
            a_elem: element.Tag = ul_elem.find("a")

            if not a_elem:
                continue

            self.list_link.append(
                Link(
                    title=self.get_title_from_a_elem(a_elem),
                    url=a_elem.attrs["href"]
                )
            )
