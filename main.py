from model.scraping.top_page import TopPage
from model.scraping.category_page import CategoryPage
from model.scraping.sub_category_page import SubCategoryPage
from model.scraping.content_page import ContentPage
from model.console import Console
from model.scraping_result import ScrapingResult
from model.output_csv import OutputCsv
from model.progress_bar import ProgressBar
from model.utility import Utility


# ターミナル（コンソール）からこのファイルを実行する。
# 各クラスを呼び出して、実際に処理を行うファイル

# 変数宣言
idx_category: int
idx_sub_category: int
idx_content: int
category_page: CategoryPage
scraping_result: ScrapingResult
output_csv: OutputCsv
outputed_count: int
progress_bar: ProgressBar

print("Weblio国語辞典(https://www.weblio.jp)からスクレイピングを行います。")

# トップページをスクレイピングし、検索するカテゴリーのページURLを取得する
while True:
    # 変数宣言
    top_page: TopPage
    result_count = 0
    input_val = ""
    list_idx: list[str] = []
    list_url: list[str] = []

    print("トップページ「ことばを探す」の中から、カテゴリーを1つ選択し、入力してください。")

    # ①検索するキーワードを設定
    # ②トップページのHTMLソースを取得
    # ③取得したHTMLソースからリンク情報（URL等）をスクレイピング
    # ④想定しているHTMLの構造と異なるページについては、スクレイピング結果から排除
    # ⑤キーワードとタイトルが一致するリンクを抽出
    top_page = TopPage(keyword=input("カテゴリー: "))
    top_page.get_html_source_from_page()
    top_page.get_urls_from_html_source()
    top_page.remove_irregular_link()
    top_page.search_title_from_list_link()

    # 検索結果
    result_count = len(top_page.list_link)
    print(f"{result_count}件見つかりました。")

    # 検索結果が0件の場合、初めからやり直し。
    # 検索結果が1件の場合、ユーザーにURLの確認を行った後、処理を抜ける。
    # 検索結果が2件以上の場合、ユーザーに使用するURLを選択させた後、処理を抜ける。
    match result_count:
        case 0:
            print("再度カテゴリーを入力してください。")
            continue
        case 1:
            print("スクレイピングの対象とするページは\n"
                  f"{top_page.list_link[0].url}\n"
                  "でよろしいですか？")
            input_val = Console.input_answer(
                "Y/N: ", ["Y", "N"], is_upper=True
            )

            if input_val == "Y":
                idx_category = 0
            else:
                print("再度カテゴリーを入力してください。")
                continue
        case _:
            # list内の要素を変換し、別の変数に代入
            list_idx = list(map(lambda x: str(x), range(result_count)))
            list_url = list(map(lambda x: x.url, top_page.list_link))
            print(
                "該当するカテゴリーが複数あります。\n"
                "スクレイピングの対象とするページを選択してください。"
            )
            # URLを列挙し、使用する要素の番号を入力させる。
            Console.print_ordered_list(list_url)
            idx_category = int(
                Console.input_answer(f"0~{list_idx[-1]}: ", list_idx)
            )

    # エラー等で、前回処理を中断してしまっている場合、続きから実行することができる
    # 便宜上、「処理再開モード」と呼称
    print(
        "前回、処理を中断している場合は、続きから実行することができます。"
        "該当しますか？"
    )
    input_val = Console.input_answer(
        "Y/N: ", ["Y", "N"], is_upper=True
    )

    # CSVファイルの行数入力（ヘッダー込みの総数）
    if input_val == "Y":
        print("出力されたCSVファイルの行数を入力してください。")
        list_idx = list(map(lambda x: str(x), range(2, 1000000)))
        outputed_count = int(
            Console.input_answer("2〜: ", list_idx)
        )
        break
    else:
        outputed_count = 0
        break

# トップページのスクレイピング結果（カテゴリー情報）をオブジェクトに保存
scraping_result = ScrapingResult()
scraping_result.set_category(top_page, idx_category)

# 直前に保存したカテゴリー情報（URL等）を利用してカテゴリーページをスクレイピング
# サブカテゴリーページのURL等を取得する
print(Utility.get_str_datetime_now())
print("カテゴリーページのスクレイピングを実行します。", end="")
category_page = CategoryPage(scraping_result.category.url)
category_page.get_html_source_from_page()
category_page.get_urls_from_html_source()
# カテゴリーページのスクレイピング結果（サブカテゴリーページのURL等）をオブジェクトに保存
scraping_result.set_sub_category(category_page)
print(" 完了")

