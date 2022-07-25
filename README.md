# 画像処理デモ
画像認識と画像処理に関する簡易なデモです。

# 概要
 
- たけのこの里ときのこの山を対象としてます。
- 画像認識には、Tensorflow.keras.applications の MobileNetV2 を転移学習しました
- まだ上げてませんが、コールバックに EarlyStopping と ModelCheckpoint 使ってます
- 画像はそれぞれ約300枚でしたが、数が多すぎました。ただ、バリエーションが少なすぎた感じです
- OpenCV で物体抽出と面積最小な外接矩形もとめて長さ・幅・面積もとめてます
- QRコードも同時に読んで大きさの基準にする予定でしたが、カメラ解像度が低すぎてデコードできません
- 今回は QRコードも HSV抽出してます
 
# Requirement
* OpenCV4.5.5
* tensorflow2.8.0
* numpy1.22.1
 
# Usage
 
`./cp.ckpt` に転移学習済の MobileNetV2 おいてます。
USBカメラをつないで、指標にするQRコードが一緒に映り込むように対象物をうつします。<br>
背景は緑っぽいといいです。以下、実行してみてください。
 
```bash
python check_and_measure.py
```
'r'キーを押すと、認識・計測してくれるはず。

# ToDo
QRコードうまくよめないので、しかたなく自分でしきい値しらべてHSVマスクかけてます。<br>
この場合なら、HSVの S を [大津の二値化](http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#id5) で処理するといいと思います。<br>
<br>
Webカメラは少しいいの使わないとですね。QRコード読めないです。今回は　$640\times480$ でしたからね・・・
 
