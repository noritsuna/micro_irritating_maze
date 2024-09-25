# 世界最小電撃イライラ棒(英語名：Micro Irritating Maze)
半導体チップの上に電極パッドを利用して描いたイライラコース。タングステン針によるイライラ棒でイライラコースを駆け抜けろ！  
イライラコースの幅は直線の300umと100umと複雑な100umの3コースで、イライラ棒（タングステン針）は5um。人類の限界を超えろ！！！  

![Title](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/title.png)
![Layout](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/klayout_fix.jpg)


## 目的
今回の作品は、「半導体」をメインに使った作品である。そのため、多くの人は作者が半導体業界の人だと考えているのではないだろうか？  
実は、作者は、普段は無線機エンジニアで各種無線機などのPCB基板の設計をしており、この時、初めて半導体の製造（テープアウトという）を行ったのである！  
  
なぜ、このような挑戦を行ったかと言えば、「Make:のオープンハードウェア」の流れを半導体でも起こすためである。  
昔の家電メーカーしかPCB基板作れなかった時代に、今のMake:でよく作られているようなLチカをするだけのようなPCB基板の製造は許されなかった。しかし、Make:の世界が現出したことで、PCB基板が民主化し、どのようなPCB基板でも作成できる世界がやってきた。それが半導体の世界にもやってきたことを示すために半導体の民主化の象徴としてこの作品を作製した。  
さらにこの流れが進めば、近いうちに半導体と全くかかわりがない企業が半導体を絡めた事業を展開するのではないかと考えている。
Make:時代に立ち上がった企業も、ハードウェアとは無縁のソフトウェア企業などの中から「社内Make:開発部」みたいなのが立ち上がり、そこから派生したわけである。そして、その人たちが「どこで知識を身に着けてきたか？」を考えるとMake:の流れの中にあるオープンハードウェアからなわけで、ここで「ある程度まとまった数の技術者が生まれた」から、ハードウェアを絡めた事業がどこの会社でも出来るようになったと考えている。  
ここで重要なことは「事業として成功させる」には「参入したい側の業界・業務知識と半導体業界の業界・業務知識の両方を持った仲介者」が必要という点である。よくある失敗として、参入したい側が「半導体業界人を採用して、その人を中心に事業を起こす」というパターンである。この場合、半導体業界人が参入したい企業側の業界・業務知識がないため、「半導体業界ではこうである」というべき論を振りかざして進めて、参入したい側の業界・業務慣習などとあわずにチームが崩壊してしままったり、的外れな製品を作ってしまうというようなパターンである。  
  
