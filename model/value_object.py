# 値を格納するためのオブジェクト（クラス）を集約したファイル

# aタグの名称とURLを格納するためのクラス
class Link:
    def __init__(self, title: str, url: str) -> None:
        self.title = title
        self.url = url


# スクレイピングで取得したカテゴリー情報を格納するためのクラス
class Category(Link):
    def __init__(self, title: str, url: str) -> None:
        super().__init__(title, url)
        self.list_sub_category: list[SubCategory] = []


# スクレイピングで取得したサブカテゴリー情報を格納するためのクラス
class SubCategory(Link):
    def __init__(self, title: str, url: str) -> None:
        super().__init__(title, url)
        self.list_content: list[Content] = []


# スクレイピングで取得したコンテンツ情報を格納するためのクラス
class Content(Link):
    def __init__(self, title: str, url: str) -> None:
        super().__init__(title, url)
        self.explanation = ""
