import git
import os
from datetime import datetime, timedelta
import random

def git_commit_and_push(repo_path, commit_message, start_date, end_date, remote_name='origin'):
    try:
        # リポジトリのオープン
        repo = git.Repo(repo_path)

        # 現在のブランチ名を取得
        current_branch = repo.active_branch.name

        # 日付範囲内の各日付でランダムな回数コミット
        current_date = start_date
        while current_date <= end_date:
            # 1日1～10回の範囲でランダムな回数コミット
            commit_count = random.randint(1, 10)
            for _ in range(commit_count):
                # すべての変更をステージング
                repo.git.add(A=True)

                # コミット日時の設定
                commit_date_str = current_date.strftime('%Y-%m-%dT%H:%M:%S')

                # 環境変数を設定してコミット
                os.environ['GIT_COMMITTER_DATE'] = commit_date_str
                repo.index.commit(commit_message, author_date=commit_date_str)
                print(f"コミットが成功しました: {commit_date_str}")

            # 次の日付に進む
            current_date += timedelta(days=1)

        # 環境変数を元に戻す
        del os.environ['GIT_COMMITTER_DATE']

        # リモートリポジトリにプッシュ
        origin = repo.remote(name=remote_name)
        origin.push(refspec=f"{current_branch}:{current_branch}")
        print(f"{current_branch} ブランチにプッシュが成功しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        if 'GIT_COMMITTER_DATE' in os.environ:
            del os.environ['GIT_COMMITTER_DATE']

# 現在のリポジトリのパス
repo_path = os.getcwd()

# コミットメッセージ
commit_message = "自動コミットメッセージ"

# コミット日時の範囲設定
start_date = datetime(2024, 7, 1)  # 開始日付
end_date = datetime.now          # 今日の日付を終了日付に設定

# 関数の呼び出し
git_commit_and_push(repo_path, commit_message, start_date, end_date)