そこで、作者は、そういう仲介が出来るような「両方の業界・業務知識」を持った人を育てるため、まず、自分で挑戦を始めて「[ISHI会](https://ishi-kai.org/)」というオープンソース半導体のコミュニティーを立ち上げたのである。  
そこで、ISHI会は、情報学部の学生や全く知識ゼロのソフトウェアやハードウェア（Web、FPGA、IoTなど）技術者を対象として「とりあえず、半導体系のツールを触ってみてもらう」のを目的として「[一日で環境構築～回路～レイアウト～テープアプトまでを一気にやる企画](https://ishikai.connpass.com/event/322814/)」などをやっている。これは、Make:で活躍しているような人も、最初は「初めてKiCADを触ってみるイベント」的なところから始めたという人をよく聞くので、それを参考に始めた企画である。  
  
もし、半導体設計・製造に興味のある方がいたら、 [ISHI-Kai Link](https://ishi-kai.org/)からいろいろと参加してもらいたい。  
![ISHI-KaiGrandDesign](https://ishi-kai.org/assets/images/ishikai_granddesign_fig.png)


# 全体システム像
こちらが全体像となる。  
- シリコンベアダイによるイライラコース
	- シリコンベアダイ上に描かれた世界最小イライラコース
- 8インチシリコンウェハー
	- シリコンベアダイはこれより採取されたもの
- 顕微鏡カメラ
	- シリコンベアダイを拡大してイライラコースを映し出す
- 顕微鏡カメラ用のモバイルモニター
	- イライラコース視認用
- イライラ棒
	- 5umのタングステン針とホルダーで構成
- 電極プローブ
	- 電子工作用作業ヘルパーピンセット台をベースにしたDIYプローバー
- M5 Stack製コントローラー
	- 経過時間計測と壁への接触を検知するためのコントローラー

![Operation Image](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/system.png)

シリコンベアダイ部分を拡大図。DIYプローバーがシリコンベアダイ上の電極に刺さっている。  
![Operation Image Zoom Silicon Die](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/operation1.png)

そして、イライラコースは300umの直線コースとなっている。  
![Operation Image Zoom Cource](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/operation3.png)
![Operation Image Zoom Cource](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/operation2.png)
ちなみに、シリコンベアダイと半導体チップのサイズ感は昭和風に表現するとこんな感じになる。  
![Operation size_image](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/size_image.png)

コントローラーには、DIYプローバーからの電線（イライラコースの壁へと接続されている）がGPIO13へ接続されており、イライラ棒からの電線がGNDへと接続されている。  
これにより、イライラ棒がイライラコースの壁に接触したことを検知している。  
![Operation Image Controller](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/operation_controller1.png)

コントローラの画面には、スタートからゴールまでの経過時間と壁に接触した回数とランキングが表示される仕組みとなっている。  
![Operation Image Zoom Controller](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/operation_controller2.png)


## イライラコースの種類
イライラコースは、3段階を用意。
+ 300um幅の横一直線イライラコース
    - 中段の緑色の囲み内
+ 100um幅の横一直線イライラコース
    - 下段の黄色の囲みの左側
+ 100um幅の複雑なイライラコース
    - 下段の黄色の囲み内
![Cource List](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/cource_list.png)


## 手作りプローバー
商用のプローバー（[例:アポロウェーブ社マニュアルプローバー α100](https://www.apollowave.co.jp/lineup/%E3%83%9E%E3%83%8B%E3%83%A5%E3%82%A2%E3%83%AB%E3%83%97%E3%83%AD%E3%83%BC%E3%83%90%E3%83%BC-%CE%B1100/)）を買おうとすると100～200万円くらいし、さらにとても重いため持ち運びは不可能である。  
![commercial prober system](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/a100-2-281x300.jpg)
  
そこで、Goot社の電子工作用作業ヘルパーピンセット台やAliexpressで販売している激安のカメラ付き顕微鏡、モノタロウで販売している1万円のプローブ用のタングステン針などにより、5万円ほどで自作プローバーを作成した。  
![prober system view](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/prober_system_view.png)
![prober system](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/prober_system.png)


## シリコンテープ
本システムはディスプレイに映し出す関係で立体的に見ることはできない。そうすると、イライラ棒がコースに触れているかを「視覚」的に判定することが難しい。  
そこで、試行錯誤した結果、シリコンベアダイは厚めのシリコンテープの上に載せることとした。これにより、ちょうどよい弾力によるタッチ感を出し、「触覚」により触れていることを判定できるようになった。  
  
その他に下記の理由もある。  
- 押し付ける力があまりに強いとイライラ棒の先端が曲がってしまうため、これを弾力により吸収する
- イライラ棒を押し付けることで手振れ防止をする不正を防ぐ

![Silicon Tape](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/operation_silicon.png)

### 立体顕微鏡を使わない理由
立体顕微鏡を利用することも考えたが、展示会で多くの人に試遊してもらうには手間と考えて断念した。  
昨今のコロナ事情などから、肌に触れる部分がある場合、毎回消毒処理をしなくてならなず、さらに立体顕微鏡は他人事にピントがズレるのでピント合わせもしないとならないとなると、かなり回転率が悪くなることが予想されるためである。  


## ベアダイ
下図の左側が今回利用した半導体のシリコンベアダイと呼ばれるもので、右側がそれを樹脂でパッケージした半導体ICである。  
通常の半導体製造においては、パッケージ済みIC化したものを注文するが、今回はオプションとして用意されている「ベアダイ」を選択した。（シャトルによるが、大抵はオプションにて、ベアダイn個、パッケージ済みm個と指定できる）  
![Silicon Die](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/silicon_die.png)


# 半導体開発編
## 一般的な半導体開発について
半導体開発は、大きくアナログ回路とデジタル回路に分けられる。  
デジタル回路はCPUのようなもので、アナログ回路はADC/DAC、オペアンプなどのことである。そして、これらを混載する手法もある。  
![Develop Standard Flow](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/develop_standard.png)


### 一般的なアナログ回路
トランジスターとレジスターとキャパシターとインダクターのみで回路設計をして、シミュレーション解析をして設計通りの性能であることを確認したら、回路図通りにトランジスタなどのレイアウトを行う流れである。  
要は、電子回路の開発手法と同じような手順となる。  
![Develop Analog Flow](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/develop_analog.png)

誤解を恐れずに言えば、トランジスターとレジスターとキャパシターとインダクターだけで行う電子回路開発と言える。  
![PDK Symbols](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/pdk_symbols.png)

ちなみに、インダクターはメタル層をコイル状にすることで形成する。  
![Inductor](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/inductor.png)
![FastHenry](https://github.com/noritsuna/tt08-analog-Vctrl_LC_oscillator/raw/main/docs/images/fasthenry.png)

### 一般的なデジタル回路
Verilogで記述すればあとはツールが半導体開発に必要な変換（コンパイル）などを行ってくれる。  
誤解を恐れずに言えば、FPGAの開発と変わらず、BitStreamに変換するか、GDSに変換するかの違いである。  
ちなみに、このGDSは電子回路設計のガーバーデータに相当するものであり、これ工場（ファブ）に提出することとなる。  
![Develop Digital Flow](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/develop_digital.png)


## 今回の回路
今回の回路は、アナログ回路で「電極パッド」と「イライラコース」を、デジタル回路で「制御回路」を製作したデジアナ混載回路となっている。  

### アナログ回路
#### 回路図
各パッドを「抵抗」で接続しただけである。  
このアナログ回路は、各パッドとデジタル回路部のピンを接続している。  
イライラ棒が各パッドに触れるとVSSに接続され、デジタル回路の各ピンが負論理で動作するようになる。  
![Develop Analog Pad&Reg](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/develop_analog_pad_reg.png)


#### レイアウト
「各パッド」も「イライラコース」もメタル第5層をパッド化して、人間が扱えるサイズ感でレイアウトしただけである。  
イライラコースはklayoutプラグインによって自動的に生成している。  
[/klayout/maze2metal5_generater.py](https://github.com/noritsuna/micro_irritating_maze/raw/main/klayout/maze2metal5_generater.py)
![Generated Maze Sample](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/maze_sample.jpg)

##### こだわりのコース幅
コースの幅の300umは、は人類の手の震え幅とほぼ同じ幅として設定した。  
本システムの前身となるシステムと半導体ダイで実際に計測して、ちょうど手の震えと同じ幅となるように、この「300um」は決められている。  
実際に体験した人の意見でも「ギリギリ接触しない幅」であるとのコメントをいただいている。  
![Develop Analog Course](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/develop_analog_course.png)


### デジタル回路
20ビットの経過時間と7ビットの壁の接触カウンタ、各パッドへの接触を検知する回路で構成されている。  
![Develop Digital Verilog](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/develop_digital_verilog.png)
[Develop Digital Verilog](https://github.com/noritsuna/micro_irritating_maze/raw/main/verilog/rtl//micro_irritating_maze.v)

ただし、今回は、これらの出力は、外周部の小型パッド（紫色の囲み内）からプローブで取得する必要があるため、利用を断念した。  
![Outside Pad](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/klayout_vs.png)


実際のレイアウトとしては、イライラコースの壁が壁への接触検知パッドになっており、イライラ棒が触れるとカウントアップする回路とイライラ棒がスタートパッド（丸形）に触れると時間計測を開始し、ゴールパッド（十字の形）に触れると時間計測が停止して、その時間と壁への接触回数を出力する回路で構成されている。  
- イライラコースの壁パッド
	- イライラ棒が接触したことを検知する回路へ接続されている
- 丸形パッド
	- 時間計測開始と壁への接触カウンターリセットする回路へ接続されている
- 十字パッド
	- 時間計測停止と壁への接触カウンターを出力する回路へ接続されている
![Develop Digital Start&Goal](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/maze_exp.jpg)

下図は、Verilogで生成された回路を半導体チップ上にレイアウトした図となる。（これがGDSファイルである）  
![Develop Digital GDS](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/develop_digital_gds.png)


### デジアナ混載回路
最終的なレイアウトは、OpenLANEが生成したデジタル回路のレイアウトをKlayoutで編集し、イライラコースやパッドなどのアナログ回路を組み込んで作成した。  
![Final Layout](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/klayout_fix.jpg)

リアルチップとレイアウトの対応  
![VS Layout](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/klayout_vs.png)

#### 製作手順
+ メタル5層にパッドを作りたいので、Verilogで自動生成されたGDSファイルから不要なVDDとVSSを取り除き、空き領域を作る。  
    ![OpenLANE Generated Digital Layout](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/klayout_default.jpg)
    ![Delete Metal5 Layer Layout](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/klayout_del_mel5.jpg)
+ メタル5層の空き領域に以下のパッドを配置し、必要な配線を行う。  
    - イライラコースの壁パッド
        - このパッドはデジタル回路の Crash 端子に接続する。
    - スタートパッド
        - デジタル回路の RST 端子に接続する。
    - ゴールパッド
        - デジタル回路の Goal 端子に接続する。
    - VDDパッド
        - このパッドはデジタル回路の VDD に接続する。
    - VSSパッド（GNDパッド）
        - このパッドはデジタル回路の VSS に接続する。
+ イライラ棒は5umなので、パッドサイズは800umに設定した。  
    ![5um Tungsten Needle](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/needle_pen.png)
    ![Pad Explanation](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/pad_exp.jpg)
+ イライラコースを生成する。イライラコースの経路幅は300umとした。手元にあったチップを使い、手の震えの幅と合わせた。  
    ![Maze Explanation](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/maze_exp.jpg)
+ レイアウト上にパッドとイライラコースを配置し、デジタル回路に配線する。  
    ![Conbine Pad&Regsiter&Digital Layout](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/klayout_fix.jpg)


# コントローラ編
## M5 Stack CoreS3 SE選定理由
コントローラとして、ディスプレイにランキングなどを表示したかったのでディスプレイも欲しかったためM5 Stackを選定した。  
さらに、M5 Stack CoreS3 SEを選定した理由は、壁への接触時に「爆発音」を再生したかったためである。  
![Develop Controller](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/operation_controller2.png)
![Develop Controller Connecting](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/operation_controller_connecting.png)


## 開発環境
開発環境としては、VSCode+PlatformIOを採用した。  
選定理由は、VSCodeを使い慣れている以上の意味はない。  
![Develop Controller VSCode](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/operation_controller_vscode.png)

## 開発内容
壁への接触判定は、イライラコースの壁パッドにプローブを刺してGPIO13ピンに接続し、イライラ棒をGNDに接続することで、GPIO13版の1->0の変化を壁への接触を判定としている。  
工夫した点としては、コースの幅があまりに狭いため、一度壁にあたってしまうと元のイライラコースにイライラ棒を戻す時に連続して壁に触れてしまうので、そこは「無敵時間」として、壁への接触判定後に「秒単位」の「無敵時間」≒「チャタリング防止機構」を入れた。  
[Develop Controller Dir](https://github.com/noritsuna/micro_irritating_maze/raw/main/counter_app/micro_irritating_maze/)
[Develop Controller Code](https://github.com/noritsuna/micro_irritating_maze/raw/main/counter_app/micro_irritating_maze/src/main.cpp)


#システム構築編
## 価格リスト
今回、購入したものと価格の一覧表である。これに細かいシリコンテープなどを入れると大体**5万円**というところである  
安さのキモは「半導体系の製品をDIY（手作り）」したり、「OSSのツールを利用」したり、「無料のサービス」をうまく組み合わせたためである。  
![System Price List](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/price_list.png)

- カメラ付き顕微鏡
    ![Microscope](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/price_scope.png)
- 5umタングステン針とホルダー（イライラ棒として使用）
    ![5um Tungsten Needle](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/price_needle.png)
    ![5um Tungsten Needle Holder](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/price_needle_holder.png)
- M5 Stack CoreS3 SE
    ![M5 Stack](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/price_m5stack.png)


## 半導体シャトル
もし、「自分も半導体を利用した作品を制作したい！」と思った方への情報を記載する。  
- いろいろなシャトルのリスト
	- ![System Shuttle List](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/shuttle_list.png)
- ISHI会のシャトルシェアサポート
	- ![System Shuttle Share](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/shuttle_share.png)
	- [ISHI会リンク集](https://ishi-kai.org/links/)

# 各ファイル
- [/klayout/maze2metal5_generater.py](https://github.com/noritsuna/micro_irritating_maze/raw/main/klayout/maze2metal5_generater.py) 
	- イライラコースを自動生成するKlayoutのプラグインです。
	- ![Generated Maze Sample](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/maze_sample.jpg)
- [/verilog/rtl/micro_irritating_maze.v](https://github.com/noritsuna/micro_irritating_maze/raw/main/verilog/rtl/micro_irritating_maze.v) 
	- イライラコースの壁にぶつかった回数と、イライラコースのスタートからゴールまでの時間を計測するデジタル回路。
- [/gds/maze_Large.gds](https://github.com/noritsuna/micro_irritating_maze/raw/main/gds/maze_Large.gds) 
	- これは道幅300umの大きなイライラコースである。
- [/gds/maze_Small.gds](https://github.com/noritsuna/micro_irritating_maze/raw/main/gds/maze_Small.gds)
	- 道幅100μmの小さなイライラコース。人類の限界に挑戦！ 
- [/gds/maze_Complex.gds](https://github.com/noritsuna/micro_irritating_maze/raw/main/gds/maze_Complex.gds) 
	- パス幅100μmのやや複雑な形状のイライラコース。まだクリアできたものはいない。 
	- ![Complex Maze](https://github.com/noritsuna/micro_irritating_maze/raw/main/images/maze_complex.jpg) 
- [/xschem/maze.sch](https://github.com/noritsuna/micro_irritating_maze/raw/main/xschem/maze.sch) 
	- イライラコース部とデジタル回路部を接続するアナログ回路図。
- [/gds/pad_and_resistor.gds](https://github.com/noritsuna/micro_irritating_mazegds/raw/main/gds/pad_and_resistor.gds)
	- VDDパッド、VSSパッド、各イライラコース動作用ピンのパッド。[/xschem/maze.sch](https://github.com/noritsuna/micro_irritating_maze/raw/main/xschem/maze.sch)に実装。
	- DIYプローバー用（800um x 800um）と業務用プロービングシステム用（80um x 80um）の2種類のパッドを用意している。
- [/counter_app/micro_irritating_maze/](https://github.com/noritsuna/micro_irritating_mazegds/raw/main/counter_app/micro_irritating_maze/)
	- コントローラー用のファイル一式。


# Forked from the Caravel User Project

| :exclamation: Important Note            |
|-----------------------------------------|

## Caravel information follows

Refer to [README](docs/source/index.rst#section-quickstart) for a quickstart of how to use caravel_user_project

Refer to [README](docs/source/index.rst) for this sample project documentation. 

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![UPRJ_CI](https://github.com/efabless/caravel_project_example/actions/workflows/user_project_ci.yml/badge.svg)](https://github.com/efabless/caravel_project_example/actions/workflows/user_project_ci.yml) [![Caravel Build](https://github.com/efabless/caravel_project_example/actions/workflows/caravel_build.yml/badge.svg)](https://github.com/efabless/caravel_project_example/actions/workflows/caravel_build.yml)
