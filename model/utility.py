from datetime import datetime
import os
import traceback


# インスタンス化せずに使える、汎用的なメソッドを集約したクラス
class Utility:
    # 現在日時を文字列として取得
    # (例)2022/11/18 20:00:00
    @classmethod
    def get_str_datetime_now(cls) -> str:
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # 指定したパスににファイルが存在するか確認（存在する場合、True）
    @classmethod
    def check_file_exist(cls, file_path: str) -> bool:
        return os.path.isfile(file_path)

    # エラーメッセージに指定したワードが含まれているか確認（含まれている場合、True）
    @classmethod
    def check_contain_word_from_err_msg(
        cls, ex: Exception, list_words: list[str]
    ) -> bool:

        # Exceptionクラスのインスタンスから、エラーメッセージの最終行を抽出
        list_err_msg = traceback.format_exception_only(type(ex), ex)
        # 改行コード削除
        err_msg = list_err_msg[0].rstrip("\n")

        for word in list_words:
            if word in err_msg:
                return True

        return False
