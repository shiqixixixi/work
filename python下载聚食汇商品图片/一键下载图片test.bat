@echo off
:input
title 一键下载聚食汇商品图片
::一键下载聚食汇商品图片
echo 1.执行一键下载聚食汇商品图片。"
echo 2.退出当前程序！"
set /p "num=请输入按键“1”或“2”，然后按下回车键："
if "%num%"=="1" cls & goto 1
if "%num%"=="2" cls & goto 2
echo. & echo 不能输入除了“1”和“2”之外的其他字符！ & pause>nul & cls & goto input
:1
echo 现在正在一键下载图片
echo =====================================================
echo ==============python downloads_img.py================
echo =====================================================
pause>nul
python downloads_img.py
:2
echo 现在正在退出
echo ===============================
echo ==============exit=============
echo ===============================
pause>nul
exit