# プログレスバー（進捗ゲージ）を作成
progress_bar = ProgressBar(
    total_task_num=scraping_result.sub_category_count
)
progress_bar.calc_unit_task_num()
print("サブカテゴリーページのスクレイピングを実行します。")
# プログレスバーの初回表示（枠だけ表示）
print(progress_bar.get_progress_bar(init=True), end="")

idx_content = 0

# 直前に保存したサブカテゴリー情報（URL等）を利用してサブカテゴリーページをスクレイピング
# コンテンツページのURL等を取得する
for sub_category in scraping_result.category.list_sub_category:
    sub_category_page = SubCategoryPage(sub_category.url)
    sub_category_page.get_html_source_from_page()
    sub_category_page.get_urls_from_html_source()
    # サブカテゴリーページのスクレイピング結果（コンテンツページのURL等）をオブジェクトに保存
    scraping_result.set_content(sub_category_page, idx_content)

    # プログレスバーを進める（表示を更新）
    print(progress_bar.get_progress_bar(), end="")
    idx_content += 1

# スクレイピング結果を出力するCSVファイルのパスを作成
output_csv = OutputCsv(scraping_result.category)
output_csv.set_file_path()

# CSVファイルを作成
# 既に同名のファイルがある場合は、上書きするか確認
# 処理再開モードの場合は、スキップ
if outputed_count == 0:
    is_file = Utility.check_file_exist(output_csv.file_path)
    input_val = ""
    if is_file:
        print(
            "\n出力先に同じ名前のファイルが存在します。"
            "上書きしてよろしいですか？"
        )
        input_val = Console.input_answer(
            "Y/N: ", ["Y", "N"], is_upper=True
        )
    else:
        output_csv.make_csv_file()
    if input_val == "Y":
        output_csv.make_csv_file()
    elif input_val == "N":
        print("処理を中断します。")
        exit()

# 新しいプログレスバーを作成
progress_bar = ProgressBar(scraping_result.content_count)
progress_bar.calc_unit_task_num()
print("\nコンテンツページのスクレイピングを実行します。")
# プログレスバーの初回表示（枠だけ表示）
print(progress_bar.get_progress_bar(init=True), end="")

idx_sub_category = 0
idx_content = 0
idx_total = 0

# ①直前に保存したコンテンツ情報（URL等）を利用してコンテンツページをスクレイピング
# ②コンテンツページの説明文（解説）を取得
# ③スクレイピング結果を格納したオブジェクトを2次元配列に変換
# ④CSVファイルに書き出し
for sub_category in scraping_result.category.list_sub_category:
    # 処理再開モードの場合、出力済みのページはスキップ
    is_skip = outputed_count != 0 and idx_total < outputed_count - 2

    for content in sub_category.list_content:
        if is_skip:
            print(progress_bar.get_progress_bar(), end="")
            idx_content += 1
            idx_total += 1
            continue

        content_page = ContentPage(content.url)

        try:
            content_page.get_html_source_from_page()
            content_page.get_explanation_from_html_source()
        except Exception as ex:
            # サーバーエラーが発生した場合、このコンテンツページは処理をスキップ
            # 500エラー（メンテナンス中）、503エラー
            if Utility.check_contain_word_from_err_msg(
                ex, ["Exception: 500", "Exception: 503"]
            ):
                content_page.list_explanation = [""]
            else:
                raise

        # ページから取得したテキストを改行コード（\n）で結合し、インスタンス変数へ記録
        (scraping_result.category
         .list_sub_category[idx_sub_category]
         .list_content[idx_content].explanation) = (
            " ".join(content_page.list_explanation)
        )

        # プログレスバーを進める（表示を更新）
        print(progress_bar.get_progress_bar(), end="")
        idx_content += 1
        idx_total += 1

    if is_skip:
        idx_content = 0
        idx_sub_category += 1
        continue

    # オブジェクト⇒2次元配列⇒CSV
    output_csv = OutputCsv(scraping_result.category, idx_sub_category)
    output_csv.convert_obj_to_list()
    output_csv.drop_list_content()
    output_csv.write_csv_file()

    idx_content = 0
    idx_sub_category += 1

# 処理完了
print(f"\n{Utility.get_str_datetime_now()}")
print("全ての処理が完了しました。")
