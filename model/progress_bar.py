import math


# プログレスバー（進捗ゲージ）を作成するためのクラス
class ProgressBar:
    # 全てのインスタンスで共有する変数（クラス変数）
    # 表示するプログレスバーの最大ブロック数
    __MAX_BAR_COUNT = 50

    def __init__(self, total_task_num: int) -> None:
        # 現在完了しているタスク数
        self.current_task_num = 0
        # タスクの総数
        self.total_task_num = total_task_num
        # プログレスバー1ブロックあたりのタスク数
        self.unit_task_num = 0.0

    # プログレスバー1ブロックあたりのタスク数を計算
    def calc_unit_task_num(self) -> None:
        # タスクの総数 ÷ プログレスバーの最大ブロック数
        self.unit_task_num = self.total_task_num / ProgressBar.__MAX_BAR_COUNT

    # コンソールに表示するためのプログレスバーを取得
    def get_progress_bar(self, init: bool = False) -> str:
        current_bar_count = 0
        bar = ""
        rate = 0.0

        # 2回目以降は、完了タスク数を1増加
        if not init:
            self.current_task_num += 1

        # プログレスバーの進捗
        # 完了タスク数 ÷ 1ブロックあたりのタスク数
        current_bar_count = math.floor(
            self.current_task_num / self.unit_task_num)
        # プログレスバーを作成
        bar = (
            "\r\033[K["
            f"{'■' * current_bar_count}"
            f"{'□' * (ProgressBar.__MAX_BAR_COUNT - current_bar_count)}"
            "] "
        )
        # 進捗割合（%）を計算
        rate = self.current_task_num / self.total_task_num * 100
        # プログレスバーと進捗割合を返却
        return (
            f"{bar} {rate:.02f}% "
            f"({self.current_task_num}/{self.total_task_num})"
        )
