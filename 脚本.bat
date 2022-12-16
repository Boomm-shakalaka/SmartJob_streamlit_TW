chcp 65001
@echo off
call activate
call conda activate web
streamlit run main.py
Pause
