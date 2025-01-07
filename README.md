# Saica (彩華)

[miiton](https://github.com/miiton) 氏作成の [Cica](https://github.com/miiton/Cica) をベースに改良を施したフォントとなります。

## 特徴

- Cica の特徴を継承し、一部変更を加えたフォントとなっています
- 以下の変更を加えています:
    - Powerline フォントの位置ずれが起きる問題を修正
    - Nerd Fonts をアップデートし一部アイコンの追加/削除
        - \+ [Weather](https://github.com/erikflowers/weather-icons)
        - \+ [DevIcon](https://github.com/devicons/devicon)
        - \+ [Font Logos](https://github.com/Lukas-W/font-logos)
        - \+ [Material Design Icons](https://github.com/Templarian/MaterialDesign)
        - \+ [Codicons](https://github.com/microsoft/vscode-codicons)
        - \+ [Pomicons](https://github.com/gabrielelana/pomicons) (ライセンスが OFL になったため)
        - \- [DevIcons](https://github.com/vorillaz/devicons)
        - \- [Icons for Devs](https://github.com/mirmat/iconsfordevs)

依存関係:
```
o Saica
|
o Cica
|\
* * Nerd Fonts
|\
* * Noto Emoji
|\
* * DejaVu Sans Mono
|\
* * Hack
 \
  * Rounded Mgen+
  |\
  | * 源の角ゴシック
  |
  * Rounded M+
  |
  * M+ OUTLINE FONTS
```

- ※アイコン類はフォントをインストール後 [https:\/\/miiton.github.io\/Cica\/](https://miiton.github.io/Cica/) で確認出来ます。

## ビルド手順

### Dockerを使う場合

```sh
git clone https://github.com/KashEight/Saica
cd Saica
docker-compose build ; docker-compose run --rm cica  # ./dist/ に出力される
```

### 手動でやる場合

2018-08-27時点、Ubuntu 16.04 にて

```sh
sudo apt-get update
sudo apt-get -y install apt-file
sudo apt-file update
sudo apt-file search add-apt-repository
sudo apt-get -y install software-properties-common
sudo apt-get -y install fontforge unar
git clone git@github.com:KashEight/Saica
cd Cica
curl -L https://github.com/source-foundry/Hack/releases/download/v3.003/Hack-v3.003-ttf.zip -o hack.zip
unar hack.zip
cp ttf/* sourceFonts/
rm hack.zip
rm -r ttf
curl -LO https://osdn.jp/downloads/users/8/8598/rounded-mgenplus-20150602.7z
unar rounded-mgenplus-20150602.7z
cp rounded-mgenplus-20150602/rounded-mgenplus-1m-regular.ttf ./sourceFonts
cp rounded-mgenplus-20150602/rounded-mgenplus-1m-bold.ttf ./sourceFonts
curl -L https://github.com/googlefonts/noto-emoji/raw/main/fonts/NotoEmoji-Regular.ttf -o sourceFonts/NotoEmoji-Regular.ttf
curl -LO http://sourceforge.net/projects/dejavu/files/dejavu/2.37/dejavu-fonts-ttf-2.37.zip
unar dejavu-fonts-ttf-2.37.zip
mv dejavu-fonts-ttf-2.37/ttf/DejaVuSansMono.ttf ./sourceFonts/
mv dejavu-fonts-ttf-2.37/ttf/DejaVuSansMono-Bold.ttf ./sourceFonts/
curl -L https://github.com/mirmat/iconsfordevs/raw/master/fonts/iconsfordevs.ttf -o sourceFonts/iconsfordevs.ttf
fontforge -lang=py -script cica.py
```

## ライセンス

- フォント: SIL Open Font License 1.1
- ソースコード: MIT

## 謝辞

Cicaフォントの合成にあたり素晴らしいフォントを提供してくださっている製作者の方々に感謝いたします。

- Hack : [Hack \| A typeface designed for source code](https://sourcefoundry.org/hack/)
- Rounded Mgen+ : [自家製フォント工房](http://jikasei.me/)
- M+ OUTLINE FONTS : [M\+ FONTS](https://mplus-fonts.osdn.jp/)
- Rounded M+ : [自家製フォント工房](http://jikasei.me/)
- 源の角ゴシック : [adobe\-fonts/source\-han\-sans: Source Han Sans \| 思源黑体 \| 思源黑體 \| 源ノ角ゴシック \| 본고딕](https://github.com/adobe-fonts/source-han-sans)
- Noto Emoji : [googlei18n/noto\-emoji: Noto Emoji fonts](https://github.com/googlei18n/noto-emoji)
- Nerd Fonts (without Pomicons) : [Nerd Fonts \- Iconic font aggregator, collection, and patcher](https://nerdfonts.com/)
- DejaVu Sans Mono : [DejaVu Fonts](https://dejavu-fonts.github.io/)
