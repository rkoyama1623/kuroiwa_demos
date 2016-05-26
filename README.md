# kuroiwa_demos

[![Build Status](https://travis-ci.org/eisoku9618/kuroiwa_demos.svg?branch=master)](https://travis-ci.org/eisoku9618/kuroiwa_demos)

### 数式メモ
TeX関連は https://github.com/eisoku9618/report を``subtree add``した
- [KalmanFilter](https://github.com/eisoku9618/kuroiwa_demos/blob/master/tex/KalmanFilter/kf.pdf)

### PRMLメモ
- [PRMLを読んで学んだこと](https://github.com/eisoku9618/kuroiwa_demos/blob/master/PRML/README.md)

### Ubuntu iso をカスタマイズする方法
```
sudo apt-get install uck
```
してuckをインストールして，
```
uck-gui
```
で立ち上がるGUI通りに進めていけばOK．
という記事が散見されるけど，``gnome-terminal``のオプションが変わったみたいで，動かないので，GUIは使えないっぽい．

ので，
- https://github.com/tork-a/live-cd/blob/master/00-create-cd.sh
- https://peteris.rocks/blog/customize-ubuntu-desktop-live-cd-usb/
を参考にCUIで進めればOK．

```
wget http://releases.ubuntu.com/16.04/ubuntu-16.04-desktop-amd64.iso
sudo uck-remaster-clean
sudo uck-remaster-unpack-iso ubuntu-16.04-desktop-amd64.iso
sudo uck-remaster-unpack-rootfs
sudo uck-remaster-chroot-rootfs
```
とすると，``~/tmp``以下にいろいろ作りつつ，作ろうとしているUbuntuのコマンドラインに移行するので，
```
add-apt-repository universe
add-apt-repository multiverse
apt-get update
apt-get upgrade
apt-get install aptitude
cd /etc/kernel/postinst.d/
mv zz-update-grub zz-update-grub.bak
aptitude upgrade
mv zz-update-grub.bak zz-update-grub
```
でもろもろ最新にしてから（``/etc/kernel/postinst.d/zz-update-grub``の21行目がUbuntu14.04ではあったのに，Ubuntu16.04ではコメントアウトされていて，そのため文法エラーが出る気がするので，一旦退避させている）
```
aptitude install emacs htop indicator-multiload ipython ipython-notebook byobu ssh xsel git ntp libgnome2-bin texlive-lang-cjk texlive-xetex texlive-fonts-recommended latexmk ibus-mozc
aptitude install `check-language-support -l ja`
im-config -n ibus
```
で基本的なパッケージを入れて Keyboard input method system をIBusにして（デフォルトでIBusだけど一応念の為）
```
sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 0xB01FA116
aptitude update
aptitude install ros-kinetic-desktop-full
aptitude install python-wstool python-catkin-tools
```
でROSを入れて
```
rm /var/crash/*
```
でエラーを消しておく．

で，終わったら``exit``して，
```
sudo uck-remaster-pack-rootfs -c
sudo uck-remaster-pack-iso my-ubuntu-16.04-desktop-amd64.iso -h -g -d "My Live Ubuntu"
```

#### 未解決問題
解決したい順に並べると
- CapslockとCtrlを入れ替えるのはどうするのか？
   - rootだとdconfで設定できない？
- 日本語入力をするにはどうすれば？？
   - Live USBからinstallするときに日本語キーボードを選択する想定
      - これは選択するだろうから，上のisoを作る段階ではほっておいて良い（==isoを作る段階ではEnでも良い）
   - Text Entry にMozcを追加する必要があるが，これをisoを作る段階で実行する方法が分からない
   - 半角／全角ボタンで日本語と英語を切り替えるのをデフォルトにする方法が分からない
- ``zz-update-grub``の件はどこにパッチを送ればよいのかがLinux力足りていなくて分からない
- chromeも調べてはじめから入っているようにする
- indicator-multiloadをauto startする方法が分からない（これは調べていないだけかも）
- 右上の日付表示を自分好みにしたい
