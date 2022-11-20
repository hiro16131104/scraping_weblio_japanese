from model.value_object import Category, SubCategory, Content
from .scraping.top_page import TopPage
from .scraping.category_page import CategoryPage
from .scraping.sub_category_page import SubCategoryPage


# スクレイピングの結果を格納するためのクラス
class ScrapingResult:
    # 全てのインスタンスで共有する変数（クラス変数）
    # コンテンツページの数を記録するための変数
    content_count = 0
    # サブカテゴリーページの数を記録するための変数
    sub_category_count = 0

    def __init__(self) -> None:
        # インスタンス変数'category'の構造
        # ・Category(title,url)
        # 　・SubCategory(title,url)
        # 　　・Content(title,url,reading)
        # 　　・Content
        # 　・SubCategory
        # 　（以下略）
        self.category: Category

    # トップページのスクレイピング結果からカテゴリー情報を取得し、インスタンス変数に格納
    def set_category(self, top_page: TopPage, idx: int):
        self.category = Category(
            title=top_page.list_link[idx].title,
            url=top_page.list_link[idx].url
        )

    # カテゴリーページのスクレイピング結果からサブカテゴリー情報を取得し、インスタンス変数に格納
    def set_sub_category(self, category_page: CategoryPage):
        for link in category_page.list_link:
            self.category.list_sub_category.append(
                SubCategory(
                    title=link.title,
                    url=link.url
                )
            )
            # サブカテゴリーページの数を加算
            ScrapingResult.sub_category_count += 1

    # サブカテゴリーページのスクレイピング結果からコンテンツ情報を取得し、インスタンス変数に格納
    def set_content(self, sub_category_page: SubCategoryPage, idx: int):
        for link in sub_category_page.list_link:
            self.category.list_sub_category[idx].list_content.append(
                Content(
                    title=link.title,
                    url=link.url
                )
            )
            # コンテンツページの数を加算
            ScrapingResult.content_count += 1
