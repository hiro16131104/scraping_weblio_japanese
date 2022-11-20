from .value_object import Category, SubCategory
from datetime import datetime
import csv
import os
import gc


# スクレイピングの結果をCSVファイルに書き込むためのクラス
class OutputCsv:
    # 全てのインスタンスで共有する変数（クラス変数）
    # CSVファイル（成果物）の保存先の絶対パスを格納するための変数
    file_path: str

    def __init__(
        self, category: Category, idx_sub_category: int = None
    ) -> None:

        self.category = category
        self.idx_sub_category = idx_sub_category
        # CSV出力用にオブジェクトから変換した配列を格納する変数
        self.list_output_record: list[list[str]]

    # CSV出力用のファイルパスを作成
    def set_file_path(self) -> None:
        # カレントディレクトリのパスにCSVファイルの名称を追記
        # (例)~/2022-11-16_修飾語.csv
        OutputCsv.file_path = (
            f"{os.getcwd()}"
            f"/{datetime.now().date().strftime('%Y-%m-%d')}"
            f"_{self.category.title}.csv"
        )

    # CSVファイルを作成
    def make_csv_file(self) -> None:
        # ファイルを新規作成し、ヘッダーを書き込む
        with open(OutputCsv.file_path, "w") as file:
            # 値はダブルクォーテーションで囲み、改行コードはLFを採用
            csv.writer(
                file,
                quoting=csv.QUOTE_ALL,
                lineterminator="\n"
            ).writerow(
                ["カテゴリ", "サブカテゴリ", "コンテンツ_名称", "コンテンツ_説明"]
            )

    # 'list'型に整形されたスクレイピング結果をCSVファイルに書き込む
    def write_csv_file(self) -> None:
        # 既存ファイルに追記
        with open(OutputCsv.file_path, "a")as file:
            # 値はダブルクォーテーションで囲み、改行コードはLFを採用
            csv.writer(
                file,
                quoting=csv.QUOTE_ALL,
                lineterminator="\n"
            ).writerows(
                self.list_output_record
            )

    # スクレイピング結果が格納されたオブジェクトを2次元配列（'list[list[str]]'型）に変換
    def convert_obj_to_list(self) -> None:
        # 変換前
        #   Category: {
        #     SubCategory: {
        #       Content: {
        #         title: "名称",
        #         explanation: "説明"
        #       },
        #       Content: {
        #         title: "名称",
        #         explanation: "説明"
        #       }
        #     }
        #   }
        # 変換後
        #   [
        #     [Category, SubCategory, Content.title, Content.explanation],
        #     [Category, SubCategory, Content.title, Content.explanation]
        #   ]
        sub_category: SubCategory = (
            self.category.list_sub_category[self.idx_sub_category]
        )
        content_count = len(sub_category.list_content)
        # 初期化
        self.list_output_record = []

        for i in range(content_count):
            record: list[str] = []
            record.append(self.category.title)
            record.append(sub_category.title)
            record.append(sub_category.list_content[i].title)
            record.append(sub_category.list_content[i].explanation)
            self.list_output_record.append(record)

    # CSVに書き出したオブジェクトを削除し、メモリを解放
    def drop_list_content(self) -> None:
        # オブジェクト削除
        del self.category.list_sub_category[self.idx_sub_category].list_content
        # メモリ解放
        gc.collect()
