from .base_page import BasePage
from bs4 import element


# Weblioコンテンツページ（4ページ目）をスクレイピングするためのクラス
# コンテンツの説明文を取得する
# BasePageクラスを継承
class ContentPage(BasePage):
    def __init__(self, request_url: str) -> None:
        super().__init__(request_url)
        self.list_explanation: list[str]

    # 取得したHTMLソースを解析し、リンク（aタグ）のタイトルとURLを取得
    # 抽象クラスで定義したメソッドをオーバーライド（上書き）
    def get_explanation_from_html_source(self) -> None:
        div_elems: element.ResultSet = self.soup_html_source.find_all(
            "div", class_="kijiWrp"
        )
        # 初期化
        self.list_explanation = []

        for div_elem in div_elems:
            self.list_explanation.append(div_elem.get_text())

    # 抽象クラスで定義したメソッドをオーバーライド（上書き）
    # コンテンツページではこのメソッドは使用しない
    def get_urls_from_html_source(self) -> None:
        pass
