import re
import importlib
from sudachipy import tokenizer
from sudachipy import dictionary

setting = importlib.import_module('setting')
tokenizer_obj = dictionary.Dictionary().create()
#分割単位を最長に設定
split_mode = tokenizer.Tokenizer.SplitMode.C
#読み込むテキストファイルのパス
searchfile_path =  setting.search_file_name
#書き出すテキストファイルのパス
savefile_path =  setting.save_file_name
#俳句、短歌のモード切替
if setting.mode == 1:
    break_points = [5, 12, 17]
else:
    break_points = [5, 12, 17, 24, 31]
#カタカナの正規表現
re_katakana = re.compile(r'[\u30A1-\u30F4]+')


nekochan = searchfile_path
with open(nekochan, 'r', encoding='cp932') as f:
    nekochan2 = f.read()
# ファイル整形
import re
# | の除去
nekochan2 = nekochan2.replace('|', '')
# ルビの削除
nekochan2 = re.sub('《.+?》', '', nekochan2)
# 入力注の削除
nekochan2 = re.sub('［＃.+?］', '',nekochan2)
nekochan2 = nekochan2.replace('　', '')

with open(nekochan, mode="w", encoding="cp932") as f:
    f.write(nekochan2)




#テキストファイルオープン
with open(searchfile_path, encoding="cp932") as f:
    #全行読み込んでリスト化
    areas = f.readlines()
    for line in areas:
        # "。" または "." または改行で区切る
        sentences = re.split('[.。\n]', line)
        for sentence in sentences:
            # 文章単位で検索する場合はスルー
            if setting.precision == 1:
                pass
            # 短歌、俳句、それぞれの文字数以上の文章は検出対象としない
            else:
                if len(sentence) > break_points[-1]:
                    continue

            # 形態素解析
            m = tokenizer_obj.tokenize(sentence, split_mode)
            # MorphemeListをListにキャスト
            m = list(m)

            retry = True
            while retry:
                break_point_header_flag = True
                retry = False
                counter = 0
                break_point_index = 0
                reading = ""
                surface = ""
                # それぞれの句の区切りで文章が切れているか判別
                for mm in m:
                    if break_point_header_flag == True:
                        text_type = mm.part_of_speech()[0]
                        #　それぞれの句の頭が適切な品詞でない場合は検出対象としない
                        if text_type in setting.skip_text_type:
                            # 長文捜査onの場合はもう一度検索
                            if setting.precision == 1:
                                retry = True
                                del m[0]
                                break
                            else:
                                counter = 0
                                break
                        else:
                            break_point_header_flag = False
                    # 読みを解析
                    reading_text = mm.reading_form()
                    surface_text = mm.surface()
                    if len(reading_text) > 7:
                        # 長文捜査onの場合はもう一度検索
                        if setting.precision == 1:
                            retry = True
                            del m[0]
                            break
                        else:
                            counter = 0
                            break
                    # 解析結果がスキップすべき文字の場合は飛ばす
                    if reading_text in setting.skip_text:
                        sentence = sentence.replace(mm.surface(), "")
                        continue
                    # カタカナの人名が入ってこないので、surfaceで補完する
                    if reading_text == "":
                        text_surface = mm.surface()
                        if re_katakana.fullmatch(text_surface):
                            reading_text = text_surface
                        # 辞書で読めない漢字が出現したらスキップ
                        else:
                            # 長文捜査onの場合はもう一度検索
                            if setting.precision == 1:
                                retry = True
                                del m[0]
                                break
                            else:
                                counter = 0
                                break
                    # 読みの音素数をカウント
                    counter += len(reading_text)
                    reading = reading + reading_text
                    surface = surface + surface_text
                    # カウントしない相性の音素があればカウントをマイナス
                    for letter in setting.skip_letters:
                        if letter in reading_text:
                            counter -= reading_text.count(letter)
                    # それぞれの句の文字数分カウントが進んだか。
                    if counter == break_points[break_point_index]:
                        break_point_header_flag = True
                        # 最後まで来ていなければ次の句へ
                        if counter != break_points[-1]:
                            break_point_index += 1
                            reading = reading + " "
                    # それぞれの句の指定文字数を超えてしまったら弾く。
                    elif counter > break_points[break_point_index]:
                        # 長文捜査onの場合はもう一度検索
                        if setting.precision == 1:
                            retry = True
                            del m[0]
                            break
                        else:
                            counter = 0
                            break

                # 指定文字数ぴったりで検出できたものをピックアップしてファイルに追記
                if counter == break_points[-1]:
                    with open(savefile_path, "a") as f:
                        try:
                            print(surface + " ")
                            print("(" + reading + ")" + "\n")
                            f.write(surface  + "\n")
                            f.write("(" + reading + ")" + "\n")
                            f.write("\n")
                        except Exception as e:
                            print(e)

                if len(m) < len(break_points):
                    break
