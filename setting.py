# mode (検出モード) 1:俳句 2:短歌
mode = 2
# precision (精度) 1:低 2:高
# 低　検出数:多,ノイズ:多、実行時間:高
# 高　検出数:少,ノイズ:少、実行時間:少
precision = 2
# 音素としてカウントしない文字
skip_letters = ['ャ','ュ','ョ']
# 検出対象とするファイル
search_file_name = "/Users/rickshinmi/Downloads/dogura_magura 3.txt"
# 検出結果を保存するファイル
save_file_name = "/Users/rickshinmi/Downloads/aozorabunko_text-master/cards/001095/files/results.txt"
# 句の頭に来るべきでない品詞
skip_text_type = ["助詞", "助動詞", "接尾辞", "補助記号"]
# 解析対象に含まない文字
skip_text = ["、", "キゴウ", "=", "・"]

#cat *.txt > data.txt 