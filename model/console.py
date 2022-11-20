# CUI（ターミナル）からの入出力を制御するためのクラス
# '@classmethod'を付けている場合は、インスタンス化せずに使用可
class Console:
    # CUIから入力された値が、有効な値（想定された値）であるか検証する
    @classmethod
    def input_answer(
        cls, msg: str, list_option: list[str],
        is_upper: bool = False, is_lower: bool = False
    ) -> str:

        # バリデーション
        if is_upper and is_lower:
            raise Exception(
                "引数'is_upper'又は'is_lower'の値が不正です。\n"
                "どちらかは'False'に設定してください。"
            )

        # 有効な値が入力されるまでループ
        while True:
            answer = input(msg)

            if is_upper:
                answer = answer.upper()
            elif is_lower:
                answer = answer.lower()

            # 想定された選択肢と一致する場合、その入力値を返却
            if answer in list_option:
                return answer

            print(
                "無効な値が入力されました。\n"
                f"入力できる値は[{','.join(list_option)}]です。"
            )

    # 第2引数（list）の各要素の先頭に番号を付した上で一覧表示
    @classmethod
    def print_ordered_list(cls, list: list[str]) -> None:
        idx = 0

        for item in list:
            print(f"{idx}: {item}")
            idx += 1
